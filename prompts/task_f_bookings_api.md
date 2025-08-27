You are an expert backend software engineer. Your task is to implement the booking and negotiation system API for the laundr.me application.

**Context:** The core financial "Loads" API (Task D) is complete.

**Core Requirements:**
1.  **Implement Booking System API:** In `/backend`, create endpoints for:
    - Freelancer calendar availability (`/calendar/availability`).
    - Creating specific and generic booking requests.
    - Managing (creating/updating/deleting) freelancer calendar events.
2.  **Build "No-Chat Negotiation Loop":** Create the stateful endpoints for the negotiation process: `/bookings/approve`, `/bookings/decline`, `/bookings/counter`.
3.  **Implement Deposit Handling:** A deposit request must be processed as a standard P2P "Load" transfer. You must call the financial API from Task D to execute this.
4.  **Implement Slot Reservation:** Implement a 10-minute temporary hold (e.g., using a Redis cache or similar) on a time slot when a client begins the booking process.
5.  **Log Negotiation History:** Every step of the negotiation and booking lifecycle must be logged to the audit service (stubbed).
6.  **Write Unit Tests:** Write tests covering the entire booking lifecycle: request -> counter -> approval -> deposit -> confirmation.
