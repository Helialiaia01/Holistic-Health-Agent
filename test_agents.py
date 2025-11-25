#!/usr/bin/env python3
"""
Simple test script for Holistic Health Agent
Run this to test individual agents or the full system
"""

import os
import sys

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Environment Check")
    print("=" * 60)
    
    # Check for .env file
    env_exists = os.path.exists('.env')
    print(f"{'✅' if env_exists else '❌'} .env file: {env_exists}")
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    has_key = api_key is not None and api_key != 'your-gemini-api-key'
    print(f"{'✅' if has_key else '❌'} GOOGLE_API_KEY: {'Set' if has_key else 'Not set'}")
    
    # Check dependencies
    try:
        import google.adk
        print("✅ google.adk: Installed")
    except ImportError:
        print("❌ google.adk: Not installed")
        return False
    
    try:
        import google.genai
        print("✅ google.genai: Installed")
    except ImportError:
        print("❌ google.genai: Not installed")
        return False
    
    print()
    
    if not env_exists or not has_key:
        print("⚠️  SETUP REQUIRED:")
        print("1. Copy .env.template to .env")
        print("2. Add your GOOGLE_API_KEY to .env")
        print("3. Get API key from: https://aistudio.google.com/apikey")
        print()
        return False
    
    return True


def test_specialty_router():
    """Test the specialty router agent"""
    print("\n🏥 Testing Specialty Router Agent")
    print("=" * 60)
    
    try:
        from src.agents.specialty_router_agent import recommend_specialist
        
        # Test case 1: Metabolic symptoms
        print("\n📋 Test Case 1: Metabolic Symptoms")
        result = recommend_specialist(
            symptoms="Constant fatigue, sugar cravings, weight gain around waist",
            body_system="Metabolic",
            duration_days=90,
            severity="moderate"
        )
        print(f"✅ Recommended: {result['recommended_specialists'][0]['name']}")
        print(f"   Reasoning: {result['reasoning'][:100]}...")
        
        # Test case 2: Digestive symptoms
        print("\n📋 Test Case 2: Digestive Symptoms")
        result = recommend_specialist(
            symptoms="Bloating, gas, stomach pain after meals",
            body_system="Digestive",
            duration_days=30,
            severity="moderate"
        )
        print(f"✅ Recommended: {result['recommended_specialists'][0]['name']}")
        
        print("\n✅ Specialty Router working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing specialty router: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_base():
    """Test the medical knowledge base"""
    print("\n📚 Testing Medical Knowledge Base")
    print("=" * 60)
    
    try:
        from src.knowledge.medical_knowledge_base import (
            MEDICAL_SPECIALTIES, 
            RED_FLAGS,
            route_to_specialist,
            validate_recommendation_confidence
        )
        
        print(f"✅ Medical specialties loaded: {len(MEDICAL_SPECIALTIES)} specialists")
        print(f"✅ Red flags loaded: {len(RED_FLAGS)} conditions")
        
        # Test routing
        print("\n📋 Test Routing:")
        result = route_to_specialist(
            symptoms=["fatigue", "weight gain", "sugar cravings"],
            body_system="metabolic"
        )
        print(f"✅ Routing result: {result}")
        
        # Test confidence validation
        print("\n📋 Test Confidence Validation:")
        validation = validate_recommendation_confidence(
            agent_confidence=0.75,
            has_red_flags=False,
            symptom_severity="moderate"
        )
        print(f"✅ Confidence validation: {validation['action']}")
        
        print("\n✅ Knowledge base working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing knowledge base: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_context_engineering():
    """Test the context engineering system"""
    print("\n🔧 Testing Context Engineering")
    print("=" * 60)
    
    try:
        from src.knowledge.context_engineering import (
            ContextManager,
            TaskType,
            calculate_agent_confidence
        )
        
        # Test context manager
        print("\n📋 Test Context Manager:")
        cm = ContextManager()
        
        # Add some context
        cm.add_context(TaskType.INTAKE, {"symptom": "fatigue"})
        cm.add_context(TaskType.ANALYSIS, {"pattern": "insulin resistance"})
        
        print(f"✅ Context added successfully")
        print(f"   Active contexts: {len(cm.context_history)}")
        
        # Test confidence calculation
        print("\n📋 Test Confidence Calculation:")
        confidence = calculate_agent_confidence(
            symptom_clarity=0.8,
            pattern_match_strength=0.75,
            red_flag_present=False,
            medical_complexity=0.5
        )
        print(f"✅ Confidence level: {confidence.confidence_level:.2f}")
        print(f"   Should escalate: {confidence.should_escalate}")
        
        print("\n✅ Context engineering working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing context engineering: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_dr_berg_prompts():
    """Test Dr. Berg style prompts"""
    print("\n👨‍⚕️ Testing Dr. Berg Style Prompts")
    print("=" * 60)
    
    try:
        from src.prompts.dr_berg_style import (
            DR_BERG_BASE_STYLE,
            INTAKE_AGENT_INSTRUCTION,
            KNOWLEDGE_AGENT_INSTRUCTION,
            ROOT_CAUSE_AGENT_INSTRUCTION,
            RECOMMENDER_AGENT_INSTRUCTION
        )
        
        print(f"✅ Base style prompt: {len(DR_BERG_BASE_STYLE)} characters")
        print(f"✅ Intake instruction: {len(INTAKE_AGENT_INSTRUCTION)} characters")
        print(f"✅ Knowledge instruction: {len(KNOWLEDGE_AGENT_INSTRUCTION)} characters")
        print(f"✅ Root cause instruction: {len(ROOT_CAUSE_AGENT_INSTRUCTION)} characters")
        print(f"✅ Recommender instruction: {len(RECOMMENDER_AGENT_INSTRUCTION)} characters")
        
        print("\n📋 Sample from Dr. Berg Base Style:")
        print(DR_BERG_BASE_STYLE[:200] + "...")
        
        print("\n✅ Dr. Berg prompts loaded correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing Dr. Berg prompts: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def demo_full_output():
    """Show what the full system would output (without API call)"""
    print("\n🎬 Demo: Expected Full System Output")
    print("=" * 80)
    
    print("""
User Query:
"I'm constantly fatigued, have strong sugar cravings, and don't know 
if I should see an endocrinologist or primary care doctor."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 SPECIALTY ROUTER OUTPUT:

Recommended Medical Specialist: Endocrinologist

Reasoning:
• Fatigue + sugar cravings = classic insulin resistance pattern
• Endocrinologist specializes in metabolic/hormone disorders
• Can order: fasting insulin, HbA1c, thyroid panel, cortisol

Urgency: SOON (1-2 weeks)
Confidence: 0.88

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 KNOWLEDGE AGENT OUTPUT:

Key Pattern: Insulin Resistance

Mechanism (Dr. Berg style):
"When you eat carbs frequently, insulin is constantly elevated. Over time, 
cells become RESISTANT to insulin. Your pancreas makes MORE insulin to 
compensate. High insulin BLOCKS fat burning (you can't access stored energy) 
AND causes sugar cravings (cells are starving despite full energy stores)."

Confidence: 0.78

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 ROOT CAUSE AGENT OUTPUT:

Root Cause Cascade:
  High-carb diet + Frequent eating
    ↓
  Insulin constantly elevated
    ↓
  Cells become insulin resistant
    ↓
  Even MORE insulin produced
    ↓
  Symptoms: Fatigue, cravings, weight gain

Keystone Fix: Intermittent fasting + low-carb (breaks insulin cycle)

Confidence: 0.80

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 RECOMMENDER AGENT OUTPUT (Dr. Berg Precision):

PHASE 1 (Week 1-2): METABOLIC RESET

1. INTERMITTENT FASTING
   Start: 14:10 (14 hours fasting, 10 hour eating window)
   Progress to: 16:8 (skip breakfast, eat 12pm-8pm)
   
   Why: Lowers insulin. Only when insulin is LOW can you burn fat.

2. LOW-CARB NUTRITION
   Target: 50g net carbs per day
   Remove: Cereal, bread, pasta, rice
   Add: Leafy greens (7-10 cups), healthy fats, moderate protein

3. MAGNESIUM SUPPLEMENTATION
   Form: Magnesium Bisglycinate 400mg
   (NOT Oxide - only 4% absorbed)
   Timing: Before bed
   Why: Stress depletes magnesium. Insulin blocks absorption.
   
Expected timeline: 2-3 weeks for energy improvement

Confidence: 0.75 (Strong pattern, safe recommendations)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is the quality level our system produces! 🎯
    """)


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("🧪 HOLISTIC HEALTH AGENT - TEST SUITE")
    print("=" * 80)
    
    # Environment check
    if not check_environment():
        print("\n❌ Environment setup incomplete. Please fix issues above.")
        return False
    
    # Run tests
    results = []
    results.append(("Specialty Router", test_specialty_router()))
    results.append(("Knowledge Base", test_knowledge_base()))
    results.append(("Context Engineering", test_context_engineering()))
    results.append(("Dr. Berg Prompts", test_dr_berg_prompts()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\n💡 Want to see expected output? Run:")
        print("   python test_agents.py --demo")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
    
    return passed == total


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_full_output()
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
