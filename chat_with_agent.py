from src.orchestrator import HealthAgentOrchestrator

orchestrator = HealthAgentOrchestrator()

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
    
    print("\nDorost is analyzing...\n")
    result = orchestrator.run_consultation(user_input)
    
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"Overall Confidence: {result['overall_confidence']:.0%}")
    print("=" * 70)
    
    # Show the recommendation
    if 'specialty_router' in result['stages']:
        print(f"\n🏥 SPECIALIST RECOMMENDATION:")
        print(f"   {result['stages']['specialty_router'].get('recommendation', 'N/A')}")
    
    # Show red flags if detected
    if result.get('red_flags'):
        print(f"\n⚠️  RED FLAGS DETECTED: {len(result['red_flags'])}")
        for flag in result['red_flags']:
            print(f"   - {flag.symptom} (Urgency: {flag.urgency.value})")
    
    # Show all 6 stages
    print(f"\n📊 ALL STAGES COMPLETED:")
    for stage_name, stage_data in result['stages'].items():
        confidence = stage_data.get('confidence', 0)
        print(f"   ✓ {stage_name.replace('_', ' ').title()}: {confidence:.0%} confidence")
    
    print("\n" + "-" * 70 + "\n")
