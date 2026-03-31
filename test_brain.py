# test_brain.py
import os
import sys

# Tell Python where the backend folder is
sys.path.append(os.path.join(os.getcwd(), "backend"))

from backend.app.services.orchestrator import CourseOrchestrator


def test_mini2():
    print("Testing Mini2 Local Brain...")
    try:
        # Initialize for DBMS
        bot = CourseOrchestrator("DBMS")

        # Ask a question found in your PDF
        query = "What is Normalization?"
        print(f"User Query: {query}")

        # Generate Answer
        response = bot.generate(query)

        print("\n--- AI RESPONSE ---")
        print(response)
        print("-------------------\n")
        print("Test Passed: RAG and LLM are communicating!")

    except Exception as e:
        print(f"Test Failed! Error: {e}")


if __name__ == "__main__":
    test_mini2()