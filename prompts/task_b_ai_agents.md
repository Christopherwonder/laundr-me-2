You are an expert AI/ML engineer. Your task is to implement the foundational stubs for the autonomous AI workforce for the laundr.me application, specifically the Security Agents. You must adhere to the project's master specifications.

**Project Monorepo Structure:**

- `/agents`: This is your focus directory.
- The scaffolding is already complete. You will be working in the `/agents` directory.

**Core Requirements:**

1.  **Implement Foundational Stubs:** Your primary goal is to create the Python stubs for the core Security Agent services. These services will be called by the main backend API.
2.  **Create Core Services:**
    - **`FraudService`:** Create a class or function that provides risk scoring for transactions. For now, this can be a simple rule-based function (e.g., based on transaction amount), but it must have a clear input (transaction details) and output (a risk score).
    - **`VelocityChecker`:** Create a service to flag rapid, repeated transactions. It should accept user ID and transaction details and return a flag if thresholds are exceeded. The logic can be mocked for now.
    - **`AnomalyDetector`:** Create a service for behavioral analysis. It should accept user actions and identify unusual patterns. The logic can be mocked for now.
3.  **Design for Integration:** Each service must be designed as a callable function or class with clear inputs and outputs, ready to be integrated into the backend's compliance middleware.
4.  **Implement Audit Logging:** Every decision, check, or flag raised by an agent must be logged. You can implement this by printing to the console or calling a stubbed logging service.
5.  **Mock Data:** For this initial task, the services can return mock or hardcoded data (e.g., `return {'risk_score': 0.1}`), but they **must** have the correct signatures and logic structure to be integrated into the backend later.
