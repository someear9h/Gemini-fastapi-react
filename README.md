# AI-Powered Interactive Story Generator

[![Status](https://img.shields.io/badge/status-live-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

This is a full-stack web application that leverages the power of Google's Gemini 1.5 Flash to create dynamic, choice-driven narratives. Users provide a theme, and the AI crafts a unique story in real-time, offering branching paths that allow the user to shape their own adventure.

This project showcases a modern architecture, seamless frontend-backend communication, and the integration of a cutting-edge Large Language Model (LLM) into a user-facing product.

---

## 🚀 Live Demo

**Experience the application live:** **[https://bd2d1ae1-6d74-40e9-8fa6-9162d91109d4.e1-us-east-azure.choreoapps.dev/](https://bd2d1ae1-6d74-40e9-8fa6-9162d91109d4.e1-us-east-azure.choreoapps.dev/)**

*(Note: The initial story generation might take a few seconds as the AI crafts the narrative.)*

![Project Screenshot or GIF](https://your-link-to-a-screenshot-or-gif.com/demo.gif)
*(Recommendation: Record a short GIF of your app in action and replace the link above. It's highly effective.)*

---

## ✨ Key Features

* **Dynamic Story Generation:** Utilizes the Gemini 1.5 Flash API to generate creative and coherent stories from a single user-provided theme.
* **Interactive Branching Narratives:** Presents users with multiple choices at key points, directly influencing the story's direction and outcome.
* **Real-time Interaction:** A responsive React frontend communicates seamlessly with the FastAPI backend to provide a smooth, engaging user experience.
* **Scalable Backend:** Built with FastAPI for high-performance, asynchronous request handling, ready to scale for more users.
* **Cloud-Native Deployment:** Fully containerized and deployed on Choreo, demonstrating a modern CI/CD workflow and cloud architecture.
* **(In Progress) Persistent Adventures:** Database integration using PostgreSQL to allow users to save and continue their stories across sessions.

---

## 💻 Tech Stack & Architecture

This project was built using a modern, robust tech stack designed for performance, scalability, and a great developer experience.

| Frontend                                                                                                                              | Backend                                                                                                                                  | AI & Database                                                                                                                                               | Deployment                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)                                     | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)                                                   | ![Google Gemini](https://img.shields.io/badge/Gemini_1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)                                     | ![Choreo](https://img.shields.io/badge/Choreo-FF7300?style=for-the-badge&logo=wSo2&logoColor=white)                                       |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)                       | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)                                     | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) *(or SQLite for local dev)* | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)                                   |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)                                         | ![Uvicorn](https://img.shields.io/badge/Uvicorn-009688?style=for-the-badge)                                                               | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-b30000?style=for-the-badge)                                                                          |                                                                                                                                        |

### System Architecture
The application follows a classic microservices-oriented architecture:

`User (React Frontend)` ➡️ `Choreo API Gateway` ➡️ `FastAPI Backend Service` ➡️ `Google Gemini API & PostgreSQL Database`

---

## 🛠️ Getting Started Locally

To run this project on your local machine, follow these steps.

### Prerequisites

* Python 3.9+
* Node.js v18+ and npm
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Setup Environment Variables

The application requires API keys to function. Create a `.env` file in the `backend` directory:

```bash
# backend/.env

GEMINI_API_KEY="your_google_gemini_api_key"
# Add this line after you set up a cloud database
# DATABASE_URL="postgresql://user:password@host:port/dbname"
```

### 3. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```
The backend API will be running at `http://localhost:8000`.

### 4. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Run the development server
npm start
```
The React application will be available at `http://localhost:3000`.

---

## 🔮 Future Improvements

I believe in iterative development. Here are some features I plan to add:

* **User Authentication:** Implement JWT-based authentication to allow users to create accounts and save their unique stories.
* **Story Gallery:** Create a public gallery where users can share their favorite completed narratives with others.
* **AI-Generated Images:** Integrate an image generation model (e.g., DALL-E or Midjourney) to create a unique visual for each step of the story.

---

## 📫 Contact

I'm actively seeking Full-Stack and Backend Developer roles. If you liked my project and think I'd be a good fit for your team, I'd love to connect!

* **Email:** samarthsetz@gmail.com