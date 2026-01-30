from typing import Optional
from pydantic import BaseModel, Field, model_validator

class ToulminChain(BaseModel):
    """
    Represents a full or partial Toulmin argument chain.
    Strictly enforces the presence of dependencies between steps.
    """
    data: Optional[str] = Field(None, description="The raw facts/evidence. Must be cited.")
    claim: Optional[str] = Field(None, description="The assertion being made based *only* on the Data.")
    warrant: Optional[str] = Field(None, description="The logical principle connecting Data to Claim.")
    backing: Optional[str] = Field(None, description="The statutory, legal, or scientific support for the Warrant.")
    rebuttal: Optional[str] = Field(None, description="The specific conditions where the Warrant does not apply (Edge cases).")
    qualifier: Optional[str] = Field(None, description="The degree of force (e.g., 'Presumably', 'Always', 'Unless').")
    verdict: Optional[str] = Field(None, description="The final synthesis. Given the Rebuttal and Qualifier, does the Claim stand?")

    @model_validator(mode='after')
    def check_dependencies(self) -> 'ToulminChain':
        # Dependency: Cannot generate a Claim without Data.
        if self.claim is not None and self.data is None:
            raise ValueError("Dependency Error: Cannot have a CLAIM without DATA.")

        # Dependency: Warrant connects Data to Claim, so needs both.
        if self.warrant is not None and (self.data is None or self.claim is None):
            raise ValueError("Dependency Error: Cannot have a WARRANT without DATA and CLAIM.")

        # Dependency: Backing supports the Warrant.
        if self.backing is not None and self.warrant is None:
            raise ValueError("Dependency Error: Cannot have BACKING without a WARRANT.")

        # Dependency: Rebuttal challenges the Warrant/Claim connection.
        if self.rebuttal is not None and self.warrant is None:
            raise ValueError("Dependency Error: Cannot have a REBUTTAL without a WARRANT.")

        # Dependency: Qualifier modifies the Claim based on Rebuttal/Warrant.
        if self.qualifier is not None and self.claim is None:
            raise ValueError("Dependency Error: Cannot have a QUALIFIER without a CLAIM.")

        # Dependency: Verdict requires everything (at least Rebuttal and Qualifier as per prompt).
        # "You cannot generate a Verdict without a Rebuttal."
        if self.verdict is not None:
            if self.rebuttal is None:
                raise ValueError("Dependency Error: Cannot have a VERDICT without a REBUTTAL.")
            if self.qualifier is None:
                raise ValueError("Dependency Error: Cannot have a VERDICT without a QUALIFIER.")
            if self.claim is None:
                raise ValueError("Dependency Error: Cannot have a VERDICT without a CLAIM.")

        return self
