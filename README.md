laundr.me: The Unified Super-App for the Side Hustle Economy
Overview
laundr.me is the essential, all-in-one digital toolkit for the modern freelancer and gig worker. Our mission is to deliver the undisputed super-app that defines the new economy by seamlessly integrating a talent marketplace, a payment network, a booking engine, and client management tools into a single, frictionless experience. The application is powered by a multi-tiered autonomous AI workforce that constantly monitors and improves security, operations, and user satisfaction.
The application is a hybrid of best-in-class service apps:
 * Yelp + TaskRabbit: A dynamic, trusted marketplace to discover, rate, and book talent. The app serves as a digital storefront for freelancers, empowering them with a professional profile and a clear, user-friendly interface for clients to find and engage them based on skills, reviews, and availability.
 * Venmo + Cash App: A viral, lightning-fast P2P payment network. Financial transfers are officially called "loads". The "Loads" tab is designed to be the fastest way to move money, making financial transfers instant and easy.
 * Calendly: A seamless, intuitive scheduling engine. The Bookings Calendar provides a shared view of availability, eliminating the back-and-forth of email chains and messages.
 * QuickBooks: A lightweight financial command center for solopreneurs. The Activity/History tab and its tax export feature give freelancers a simple, centralized tool to manage their income and expenses related to their side hustles.
 * Zoho: A simplified CRM for managing client relationships. The lightweight CRM allows users to save contacts and add private notes, which is crucial for building and maintaining a professional client list over time.
Technical Architecture
Our development philosophy is "build first and open-source second" to maximize velocity and ownership.
 * Frontend: React Native with Expo.
 * Backend: Python (FastAPI).
 * Database: PostgreSQL for persistent data like user profiles, transactions, and appointments.
 * Cache: Redis for session management and real-time features.
 * CI/CD: The project includes a continuous integration pipeline for linting, testing, and security scanning.
 * Security: We utilize JWT for API authentication, Bcrypt for password hashing, and SSL/TLS for all data in transit. All user-facing changes require human approval via a dedicated CI/CD gate before deployment.
## Running the Prototype

This repository contains a functional frontend prototype that can be run without the backend. The prototype uses mocked data to simulate API calls.

To run the prototype, follow these steps:

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install the dependencies:**
    ```bash
    npm install
    ```

3.  **Start the application:**
    ```bash
    npm start
    ```

This will start the Expo development server and open a new browser tab with the Expo Developer Tools. From there, you can:
*   **Run on an iOS simulator:** Click "Run on iOS simulator". (Requires Xcode to be installed on a Mac).
*   **Run on a physical device:** Download the "Expo Go" app on your iPhone. Then, scan the QR code shown in the terminal or in the browser tab with your phone's camera.

**Note:** The backend is not required to run the prototype. The instructions in the "Getting Started" section below are for running the full application with the live backend.

Getting Started
The laundr.me application is a monorepo that contains both frontend and backend packages.

Prerequisites:
 * Python 3.11+
 * Node.js 22+ (which includes npm)
 * Redis

Setup & Running:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/laundr.me.git
   cd laundr.me
   ```

2. **Run the backend:**
   - Install dependencies:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - Start the FastAPI server:
     ```bash
     uvicorn app.main:app --reload --app-dir backend
     ```
   The API will be available at `http://127.0.0.1:8000`.

3. **Run the frontend:**
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Install dependencies:
     ```bash
     npm install
     ```
   - Start the Expo development server:
     ```bash
     npm start
     ```
   This will open a browser window with the Expo developer tools. You can then run the app on a simulator or on your physical device using the Expo Go app.

Contribution
We follow a "build first, open-source second" philosophy to maximize velocity and ownership. The project is not currently open for external contributions.
License
All rights are reserved.
