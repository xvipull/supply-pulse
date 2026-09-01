import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class PipelineTest(unittest.TestCase):
    def test_pipeline_generates_reconciled_dashboard(self):
        subprocess.run([sys.executable, "src/generate_data.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "src/pipeline.py"], cwd=ROOT, check=True)
        report=json.loads((ROOT/"reports/data_quality_report.json").read_text())
        dashboard=json.loads((ROOT/"web/data.json").read_text())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["reconciliation"]["difference"], 0)
        self.assertEqual(len(dashboard["suppliers"]), 6)
        self.assertGreater(dashboard["totals"]["otif"], 0)
