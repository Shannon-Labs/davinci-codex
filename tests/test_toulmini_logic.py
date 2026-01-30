import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from toulmini.prompts import (
    initiate_toulmin_sequence,
    inject_logic_bridge,
    stress_test_argument,
    render_verdict
)
from toulmini.models import ToulminChain
from pydantic import ValidationError

def test_prompts():
    print("Testing Prompts...")
    
    # 1. Initiate
    p1 = initiate_toulmin_sequence("Is this copyright infringement?")
    assert "DATA" in p1
    assert "CLAIM" in p1
    assert "JSON ONLY" in p1
    print("  [x] Initiate Prompt")

    # 2. Bridge
    p2 = inject_logic_bridge("Data", "Claim")
    assert "WARRANT" in p2
    assert "BACKING" in p2
    print("  [x] Bridge Prompt")

    # 3. Stress Test
    p3 = stress_test_argument("Data", "Claim", "Warrant", "Backing")
    assert "REBUTTAL" in p3
    assert "QUALIFIER" in p3
    print("  [x] Stress Test Prompt")

    # 4. Verdict
    chain = ToulminChain(
        data="Data",
        claim="Claim",
        warrant="Warrant",
        backing="Backing",
        rebuttal="Rebuttal",
        qualifier="Qualifier"
    )
    p4 = render_verdict(chain)
    assert "VERDICT" in p4
    print("  [x] Verdict Prompt")

def test_validation():
    print("\nTesting Validation...")

    # Valid Chain
    try:
        ToulminChain(
            data="D", claim="C", warrant="W", backing="B", rebuttal="R", qualifier="Q", verdict="V"
        )
        print("  [x] Valid Chain accepted")
    except ValidationError as e:
        print(f"  [ ] Valid Chain FAILED: {e}")

    # Invalid: Claim without Data
    try:
        ToulminChain(claim="C")
        print("  [ ] Claim without Data accepted (FAIL)")
    except ValidationError as e:
        print(f"  [x] Claim without Data rejected: {e}")

    # Invalid: Warrant without Claim
    try:
        ToulminChain(data="D", warrant="W")
        print("  [ ] Warrant without Claim accepted (FAIL)")
    except ValidationError as e:
        print(f"  [x] Warrant without Claim rejected: {e}")

    # Invalid: Verdict without Rebuttal
    try:
        ToulminChain(
            data="D", claim="C", warrant="W", backing="B", qualifier="Q", verdict="V"
        )
        print("  [ ] Verdict without Rebuttal accepted (FAIL)")
    except ValidationError as e:
        print(f"  [x] Verdict without Rebuttal rejected: {e}")

if __name__ == "__main__":
    test_prompts()
    test_validation()
