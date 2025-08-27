You are an expert backend software engineer specializing in compliance and system architecture. Your task is to implement the RegOps Compliance Coprocessor and Orchestration layer for the laundr.me backend.

**Context:** The user profile/KYC endpoints (Task A) and the AI Security Agent stubs (Task B) are complete. Your job is to integrate them.

**Core Requirements:**
1.  **Implement Compliance Middleware:** In the `/backend` directory, create a FastAPI middleware layer. This middleware must intercept all incoming financial transaction requests.
2.  **Perform Real-Time Checks:** Inside the middleware, you must:
    - Verify the user's KYC status by checking the data stored from the Task A workflow.
    - Call the Security Agent services from Task B (`FraudService`, `VelocityChecker`, etc.) to perform risk analysis on the incoming request.
    - If KYC fails or risk is too high, the middleware must reject the request with an appropriate HTTP error.
3.  **Implement Astra Contract Sentinel:** Create a utility module that validates all outgoing requests to the Astra API. This utility should check that the required parameters and schemas (as defined in the project's Astra documentation) are correct before the request is sent.
4.  **Create Orchestration File:** Create the orchestration file at `/orchestration/jules_dag.yml`. This YAML file should explicitly map the dependency graph between all modules and agents (e.g., `compliance_middleware` depends on `fraud_service`).
