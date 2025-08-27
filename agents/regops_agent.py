import json
import yaml
import os
from .utils.logging import log_audit

class RegOpsAgent:
    def __init__(self, policy_path='orchestration/compliance_policy.yml', updates_path='orchestration/regulatory_updates.json'):
        self.policy_path = policy_path
        self.updates_path = updates_path
        self.report_path = 'impact_report.md'

    def monitor_and_report(self):
        log_audit("Starting regulatory monitoring and reporting cycle.")

        # Read compliance policy
        with open(self.policy_path, 'r') as f:
            policy = yaml.safe_load(f)
        log_audit(f"Loaded compliance policy from {self.policy_path}")

        # Read regulatory updates
        with open(self.updates_path, 'r') as f:
            updates = json.load(f)
        log_audit(f"Loaded regulatory updates from {self.updates_path}")

        # Analyze impact
        report_content = self._analyze_impact(policy, updates)

        # Generate report
        if report_content:
            with open(self.report_path, 'w') as f:
                f.write(report_content)
            log_audit(f"Generated impact report at {self.report_path}")
        else:
            log_audit("No new impacts detected.")

        log_audit("Regulatory monitoring and reporting cycle complete.")

    def _analyze_impact(self, policy, updates):
        impacts = []
        kyc_policy = policy.get('kyc_requirements', [])

        for update in updates.get('updates', []):
            if "KYC data point required" in update['description']:
                new_field = update['description'].split("'")[1]
                if new_field not in kyc_policy:
                    impacts.append(
                        f"- **Regulatory Update:** {update['update_id']}\n"
                        f"  - **Description:** {update['description']}\n"
                        f"  - **Impact:** The compliance policy is missing the new KYC field: `{new_field}`."
                    )

        if not impacts:
            return None

        report = "# Regulatory Impact Analysis Report\n\n"
        report += "The following regulatory updates require changes to the compliance policy:\n\n"
        report += "\n".join(impacts)
        return report
