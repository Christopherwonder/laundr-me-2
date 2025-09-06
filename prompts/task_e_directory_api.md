You are an expert backend software engineer. Your task is to implement the Directory and Marketplace API endpoints for the laundr.me application.

**Core Requirements:**

1.  **Implement Directory Endpoints:** In the `/backend` directory, create the following FastAPI endpoints:
    - `/search`: This endpoint must support searching for users and freelancers by name, `@laundrID`, skills, etc.
    - `/freelancers/filter`: An endpoint to filter freelancers by category, location, rating, etc.
    - `/freelancers/sort`: An endpoint to sort freelancers.
2.  **Integrate Ranking Agent:** The API must accept parameters for the AI Directory Ranking Agent (rating, sentiment, activity, proximity, price) to influence search results. You will not implement the agent itself, but your API must be able to use its inputs.
3.  **Differentiate User Types:** The API responses must have a clear, distinct structure for general users vs. freelancer profiles.
4.  **Write Ranking Regression Tests:** Write tests to ensure that for a given set of inputs, the sorting and ranking results are deterministic and predictable.
