"""
Demo script to test the Holistic Health Agent
Run this to see your agents in action!
"""

import asyncio
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.agents.intake_agent import intake_agent

async def demo_conversation():
    """
    Demo conversation showing the Intake Agent in action.
    This shows you exactly what the user will experience.
    """
    
    print("=" * 60)
    print("🏥 HOLISTIC HEALTH AGENT - DEMO")
    print("=" * 60)
    print()
    
    # Create the intake agent
    agent = intake_agent()
    
    # Setup session
    session_service = InMemorySessionService()
    app_name = "health_agent_demo"
    user_id = "demo_user"
    session_id = "demo_session_1"
    
    # Create session
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create runner
    runner = InMemoryRunner(agent=agent)
    
    # Simulate a real user conversation
    user_messages = [
        "I'm exhausted all the time and I don't know what's wrong with me.",
        "I sleep about 5 hours a night. Go to bed around 2am, wake up at 7am for work.",
        "My diet is pretty bad - cereal for breakfast, fast food for lunch, pasta or pizza for dinner. I work at a desk all day, no exercise really.",
        "I'm mostly indoors. My job is remote so I'm at my computer all day. I'd say my mood is like a 3 out of 10. Pretty low energy and motivation."
    ]
    
    print("🎬 Starting conversation...\n")
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'─' * 60}")
        print(f"👤 User (Message {i}): {user_message}")
        print(f"{'─' * 60}\n")
        
        # Create user content
        user_content = types.Content(parts=[types.Part(text=user_message)])
        
        # Run the agent
        print("🤖 Intake Agent:")
        async for event in runner.run_async(new_message=user_content):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text"):
                        print(part.text)
        
        print()
        
        # Small pause between messages for readability
        await asyncio.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ Demo conversation complete!")
    print("=" * 60)
    print()
    print("📊 What you just saw:")
    print("  ✓ Intake Agent asking natural follow-up questions")
    print("  ✓ Agent remembering previous responses")
    print("  ✓ Conversational tone (not survey-like)")
    print("  ✓ Gemini powering the intelligence")
    print()
    print("🔜 Next steps:")
    print("  • Analyzer Agent will identify health patterns")
    print("  • Reasoning Agent will explain root causes")
    print("  • Recommender Agent will give personalized advice")
    print()

if __name__ == "__main__":
    print()
    print("🚀 Make sure you have:")
    print("  1. Installed: pip install -r requirements.txt")
    print("  2. Created .env file (copy from .env.template)")
    print("  3. Added your GOOGLE_API_KEY to .env")
    print()
    input("Press ENTER when ready to start demo...")
    print()
    
    asyncio.run(demo_conversation())
