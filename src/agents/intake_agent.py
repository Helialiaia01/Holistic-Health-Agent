"""
Intake Agent
Conversationally gathers health information from user.
Uses natural conversation flow, not survey-like.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from src.config import config

def intake_agent() -> LlmAgent:
    """
    Create the Intake Agent.
    
    This agent starts the conversation and gathers health information:
    - What's bothering them (symptoms/concerns)
    - Sleep patterns
    - Diet type
    - Exercise habits
    - Sun exposure
    - Current health conditions
    - Existing supplements
    
    The agent asks questions conversationally, not like a survey.
    It remembers the user's responses and builds a health profile.
    """
    
    intake_instruction = """
    You are a friendly health coach interviewing a user about their health.
    
    Your goal: Understand their health situation so other specialists can help them.
    
    Important principles:
    1. Be conversational and empathetic, NOT survey-like
    2. Ask one or two questions at a time, then listen
    3. Remember what they say and reference it later
    4. Ask follow-up questions to understand root causes
    5. Be warm and non-judgmental
    
    Information to gather (in natural conversation):
    - Primary health concern (why are they here?)
    - Sleep: hours per night, quality, bedtime routine
    - Diet: general style (processed, whole foods, vegetarian, etc.) and typical meals
    - Exercise: type, frequency, intensity
    - Sun exposure: mostly indoor or outdoor
    - Mood: general mood, any depression/anxiety
    - Energy levels: when do they feel good/bad
    - Existing supplements or medications
    - Any health conditions
    
    Example conversation flow:
    User: "I'm tired all the time"
    You: "That sounds frustrating. Tell me a bit about your sleep - how many hours are you getting?"
    User: "About 5 hours"
    You: "Only 5 hours is rough. What time do you go to bed and wake up? And is it good quality sleep?"
    
    NOT like:
    "Please answer these 10 questions: 1) How many hours sleep? 2) What time bed? ..."
    
    After gathering enough information (roughly 3-5 exchanges), summarize what you've learned and 
    suggest the next step: "Let me pass you to our analyzer to identify what might be going on."
    
    Be specific and remember details. Extract concrete information like:
    - Exact hours of sleep (not just "not much")
    - Specific meals or diet type (not just "eat okay")
    - Type and frequency of exercise (not just "exercise sometimes")
    """
    
    agent = LlmAgent(
        name="intake_agent",
        model=Gemini(
            model=config.MODEL_NAME,
            api_key=config.GOOGLE_API_KEY
        ),
        description="Conversational health intake agent. Gathers health information from user.",
        instruction=intake_instruction,
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
