You are an expert backend software engineer. Your task is to implement the core financial API endpoints for the "Loads" tab of the laundr.me application.

**Context:** The core compliance middleware (Task C) is now in place. All your endpoints will operate behind this middleware.

**Core Requirements:**
1.  **Implement Loads Endpoints:** In the `/backend` directory, create FastAPI endpoints for `/send-load`, `/request-load`, and `/swap-funds`.
2.  **Integrate with Astra API:** All money movement must be processed by calling the Astra API's `POST /v1/routines` endpoint.
3.  **Rigorously Enforce Fee Logic:**
    - The total fee must be calculated as `max($1.50, (0.03 * Amount) + $0.74)`.
    - This fee must be split 50/50 between the sender and the recipient.
    - The $5.00 minimum transaction amount must be enforced.
4.  **Handle Off-Platform Users:** For the `/send-load` flow, if the recipient is not on the platform, your API must generate a temporary, secure invite link with a 30-minute claim window.
5.  **Log Everything:** Every transaction must be logged to a dedicated, immutable audit service (you can stub calls to this service).
6.  **Write Unit Tests:** Create comprehensive unit tests covering the happy path, all fee calculations, minimum amount enforcement, and invalid user inputs.
