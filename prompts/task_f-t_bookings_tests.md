You are an expert backend QA engineer. Your task is to write the missing unit tests for the Booking & Negotiation API of the laundr.me application.

**Context:**
The code for the Booking & Negotiation API has already been written by another developer as part of Task F. However, they failed to provide the required tests. Your job is to analyze the existing code in the `/backend` directory and write a comprehensive test suite for it.

**Core Requirements:**
1.  **Analyze Existing Code:** Review the existing API endpoints related to the booking system, including calendar management, creating booking requests, and the "No-Chat Negotiation Loop" (`/bookings/approve`, `/bookings/decline`, `/bookings/counter`).
2.  **Write Comprehensive Unit Tests:** Using `pytest`, write unit tests that cover the entire booking and negotiation lifecycle.
    - Test the creation of specific and generic booking requests.
    - Test the negotiation flow: a client makes a request, the freelancer counters, the client accepts.
    - Test the deposit handling logic to ensure it correctly triggers a P2P Load transfer.
    - Test all failure modes and edge cases (e.g., declining a negotiation, invalid inputs).
3.  **Ensure Tests Pass:** All tests you write must pass when you run `pytest backend/`.

**Location of Work:**
-   Analyze the code in the `/backend` directory.
-   Create your new test files within a `/backend/tests` directory. Follow standard `pytest` conventions for test file naming (e.g., `test_bookings_api.py`).
