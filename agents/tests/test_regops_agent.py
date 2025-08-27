import sys
import os
import pytest
import yaml
import json

# Add the 'agents' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.regops_agent import RegOpsAgent

@pytest.fixture
def file_setup(tmp_path):
    policy_path = tmp_path / "compliance_policy.yml"
    updates_path = tmp_path / "regulatory_updates.json"
    report_path = tmp_path / "impact_report.md"

    # Create mock policy file
    policy_content = {
        'kyc_requirements': ['full_name', 'date_of_birth']
    }
    with open(policy_path, 'w') as f:
        yaml.dump(policy_content, f)

    # Create mock updates file
    updates_content = {
        "updates": [
            {
                "update_id": "REG-2023-001",
                "description": "New KYC data point required: 'proof_of_address'.",
                "effective_date": "2023-12-01"
            }
        ]
    }
    with open(updates_path, 'w') as f:
        json.dump(updates_content, f)

    return str(policy_path), str(updates_path), str(report_path)

def test_regops_agent_report_generation(file_setup):
    policy_path, updates_path, report_path = file_setup

    agent = RegOpsAgent(policy_path=policy_path, updates_path=updates_path)
    agent.report_path = report_path
    agent.monitor_and_report()

    assert os.path.exists(report_path)

    with open(report_path, 'r') as f:
        content = f.read()

    assert "Regulatory Impact Analysis Report" in content
    assert "proof_of_address" in content
