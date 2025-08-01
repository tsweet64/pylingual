import json

# Counters
total = passed = failed = errored = 0
details = []

with open("test_output.jsonl") as f:
    for line in f:
        try:
            data = json.loads(line)
            for entry in data.get("equivalence_report", []):
                total += 1
                status = entry["status"]
                name = entry["name"]
                file = entry.get("file", "unknown")

                if status == "true":
                    passed += 1
                elif status == "false":
                    failed += 1
                elif status == "error":
                    errored += 1

                details.append(f"{status.upper():<6} {file}::{name}")
        except:
            pass

# Output summary
print(f"\n=== Test Summary ===")
print(f"Total:   {total}")
print(f"Passed:  {passed}")
print(f"Failed:  {failed}")
print(f"Errored: {errored}")
print("\n=== Details ===")
for line in details:
    print(line)

# Fail the job if any failed or errored
if failed > 0 or errored > 0:
    exit(1)

