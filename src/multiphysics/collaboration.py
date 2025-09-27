"""
Collaborative Research Platform Infrastructure

Platform for global collaboration on Leonardo's mechanical inventions.
"""

import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


@dataclass
class User:
    """User profile for collaborative platform."""
    
    user_id: str
    username: str
    email: str
    institution: str
    role: str  # researcher, educator, student, maker
    expertise_areas: List[str]
    reputation_score: float = 0.0
    contributions: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.contributions is None:
            self.contributions = []
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Project:
    """Collaborative research project."""
    
    project_id: str
    name: str
    description: str
    owner_id: str
    collaborators: List[str]
    invention_focus: str  # ornithopter, cart, parachute, etc.
    project_type: str  # research, education, competition, replication
    status: str  # active, completed, paused, archived
    visibility: str  # public, private, institutional
    
    simulation_configs: Dict[str, Any] = None
    experimental_data: Dict[str, Any] = None
    analysis_results: Dict[str, Any] = None
    
    created_at: datetime = None
    last_modified: datetime = None
    
    def __post_init__(self):
        for field in ['simulation_configs', 'experimental_data', 'analysis_results']:
            if getattr(self, field) is None:
                setattr(self, field, {})
        
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_modified is None:
            self.last_modified = datetime.now()


@dataclass
class Challenge:
    """Global research challenge."""
    
    challenge_id: str
    title: str
    description: str
    organizer_id: str
    invention_target: str
    performance_metrics: Dict[str, float]
    
    start_date: datetime
    end_date: datetime
    submission_deadline: datetime
    
    participants: List[str] = None
    submissions: List[str] = None
    prize_pool: float = 0.0
    status: str = "upcoming"
    
    def __post_init__(self):
        if self.participants is None:
            self.participants = []
        if self.submissions is None:
            self.submissions = []


class CollaborationEngine:
    """Core engine for managing collaborative research activities."""
    
    def __init__(self, data_directory: str = "collaboration_data"):
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(exist_ok=True)
        
        self.users: Dict[str, User] = {}
        self.projects: Dict[str, Project] = {}
        self.challenges: Dict[str, Challenge] = {}
        self.active_sessions: Dict[str, Dict] = {}
        
        logger.info("Collaboration engine initialized")
    
    def register_user(self, username: str, email: str, institution: str, 
                     role: str, expertise_areas: List[str]) -> str:
        """Register a new user."""
        
        user_id = str(uuid.uuid4())
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            institution=institution,
            role=role,
            expertise_areas=expertise_areas
        )
        
        self.users[user_id] = user
        self._save_user(user)
        
        logger.info(f"Registered user {username} from {institution}")
        return user_id
    
    def create_project(self, name: str, description: str, owner_id: str,
                      invention_focus: str, project_type: str = "research",
                      visibility: str = "public") -> str:
        """Create a new collaborative project."""
        
        if owner_id not in self.users:
            raise ValueError("Invalid owner ID")
        
        project_id = str(uuid.uuid4())
        
        project = Project(
            project_id=project_id,
            name=name,
            description=description,
            owner_id=owner_id,
            collaborators=[owner_id],
            invention_focus=invention_focus,
            project_type=project_type,
            status="active",
            visibility=visibility
        )
        
        self.projects[project_id] = project
        self._save_project(project)
        
        self.users[owner_id].contributions.append(project_id)
        
        logger.info(f"Created project '{name}' by {self.users[owner_id].username}")
        return project_id
    
    def join_project(self, project_id: str, user_id: str) -> bool:
        """Add user as collaborator to project."""
        
        if project_id not in self.projects or user_id not in self.users:
            return False
        
        project = self.projects[project_id]
        
        if project.visibility == "private":
            return False
        
        if user_id not in project.collaborators:
            project.collaborators.append(user_id)
            project.last_modified = datetime.now()
            
            self.users[user_id].contributions.append(project_id)
            
            logger.info(f"User {self.users[user_id].username} joined project {project.name}")
            return True
        
        return False
    
    def create_challenge(self, title: str, description: str, organizer_id: str,
                        invention_target: str, performance_metrics: Dict[str, float],
                        start_date: datetime, end_date: datetime,
                        prize_pool: float = 0.0) -> str:
        """Create a global research challenge."""
        
        if organizer_id not in self.users:
            raise ValueError("Invalid organizer ID")
        
        challenge_id = str(uuid.uuid4())
        
        submission_deadline = datetime.fromtimestamp(
            end_date.timestamp() - 7 * 24 * 3600
        )
        
        challenge = Challenge(
            challenge_id=challenge_id,
            title=title,
            description=description,
            organizer_id=organizer_id,
            invention_target=invention_target,
            performance_metrics=performance_metrics,
            start_date=start_date,
            end_date=end_date,
            submission_deadline=submission_deadline,
            prize_pool=prize_pool
        )
        
        self.challenges[challenge_id] = challenge
        self._save_challenge(challenge)
        
        logger.info(f"Created challenge '{title}' with ${prize_pool} prize pool")
        return challenge_id
    
    def start_collaborative_session(self, project_id: str, user_id: str,
                                   session_type: str = "simulation") -> str:
        """Start a real-time collaborative session."""
        
        if project_id not in self.projects or user_id not in self.users:
            raise ValueError("Invalid project or user ID")
        
        project = self.projects[project_id]
        
        if user_id not in project.collaborators:
            raise ValueError("User is not a collaborator on this project")
        
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "project_id": project_id,
            "host_id": user_id,
            "session_type": session_type,
            "participants": [user_id],
            "started_at": datetime.now(),
            "status": "active",
            "shared_state": {},
            "activity_log": []
        }
        
        self.active_sessions[session_id] = session
        
        logger.info(f"Started {session_type} session for project {project.name}")
        return session_id
    
    def search_projects(self, query: str, invention_focus: str = None) -> List[Dict[str, Any]]:
        """Search for projects based on criteria."""
        
        results = []
        
        for project in self.projects.values():
            if project.visibility == "private":
                continue
            
            if invention_focus and project.invention_focus != invention_focus:
                continue
            
            if query.lower() in project.name.lower() or query.lower() in project.description.lower():
                
                collaborator_info = []
                for collab_id in project.collaborators:
                    if collab_id in self.users:
                        user = self.users[collab_id]
                        collaborator_info.append({
                            "username": user.username,
                            "institution": user.institution,
                            "role": user.role
                        })
                
                results.append({
                    "project_id": project.project_id,
                    "name": project.name,
                    "description": project.description,
                    "invention_focus": project.invention_focus,
                    "project_type": project.project_type,
                    "status": project.status,
                    "collaborators": collaborator_info,
                    "created_at": project.created_at,
                    "last_modified": project.last_modified
                })
        
        results.sort(key=lambda x: x["last_modified"], reverse=True)
        return results
    
    def get_user_recommendations(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get personalized recommendations for user."""
        
        if user_id not in self.users:
            return {}
        
        user = self.users[user_id]
        
        recommendations = {
            "projects": [],
            "challenges": [],
            "collaborators": []
        }
        
        # Project recommendations
        for project in self.projects.values():
            if (project.visibility == "public" and 
                user_id not in project.collaborators and
                project.status == "active" and
                project.invention_focus in user.expertise_areas):
                
                recommendations["projects"].append({
                    "project_id": project.project_id,
                    "name": project.name,
                    "invention_focus": project.invention_focus,
                    "match_reason": f"Expertise in {project.invention_focus}"
                })
        
        # Challenge recommendations
        now = datetime.now()
        for challenge in self.challenges.values():
            if (challenge.status in ["upcoming", "active"] and
                user_id not in challenge.participants and
                challenge.start_date <= now <= challenge.end_date and
                challenge.invention_target in user.expertise_areas):
                
                recommendations["challenges"].append({
                    "challenge_id": challenge.challenge_id,
                    "title": challenge.title,
                    "invention_target": challenge.invention_target,
                    "prize_pool": challenge.prize_pool
                })
        
        # Limit recommendations
        for category in recommendations:
            recommendations[category] = recommendations[category][:5]
        
        return recommendations
    
    def generate_collaboration_analytics(self) -> Dict[str, Any]:
        """Generate analytics about platform collaboration."""
        
        analytics = {
            "users": {
                "total_users": len(self.users),
                "users_by_role": {},
                "average_reputation": 0.0
            },
            "projects": {
                "total_projects": len(self.projects),
                "projects_by_type": {},
                "active_projects": 0
            },
            "challenges": {
                "total_challenges": len(self.challenges),
                "active_challenges": 0,
                "total_prize_pool": 0.0
            }
        }
        
        # User analytics
        roles = [user.role for user in self.users.values()]
        for role in set(roles):
            analytics["users"]["users_by_role"][role] = roles.count(role)
        
        if self.users:
            analytics["users"]["average_reputation"] = sum(
                user.reputation_score for user in self.users.values()
            ) / len(self.users)
        
        # Project analytics
        project_types = [proj.project_type for proj in self.projects.values()]
        for proj_type in set(project_types):
            analytics["projects"]["projects_by_type"][proj_type] = project_types.count(proj_type)
        
        analytics["projects"]["active_projects"] = sum(
            1 for proj in self.projects.values() if proj.status == "active"
        )
        
        # Challenge analytics
        analytics["challenges"]["active_challenges"] = sum(
            1 for challenge in self.challenges.values() 
            if challenge.status in ["active", "upcoming"]
        )
        
        analytics["challenges"]["total_prize_pool"] = sum(
            challenge.prize_pool for challenge in self.challenges.values()
        )
        
        return analytics
    
    def _save_user(self, user: User):
        """Save user data to file."""
        file_path = self.data_dir / f"user_{user.user_id}.json"
        with open(file_path, 'w') as f:
            json.dump(asdict(user), f, default=str, indent=2)
    
    def _save_project(self, project: Project):
        """Save project data to file."""
        file_path = self.data_dir / f"project_{project.project_id}.json"
        with open(file_path, 'w') as f:
            json.dump(asdict(project), f, default=str, indent=2)
    
    def _save_challenge(self, challenge: Challenge):
        """Save challenge data to file."""
        file_path = self.data_dir / f"challenge_{challenge.challenge_id}.json"
        with open(file_path, 'w') as f:
            json.dump(asdict(challenge), f, default=str, indent=2)


class DistributedSimulationManager:
    """Manager for distributed multi-physics simulations."""
    
    def __init__(self, collaboration_engine: CollaborationEngine):
        self.collaboration_engine = collaboration_engine
        self.active_simulations: Dict[str, Dict] = {}
        self.compute_nodes: List[Dict] = []
        
        logger.info("Distributed simulation manager initialized")
    
    def register_compute_node(self, node_info: Dict[str, Any]) -> str:
        """Register a compute node for distributed simulation."""
        
        node_id = str(uuid.uuid4())
        
        node = {
            "node_id": node_id,
            "host": node_info.get("host", "localhost"),
            "port": node_info.get("port", 8080),
            "capabilities": node_info.get("capabilities", []),
            "max_concurrent_jobs": node_info.get("max_concurrent_jobs", 1),
            "current_jobs": 0,
            "status": "available",
            "registered_at": datetime.now()
        }
        
        self.compute_nodes.append(node)
        
        logger.info(f"Registered compute node {node_id}")
        return node_id
    
    def submit_distributed_simulation(self, project_id: str, user_id: str,
                                    simulation_config: Dict[str, Any]) -> str:
        """Submit simulation for distributed execution."""
        
        if project_id not in self.collaboration_engine.projects:
            raise ValueError("Invalid project ID")
        
        project = self.collaboration_engine.projects[project_id]
        if user_id not in project.collaborators:
            raise ValueError("User is not a collaborator on this project")
        
        simulation_id = str(uuid.uuid4())
        
        simulation = {
            "simulation_id": simulation_id,
            "project_id": project_id,
            "user_id": user_id,
            "config": simulation_config,
            "status": "queued",
            "submitted_at": datetime.now(),
            "results": None
        }
        
        self.active_simulations[simulation_id] = simulation
        
        logger.info(f"Submitted distributed simulation {simulation_id}")
        return simulation_id
    
    def get_simulation_status(self, simulation_id: str) -> Dict[str, Any]:
        """Get status of distributed simulation."""
        
        if simulation_id not in self.active_simulations:
            return {"error": "Simulation not found"}
        
        simulation = self.active_simulations[simulation_id]
        
        return {
            "simulation_id": simulation_id,
            "status": simulation["status"],
            "submitted_at": simulation["submitted_at"],
            "results_available": simulation["results"] is not None
        }


def create_leonardo_collaboration_platform():
    """Initialize the complete Leonardo collaboration platform."""
    
    collaboration_engine = CollaborationEngine("leonardo_collaboration_data")
    simulation_manager = DistributedSimulationManager(collaboration_engine)
    
    # Register example compute nodes
    simulation_manager.register_compute_node({
        "host": "compute1.leonardo-platform.org",
        "capabilities": ["aerodynamics", "structures", "multiphysics"],
        "max_concurrent_jobs": 4
    })
    
    simulation_manager.register_compute_node({
        "host": "compute2.leonardo-platform.org", 
        "capabilities": ["materials", "optimization", "visualization"],
        "max_concurrent_jobs": 2
    })
    
    return {
        "collaboration_engine": collaboration_engine,
        "simulation_manager": simulation_manager
    }