You are an expert AI/ML engineer specializing in RegTech. Your task is to build the persistent Regulatory Compliance Agent.

**Core Requirements:**

1.  **Scaffold Agent:** In the `/agents` directory, create a new, persistent agent: `/agents/regops_agent.py`.
2.  **Implement Regulatory Monitoring:** Create a module for the agent to monitor external regulatory data sources. For this build, simulate this by having the agent periodically read a `regulatory_updates.json` file that contains mock updates (e.g., "New KYC data point required").
3.  **Implement Policy-as-Code:** Externalize all critical compliance parameters into a version-controlled configuration file: `/orchestration/compliance_policy.yml`. This file should define rules like required KYC fields, transaction velocity limits, etc.
4.  **Implement Impact Analysis:** When the agent detects a change, it must determine which rules in `compliance_policy.yml` are affected and generate a markdown report for the human oversight team outlining the change and its impact.
5.  **Log All Actions:** Ensure every action taken by the agent is logged to the main audit service (stubbed).
