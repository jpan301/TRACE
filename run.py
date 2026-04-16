from auditor import run_audit
import sys

if __name__ == "__main__":
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    run_audit(repo_path)
