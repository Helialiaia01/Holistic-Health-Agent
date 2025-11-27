"""
Context Engineering & Prompt Optimization
===========================================

This module ensures:
1. Clean, relevant context (no stale logs)
2. High success rate through prompt engineering
3. Agent self-awareness of limitations
4. Clear subtask tracking
5. Confidence scoring

Principles:
- Single source of truth (medical_knowledge_base.py)
- Clear boundaries (what agents can/cannot do)
- Explicit task decomposition
- Validation at each step
- Safety first (red flag detection, escalation)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# TASK DECOMPOSITION
# ============================================================================

class TaskType(Enum):
    INTAKE = "intake"                      # Gathering initial information
    DIAGNOSTIC = "diagnostic"              # Physical self-examination
    ANALYSIS = "analysis"                  # Pattern identification
    ROOT_CAUSE = "root_cause"              # Mechanism explanation
    RECOMMENDATION = "recommendation"      # Action plan
    ROUTING = "routing"                    # Specialist recommendation
    FOLLOW_UP = "follow_up"                # Progress tracking

@dataclass
class SubTask:
    """
    Clear subtask definition with success criteria.
    No stale or irrelevant information - only current task context.
    """
    task_type: TaskType
    description: str
    inputs_needed: List[str]
    outputs_expected: List[str]
    success_criteria: List[str]
    agent_responsible: str
    limitations: List[str]
    
    def to_context_string(self) -> str:
        """Convert to clean context string for agent"""
        return f"""
CURRENT TASK: {self.task_type.value}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIVE: {self.description}

INPUTS AVAILABLE:
{self._format_list(self.inputs_needed)}

EXPECTED OUTPUTS:
{self._format_list(self.outputs_expected)}

SUCCESS CRITERIA:
{self._format_list(self.success_criteria)}

YOUR LIMITATIONS (Be transparent about these):
{self._format_list(self.limitations)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def _format_list(self, items: List[str]) -> str:
        return '\n'.join(f"  • {item}" for item in items)


# ============================================================================
# PREDEFINED TASKS (Single Source of Truth)
# ============================================================================

TASK_DEFINITIONS = {
    TaskType.INTAKE: SubTask(
        task_type=TaskType.INTAKE,
        description="Gather comprehensive health information through conversation",
        inputs_needed=[
            "User's initial complaint or concern",
            "Conversation history (if returning user)"
        ],
        outputs_expected=[
            "Detailed symptom description",
            "Duration and severity of symptoms",
            "Diet, sleep, exercise, stress patterns",
            "Sun exposure and lifestyle factors",
            "Current medications/supplements",
            "Medical history",
            "What patient wants to achieve"
        ],
        success_criteria=[
            "Collected enough information to identify patterns",
            "Understood patient's primary concern",
            "Identified any red flag symptoms",
            "Gathered lifestyle context (diet, sleep, stress)",
            "Patient feels heard and understood"
        ],
        agent_responsible="intake_agent",
        limitations=[
            "Cannot diagnose medical conditions",
            "Cannot prescribe medications",
            "Must escalate if red flags detected",
            "Cannot interpret lab results definitively",
            "Cannot provide emergency medical advice"
        ]
    ),
    
    TaskType.DIAGNOSTIC: SubTask(
        task_type=TaskType.DIAGNOSTIC,
        description="Guide patient through physical self-examination to gather objective data",
        inputs_needed=[
            "Health profile from intake",
            "Specific symptoms to investigate",
            "Patient's ability to perform self-exams"
        ],
        outputs_expected=[
            "Tongue examination findings",
            "Nail examination findings",
            "Skin condition observations",
            "Capillary refill time",
            "Orthostatic test results",
            "Other visible signs (dark circles, bruising, etc.)"
        ],
        success_criteria=[
            "Patient successfully performed examinations",
            "Gathered objective physical findings",
            "Findings documented clearly",
            "Patient understands what findings mean",
            "Identified any red flag signs requiring medical attention"
        ],
        agent_responsible="diagnostic_agent",
        limitations=[
            "Cannot perform medical examinations (only guide self-exam)",
            "Cannot replace professional physical exam",
            "Cannot diagnose from photos alone",
            "Must recommend doctor visit if findings are concerning",
            "Cannot assess internal organs or systems"
        ]
    ),
    
    TaskType.ANALYSIS: SubTask(
        task_type=TaskType.ANALYSIS,
        description="Analyze symptoms and findings using medical knowledge to identify patterns",
        inputs_needed=[
            "Health profile (symptoms, lifestyle)",
            "Diagnostic findings (physical exam)",
            "Patient context (age, sex, duration)",
            "Medical knowledge database"
        ],
        outputs_expected=[
            "Likely nutrient deficiencies identified",
            "Metabolic issues identified (insulin resistance, etc.)",
            "Body systems affected (gut, hormones, etc.)",
            "Confidence score for assessment",
            "Differential considerations",
            "Which specialists might be needed"
        ],
        success_criteria=[
            "Identified 2-4 most likely issues",
            "Analysis is evidence-based",
            "Confidence score calculated",
            "Clear reasoning provided",
            "Red flags assessed and escalated if present"
        ],
        agent_responsible="knowledge_agent",
        limitations=[
            "Cannot make medical diagnosis (only identify patterns)",
            "Cannot replace bloodwork or medical tests",
            "Confidence varies based on symptom clarity",
            "May miss rare conditions",
            "Cannot account for all individual variations"
        ]
    ),
    
    TaskType.ROOT_CAUSE: SubTask(
        task_type=TaskType.ROOT_CAUSE,
        description="Explain underlying mechanisms and root causes in accessible language",
        inputs_needed=[
            "Analysis results (deficiencies, issues identified)",
            "Patient's symptoms",
            "Lifestyle factors contributing"
        ],
        outputs_expected=[
            "Explanation of root causes (not just proximal causes)",
            "Biochemical mechanisms in simple language",
            "How symptoms connect to root causes",
            "Cascade effects and vicious cycles",
            "Why generic advice hasn't worked"
        ],
        success_criteria=[
            "Patient understands WHY symptoms are happening",
            "Root causes clearly identified (not just symptoms)",
            "Mechanisms explained at appropriate level",
            "Shows interconnections between issues",
            "Patient empowered with knowledge"
        ],
        agent_responsible="root_cause_agent",
        limitations=[
            "Explanations are educational, not diagnostic",
            "May not capture all complexity of individual case",
            "Cannot account for genetic factors without testing",
            "Cannot determine causation definitively without medical workup"
        ]
    ),
    
    TaskType.RECOMMENDATION: SubTask(
        task_type=TaskType.RECOMMENDATION,
        description="Provide specific, actionable recommendations (supplements, diet, lifestyle)",
        inputs_needed=[
            "Root causes identified",
            "Deficiencies identified",
            "Patient's goals and constraints",
            "Safety information (medications, allergies, conditions)",
            "Confidence score from analysis"
        ],
        outputs_expected=[
            "Specific supplements with forms, dosages, timing",
            "Diet recommendations with food sources and amounts",
            "Lifestyle interventions (sleep, exercise, stress)",
            "What to avoid and why",
            "Timeline with weekly expectations",
            "Safety considerations and interactions",
            "When to see doctor"
        ],
        success_criteria=[
            "Recommendations are specific and actionable",
            "Dosages, forms, timing all specified",
            "Safety checked (interactions, contraindications)",
            "Patient understands WHY each recommendation",
            "Timeline set for follow-up",
            "Clear guidance on when to see doctor"
        ],
        agent_responsible="recommender_agent",
        limitations=[
            "Recommendations are educational, not prescriptions",
            "Cannot account for all individual health factors",
            "Cannot guarantee results",
            "Must defer to doctor if patient has serious conditions",
            "Cannot provide recommendations for pregnant/breastfeeding without medical supervision",
            "Low confidence = recommend seeing doctor instead"
        ]
    ),
    
    TaskType.ROUTING: SubTask(
        task_type=TaskType.ROUTING,
        description="Recommend which medical specialist patient should consult",
        inputs_needed=[
            "Symptoms and their severity",
            "Body system affected",
            "Duration of symptoms",
            "Red flags present or not"
        ],
        outputs_expected=[
            "Primary specialist recommendation",
            "Secondary/alternative specialists",
            "Reasoning for recommendation",
            "What tests specialist might do",
            "Urgency level (routine, soon, urgent, emergency)"
        ],
        success_criteria=[
            "Patient knows which type of doctor to see",
            "Understands why this specialist is appropriate",
            "Knows what to expect from appointment",
            "Urgency clearly communicated",
            "Alternative options provided if needed"
        ],
        agent_responsible="specialty_router_agent",
        limitations=[
            "Recommendations based on symptom patterns only",
            "Cannot replace doctor's referral process",
            "May not account for regional healthcare availability",
            "Cannot guarantee specialist will agree with routing",
            "Emergency symptoms = call 911, not routing agent"
        ]
    ),
    
    TaskType.FOLLOW_UP: SubTask(
        task_type=TaskType.FOLLOW_UP,
        description="Track progress, assess intervention effectiveness, adjust plan",
        inputs_needed=[
            "Baseline symptoms and severity",
            "Interventions implemented",
            "Current symptoms and severity",
            "Compliance with recommendations",
            "Time since baseline"
        ],
        outputs_expected=[
            "Progress assessment (% improvement)",
            "Which interventions are working",
            "Which interventions need adjustment",
            "New recommendations based on response",
            "When to follow up again",
            "When to see doctor if not improving"
        ],
        success_criteria=[
            "Clear assessment of progress",
            "Specific adjustments if needed",
            "Patient knows what's working",
            "Timeline for next check-in established",
            "Escalation to doctor if no improvement"
        ],
        agent_responsible="follow_up_agent",
        limitations=[
            "Cannot assess internal changes without medical tests",
            "Relies on patient self-reporting",
            "Cannot determine if underlying disease is progressing",
            "Must recommend doctor visit if no improvement by 8 weeks"
        ]
    ),
}


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class ContextManager:
    """
    Manages clean, relevant context for agents.
    No stale logs, no irrelevant info - only what's needed for current task.
    """
    
    def __init__(self):
        self.current_task: Optional[SubTask] = None
        self.session_data: Dict = {}
        self.completed_tasks: List[TaskType] = []
    
    def set_current_task(self, task_type: TaskType):
        """Set the current task and clear stale context"""
        self.current_task = TASK_DEFINITIONS[task_type]
        # Clear any task-specific temporary data from previous tasks
        self._clear_stale_data()
    
    def get_task_context(self) -> str:
        """Get clean context string for current task"""
        if not self.current_task:
            return "No current task set."
        
        context = self.current_task.to_context_string()
        
        # Add relevant session data ONLY
        relevant_data = self._get_relevant_session_data()
        if relevant_data:
            context += "\nRELEVANT INFORMATION FROM PREVIOUS TASKS:\n"
            for key, value in relevant_data.items():
                context += f"  • {key}: {value}\n"
        
        # Add limitations reminder
        context += "\n⚠️ REMEMBER YOUR LIMITATIONS ⚠️\n"
        context += "You must be transparent when you reach the limits of what you can do.\n"
        context += "When in doubt, recommend consulting a healthcare professional.\n"
        
        return context
    
    def _get_relevant_session_data(self) -> Dict:
        """Get only relevant data for current task (no stale logs)"""
        if not self.current_task:
            return {}
        
        relevant = {}
        inputs_needed = self.current_task.inputs_needed
        
        for input_key in inputs_needed:
            # Extract key words to search session data
            search_terms = self._extract_search_terms(input_key)
            for term in search_terms:
                if term in self.session_data:
                    relevant[term] = self.session_data[term]
        
        return relevant
    
    def _extract_search_terms(self, input_description: str) -> List[str]:
        """Extract search terms from input description"""
        # Simple mapping - could be more sophisticated
        mappings = {
            "symptom": ["symptoms", "primary_concern", "complaints"],
            "lifestyle": ["diet", "sleep", "exercise", "stress"],
            "diagnostic": ["diagnostic_findings", "physical_exam"],
            "analysis": ["identified_issues", "deficiencies"],
            "confidence": ["confidence_score", "reliability"]
        }
        
        terms = []
        for key, values in mappings.items():
            if key in input_description.lower():
                terms.extend(values)
        
        return terms
    
    def _clear_stale_data(self):
        """Remove temporary data from previous tasks"""
        # Keep core data (symptoms, history) but clear task-specific temporary data
        temp_keys = ["_temp_", "_debug_", "_intermediate_"]
        for key in list(self.session_data.keys()):
            if any(temp in key for temp in temp_keys):
                del self.session_data[key]
    
    def store_task_output(self, task_type: TaskType, data: Dict):
        """Store output from completed task"""
        self.session_data[task_type.value] = data
        self.completed_tasks.append(task_type)
    
    def get_task_status(self) -> Dict:
        """Get status of all tasks"""
        return {
            "current_task": self.current_task.task_type.value if self.current_task else None,
            "completed_tasks": [t.value for t in self.completed_tasks],
            "session_data_keys": list(self.session_data.keys())
        }


# ============================================================================
# PROMPT OPTIMIZATION
# ============================================================================

def create_optimized_prompt(
    base_instruction: str,
    current_task: SubTask,
    examples: Optional[List[Dict]] = None,
    constraints: Optional[List[str]] = None
) -> str:
    """
    Create an optimized prompt with:
    - Clear instructions
    - Task context
    - Examples (if provided)
    - Constraints and limitations
    - Success criteria
    
    This increases success rate by being explicit about expectations.
    """
    
    prompt = base_instruction + "\n\n"
    prompt += "=" * 70 + "\n"
    prompt += current_task.to_context_string()
    
    if examples:
        prompt += "\n" + "=" * 70 + "\n"
        prompt += "EXAMPLES OF GOOD RESPONSES:\n"
        prompt += "=" * 70 + "\n\n"
        for i, example in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Input: {example.get('input', 'N/A')}\n"
            prompt += f"Good Response: {example.get('response', 'N/A')}\n\n"
    
    if constraints:
        prompt += "\n" + "=" * 70 + "\n"
        prompt += "IMPORTANT CONSTRAINTS:\n"
        prompt += "=" * 70 + "\n"
        for constraint in constraints:
            prompt += f"  • {constraint}\n"
    
    # Always add safety reminder
    prompt += "\n" + "=" * 70 + "\n"
    prompt += "SAFETY & ESCALATION:\n"
    prompt += "=" * 70 + "\n"
    prompt += """
  • If you detect red flag symptoms → Immediately inform user and recommend appropriate urgency (911, ER, 24hr, etc.)
  • If confidence in assessment is low (<60%) → Recommend seeing a doctor
  • If symptoms persist >8 weeks without improvement → Must see doctor
  • If patient has serious medical conditions → Defer to their doctor
  • Always end with: "This is educational information. Consult a healthcare professional for medical advice."
"""
    
    return prompt


# ============================================================================
# CONFIDENCE SCORING
# ============================================================================

@dataclass
class ConfidenceAssessment:
    """Agent's self-assessment of confidence"""
    score: float  # 0.0 to 1.0
    factors_increasing: List[str]
    factors_decreasing: List[str]
    reliability: str  # "high", "medium", "low"
    should_escalate: bool
    escalation_reason: Optional[str] = None

def calculate_agent_confidence(
    symptom_clarity: float,  # 0-1, how specific symptoms are
    pattern_match_strength: float,  # 0-1, how well symptoms match known patterns
    red_flags_present: bool,
    duration_weeks: int,
    patient_complexity: float,  # 0-1, how complex patient case is
) -> ConfidenceAssessment:
    """
    Calculate agent's confidence in its assessment.
    High confidence = agent can provide recommendations.
    Low confidence = must escalate to medical professional.
    """
    
    base_score = 0.5
    factors_up = []
    factors_down = []
    
    # Increase confidence
    if symptom_clarity > 0.7:
        base_score += 0.15
        factors_up.append("Symptoms are specific and well-described")
    
    if pattern_match_strength > 0.8:
        base_score += 0.20
        factors_up.append("Strong match to known health patterns")
    
    if duration_weeks >= 2:
        base_score += 0.10
        factors_up.append("Symptom duration allows for pattern recognition")
    
    # Decrease confidence
    if symptom_clarity < 0.4:
        base_score -= 0.20
        factors_down.append("Symptoms are vague or nonspecific")
    
    if red_flags_present:
        base_score = 0.20  # Force low confidence
        factors_down.append("Red flag symptoms detected - requires medical evaluation")
    
    if patient_complexity > 0.7:
        base_score -= 0.15
        factors_down.append("Complex case with multiple interacting factors")
    
    if duration_weeks < 1:
        base_score -= 0.10
        factors_down.append("Very short duration makes assessment uncertain")
    
    # Cap between 0 and 1
    final_score = max(0.0, min(1.0, base_score))
    
    # Determine reliability
    if final_score >= 0.75:
        reliability = "high"
    elif final_score >= 0.50:
        reliability = "medium"
    else:
        reliability = "low"
    
    # Should escalate?
    should_escalate = (
        final_score < 0.60 or
        red_flags_present or
        patient_complexity > 0.8 or
        duration_weeks > 12  # Chronic issues need medical workup
    )
    
    escalation_reason = None
    if should_escalate:
        if red_flags_present:
            escalation_reason = "Red flag symptoms require immediate medical attention"
        elif final_score < 0.60:
            escalation_reason = "Confidence too low for reliable recommendations"
        elif patient_complexity > 0.8:
            escalation_reason = "Case complexity requires medical expertise"
        elif duration_weeks > 12:
            escalation_reason = "Chronic symptoms (>12 weeks) require medical workup"
    
    return ConfidenceAssessment(
        score=round(final_score, 2),
        factors_increasing=factors_up,
        factors_decreasing=factors_down,
        reliability=reliability,
        should_escalate=should_escalate,
        escalation_reason=escalation_reason
    )


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'TaskType',
    'SubTask',
    'TASK_DEFINITIONS',
    'ContextManager',
    'create_optimized_prompt',
    'ConfidenceAssessment',
    'calculate_agent_confidence',
]
