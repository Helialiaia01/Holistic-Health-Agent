"""
Intake agent - does the initial health interview.
Asks about symptoms, diet, sleep, stress - tries to find root causes like Dr. Berg does.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from src.config import config
from src.prompts.dr_berg_style import INTAKE_AGENT_INSTRUCTION

def intake_agent() -> LlmAgent:
    """
    Sets up the intake agent with Dr. Berg's style.
    It asks follow-up questions to dig into root causes, not just list symptoms.
    """
    
    agent = LlmAgent(
        name="intake_agent",
        model=Gemini(
            model=config.MODEL_NAME,
            api_key=config.GOOGLE_API_KEY
        ),
        description="Dr. Berg-style health intake agent. Gathers metabolic health information with educational approach.",
        instruction=INTAKE_AGENT_INSTRUCTION,
        output_key="health_profile",  # Store for next agent
    )
    
    return agent


# Just for testing - runs a sample conversation
async def run_intake_example():
    """Quick test to see if the agent responds properly"""
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    
    # Create agent
    agent = intake_agent()
    
    # Just setting up a test session
    session_service = InMemorySessionService()
    app_name = "health_agent"
    user_id = "demo_user"
    session_id = "demo_session_1"
    
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    runner = InMemoryRunner(agent=agent)
    
    # Try a test message
    user_message = "I'm exhausted all the time. I don't know what's wrong with me."
    user_content = types.Content(parts=[types.Part(text=user_message)])
    
    print(f"User: {user_message}\n")
    
    # See what the agent says back
    async for event in runner.run_async(new_message=user_content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(f"Intake Agent: {part.text}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_intake_example())
