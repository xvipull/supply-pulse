import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def test_pipeline_generates_reconciled_dashboard():
    subprocess.run([sys.executable, "src/generate_data.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "src/pipeline.py"], cwd=ROOT, check=True)
    report=json.loads((ROOT/"reports/data_quality_report.json").read_text())
    dashboard=json.loads((ROOT/"web/data.json").read_text())
    assert report["status"] == "PASS" and report["reconciliation"]["difference"] == 0
    assert len(dashboard["suppliers"]) == 6 and dashboard["totals"]["otif"] > 0
