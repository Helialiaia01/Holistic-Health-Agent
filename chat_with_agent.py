from src.orchestrator import HealthAgentOrchestrator

def generate_followup_response(user_input, initial_result, history):
    """Generate contextual follow-up responses based on the initial consultation."""
    user_lower = user_input.lower()
    
    # Response categories
    if any(word in user_lower for word in ['what', 'why', 'how']):
        # Explain the findings
        if 'knowledge' in initial_result['stages']:
            mechanisms = initial_result['stages']['knowledge'].get('mechanisms', '')
            if mechanisms:
                return f"Based on your symptoms, here's what's happening in your body: {mechanisms}\n\nThis pattern suggests metabolic stress affecting multiple systems. Would you like specific recommendations?"
        return "Your symptoms suggest a interconnected health pattern. The initial consultation identified several contributing factors. What aspect would you like me to explain further?"
    
    elif any(word in user_lower for word in ['recommend', 'what should', 'treatment', 'help', 'fix']):
        # Provide recommendations
        if 'recommender' in initial_result['stages']:
            recommendations = initial_result['stages']['recommender'].get('recommendations', [])
            if recommendations:
                rec_text = "\n".join([f"• {rec}" for rec in recommendations[:3]])
                return f"Based on your root causes, here are key recommendations:\n{rec_text}\n\nThese should be implemented over 8-12 weeks. Start with the first one for best results."
        return "The key is addressing your root causes systematically. From the analysis, focus on sleep optimization first, then dietary changes. Would you like specific details on any of these?"
    
    elif any(word in user_lower for word in ['specialist', 'doctor', 'urgent', 'emergency']):
        # Address medical questions
        specialist = initial_result['stages']['specialty_router'].get('recommendation', 'Primary Care')
        return f"You should see a {specialist}. They can run bloodwork to confirm the patterns we've identified. If you experience severe symptoms (worst headache of life, chest pain, can't breathe), seek emergency care immediately."
    
    elif any(word in user_lower for word in ['timeline', 'when', 'how long', 'improve']):
        # Timeline questions
        if 'recommender' in initial_result['stages']:
            timeline = initial_result['stages']['recommender'].get('timeline', '')
            if timeline:
                return f"Improvement timeline: {timeline}\n\nYou should notice initial changes within 1-2 weeks, significant improvement by week 4-8. Be consistent with the recommendations."
        return "Most people see initial changes within 1-2 weeks, with significant improvements by 8-12 weeks. Consistency is key - these are lifestyle changes, not quick fixes."
    
    elif any(word in user_lower for word in ['diet', 'food', 'eat', 'nutrition']):
        return "Nutrition is foundational. Based on your patterns, focus on:\n• Whole foods (eliminate processed foods)\n• Consistent meal timing\n• Adequate protein and healthy fats\n• Reduce high-carb snacking\n\nWould you like specific food recommendations?"
    
    elif any(word in user_lower for word in ['sleep', 'rest', 'tired']):
        return "Sleep is your foundation for healing. Prioritize:\n• 7-9 hours consistently\n• Same bedtime/wake time daily\n• Dark, cool bedroom\n• No screens 1 hour before bed\n\nMagnesium supplementation often helps. See your results for specific recommendations."
    
    elif any(word in user_lower for word in ['supplement', 'vitamin', 'mineral']):
        return "Supplements address specific deficiencies identified in your analysis. The key is:\n• Right form (not all supplements are created equal)\n• Proper dosage\n• Correct timing\n• Quality source\n\nFollow the specific recommendations from your results. Start with one supplement at a time to assess tolerance."
    
    elif any(word in user_lower for word in ['stress', 'anxiety', 'mental']):
        return "Mental and physical health are deeply interconnected. Your stress is likely amplifying your physical symptoms. Recommendations:\n• Daily meditation (10-20 mins)\n• Regular exercise\n• Connection with others\n• Stress management practices\n\nThis is as important as the dietary changes."
    
    # Default response
    elif user_input.strip() in ['so?', 'ok', 'and?', 'what now?']:
        return "The initial consultation identified your main issues and root causes. You can now:\n1. Ask questions about specific aspects (sleep, diet, supplements, etc.)\n2. Ask when you'll see improvements\n3. Ask for clarification on specialist recommendations\n\nWhat would you like to know more about?"
    
    else:
        # Generic contextual response
        return f"Based on your question about '{user_input}': Your symptoms suggest you need a comprehensive approach addressing sleep, stress, nutrition, and targeted supplementation. Each of these is explained in your results. Which area interests you most?"

orchestrator = HealthAgentOrchestrator()
consultation_history = []
initial_result = None

print("=" * 70)
print("CHAT WITH DOROST - Health Agent")
print("=" * 70)
print("\nTell me your health concerns (or type 'quit' to exit)\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nGoodbye! Remember to consult a doctor for professional advice.\n")
        break
    
    if not user_input:
        continue
    
    # First message: run full consultation
    if not consultation_history:
        print("\nDorost is analyzing...\n")
        initial_result = orchestrator.run_consultation(user_input)
        consultation_history.append({"user": user_input, "type": "initial"})
        
        print("=" * 70)
        print(f"Status: {initial_result['status']}")
        print(f"Overall Confidence: {initial_result['overall_confidence']:.0%}")
        print("=" * 70)
        
        # Show the recommendation
        if 'specialty_router' in initial_result['stages']:
            print(f"\n🏥 SPECIALIST RECOMMENDATION:")
            print(f"   {initial_result['stages']['specialty_router'].get('recommendation', 'N/A')}")
        
        # Show red flags if detected
        if initial_result.get('red_flags'):
            print(f"\n⚠️  RED FLAGS DETECTED: {len(initial_result['red_flags'])}")
            for flag in initial_result['red_flags']:
                print(f"   - {flag}")
        
        # Show all 6 stages
        print(f"\n📊 ALL STAGES COMPLETED:")
        for stage_name, stage_data in initial_result['stages'].items():
            confidence = stage_data.get('confidence', 0)
            print(f"   ✓ {stage_name.replace('_', ' ').title()}: {confidence:.0%} confidence")
        
        print("\n" + "-" * 70)
        print("\n💬 You can now ask follow-up questions about your results:\n")
    
    # Follow-up messages: provide contextual responses based on initial consultation
    else:
        consultation_history.append({"user": user_input, "type": "followup"})
        
        # Generate contextual responses based on the initial consultation
        response = generate_followup_response(user_input, initial_result, consultation_history)
        
        print(f"\nDorost: {response}\n")
        print("-" * 70 + "\n")


