from .models import ToulminChain

def initiate_toulmin_sequence(query: str) -> str:
    return f"""
You are a Logic Engine. You do not chat. You do not explain.
You are initializing a Toulmin Argumentation Sequence for the following query:
"{query}"

Your Goal: Extract the raw DATA (Grounds) and formulate the initial CLAIM.
Do NOT provide the Warrant, Backing, Rebuttal, or Verdict yet.

Output Format: JSON ONLY.
{{
    "data": "The raw facts/evidence. Must be cited if possible.",
    "claim": "The assertion being made based ONLY on the Data."
}}
"""

def inject_logic_bridge(data: str, claim: str) -> str:
    return f"""
You are a Logic Engine.
Current State:
DATA: {data}
CLAIM: {claim}

Your Goal: Provide the WARRANT and BACKING.
- WARRANT: The logical principle connecting Data to Claim.
- BACKING: The statutory, legal, or scientific support for the Warrant.

If the Backing is weak, you must reject the Warrant (but for this step, attempt to find the strongest backing).

Output Format: JSON ONLY.
{{
    "warrant": "The logical bridge.",
    "backing": "The support for the bridge."
}}
"""

def stress_test_argument(data: str, claim: str, warrant: str, backing: str) -> str:
    return f"""
You are a Logic Engine.
Current State:
DATA: {data}
CLAIM: {claim}
WARRANT: {warrant}
BACKING: {backing}

Your Goal: Identify the REBUTTAL and QUALIFIER.
- REBUTTAL: Specific conditions where the Warrant does not apply (Edge cases, "Black Swans").
- QUALIFIER: The degree of force (e.g., "Presumably", "Always", "Unless").

Look for exceptions. Be critical.

Output Format: JSON ONLY.
{{
    "rebuttal": "The exception/counter-argument.",
    "qualifier": "The degree of certainty."
}}
"""

def render_verdict(chain: ToulminChain) -> str:
    # We assume chain is fully populated except maybe verdict, or we are asking for verdict.
    # The tool input is the full chain so far.
    return f"""
You are a Logic Engine.
Final Step: Synthesis.

Review the full Toulmin Chain:
DATA: {chain.data}
CLAIM: {chain.claim}
WARRANT: {chain.warrant}
BACKING: {chain.backing}
REBUTTAL: {chain.rebuttal}
QUALIFIER: {chain.qualifier}

Your Goal: Render the VERDICT.
Given the Rebuttal and Qualifier, does the Claim stand?

Output Format: JSON ONLY.
{{
    "verdict": "The final synthesis."
}}
"""
