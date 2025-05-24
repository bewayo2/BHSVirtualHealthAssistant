# JAMCare Virtual Health Assistant Frontend

This is the React frontend for the JAMCare Virtual Health Assistant. It is designed to be mobile-first, accessible, and compliant with Jamaican and international health data regulations.

## Features
- Mobile-first, accessible chat interface
- "Request Nurse Call-Back" button after each answer
- Language toggle: English | Patwa (Patois)
- High-contrast mode and text resize
- Audio summary option for low-vision users
- Compliance banners and privacy notice

## Setup
1. Install dependencies:
   ```
   npm install
   ```
2. Start the development server:
   ```
   npm run dev
   ```

## Configuration
- The frontend expects the backend to be running at `http://localhost:8000` by default. You can change this in the `.env` file.

## Next Steps
- Connect to the FastAPI backend
- Implement accessibility and compliance features 