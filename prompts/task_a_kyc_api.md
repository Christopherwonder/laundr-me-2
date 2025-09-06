You are an expert backend software engineer. Your task is to implement the Profile, Settings, and KYC API endpoints for the laundr.me application. You must adhere to the project's master specifications.

**Project Monorepo Structure:**

- `/frontend`: React Native (Expo) app
- `/backend`: Python FastAPI service (this is your focus)
- The scaffolding is already complete. You will be working in the `/backend` directory.

**Core Requirements:**

1.  **Implement User Profile Management:** Create FastAPI endpoints for creating and updating user profiles. This includes managing a user's unique `@laundrID`, bio, professional headline, skill tags, etc.
2.  **Integrate Astra for KYC:** The user creation process **must** be integrated with the Astra Financial API's UserIntent workflow.
    - When a new user signs up, your endpoint must call Astra's `POST /v1/user_intents` endpoint to create a UserIntent.
    - This is a mandatory step. Store the resulting `user_intent_id`.
3.  **Enforce KYC Verification:** Implement a dependency or middleware that gates all financial and sensitive endpoints. These endpoints must check that the user has a "verified" KYC status before allowing the request to proceed. Unverified users cannot transact.
4.  **Implement Settings Endpoints:** Create API endpoints for managing account and security settings, including toggles for biometric/PIN requirements, notification preferences, and spending limits.
5.  **Write Unit Tests:** Create comprehensive unit tests for your endpoints. Crucially, write tests to verify that the KYC enforcement correctly blocks unverified users and that user preferences are saved and retrieved correctly.

**Key Invariants to Follow:**

- **Technology:** Python with FastAPI.
- **Database:** Assume PostgreSQL (you can mock the database connection for now).
- **Security:** All state-changing actions must be designed to be logged by a dedicated audit service (you can stub calls to this service).
