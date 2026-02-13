import asyncio
import os
import uuid

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agent import create_travel_agent

async def main():
    print("Initializing Travel Agent...")
    agent = create_travel_agent()
    
    # Initialize runner and session
    session_service = InMemorySessionService()
    app_name = "travel_app"
    user_id = "family"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    print("\n✈️  Travel Agent is ready! (Type 'quit' to exit)")
    print("--------------------------------------------------")
    
    # Simple interactive loop
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print("Agent is thinking...", end="\r")
        
        user_content = types.Content(role="user", parts=[types.Part(text=user_input)])
        final_text = None
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=user_content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_text = event.content.parts[0].text
        if final_text:
            print(f"Agent: {final_text}")
        else:
            print("Agent: I couldn't generate a response. Please try again.")

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  WARNING: GOOGLE_API_KEY is not set in environment.")
        print("Please create a .env file or set it in your environment.")
    
    asyncio.run(main())
