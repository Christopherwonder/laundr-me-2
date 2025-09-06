You are an expert frontend software engineer. Your task is to implement the complete user interface for the laundr.me mobile application and connect it to the backend APIs.

**Context:** All backend APIs are now complete and documented. The frontend project has been initialized in `/frontend` with React Native (Expo) and Tailwind CSS.

**Core Requirements:**

1.  **Implement All 5 Tabs:** Build the UI for the 5 primary tabs using React Native and Tailwind CSS: Loads, Directory, Bookings, Activity, Profile.
2.  **Adhere to Branding:**
    - **Typography:** Use Nunito Sans exclusively.
    - **Color Palette:** Use Primary Black (#000000), Primary White (#FFFFFF), and Brand Hot Pink (#FF0088).
    - **Signature Effect:** All active buttons, CTAs, and interactive elements must have the signature Neon Glow Effect: `box-shadow: 0 0 20px rgba(255, 0, 136, 0.6)`.
3.  **Connect to Backend:** Connect all frontend components to the backend APIs you've been provided with. Implement client-side state management to handle user data, transaction history, etc.
4.  **Implement Core Flows:**
    - **KYC Onboarding:** The very first flow a user sees must be the KYC onboarding. The main app should be inaccessible until KYC is verified.
    - **Real-Time Fee Calculation:** On the Loads tab, the fee must be calculated and displayed in real-time as the user types.
    - **Biometric Authorization:** Use native device authentication (Face ID/Touch ID/PIN) to authorize all transactions.
5.  **Write Component Unit Tests:** Use a library like React Testing Library to verify component rendering and user interactions.
