import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from tools import (
    search_flights,
    book_flight,
    search_hotels,
    book_hotel,
    search_attractions,
    book_attraction,
)

# Load environment variables
load_dotenv()

def create_travel_agent():
    """Creates and configures the travel planning agent."""
    
    # Initialize the model
    # Using flash-lite as per recommended practices for efficiency
    model = Gemini(model="gemini-2.5-flash-lite")
    
    # Define instructions
    instructions = """
    You are a helpful and capable Travel Planning Agent.
    Your goal is to help a family plan their travel, including flights, hotels, and attractions.

    Current Date: 2025-05-15 (Simulated)

    GUIDELINES:
    1.  **Gather Information**: First, understand the user's destination, dates, budget, and preferences.
    2.  **Plan**: Use search tools to find options for flights, hotels, and attractions that fit the user's needs.
    3.  **Propose Itinerary**: Present a plan to the user with costs.
    4.  **Confirm**: EXTREMELY IMPORTANT: You MUST ask for explicit permission from the user before booking anything.
        - Do NOT call `book_flight`, `book_hotel`, or `book_attraction` without a clear "yes" or "go ahead" from the user for that specific item.
        - If the user says "book it all", verify the details one last time.
    5.  **Book**: Once confirmed, use the booking tools to finalize the reservations.

    Be polite, professional, and thorough.
    """

    # Initialize tools
    tools = [
        search_flights,
        book_flight,
        search_hotels,
        book_hotel,
        search_attractions,
        book_attraction,
    ]

    # Create the agent
    agent = LlmAgent(
        model=model,
        name="TravelAgent",
        description="A travel planner asking for confirmation before booking.",
        instruction=instructions,
        tools=tools
    )

    return agent

if __name__ == "__main__":
    # verification
    print("Travel Agent configured successfully.")
