You are an expert QA engineer. Your task is to write and run a full end-to-end integration test suite for the laundr.me application.

**Core Requirements:**

1.  **Write E2E Test Suite:** Using a suitable framework (e.g., Playwright for web, or a custom script), write tests that simulate full user flows in the Astra Sandbox Environment.
2.  **Validate Golden Paths:** The suite must validate at a minimum:
    - User Signup -> KYC Verification -> Send Load -> Recipient Receives Funds.
    - Client Finds Freelancer -> Requests Booking -> Freelancer Counters -> Client Accepts -> Pays Deposit.
3.  **Validate Fee Calculation:** Create a "fee math oracle" test that sends transactions of various amounts ($10, $50, $100, $500) and asserts that the fee calculation and 50/50 split are correct to the cent.
4.  **Test Webhooks:** Implement a test to verify that the backend correctly handles and verifies HMAC signatures on incoming webhooks from Astra.
5.  **Test Idempotency:** Write a test that sends the same creation request (e.g., send load) multiple times and asserts that the action is only performed once.
6.  **Generate Report:** The final output of this task must be a script that runs all tests and generates a `spec_conformance_report.md`.
