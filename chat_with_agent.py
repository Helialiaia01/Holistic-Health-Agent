"""
Dorost - Real Health Consultation Conversation
Warm, empathetic, and genuinely helpful
"""

from src.orchestrator import HealthAgentOrchestrator, ConsultationValidator

class DorostHealthCoach:
    """A genuinely caring health conversation partner."""
    
    def __init__(self):
        self.orchestrator = HealthAgentOrchestrator()
        self.validator = ConsultationValidator()
        self.conversation_history = []
        self.initial_analysis = None
        self.turn_count = 0
        self.user_concern = ""
        self.explored_topics = set()
        self.consultation_quality_score = 0.0
    
    def add_message(self, speaker, message):
        """Track conversation."""
        self.conversation_history.append({
            'speaker': speaker,
            'message': message
        })
    
    def _check_emergency(self, text):
        """Check for emergency - only REAL emergencies."""
        lower = text.lower()
        critical = [
            ('chest', 'pain'),
            ('worst headache', 'ever'),
            ('cant breathe', 'breath'),
            ('loss of consciousness', 'unconscious'),
            ('severe bleeding',),
            ('sudden weakness', 'paralysis'),
        ]
        for words in critical:
            if all(w in lower for w in words):
                return True
        return False
    
    def _understand_concern(self, user_input):
        """Understand what's really bothering them."""
        lower = user_input.lower()
        
        # Detect main issue
        if any(w in lower for w in ['headache', 'migraine', 'head pain']):
            return 'headache'
        if any(w in lower for w in ['period', 'cycle', 'menstrual', 'pms']):
            return 'hormonal'
        if any(w in lower for w in ['tired', 'fatigue', 'exhausted', 'drained']):
            return 'fatigue'
        if any(w in lower for w in ['bloat', 'gas', 'digest', 'stomach']):
            return 'digestion'
        if any(w in lower for w in ['anxiety', 'anxious', 'stress', 'worried']):
            return 'anxiety'
        if any(w in lower for w in ['sleep', 'insomnia', 'cant sleep']):
            return 'sleep'
        
        return 'general_concern'
    
    def generate_response(self, user_input):
        """Generate warm, conversational response."""
        
        # Check for emergency
        if self._check_emergency(user_input):
            self.add_message('user', user_input)
            response = "I'm hearing something that needs immediate medical attention. Please call 911 or go to an emergency room right now. This is urgent."
            self.add_message('assistant', response)
            return response
        
        # First turn - initial consultation
        if self.turn_count == 0:
            print("\nLet me analyze what you're describing...\n")
            
            self.add_message('user', user_input)
            self.user_concern = user_input
            
            # Run orchestrator to get insights
            self.initial_analysis = self.orchestrator.run_consultation(user_input)
            
            # Get key information
            patterns = self.initial_analysis.get('stages', {}).get('knowledge', {}).get('patterns_identified', [])
            recommendations = self.initial_analysis.get('stages', {}).get('recommender', {}).get('recommendations', [])
            
            concern_type = self._understand_concern(user_input)
            
            # Build WARM, empathetic response
            if concern_type == 'headache' and 'period' in user_input.lower():
                response = f"""I hear you - period-related headaches can be really disruptive. You're definitely not alone in experiencing this.

What you're describing makes a lot of sense. Hormonal headaches happen because of the changes in estrogen and progesterone during your cycle. The good news? This is very addressable with the right approach.

To help you best, I'd like to understand your full picture:
- How often does this happen - every cycle, or just sometimes?
- What else changes during your period besides the headaches?
- How are you managing everything else right now - sleep, stress, energy levels?

Once I understand more, I can give you specific things to try that actually work."""
            
            elif concern_type == 'fatigue':
                response = f"""I'm hearing that you're feeling exhausted, and I want to acknowledge how draining that can be.

Fatigue usually isn't random - it's your body's way of telling us something needs attention. Whether it's related to how you're sleeping, what you're eating, stress, or how your body's hormones are running, we can figure it out.

Tell me:
- When does the fatigue hit worst - mornings, afternoons, or all day?
- What's your sleep like when you do get to sleep?
- Have you noticed any patterns - like does it get worse at certain times?

The answers will tell me a lot about what's really going on."""
            
            elif concern_type == 'digestion':
                response = f"""Digestive issues are frustrating, and I'm glad you're bringing this up because it matters.

What you're experiencing - the bloating, gas, or whatever it is - tells me your gut is trying to communicate something. Often it's about what you're eating, how your body's processing things, or even stress affecting your digestion.

Help me understand better:
- When does it happen most - after certain foods, times of day, or is it pretty constant?
- Does anything make it better or worse?
- How long has this been going on?

Once I know more, we can figure out what's actually driving this."""
            
            elif concern_type == 'sleep':
                response = f"""Sleep problems are exhausting - literally. And I appreciate you naming this because sleep is foundational to everything else.

Poor sleep affects your energy, your mood, your hormones, your digestion - basically everything. So fixing this often fixes a lot of other things too.

Let me ask:
- What's happening with your sleep - can't fall asleep, wake up during the night, or wake up too early?
- What do you think is driving it - your mind racing, physical discomfort, life stress?
- How long has this been going on?

Understanding what's disrupting your sleep will help us figure out real solutions."""
            
            else:
                response = f"""Thanks for sharing what's going on. I want to understand this better so I can actually help.

Here's what I'm hearing: {user_input}

This tells me a few things might be going on, but I need to know more to give you something genuinely useful.

Walk me through:
- How long has this been happening?
- What makes it better or worse?
- What else have you noticed changing along with this?

The details will help me see the full picture."""
            
            self.add_message('assistant', response)
            self.turn_count += 1
            return response
        
        # Follow-up turns - deepen understanding
        else:
            self.add_message('user', user_input)
            
            # Track what we've learned
            lower = user_input.lower()
            
            if any(w in lower for w in ['sleep', 'hour', 'wake', 'insomnia', 'deep sleep', 'slept']):
                self.explored_topics.add('sleep')
            if any(w in lower for w in ['stress', 'work', 'anxious', 'worried', 'student', 'school']):
                self.explored_topics.add('stress')
            if any(w in lower for w in ['eat', 'food', 'diet', 'sugar', 'caffeine', 'meat', 'fiber']):
                self.explored_topics.add('diet')
            if any(w in lower for w in ['exercise', 'workout', 'movement', 'active', 'moving', 'minutes']):
                self.explored_topics.add('exercise')
            
            # Build smart response without repeating their words verbatim
            # Instead, paraphrase and connect
            response_parts = []
            
            # Smart acknowledgment - paraphrase, don't repeat
            if 'period' in lower or 'cycle' in lower or 'bleeding' in lower or 'menstrual' in lower:
                response_parts.append("I'm picking up on something important about your cycle - the changes in bleeding and timing along with your headaches tells me your hormones are shifting in specific ways.")
            elif 'sleep' in lower:
                response_parts.append("Your sleep situation is giving me real clues about what's happening.")
            elif 'stress' in lower or 'student' in lower or 'school' in lower or 'work' in lower:
                response_parts.append("Your stress load is really relevant here - that's often the hidden driver of hormonal issues.")
            elif 'eat' in lower or 'food' in lower or 'diet' in lower:
                response_parts.append("What you're eating matters more than you might think - nutrition directly impacts hormonal balance.")
            elif 'exercise' in lower or 'movement' in lower or 'workout' in lower:
                response_parts.append("Your movement and exercise habits are definitely part of the picture.")
            
            # Connect specific insights
            if 'period' in self.user_concern.lower():
                if 'sleep' in lower and 'deep sleep' in lower:
                    response_parts.append("You mentioned having deep sleep - that's actually good, but if you're only sleeping deeply, you might not be cycling through all the sleep stages your body needs. That could affect how you feel.")
                if 'stress' in lower:
                    response_parts.append("Stress directly raises cortisol, which interferes with estrogen and progesterone. That's a key piece of why your symptoms get worse.")
                if 'exercise' in lower and 'period' in lower:
                    response_parts.append("Smart move not exercising during your period - that shows you're already listening to your body.")
                if 'bleeding' in lower and 'headache' in lower:
                    response_parts.append("The connection between changes in your bleeding and your headaches is significant - they're both hormonal signs telling us something about your cycle.")
            
            # Determine next question - skip already covered topics
            next_question = ""
            if 'sleep' not in self.explored_topics:
                next_question = "How's your sleep looking generally - are you getting enough of it?"
            elif 'stress' not in self.explored_topics:
                next_question = "Tell me more about your stress - what's the biggest source right now?"
            elif 'diet' not in self.explored_topics:
                next_question = "What does a typical day of eating look like for you?"
            elif 'exercise' not in self.explored_topics:
                next_question = "Are you doing any regular exercise or movement?"
            else:
                # All major topics covered - time for insights
                next_question = "Based on everything you've shared, I'm seeing the real picture now. The biggest thing I'd focus on first would be your stress - that's the domino that's probably setting everything else off. Does that match what you're feeling?"
            
            # Build final response
            if response_parts:
                response = "\n\n".join(response_parts) + f"\n\n{next_question}"
            else:
                response = next_question
            
            self.add_message('assistant', response)
            self.turn_count += 1
            return response


# Main execution
if __name__ == "__main__":
    coach = DorostHealthCoach()

    print("\n" + "=" * 80)
    print("                  DOROST - Your Health Coach")
    print("=" * 80)
    print("\nHey there. I'm here to listen and help you figure out what's going on.")
    print("Tell me what's been bothering you - no need for medical terminology, just be real.\n")
    print("(Type 'quit' when you're done)\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
            print("\nTake care of yourself. Remember, these conversations are for understanding,")
            print("but always check with your doctor for medical decisions. You've got this.\n")
            break
        
        if not user_input:
            continue
        
        response = coach.generate_response(user_input)
        print(f"\nDorost: {response}\n")
