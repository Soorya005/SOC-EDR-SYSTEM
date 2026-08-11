import os
import sys
import yaml

# Make detection/ available for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from sigma.engine import SigmaEngine


# ---------------------------------------------------------
# Find the LSASS rule
# ---------------------------------------------------------
RULE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "sigma-rules",
    "custom",
    "lsass_access_non_standard.yml"
)


# ---------------------------------------------------------
# Load the real rule
# ---------------------------------------------------------
if not os.path.exists(RULE_PATH):
    print(f"[ERROR] Rule file not found:")
    print(RULE_PATH)
    sys.exit(1)

with open(RULE_PATH, "r", encoding="utf-8") as f:
    rule = yaml.safe_load(f)

print("=" * 60)
print("LSASS SIGMA RULE TEST")
print("=" * 60)
print(f"Rule: {rule.get('title')}")
print(f"ID:   {rule.get('id')}")
print()


# ---------------------------------------------------------
# Create Sigma engine using the REAL rule
# ---------------------------------------------------------
engine = SigmaEngine([rule])


# ---------------------------------------------------------
# Test events
# ---------------------------------------------------------
tests = [

    {
        "name": "Legitimate McAfee access",
        "event": {
            "event_id": 10,
            "source_image":
                r"C:\Program Files\McAfee\WebAdvisor\ServiceHost.exe",
            "target_image":
                r"C:\Windows\System32\lsass.exe",
            "granted_access": "0x1000"
        },
        "expected": False
    },

    {
        "name": "Potential suspicious LSASS access",
        "event": {
            "event_id": 10,
            "source_image":
                r"C:\EDR-Test\test-process.exe",
            "target_image":
                r"C:\Windows\System32\lsass.exe",
            "granted_access": "0x1410"
        },
        "expected": True
    },

    {
        "name": "Substring test - 0x101000",
        "event": {
            "event_id": 10,
            "source_image":
                r"C:\EDR-Test\test-process.exe",
            "target_image":
                r"C:\Windows\System32\lsass.exe",
            "granted_access": "0x101000"
        },
        "expected": False
    }
]


# ---------------------------------------------------------
# Run tests
# ---------------------------------------------------------
passed = 0
failed = 0

for test in tests:

    name = test["name"]
    event = test["event"]
    expected = test["expected"]

    print("-" * 60)
    print(f"TEST: {name}")
    print(f"Source:  {event['source_image']}")
    print(f"Target:  {event['target_image']}")
    print(f"Access:  {event['granted_access']}")

    matches = engine.match_event(event)

    actual = bool(matches)

    print(f"Expected: {'MATCH' if expected else 'NO MATCH'}")
    print(f"Actual:   {'MATCH' if actual else 'NO MATCH'}")

    if actual == expected:
        print("RESULT:   PASS")
        passed += 1
    else:
        print("RESULT:   FAIL")
        failed += 1

    if matches:
        for match in matches:
            print(f"Rule:     {match['rule_name']}")
            print(f"Severity: {match['severity']}")
            print(f"MITRE:    {match['technique_id']}")


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print()
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed == 0:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")