#!/usr/bin/env python3
"""
Simple chat interface with the health agent
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file")
    exit(1)

# Configure Gemini
genai.configure(api_key=api_key)

def chat():
    """Simple chat with health agent"""
    
    # Import prompts
    from src.prompts.dr_berg_style import (
        DR_BERG_BASE_STYLE,
        INTAKE_AGENT_INSTRUCTION
    )
    
    # Create model with Dr. Berg style
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        system_instruction=DR_BERG_BASE_STYLE + "\n\n" + INTAKE_AGENT_INSTRUCTION
    )
    
    # Start chat
    chat = model.start_chat(history=[])
    
    print("\n" + "=" * 80)
    print("🏥 DOROST - Your Personal Health Guide")
    print("=" * 80)
    print("\nHey, I'm Dorost. I'm here to help you understand your health symptoms.")
    print("Ask me anything about your health concerns!")
    print("\nType 'quit' or 'exit' to end the conversation.\n")
    print("=" * 80)
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Take care! Remember to consult with healthcare professionals.")
            break
        
        try:
            # Get AI response
            response = chat.send_message(user_input)
            print(f"\n🤖 Dorost:\n{response.text}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Try asking in a different way.")

if __name__ == "__main__":
    chat()
