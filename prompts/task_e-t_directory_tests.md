You are an expert backend QA engineer. Your task is to write the missing unit and regression tests for the Directory & Marketplace API of the laundr.me application.

**Context:**
The code for the Directory & Marketplace API has already been written by another developer as part of Task E. However, they failed to provide the required tests. Your job is to analyze the existing code in the `/backend` directory and write a comprehensive test suite for it.

**Core Requirements:**
1.  **Analyze Existing Code:** Review the existing API endpoints related to the Directory and Marketplace (`/search`, `/freelancers/filter`, `/freelancers/sort`).
2.  **Write Unit Tests:** Using `pytest`, write unit tests that cover the functionality of these endpoints. This should include testing with valid inputs, invalid inputs, edge cases, and different user types.
3.  **Write Ranking Regression Tests:** A key requirement from the original task was to write regression tests for the sorting and ranking logic. You must create tests that provide a fixed set of inputs (for freelancer data and ranking parameters) and assert that the sorted/ranked output is exactly as expected. This ensures that changes to the ranking algorithm in the future do not have unintended consequences.
4.  **Ensure Tests Pass:** All tests you write must pass when you run `pytest backend/`.

**Location of Work:**
-   Analyze the code in the `/backend` directory.
-   Create your new test files within a `/backend/tests` directory (you may need to create this directory). Follow standard `pytest` conventions for test file naming (e.g., `test_directory_api.py`).
