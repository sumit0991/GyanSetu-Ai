Mini2: Professional Exam Notes Generator
Mini2 is an AI-powered educational tool designed to transform a raw syllabus
into highly structured, exam-ready study materials. It leverages RAG (Retrieval-Augmented Generation) 
to extract context from local subject PDFs and synthesizes it into a professional layout
complete with diagrams and video tutorials.

🚀 Key Features
Vertical Structured Notes: Automatically generates content in a specific hierarchy:
Definition → Detailed Explanation → Key Features → Advantages/Disadvantages → Examples.

Intelligent RAG System: Pulls factual data from your uploaded Subject Library (e.g., DBMS PDFs) 
to ensure technical accuracy.

Smart Media Injection:

Diagrams: Fetches technical reference images and injects them into relevant sections of the notes.

Videos: Curates full-width YouTube tutorials for every topic.

Exam-Ready UI: Features a clean, dual-tab interface for "Study Notes" and "Videos," optimized for both 
digital reading and physical printing.

⚙️ Setup & Installation
1. Backend Setup
Navigate to the backend folder.

Install dependencies: pip install fastapi uvicorn openai chromadb langchain
(ensure your specific RAG requirements are met).

Place your subject PDFs in the data/docs/ folder.

Run the server:

Bash
uvicorn backend.app.main:app --reload

2. Frontend Setup
Open index.html in any modern web browser.

Ensure the backend URL in the askAI() function matches your running server (default: http://127.0.0.1:8000).

📖 How to Use
Select Subject: Choose your subject from the "Subject Library" dropdown (e.g., DBMS).

Paste Syllabus: Enter your topics in the "Module Syllabus" box, separated by hyphens
(e.g., ACID Properties - Indexing - Deadlocks).

Generate: Click Generate Detailed Notes.

Study & Print:

Toggle between the 📄 STUDY NOTES and 🎥 VIDEO TUTORIALS tabs.

Use the 🖨️ Print Notes button to save a perfectly formatted PDF version for offline study.

📝 Note on Structure
The system is hard-coded to follow a strict professional flow to prevent cluttered text blocks.
If you wish to change the sections, modify the structured_instruction variable within orchestrator.py.