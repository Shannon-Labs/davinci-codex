from mcp.server.fastmcp import FastMCP
from .models import ToulminChain
from .prompts import (
    initiate_toulmin_sequence,
    inject_logic_bridge,
    stress_test_argument,
    render_verdict
)

mcp = FastMCP("toulmini")

@mcp.tool()
def get_initiation_prompt(query: str) -> str:
    """
    Generates the System Prompt to initiate the Toulmin sequence.
    Forces the LLM to extract DATA and CLAIM from the query.
    """
    return initiate_toulmin_sequence(query)

@mcp.tool()
def get_logic_bridge_prompt(data: str, claim: str) -> str:
    """
    Generates the System Prompt to inject the Logic Bridge (WARRANT and BACKING).
    Requires DATA and CLAIM.
    """
    # Validate inputs using ToulminChain (partial)
    # We just check if they are provided, the prompt logic handles the rest.
    # But we can use the model to validate dependencies if we want strictness here.
    # For now, we trust the type hints and the prompt logic.
    return inject_logic_bridge(data, claim)

@mcp.tool()
def get_stress_test_prompt(data: str, claim: str, warrant: str, backing: str) -> str:
    """
    Generates the System Prompt to stress test the argument (REBUTTAL and QUALIFIER).
    Requires DATA, CLAIM, WARRANT, and BACKING.
    """
    return stress_test_argument(data, claim, warrant, backing)

@mcp.tool()
def get_verdict_prompt(data: str, claim: str, warrant: str, backing: str, rebuttal: str, qualifier: str) -> str:
    """
    Generates the System Prompt to render the final VERDICT.
    Requires the full chain (DATA, CLAIM, WARRANT, BACKING, REBUTTAL, QUALIFIER).
    """
    # Construct the chain to validate dependencies
    chain = ToulminChain(
        data=data,
        claim=claim,
        warrant=warrant,
        backing=backing,
        rebuttal=rebuttal,
        qualifier=qualifier,
        verdict=None # Not yet generated
    )
    # If validation passes (which it should if inputs are valid), generate prompt.
    return render_verdict(chain)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
