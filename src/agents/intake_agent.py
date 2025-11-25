"""
Intake Agent - Dr. Berg Style
Gathers metabolic health information using Dr. Berg's educational approach.
Focuses on root causes, not just symptoms.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from src.config import config
from src.prompts.dr_berg_style import INTAKE_AGENT_INSTRUCTION

def intake_agent() -> LlmAgent:
    """
    Create the Intake Agent with Dr. Berg's teaching style.
    
    This agent:
    - Gathers comprehensive metabolic health information
    - Uses Dr. Berg's framework (insulin resistance, deficiencies, gut health)
    - Asks questions that reveal root causes
    - Educates while gathering information
    - Builds a complete health profile for analysis
    
    The agent is conversational but thorough, helping patients understand
    what information matters and why.
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


# Example usage function for testing
async def run_intake_example():
    """Test the intake agent with a sample conversation"""
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    
    # Create agent
    agent = intake_agent()
    
    # Setup session
    session_service = InMemorySessionService()
    app_name = "health_agent"
    user_id = "demo_user"
    session_id = "demo_session_1"
    
    # Create session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create runner
    runner = InMemoryRunner(agent=agent)
    
    # Sample user message
    user_message = "I'm exhausted all the time. I don't know what's wrong with me."
    user_content = types.Content(parts=[types.Part(text=user_message)])
    
    print(f"User: {user_message}\n")
    
    # Run the agent
    async for event in runner.run_async(new_message=user_content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(f"Intake Agent: {part.text}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_intake_example())
