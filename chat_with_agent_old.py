from src.orchestrator import HealthAgentOrchestrator

class ConversationManager:
    """Manages multi-turn conversation with context retention."""
    
    def __init__(self):
        self.orchestrator = HealthAgentOrchestrator()
        self.initial_result = None
        self.conversation_history = []
        self.discussed_topics = set()
        self.user_profile = {
            'cravings': None,
            'sleep_quality': None,
            'stress_level': None,
            'diet_triggers': None,
            'energy_pattern': None,
            'exercise': None,
            'water_intake': None
        }
        self.stage = 'initial'  # initial -> gathering -> advising -> refining
    
    def add_message(self, speaker, message):
        """Add message to history."""
        self.conversation_history.append({'speaker': speaker, 'message': message})
    
    def update_profile(self, user_input):
        """Extract information from user input to update profile."""
        lower_input = user_input.lower()
        
        # Get last question to understand context
        last_assistant_msg = ''
        if len(self.conversation_history) >= 1:
            for msg in reversed(self.conversation_history):
                if msg['speaker'] == 'assistant':
                    last_assistant_msg = msg['message'].lower()
                    break
        
        # Detect cravings
        if any(word in lower_input for word in ['chocolate', 'salt', 'sugar', 'craving', 'crave']):
            self.user_profile['cravings'] = 'yes'
            self.discussed_topics.add('cravings')
        # Context: if we asked about cravings and they give any answer
        elif 'craving' in last_assistant_msg and 'food craving' in last_assistant_msg:
            self.user_profile['cravings'] = user_input.strip()
            self.discussed_topics.add('cravings')
        
        # Detect sleep issues
        if any(word in lower_input for word in ['sleep', 'insomnia', 'wake', 'tired', 'fatigue', 'hours']):
            self.user_profile['sleep_quality'] = 'disrupted'
            self.discussed_topics.add('sleep')
        # Context: if we asked about sleep hours and they give a numeric answer
        elif 'how many hours of sleep' in last_assistant_msg and any(char.isdigit() for char in user_input):
            self.user_profile['sleep_quality'] = user_input.strip()
            self.discussed_topics.add('sleep')
        
        # Detect stress - including numeric answers
        if any(word in lower_input for word in ['stress', 'anxious', 'anxiety', 'worried', 'overwhelmed']):
            self.user_profile['stress_level'] = 'elevated'
            self.discussed_topics.add('stress')
        # Context: if we asked about stress level and they give a numeric answer
        elif 'how would you rate your current stress level' in last_assistant_msg and any(char.isdigit() for char in user_input):
            self.user_profile['stress_level'] = user_input.strip()
            self.discussed_topics.add('stress')
        
        # Detect energy patterns
        if any(word in lower_input for word in ['energy', 'morning', 'afternoon', 'crash', 'lunch']):
            self.user_profile['energy_pattern'] = 'identified'
            self.discussed_topics.add('energy')
        # Context: if we asked about energy and they answer
        elif 'energy level' in last_assistant_msg or 'feel most tired' in last_assistant_msg:
            self.user_profile['energy_pattern'] = user_input.strip()
            self.discussed_topics.add('energy')
    
    def get_next_question(self):
        """Generate next clarifying question based on what we know."""
        # Priority questions we haven't discussed
        if 'sleep' not in self.discussed_topics:
            return "How many hours of sleep are you getting per night, and do you wake up during the night?"
        
        if 'stress' not in self.discussed_topics:
            return "On a scale of 1-10, how would you rate your current stress level?"
        
        if 'cravings' not in self.discussed_topics:
            return "Do you notice any specific food cravings, especially before your period?"
        
        if 'energy' not in self.discussed_topics:
            return "How would you describe your energy levels - are there specific times of day when you feel most tired?"
        
        # All key topics covered, move to advice stage
        return None
    
    def generate_response(self, user_input):
        """Generate contextual response based on conversation stage and history."""
        
        if self.stage == 'initial':
            # First message - run orchestrator
            print("\nAnalyzing your health profile...\n")
            self.initial_result = self.orchestrator.run_consultation(user_input)
            self.add_message('user', user_input)
            self.stage = 'gathering'
            
            patterns = self.initial_result['stages'].get('knowledge', {}).get('patterns_identified', [])
            
            # Check for emergency
            if self.initial_result.get('red_flags'):
                response = (
                    f"I need to pause here - I'm seeing symptoms that require immediate medical attention:\n\n"
                    f"{chr(10).join('• ' + flag for flag in self.initial_result['red_flags'])}\n\n"
                    f"Please call 911 or go to the nearest emergency room right away."
                )
                self.stage = 'emergency'
                return response
            
            # Acknowledge and start gathering
            if any('headache' in p.lower() or 'migraine' in p.lower() for p in patterns):
                response = (
                    "I understand - period-related headaches can be very disruptive. These are typically triggered "
                    "by hormonal fluctuations, specifically the drop in estrogen that occurs during menstruation.\n\n"
                    "To develop the most effective approach for you, I need to understand your specific pattern. "
                    "Let me ask you a few questions:\n\n"
                    "How many hours of sleep are you getting per night, and do you wake up during the night?"
                )
            else:
                response = (
                    "Thank you for sharing that. To give you the most helpful guidance, I need to understand "
                    "your situation in more detail.\n\n"
                    "How many hours of sleep are you getting per night, and do you wake up during the night?"
                )
            
            self.add_message('assistant', response)
            return response
        
        elif self.stage == 'gathering':
            # Gathering information phase
            self.add_message('user', user_input)
            self.update_profile(user_input)
            
            # Build contextual response
            response = self._build_contextual_acknowledgment(user_input)
            
            # Get next question or move to advice
            next_question = self.get_next_question()
            
            if next_question:
                response += f"\n\n{next_question}"
                self.add_message('assistant', response)
                return response
            else:
                # Enough information gathered, provide comprehensive advice
                self.stage = 'advising'
                response += "\n\nBased on what you've shared, I can now provide you with specific recommendations. "
                response += "Let me explain what's happening and what you can do about it."
                self.add_message('assistant', response)
                return response
        
        elif self.stage == 'advising':
            # Providing recommendations
            self.add_message('user', user_input)
            user_lower = user_input.lower()
            
            # Check what they're asking about
            if any(word in user_lower for word in ['what should', 'how', 'protocol', 'treatment', 'recommend', 'do', 'help', 'plan']):
                response = self._generate_personalized_plan()
                self.discussed_topics.add('protocol')
                self.stage = 'refining'
            
            elif any(word in user_lower for word in ['supplement', 'vitamin', 'magnesium', 'pill']):
                response = self._generate_supplement_protocol()
                self.discussed_topics.add('supplements')
            
            elif any(word in user_lower for word in ['diet', 'food', 'eat', 'nutrition', 'meal']):
                response = self._generate_diet_advice()
                self.discussed_topics.add('diet')
            
            elif any(word in user_lower for word in ['how long', 'when', 'timeline', 'expect', 'improve']):
                response = self._generate_timeline()
                self.discussed_topics.add('timeline')
            
            elif any(word in user_lower for word in ['why', 'explain', 'how does', 'mechanism', 'science']):
                response = self._explain_mechanism()
                self.discussed_topics.add('mechanism')
            
            else:
                # Default: provide comprehensive plan
                response = self._generate_personalized_plan()
                self.discussed_topics.add('protocol')
                self.stage = 'refining'
            
            self.add_message('assistant', response)
            return response
        
        elif self.stage == 'refining':
            # Answering follow-up questions
            self.add_message('user', user_input)
            user_lower = user_input.lower()
            
            if any(word in user_lower for word in ['supplement', 'vitamin', 'magnesium']) and 'supplements' not in self.discussed_topics:
                response = self._generate_supplement_protocol()
                self.discussed_topics.add('supplements')
            
            elif any(word in user_lower for word in ['diet', 'food', 'eat']) and 'diet' not in self.discussed_topics:
                response = self._generate_diet_advice()
                self.discussed_topics.add('diet')
            
            elif any(word in user_lower for word in ['how long', 'when', 'timeline']) and 'timeline' not in self.discussed_topics:
                response = self._generate_timeline()
                self.discussed_topics.add('timeline')
            
            elif any(word in user_lower for word in ['why', 'explain', 'mechanism']) and 'mechanism' not in self.discussed_topics:
                response = self._explain_mechanism()
                self.discussed_topics.add('mechanism')
            
            elif any(word in user_lower for word in ['cycle', 'period', 'hormone', 'estrogen']):
                response = self._explain_cycle_dynamics()
                self.discussed_topics.add('cycle')
            
            else:
                # Provide clarification or ask what else they need
                response = (
                    "I want to make sure you have everything you need. Is there a specific aspect you'd like me to clarify?\n\n"
                    "I can explain:\n"
                    "• The specific supplement protocol with dosages\n"
                    "• Dietary modifications that will help\n"
                    "• The timeline for seeing improvements\n"
                    "• Why this happens in your body\n"
                    "• How your menstrual cycle affects symptoms\n\n"
                    "What would be most helpful?"
                )
            
            self.add_message('assistant', response)
            return response
        
        else:  # emergency
            return "Please seek immediate medical care for your symptoms."
    
    def _build_contextual_acknowledgment(self, user_input):
        """Build acknowledgment that references previous conversation."""
        lower_input = user_input.lower()
        
        # Get the last question asked to provide context-appropriate response
        last_assistant_msg = ''
        if len(self.conversation_history) >= 2:
            for msg in reversed(self.conversation_history):
                if msg['speaker'] == 'assistant':
                    last_assistant_msg = msg['message'].lower()
                    break
        
        # Reference stress - only if last question ASKS about stress level (ends with the question)
        if 'how would you rate your current stress level' in last_assistant_msg:
            stress_level = None
            # Look for numeric stress levels including decimals
            for num in ['10', '9.5', '9', '8.5', '8', '7.5', '7', '6.5', '6', '5.5', '5']:
                if num in user_input:
                    stress_level = num
                    break
            
            if stress_level:
                stress_float = float(stress_level)
                if stress_float >= 7:
                    return (
                        f"A stress level of {stress_level}/10 is quite elevated. This is important because chronic stress "
                        f"raises cortisol, which directly interferes with estrogen and progesterone balance. "
                        f"This is likely amplifying your symptoms."
                    )
                else:
                    return f"I understand. A stress level of {stress_level}/10 is still something we should address in your plan."
            else:
                return "Understood. Stress management will be an important component."
        
        # Reference sleep issues - only if last question ASKS about sleep
        if 'how many hours of sleep' in last_assistant_msg or 'sleep are you getting' in last_assistant_msg:
            if '6' in user_input or 'six' in user_input:
                return (
                    "Six hours is below optimal - most adults need 7-9 hours for proper hormonal regulation. "
                    "The nighttime waking you mention is significant too. This sleep disruption affects cortisol, "
                    "which can worsen hormonal symptoms."
                )
            elif '5' in user_input or 'five' in user_input:
                return (
                    "Five hours is significantly below what your body needs for hormonal regulation. "
                    "Sleep deprivation directly impacts cortisol and hormone balance, which can worsen symptoms."
                )
            elif '7' in user_input or '8' in user_input or 'seven' in user_input or 'eight' in user_input:
                return "That's a reasonable amount. Let's explore other factors that might be contributing."
            else:
                return "I see. Sleep quality and hormonal balance are closely connected."
        
        # Reference energy patterns
        if 'energy' in lower_input or 'tired' in lower_input or 'crash' in lower_input or 'afternoon' in lower_input:
            return (
                "That energy pattern you describe - gradual decline after lunch with a crash - is characteristic "
                "of blood sugar dysregulation. When combined with hormonal fluctuations, this creates a "
                "perfect storm for worsening symptoms."
            )
        
        # Reference cravings
        if 'chocolate' in lower_input or 'sugar' in lower_input or 'carb' in lower_input or 'craving' in lower_input:
            return (
                "Those cravings are your body's way of signaling nutrient needs, particularly magnesium. "
                "This is directly relevant to your headaches."
            )
        
        # Generic acknowledgment
        return "Thank you for that information."
    
    def _generate_personalized_plan(self):
        """Generate plan incorporating discussed profile details."""
        recommendations = self.initial_result['stages'].get('recommender', {}).get('recommendations', [])
        
        response = "Based on our conversation, here's your personalized protocol:\n\n"
        
        # Reference specific things discussed
        if self.user_profile['sleep_quality'] == 'disrupted':
            response += "**Priority #1: Sleep Optimization** (addressing the disruption you mentioned)\n"
            response += "• Target 7-9 hours consistently\n"
            response += "• Magnesium glycinate 300-400mg one hour before bed (helps with the nighttime waking)\n"
            response += "• Dark, cool room (16-19°C)\n"
            response += "• No screens 60 minutes before sleep\n\n"
        
        if self.user_profile['stress_level'] == 'elevated':
            response += "**Priority #2: Stress Management** (critical given your elevated stress level)\n"
            response += "• Daily meditation or breathing exercises (10-20 minutes)\n"
            response += "• Gentle exercise (walking, yoga) - not intense training\n"
            response += "• Consider adaptogenic herbs (discuss with doctor first)\n\n"
        
        if self.user_profile['energy_pattern'] == 'identified':
            response += "**Priority #3: Blood Sugar Stabilization** (addressing those afternoon crashes)\n"
            response += "• Balanced meals with protein and healthy fats\n"
            response += "• Avoid high-glycemic carbohydrates especially at lunch\n"
            response += "• Consider intermittent fasting (16:8) to improve insulin sensitivity\n\n"
        
        # Add supplement protocol
        response += "**Supplement Protocol:**\n"
        for i, rec in enumerate(recommendations[:3], 1):
            response += f"{i}. {rec}\n"
        
        response += (
            "\n**Implementation Approach:**\n"
            "Week 1-2: Focus on sleep and stress (foundation)\n"
            "Week 2-3: Add supplements\n"
            "Week 3-4: Refine diet\n\n"
            "Does this make sense given your situation? Any questions about implementation?"
        )
        
        return response
    
    def _generate_supplement_protocol(self):
        """Detailed supplement protocol."""
        response = (
            "Here's the specific supplement protocol:\n\n"
            "**Phase 1: Foundational (Start immediately)**\n\n"
            "Magnesium Glycinate: 300-400mg before bed\n"
            "• Why glycinate: Best absorption, won't cause digestive issues\n"
            "• Timing: Before bed supports sleep and GABA activation\n"
        )
        
        if self.user_profile['sleep_quality'] == 'disrupted':
            response += "• This will specifically help with the nighttime waking you mentioned\n"
        
        response += "• Double dose days -2 to +3 around period\n\n"
        
        response += (
            "**Phase 2: Targeted Support (Week 2-4)**\n\n"
            "CoQ10: 300mg with breakfast\n"
            "• Supports mitochondrial energy in brain tissue\n"
            "• 50-70% reduction in migraine frequency in clinical studies\n\n"
            "Riboflavin (B2): 400mg daily\n"
            "• Required for cellular energy metabolism\n"
            "• Evidence-based migraine prevention\n\n"
            "**Phase 3: Hormonal Balance (Week 4+)**\n\n"
            "DIM: 200mg daily\n"
            "• Supports estrogen metabolism\n"
            "• Helps balance estrogen/progesterone ratio\n\n"
            "Vitex: 400-500mg morning, empty stomach\n"
            "• Supports progesterone production\n"
            "• Takes 2-3 months for full effect\n\n"
            "Add one supplement at a time, waiting 1-2 weeks between additions. "
            "This helps you identify what's working.\n\n"
            "Would you like to know about the dietary component?"
        )
        
        return response
    
    def _generate_diet_advice(self):
        """Detailed diet advice."""
        response = "Dietary modifications for hormonal balance:\n\n"
        
        if self.user_profile['energy_pattern'] == 'identified':
            response += (
                "**To address your afternoon energy crashes:**\n"
                "• Include protein and healthy fats at lunch (not just carbs)\n"
                "• Avoid bread, pasta, rice during midday\n"
                "• Example lunch: Salmon with vegetables and avocado\n\n"
            )
        
        response += (
            "**Foods to Minimize:**\n"
            "• Refined seed oils (soybean, canola, corn, sunflower)\n"
            "  → High omega-6 promotes inflammatory prostaglandin production\n"
            "• High-glycemic carbs (bread, pasta, sugar, processed grains)\n"
            "  → Insulin spikes disrupt hormonal balance\n"
            "• Processed foods with additives\n"
            "  → MSG, artificial sweeteners are migraine triggers\n\n"
            "**Foods to Emphasize:**\n"
            "• Wild-caught fatty fish (salmon, sardines, mackerel) 3-4x weekly\n"
            "  → Omega-3s (EPA/DHA) reduce inflammation, support serotonin\n"
            "• Cruciferous vegetables (broccoli, cauliflower, kale) 2-3 cups daily\n"
            "  → Support liver estrogen metabolism\n"
            "• Grass-fed beef, organ meats\n"
            "  → Provide CoQ10, B vitamins, iron, zinc\n"
        )
        
        if self.user_profile['cravings'] == 'yes':
            response += (
                "• Dark chocolate (85%+ cacao) in moderation\n"
                "  → Satisfies cravings while providing magnesium\n"
            )
        
        response += (
            "\n**Meal Timing:**\n"
            "• Consistent meal schedule (helps hormonal stability)\n"
            "• Don't skip breakfast\n"
            "• Avoid eating 3 hours before bed\n\n"
            "What other questions do you have?"
        )
        
        return response
    
    def _generate_timeline(self):
        """Explain expected timeline."""
        response = "Here's what to expect:\n\n"
        
        if self.user_profile['sleep_quality'] == 'disrupted':
            response += (
                "**Week 1:**\n"
                "Your sleep should improve within 7-10 days (less nighttime waking, deeper sleep). "
                "This is often the first noticeable change.\n\n"
            )
        else:
            response += "**Week 1:**\nSleep quality improves, energy starts stabilizing.\n\n"
        
        response += (
            "**Week 2:**\n"
            "Energy levels become more consistent. Mood stabilization. "
        )
        
        if self.user_profile['energy_pattern'] == 'identified':
            response += "Those afternoon crashes should reduce significantly."
        
        response += (
            "\n\n**Weeks 3-4:**\n"
            "This is when migraine improvement typically becomes apparent. "
            "Expect 40-50% reduction in frequency or severity.\n\n"
            "**Weeks 6-8:**\n"
            "60-80% improvement. Some women skip cycles entirely without migraine.\n\n"
            "**Week 12+:**\n"
            "New baseline established. Migraines become rare or much milder.\n\n"
        )
        
        if self.user_profile['stress_level'] == 'elevated':
            response += (
                "**Important:** Stress management will accelerate these improvements. "
                "With your current stress level, this is non-negotiable.\n\n"
            )
        
        response += "Consistency is essential. What else can I clarify?"
        
        return response
    
    def _explain_mechanism(self):
        """Explain the biological mechanism."""
        response = "Here's what's happening in your body:\n\n"
        
        response += (
            "**The Hormonal Cascade:**\n"
            "Before/during menstruation → Estrogen drops sharply → Serotonin decreases (they're linked) "
            "→ Blood vessels become hyperreactive → Migraine triggered\n\n"
            "**The Magnesium Connection:**\n"
            "Menstruation causes magnesium loss. Magnesium acts as a natural calcium channel blocker - "
            "it keeps blood vessels stable. Without enough magnesium, vessels become reactive.\n\n"
        )
        
        if self.user_profile['sleep_quality'] == 'disrupted':
            response += (
                "**Why Your Sleep Matters:**\n"
                "Poor sleep disrupts your HPA axis (stress-response system). This keeps cortisol elevated, "
                "which interferes with estrogen/progesterone balance. The sleep disruption you mentioned "
                "is literally making your hormonal symptoms worse.\n\n"
            )
        
        if self.user_profile['stress_level'] == 'elevated':
            response += (
                "**The Stress Impact:**\n"
                "Chronic stress → Elevated cortisol → Steals pregnenolone (precursor to progesterone) "
                "→ Less progesterone → Estrogen dominance → Worse PMS and migraines\n\n"
            )
        
        response += "That's why the protocol addresses these foundational issues. Make sense?"
        
        return response
    
    def _explain_cycle_dynamics(self):
        """Explain menstrual cycle and intervention timing."""
        return (
            "Understanding your cycle helps target interventions:\n\n"
            "**Follicular Phase (Days 1-14):**\n"
            "Estrogen rising → Serotonin rising → Lower migraine risk\n"
            "→ Maintain baseline protocol\n\n"
            "**Ovulation (Day 14):**\n"
            "Estrogen peaks then drops → Brief vulnerability window\n\n"
            "**Luteal Phase (Days 14-28):**\n"
            "Progesterone should be high. If inadequate → Estrogen dominance → PMS\n"
            "→ INCREASE interventions: 400-600mg magnesium, stricter diet, more sleep\n\n"
            "**Perimenstrual (Days -2 to +3):**\n"
            "HIGHEST RISK. Estrogen crashes → Serotonin crashes → Prostaglandins release\n"
            "→ MAXIMUM PREVENTION: Double magnesium, anti-inflammatory diet, gentle movement\n\n"
            "Tracking your cycle (apps like Clue) helps you anticipate and prevent rather than react.\n\n"
            "60-70% of menstrual migraines happen in that perimenstrual window. "
            "By increasing interventions during high-risk phases, you can dramatically reduce occurrence.\n\n"
            "Does this help explain the timing strategy?"
        )


# Main execution
if __name__ == "__main__":
    manager = ConversationManager()

    print("\n" + "=" * 80)
    print("                  DOROST - Holistic Health Consultation")
    print("=" * 80)
    print("\nWelcome. I'm here to help you understand your health concerns and develop")
    print("a personalized, evidence-based approach.")
    print("\nDescribe what's been going on, and I'll ask questions to understand your situation.")
    print("\n(Type 'quit' when finished)\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q', 'done']:
            print("\nThank you for consulting with me. This information is educational and should")
            print("complement professional medical care. Consistency is key to seeing results.")
            print("\nWishing you improved health.\n")
            break
        
        if not user_input:
            continue
        
        response = manager.generate_response(user_input)
        print(f"\nDorost: {response}\n")
