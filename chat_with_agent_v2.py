"""
Intelligent Conversational Health Agent - Hybrid Approach
Combines contextual understanding with orchestrator intelligence
"""

from src.orchestrator import HealthAgentOrchestrator
from src.knowledge.medical_knowledge_base import RED_FLAGS

class SmartHealthConversation:
    """Natural conversation with intelligent context understanding."""
    
    def __init__(self):
        self.orchestrator = HealthAgentOrchestrator()
        self.conversation_history = []
        self.initial_analysis = None
        self.turn_count = 0
        self.user_info = {}
    
    def add_message(self, speaker, message):
        """Track conversation."""
        self.conversation_history.append({
            'speaker': speaker,
            'message': message,
            'turn': self.turn_count
        })
    
    def _check_emergency(self, user_input):
        """Check for emergency symptoms - be specific, not trigger on just any word."""
        user_lower = user_input.lower()
        
        # Critical emergency patterns (not just any headache!)
        emergency_keywords = {
            'chest pain': ['chest', 'pain'],  # Must have BOTH
            'severe shortness of breath': ['difficulty breath', 'shortness of breath', 'cant breath'],
            'loss of consciousness': ['unconscious', 'passed out', 'fainted'],
            'severe bleeding': ['bleeding severely', 'gushing blood', 'cant stop bleeding'],
            'sudden severe headache': ['worst headache', 'sudden severe head'],  # Not just any headache!
            'sudden weakness': ['sudden', 'weakness', 'paralysis'],
            'confusion': ['confused', 'disoriented', 'cant think'],
        }
        
        for condition, patterns in emergency_keywords.items():
            if all(pattern in user_lower for pattern in patterns):
                return True
        
        return False
    
    def _extract_health_facts(self, user_input):
        """Extract health information from natural language."""
        lower = user_input.lower()
        facts = {
            'mentioned_symptoms': [],
            'timing': None,
            'severity': None,
            'related_factors': [],
            'lifestyle_notes': []
        }
        
        # Detect symptoms
        symptom_keywords = {
            'pain': ['pain', 'ache', 'throb', 'hurt', 'tender'],
            'fatigue': ['tired', 'fatigue', 'exhausted', 'drained', 'weak'],
            'digestion': ['bloat', 'gas', 'digest', 'bowel', 'stomach'],
            'mood': ['mood', 'anxious', 'depressed', 'irritable', 'emotional'],
            'hormonal': ['period', 'cycle', 'hormone', 'menstrual', 'pms'],
        }
        
        for category, keywords in symptom_keywords.items():
            if any(kw in lower for kw in keywords):
                facts['mentioned_symptoms'].append(category)
        
        # Detect timing/patterns
        if any(word in lower for word in ['always', 'every', 'regularly', 'monthly', 'daily']):
            facts['timing'] = 'recurring'
        if any(word in lower for word in ['sometimes', 'occasional', 'intermittent']):
            facts['timing'] = 'intermittent'
        
        # Detect severity
        if any(word in lower for word in ['terrible', 'severe', 'unbearable', 'extreme', 'worst']):
            facts['severity'] = 'high'
        elif any(word in lower for word in ['mild', 'slight', 'minor']):
            facts['severity'] = 'mild'
        
        # Lifestyle factors
        if any(word in lower for word in ['sleep', 'sleepless', 'insomnia', 'awake', 'hours']):
            facts['lifestyle_notes'].append('sleep disruption')
        if any(word in lower for word in ['stress', 'anxious', 'worried', 'overwhelmed']):
            facts['lifestyle_notes'].append('stress')
        if any(word in lower for word in ['exercise', 'workout', 'sedentary', 'active']):
            facts['lifestyle_notes'].append('exercise level')
        if any(word in lower for word in ['sugar', 'caffeine', 'chocolate', 'crave', 'carb']):
            facts['lifestyle_notes'].append('dietary patterns')
        
        return facts
    
    def _generate_smart_followup(self, user_input, initial_analysis):
        """Generate contextual follow-up questions."""
        facts = self._extract_health_facts(user_input)
        symptoms = facts['mentioned_symptoms']
        lifestyle = facts['lifestyle_notes']
        
        followups = []
        
        # Ask about root causes based on detected symptoms
        if 'pain' in symptoms and 'hormonal' in symptoms:
            if 'sleep disruption' not in lifestyle:
                followups.append("How's your sleep? Hormonal headaches often worsen with poor sleep quality.")
            if 'stress' not in lifestyle:
                followups.append("How are you managing stress? Cortisol directly impacts hormonal balance.")
        
        if 'fatigue' in symptoms:
            if 'sleep disruption' not in lifestyle:
                followups.append("First, let's understand your sleep - how many hours are you actually getting, and is it quality sleep?")
            if 'dietary patterns' not in lifestyle:
                followups.append("Do you notice your energy crashes at specific times? That often points to blood sugar issues.")
        
        if 'digestion' in symptoms:
            if 'dietary patterns' not in lifestyle:
                followups.append("What does a typical day of eating look like for you?")
            followups.append("Do these digestive issues correlate with specific foods or times of day?")
        
        if 'mood' in symptoms:
            if 'sleep disruption' not in lifestyle:
                followups.append("Sleep quality heavily influences mood regulation. How's your sleep been?")
            if 'stress' not in lifestyle:
                followups.append("Let's talk about your stress levels and what's driving them.")
        
        # Ask about patterns they haven't mentioned
        if len(lifestyle) < 3:  # They haven't mentioned many lifestyle factors
            if 'stress' not in lifestyle:
                followups.append("What's your stress level like recently? I'm asking because stress is often a root cause.")
            if 'sleep disruption' not in lifestyle:
                followups.append("How would you describe your sleep and recovery?")
            if 'exercise level' not in lifestyle:
                followups.append("What's your movement/exercise like?")
        
        return followups[:2] if followups else ["Tell me more about what you're experiencing."]
    
    def generate_response(self, user_input):
        """Generate contextual, intelligent response."""
        
        # Check emergency
        if self._check_emergency(user_input):
            self.add_message('user', user_input)
            response = (
                f"🚨 I need to pause here - I'm seeing symptoms that require immediate medical attention.\n\n"
                f"Please call 911 or go to the nearest emergency room right away.\n\n"
                f"This is not something to manage at home."
            )
            self.add_message('assistant', response)
            return response
        
        # Turn 1: Initial analysis
        if self.turn_count == 0:
            print("\nAnalyzing your health profile...\n")
            self.initial_analysis = self.orchestrator.run_consultation(user_input)
            self.add_message('user', user_input)
            
            # Extract facts
            facts = self._extract_health_facts(user_input)
            self.user_info['initial_concern'] = user_input
            self.user_info['symptoms'] = facts['mentioned_symptoms']
            
            # Build intelligent response
            patterns = self.initial_analysis['stages'].get('knowledge', {}).get('patterns_identified', [])
            specialist_rec = self.initial_analysis['stages'].get('specialty_router', {}).get('recommendation', '')
            
            response = f"""I understand - {user_input.lower()}

This presentation suggests {', '.join(patterns[:2]) if patterns else 'interconnected factors'}. Here's what I'm thinking:

These symptoms often point to {patterns[0] if patterns else 'systemic imbalances'} that need deeper investigation. 

To give you the most actionable guidance, I need to understand the full picture. Tell me:
• When did this pattern start?
• What makes it better or worse?
• How much is it impacting your daily life?

And I'm particularly interested in your {facts['lifestyle_notes'][0] if facts['lifestyle_notes'] else 'overall lifestyle factors'} - that usually holds key answers."""
            
            self.add_message('assistant', response)
            self.turn_count += 1
            return response
        
        # Turns 2+: Contextual dialogue
        else:
            self.add_message('user', user_input)
            
            # Extract new information
            facts = self._extract_health_facts(user_input)
            
            # Generate smart follow-ups
            followups = self._generate_smart_followup(user_input, self.initial_analysis)
            
            # Build response that references previous context
            recent_concern = self.user_info.get('initial_concern', '')
            recent_symptoms = self.user_info.get('symptoms', [])
            
            reference = ""
            if recent_symptoms:
                ref_symptom = recent_symptoms[0]
                reference = f"So given your {ref_symptom} that you mentioned initially, "
            
            # Connect the dots
            connection = ""
            if 'sleep disruption' in facts['lifestyle_notes'] and 'hormonal' in recent_symptoms:
                connection = "This sleep pattern is actually significant - poor sleep directly disrupts hormonal balance, which amplifies what you're experiencing. "
            elif 'stress' in facts['lifestyle_notes'] and 'fatigue' in recent_symptoms:
                connection = "Your stress level is likely the missing link here - chronic stress elevates cortisol, which drives fatigue and disrupts recovery. "
            elif 'dietary patterns' in facts['lifestyle_notes']:
                connection = "Your diet choices are telling - this suggests potential nutrient deficiencies or blood sugar dysregulation. "
            
            response = f"""{reference}here's what you're describing: {user_input.lower()}

{connection}This makes sense because {facts['mentioned_symptoms'][0] if facts['mentioned_symptoms'] else 'these symptoms'} and {facts['lifestyle_notes'][0] if facts['lifestyle_notes'] else 'lifestyle factors'} are directly connected.

{followups[0]}

{followups[1] if len(followups) > 1 else ''}"""
            
            self.add_message('assistant', response)
            self.turn_count += 1
            return response
    
    def get_consultation_summary(self):
        """Get summary of consultation."""
        summary = f"""
═══════════════════════════════════════════════════════════
CONSULTATION SUMMARY
═══════════════════════════════════════════════════════════

Initial Concern: {self.user_info.get('initial_concern', 'N/A')}
Symptoms Identified: {', '.join(self.user_info.get('symptoms', ['None']))}
Total Exchanges: {self.turn_count}

Recommendations to Explore:
{chr(10).join('• ' + rec for rec in self.initial_analysis.get('stages', {}).get('recommender', {}).get('recommendations', [])[:5]) if self.initial_analysis else 'Continue consultation for recommendations'}

═══════════════════════════════════════════════════════════
"""
        return summary


# Main execution
if __name__ == "__main__":
    conversation = SmartHealthConversation()

    print("\n" + "=" * 80)
    print("                  DOROST - Holistic Health Consultation")
    print("=" * 80)
    print("\nWelcome. I'm here to help you understand your health concerns and develop")
    print("a personalized, evidence-based approach.\n")
    print("Describe what's been going on, and I'll ask intelligent follow-up questions")
    print("tailored to what you tell me.\n")
    print("(Type 'quit' to end, 'summary' for consultation overview)\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q', 'done']:
            print(conversation.get_consultation_summary())
            print("Thank you for consulting with me. Take care!\n")
            break
        
        if user_input.lower() == 'summary':
            print(conversation.get_consultation_summary())
            continue
        
        if not user_input:
            continue
        
        response = conversation.generate_response(user_input)
        print(f"\nDorost: {response}\n")
