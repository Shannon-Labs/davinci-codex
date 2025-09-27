"""
Structural Mechanics Module for Leonardo's Mechanical Devices

Implements finite element analysis for Renaissance engineering structures.
"""

import numpy as np
import scipy.sparse as sp
from typing import Dict, List, Tuple, Optional, Any
import logging

from .core import PhysicsModule, SimulationParameters, MaterialProperties

logger = logging.getLogger(__name__)


class BeamElement:
    """Euler-Bernoulli beam element for structural frames."""
    
    def __init__(self, element_id: int, node_ids: List[int], material: MaterialProperties, 
                 cross_section_area: float, moment_of_inertia: float):
        self.element_id = element_id
        self.node_ids = node_ids
        self.material = material
        self.cross_section_area = cross_section_area
        self.moment_of_inertia = moment_of_inertia
        
        if len(node_ids) != 2:
            raise ValueError("Beam element must have exactly 2 nodes")
    
    def compute_stiffness_matrix(self, coordinates: np.ndarray) -> np.ndarray:
        """Compute beam element stiffness matrix."""
        
        node1 = coordinates[self.node_ids[0]]
        node2 = coordinates[self.node_ids[1]]
        length = np.linalg.norm(node2 - node1)
        
        E = self.material.young_modulus
        A = self.cross_section_area
        I = self.moment_of_inertia
        
        # Local stiffness matrix (12x12 for 3D beam with 6 DOF per node)
        k_local = np.zeros((12, 12))
        
        # Axial stiffness
        k_axial = E * A / length
        k_local[0, 0] = k_axial
        k_local[0, 6] = -k_axial
        k_local[6, 0] = -k_axial
        k_local[6, 6] = k_axial
        
        # Bending stiffness (simplified)
        k_bend = E * I / (length ** 3)
        k_local[1, 1] = 12 * k_bend
        k_local[7, 7] = 12 * k_bend
        
        return k_local
    
    def compute_mass_matrix(self, coordinates: np.ndarray) -> np.ndarray:
        """Compute mass matrix."""
        
        node1 = coordinates[self.node_ids[0]]
        node2 = coordinates[self.node_ids[1]]
        length = np.linalg.norm(node2 - node1)
        
        mass_per_node = self.material.density * self.cross_section_area * length / 2
        m_local = np.zeros((12, 12))
        
        # Lumped mass
        for i in range(3):
            m_local[i, i] = mass_per_node
            m_local[i + 6, i + 6] = mass_per_node
        
        return m_local


class StructuralModule(PhysicsModule):
    """Finite Element structural analysis module."""
    
    def __init__(self, parameters: SimulationParameters):
        super().__init__("structures", parameters)
        
        self.nodes = {}
        self.elements = {}
        self.materials = {}
        self.global_stiffness = None
        self.global_mass = None
        self.num_dof = 0
        self.displacements = None
        self.fixed_dof = []
        self.applied_loads = {}
        
        logger.info("Structural module initialized")
    
    def initialize(self, geometry, materials, boundary_conditions):
        """Initialize structural model."""
        
        self.geometry = geometry
        self.boundary_conditions = boundary_conditions
        
        # Load materials
        for mat_id, mat_data in materials.items():
            if isinstance(mat_data, MaterialProperties):
                self.materials[mat_id] = mat_data
            else:
                self.materials[mat_id] = MaterialProperties(**mat_data)
        
        self._generate_mesh()
        self._setup_boundary_conditions()
        self._assemble_system_matrices()
        self._initialize_solution_vectors()
        
        self.is_initialized = True
        logger.info(f"Structural model: {len(self.nodes)} nodes, {len(self.elements)} elements")
    
    def _generate_mesh(self):
        """Generate finite element mesh."""
        
        if 'wing_geometry' in self.geometry:
            wing_data = self.geometry['wing_geometry']
            wingspan = wing_data.get('wingspan', 12.0)
            
            # Simple wing box structure
            num_ribs = 5
            node_id = 0
            
            # Generate nodes
            for i in range(num_ribs):
                y_pos = (i / (num_ribs - 1)) * wingspan / 2
                for j in range(2):  # Front and rear spar
                    x_pos = 0.2 if j == 0 else 0.8
                    self.nodes[node_id] = np.array([x_pos, y_pos, 0])
                    node_id += 1
            
            # Generate beam elements for spars
            element_id = 0
            for spar in range(2):
                for rib in range(num_ribs - 1):
                    node1 = rib * 2 + spar
                    node2 = (rib + 1) * 2 + spar
                    
                    material = list(self.materials.values())[0]
                    area = 0.01  # 1 cm²
                    inertia = 1e-6  # Small moment of inertia
                    
                    element = BeamElement(element_id, [node1, node2], material, area, inertia)
                    self.elements[element_id] = element
                    element_id += 1
        
        self.num_dof = len(self.nodes) * 6
    
    def _setup_boundary_conditions(self):
        """Set up boundary conditions."""
        
        bc_data = self.boundary_conditions.get('structural', {})
        
        # Fixed supports at root
        if 'fixed_nodes' in bc_data:
            for node_id in bc_data['fixed_nodes']:
                for dof in range(6):
                    self.fixed_dof.append(node_id * 6 + dof)
        
        # Applied loads
        if 'point_loads' in bc_data:
            for load_data in bc_data['point_loads']:
                node_id = load_data['node']
                force = load_data['force']
                for i, f in enumerate(force):
                    if f != 0:
                        self.applied_loads[node_id * 6 + i] = f
    
    def _assemble_system_matrices(self):
        """Assemble global matrices."""
        
        self.global_stiffness = sp.lil_matrix((self.num_dof, self.num_dof))
        self.global_mass = sp.lil_matrix((self.num_dof, self.num_dof))
        
        for element in self.elements.values():
            elem_coords = np.array([self.nodes[node_id] for node_id in element.node_ids])
            
            k_elem = element.compute_stiffness_matrix(elem_coords)
            m_elem = element.compute_mass_matrix(elem_coords)
            
            # Assembly (simplified)
            for i, node_i in enumerate(element.node_ids):
                for j, node_j in enumerate(element.node_ids):
                    for dof_i in range(6):
                        for dof_j in range(6):
                            global_i = node_i * 6 + dof_i
                            global_j = node_j * 6 + dof_j
                            elem_i = i * 6 + dof_i
                            elem_j = j * 6 + dof_j
                            
                            self.global_stiffness[global_i, global_j] += k_elem[elem_i, elem_j]
                            self.global_mass[global_i, global_j] += m_elem[elem_i, elem_j]
        
        self.global_stiffness = self.global_stiffness.tocsr()
        self.global_mass = self.global_mass.tocsr()
    
    def _initialize_solution_vectors(self):
        """Initialize solution vectors."""
        
        self.displacements = np.zeros(self.num_dof)
        self.velocities = np.zeros(self.num_dof)
        self.internal_forces = np.zeros(self.num_dof)
        
        self.state_variables = {
            'displacements': self.displacements,
            'velocities': self.velocities,
            'internal_forces': self.internal_forces
        }
    
    def compute_residual(self, state: np.ndarray, time: float) -> np.ndarray:
        """Compute structural residual."""
        
        if len(state) >= self.num_dof:
            self.displacements = state[:self.num_dof]
        
        # Internal forces
        self.internal_forces = self.global_stiffness @ self.displacements
        
        # Applied loads
        applied_force_vector = np.zeros(self.num_dof)
        for dof, force in self.applied_loads.items():
            applied_force_vector[dof] = force
        
        # Add aerodynamic forces if available
        if hasattr(self, 'aerodynamic_forces'):
            applied_force_vector += self.aerodynamic_forces
        
        # Residual
        residual = self.internal_forces - applied_force_vector
        
        # Apply boundary conditions
        for dof in self.fixed_dof:
            residual[dof] = 0.0
        
        return residual
    
    def compute_jacobian(self, state: np.ndarray, time: float) -> sp.spmatrix:
        """Compute Jacobian matrix."""
        
        jacobian = self.global_stiffness.copy()
        
        # Apply boundary conditions
        for dof in self.fixed_dof:
            jacobian[dof, :] = 0
            jacobian[:, dof] = 0
            jacobian[dof, dof] = 1.0
        
        return jacobian
    
    def update_coupling_variables(self, coupled_data: Dict[str, Any]):
        """Update from aerodynamic coupling."""
        
        if 'panel_forces' in coupled_data:
            aero_forces = coupled_data['panel_forces']
            aero_points = coupled_data.get('control_points', [])
            
            self.aerodynamic_forces = np.zeros(self.num_dof)
            
            # Map aerodynamic forces to structure (simplified)
            for i, force in enumerate(aero_forces):
                if i < len(self.nodes):
                    # Apply force in z-direction
                    self.aerodynamic_forces[i * 6 + 2] = force
    
    def get_coupling_variables(self) -> Dict[str, Any]:
        """Return structural variables for coupling."""
        
        # Surface displacement for aerodynamic coupling
        surface_displacement = []
        for node_id in sorted(self.nodes.keys()):
            disp = self.displacements[node_id * 6:node_id * 6 + 3]
            surface_displacement.append(disp)
        
        return {
            'surface_displacement': np.array(surface_displacement),
            'node_coordinates': np.array([self.nodes[i] for i in sorted(self.nodes.keys())]),
            'max_displacement': np.max(np.abs(self.displacements)),
            'max_stress': self._compute_max_stress()
        }
    
    def _compute_max_stress(self) -> float:
        """Compute maximum stress in structure."""
        
        max_stress = 0.0
        
        for element in self.elements.values():
            # Simple stress calculation
            node_disps = []
            for node_id in element.node_ids:
                disp = self.displacements[node_id * 6:node_id * 6 + 6]
                node_disps.append(disp)
            
            # Axial strain (simplified)
            node1_disp = node_disps[0][:3]
            node2_disp = node_disps[1][:3]
            
            node1_pos = self.nodes[element.node_ids[0]] + node1_disp
            node2_pos = self.nodes[element.node_ids[1]] + node2_disp
            
            original_length = np.linalg.norm(self.nodes[element.node_ids[1]] - self.nodes[element.node_ids[0]])
            current_length = np.linalg.norm(node2_pos - node1_pos)
            
            strain = (current_length - original_length) / original_length
            stress = element.material.young_modulus * strain
            
            max_stress = max(max_stress, abs(stress))
        
        return max_stress