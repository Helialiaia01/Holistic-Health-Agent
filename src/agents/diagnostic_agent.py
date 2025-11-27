"""
Diagnostic agent - guides through physical self-checks (tongue, nails, skin).
Like Dr. Berg does - look for visible signs of deficiencies.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from src.config import config
from src.prompts.dr_berg_style import DIAGNOSTIC_AGENT_INSTRUCTION

def diagnostic_agent() -> LlmAgent:
    """
    Create the Interactive Diagnostic Agent.
    
    This agent guides patients through physical self-examinations that
    Dr. Berg would perform in his office:
    - Tongue examination (color, coating, texture, shape)
    - Nail examination (shape, color, texture)
    - Skin examination (dryness, bruising, healing)
    - Eyelid check (anemia test)
    - Capillary refill test (circulation)
    - Orthostatic hypotension test (adrenal function)
    - Additional visible signs (dark circles, light sensitivity, etc.)
    
    The agent educates while examining, explaining what each sign indicates
    and why it matters for understanding root causes.
    
    Can optionally process photos for visual analysis (multimodal).
    """
    
    agent = LlmAgent(
        name="diagnostic_agent",
        model=Gemini(
            model=config.MODEL_NAME,
            api_key=config.GOOGLE_API_KEY
        ),
        description="Interactive diagnostic agent. Guides physical self-examination using Dr. Berg's methods.",
        instruction=DIAGNOSTIC_AGENT_INSTRUCTION,
        output_key="diagnostic_findings",  # Store examination results
    )
    
    return agent


async def analyze_physical_photo(image_path: str, examination_type: str) -> dict:
    """
    Analyze a physical examination photo using Gemini Vision.
    
    Args:
        image_path: Path to the examination photo
        examination_type: Type of exam ("tongue", "nails", "skin", etc.)
    
    Returns:
        Analysis results with findings and interpretation
    """
    
    from google.genai import Client
    
    examination_prompts = {
        "tongue": """
        Analyze this tongue photo using medical diagnostic criteria:
        
        COLOR ASSESSMENT:
        - Pink → Normal, healthy
        - Pale/White → Anemia (iron, B12, or folate deficiency)
        - Red/Bright Red → B vitamin deficiency, inflammation
        - Purple/Blue → Poor circulation, blood stagnation
        - Yellow tint → Liver/gallbladder issues
        
        COATING ASSESSMENT:
        - Thin white → Normal
        - Thick white → Candida overgrowth, gut dysbiosis
        - Yellow coating → Heat, inflammation, infection
        - Brown/Black → Serious condition, requires medical attention
        - No coating (geographic tongue) → Nutrient deficiencies
        
        TEXTURE ASSESSMENT:
        - Smooth, shiny → B vitamin deficiency (especially B12, folate, niacin)
        - Deep cracks → Chronic dehydration, nutrient deficiencies
        - Shallow cracks → Normal with age, or temporary dehydration
        - Swollen → Fluid retention, thyroid issues, inflammation
        
        SHAPE ASSESSMENT:
        - Scalloped edges (teeth marks) → Fluid retention, qi deficiency, low thyroid
        - Thin → Dehydration, nutrient depletion
        - Normal width → Healthy
        
        Provide detailed analysis with confidence levels for each finding.
        List most likely nutritional implications.
        """,
        
        "nails": """
        Analyze these fingernails using medical diagnostic criteria:
        
        SHAPE ASSESSMENT:
        - Spoon-shaped (koilonychia) → Iron deficiency anemia
        - Clubbed → Oxygen issues, lung/heart disease (medical referral needed)
        - Normal convex → Healthy
        
        COLOR ASSESSMENT:
        - Pink nail beds → Normal circulation
        - Pale/White → Anemia (iron deficiency)
        - Blue/Purple → Poor oxygenation, circulation issues
        - Yellow → Fungal infection, liver issues
        - White spots (leukonychia) → Zinc deficiency, trauma
        
        TEXTURE ASSESSMENT:
        - Vertical ridges → Normal aging, dehydration
        - Horizontal ridges (Beau's lines) → Severe illness, nutritional stress
        - Brittle, breaking easily → Biotin deficiency, protein deficiency
        - Soft, peel easily → Iron, calcium, or protein deficiency
        
        SURFACE ASSESSMENT:
        - Smooth → Healthy
        - Pitted → Psoriasis, zinc deficiency
        - Thick → Fungal infection
        
        Provide detailed analysis with nutritional implications.
        """,
        
        "skin": """
        Analyze this skin photo for nutritional deficiency signs:
        
        TEXTURE ASSESSMENT:
        - Dry, rough patches → Essential fatty acid deficiency, vitamin A deficiency
        - Keratosis pilaris (bumps on arms) → Vitamin A deficiency
        - Very smooth → May indicate adequate nutrition or young age
        
        COLOR ASSESSMENT:
        - Normal tone → Adequate circulation
        - Pale → Anemia (iron, B12, folate)
        - Yellow tint (not jaundice) → High carotene intake (carrots)
        - Grayish → Severe anemia, circulation issues
        
        HEALING & MARKS:
        - Easy bruising visible → Vitamin C or K deficiency, platelet issues
        - Slow healing wounds → Zinc, vitamin C, or protein deficiency
        - Petechiae (tiny red dots) → Vitamin C deficiency (scurvy)
        
        OTHER SIGNS:
        - Dark circles under eyes → Allergies, adrenal stress, poor sleep
        - Puffy/swollen → Fluid retention, kidney issues, allergies
        
        Provide detailed analysis with nutritional implications.
        """,
        
        "eyes": """
        Analyze the eye area for health indicators:
        
        EYELID INTERIOR (when pulled down):
        - Bright red/pink → Normal, healthy blood
        - Pale/whitish → Anemia (iron, B12, or folate deficiency)
        - Very red (not pink) → Inflammation, allergy
        
        WHITES OF EYES (sclera):
        - Clear white → Normal
        - Yellow → Jaundice, liver/gallbladder issues (medical attention!)
        - Red bloodshot → Vitamin B2 deficiency, allergies, irritation
        - Red veins → Vitamin B2, essential fatty acids
        
        UNDER EYES:
        - Dark circles → Adrenal stress, allergies, poor sleep, iron deficiency
        - Puffy bags → Fluid retention, kidney issues, allergies, poor lymph drainage
        - Normal → Adequate rest and nutrition
        
        Provide detailed analysis with likely causes.
        """
    }
    
    prompt = examination_prompts.get(examination_type, examination_prompts["tongue"])
    
    # Initialize Gemini client
    client = Client(api_key=config.GOOGLE_API_KEY)
    
    # Load image
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Create multimodal request
    response = await client.models.generate_content(
        model=config.MODEL_NAME,
        contents=[
            types.Content(
                parts=[
                    types.Part(text=prompt),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type="image/jpeg",
                            data=image_data
                        )
                    )
                ]
            )
        ]
    )
    
    return {
        "examination_type": examination_type,
        "analysis": response.text,
        "image_analyzed": True
    }


# Example usage function for testing
async def run_diagnostic_example():
    """Test the diagnostic agent with a sample interaction"""
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    
    # Create agent
    agent = diagnostic_agent()
    
    # Setup session
    session_service = InMemorySessionService()
    app_name = "health_agent_demo"
    user_id = "demo_user"
    session_id = "demo_diagnostic"
    
    # Create session with health profile from intake
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Simulate health profile from intake agent
    session.state["health_profile"] = {
        "symptoms": "chronic fatigue, brain fog",
        "sleep": "5 hours per night, poor quality",
        "diet": "mostly processed foods, fast food, high carb",
        "exercise": "none, sedentary desk job",
        "sun_exposure": "indoor all day",
        "mood": "low, 3/10",
        "energy": "crashes in afternoon"
    }
    
    # Create runner
    runner = InMemoryRunner(agent=agent)
    
    # Sample user message
    user_message = "Okay, I'm ready to do the physical examinations you mentioned."
    user_content = types.Content(parts=[types.Part(text=user_message)])
    
    print("=" * 60)
    print("🩺 INTERACTIVE DIAGNOSTIC AGENT - DEMO")
    print("=" * 60)
    print(f"\nUser: {user_message}\n")
    
    # Run the agent
    async for event in runner.run_async(new_message=user_content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(f"Diagnostic Agent:\n{part.text}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_diagnostic_example())
