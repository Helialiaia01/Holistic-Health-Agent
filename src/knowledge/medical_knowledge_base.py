"""
Medical knowledge base - single source of truth for all medical info.

Everything medical goes here: symptoms, conditions, red flags, specialists.
This way all agents use the same info - no conflicts or duplicate data.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# What the agent can and can't do - important to set boundaries
# This is NOT a doctor, just educational

AGENT_CAPABILITIES = {
    "can_do": [
        "Identify patterns in symptoms and lifestyle",
        "Explain biochemical mechanisms in simple language",
        "Suggest nutrient deficiencies based on symptoms",
        "Recommend lifestyle changes (diet, sleep, exercise)",
        "Suggest supplements with dosages (educational only)",
        "Guide physical self-examination (non-invasive)",
        "Recommend which medical specialist to consult",
        "Track symptom changes over time",
        "Provide health education in Dr. Berg's style"
    ],
    
    "cannot_do": [
        "Diagnose medical conditions (only licensed doctors can diagnose)",
        "Prescribe medications (only medical doctors can prescribe)",
        "Replace medical care or professional diagnosis",
        "Interpret lab results definitively (guide to specialist instead)",
        "Provide emergency medical advice (call 911)",
        "Treat acute medical emergencies",
        "Override doctor's recommendations",
        "Guarantee outcomes or results",
        "Practice medicine or act as doctor"
    ],
    
    "must_escalate_when": [
        "Red flag symptoms detected (chest pain, severe headache, etc.)",
        "Symptoms suggest serious condition (cancer, heart disease, etc.)",
        "Patient has emergency symptoms",
        "Symptoms worsen despite interventions",
        "Lab results show abnormal values outside reference range",
        "Patient is pregnant or breastfeeding (different protocols)",
        "Patient has serious medical conditions (kidney disease, etc.)",
        "Symptoms persist beyond 8-12 weeks without improvement",
        "Confidence in assessment is low (<60%)",
        "Patient needs prescription medication",
        "Surgical evaluation may be needed"
    ]
}

MEDICAL_DISCLAIMER = """
⚠️ IMPORTANT MEDICAL DISCLAIMER ⚠️

I am an AI health education agent, NOT a licensed medical professional.

What I provide:
✓ Health education and information
✓ Nutritional guidance and lifestyle suggestions
✓ Help identifying potential nutrient deficiencies
✓ Recommendations for which specialist to consult

What I CANNOT provide:
✗ Medical diagnosis (only doctors can diagnose)
✗ Prescription medications
✗ Emergency medical care
✗ Replacement for professional medical advice

When in doubt, always consult a licensed healthcare professional.
If you have emergency symptoms, call 911 immediately.
"""


# Red flags - these need immediate medical attention
# Using urgency levels so the agent knows when to escalate

class UrgencyLevel(Enum):
    EMERGENCY_911 = "emergency_911"  # Call 911 immediately
    URGENT_24HR = "urgent_24hr"      # See doctor within 24 hours
    SOON_1WEEK = "soon_1week"        # Schedule appointment within 1 week
    ROUTINE = "routine"               # Schedule regular appointment
    MONITOR = "monitor"               # Watch and track symptoms

@dataclass
class RedFlag:
    symptom: str
    urgency: UrgencyLevel
    reason: str
    action: str
    specialist: Optional[str] = None

RED_FLAGS = [
    # EMERGENCY - Call 911
    RedFlag(
        symptom="Chest pain or pressure, especially radiating to arm/jaw",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible heart attack (myocardial infarction)",
        action="🚨 CALL 911 IMMEDIATELY. Do not drive yourself. This could be life-threatening.",
        specialist="Emergency Department → Cardiologist"
    ),
    RedFlag(
        symptom="Sudden severe headache (worst of your life)",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible brain aneurysm, stroke, or hemorrhage",
        action="🚨 CALL 911 IMMEDIATELY. This could be a stroke or aneurysm.",
        specialist="Emergency Department → Neurologist"
    ),
    RedFlag(
        symptom="Difficulty breathing or shortness of breath at rest",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible heart failure, pulmonary embolism, or severe respiratory issue",
        action="🚨 CALL 911 IMMEDIATELY. Breathing difficulty is life-threatening.",
        specialist="Emergency Department → Pulmonologist or Cardiologist"
    ),
    RedFlag(
        symptom="Sudden weakness, numbness, or paralysis on one side of body",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible stroke (cerebrovascular accident)",
        action="🚨 CALL 911 IMMEDIATELY. Time is critical in stroke treatment (tPA window is 3-4.5 hours).",
        specialist="Emergency Department → Neurologist"
    ),
    RedFlag(
        symptom="Confusion, disorientation, loss of consciousness",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible stroke, brain injury, severe metabolic issue, or infection",
        action="🚨 CALL 911 IMMEDIATELY. Altered mental status is a medical emergency.",
        specialist="Emergency Department"
    ),
    RedFlag(
        symptom="Severe abdominal pain (sudden, intense, or with vomiting blood)",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible appendicitis, ruptured organ, internal bleeding, or perforation",
        action="🚨 GO TO EMERGENCY ROOM IMMEDIATELY. Do not eat or drink.",
        specialist="Emergency Department → General Surgeon or Gastroenterologist"
    ),
    RedFlag(
        symptom="Coughing up blood or blood in vomit",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Possible GI bleed, lung issue, or vascular problem",
        action="🚨 GO TO EMERGENCY ROOM IMMEDIATELY.",
        specialist="Emergency Department → Gastroenterologist or Pulmonologist"
    ),
    RedFlag(
        symptom="Suicidal thoughts or intent to harm self/others",
        urgency=UrgencyLevel.EMERGENCY_911,
        reason="Psychiatric emergency requiring immediate intervention",
        action="🚨 CALL 911 or National Suicide Prevention Lifeline: 988. You are not alone.",
        specialist="Emergency Department → Psychiatrist"
    ),
    
    # URGENT - See doctor within 24 hours
    RedFlag(
        symptom="Unexplained weight loss (>10 lbs in month without trying)",
        urgency=UrgencyLevel.URGENT_24HR,
        reason="Possible cancer, thyroid disorder, diabetes, or serious metabolic issue",
        action="⚠️ See doctor within 24 hours. This requires immediate evaluation.",
        specialist="Primary Care → Endocrinologist or Oncologist"
    ),
    RedFlag(
        symptom="Persistent high fever (>103°F or lasting >3 days)",
        urgency=UrgencyLevel.URGENT_24HR,
        reason="Possible serious infection requiring antibiotics or hospitalization",
        action="⚠️ See doctor within 24 hours. Fever this high/long needs evaluation.",
        specialist="Primary Care → Infectious Disease (if complicated)"
    ),
    RedFlag(
        symptom="Sudden vision changes or loss",
        urgency=UrgencyLevel.URGENT_24HR,
        reason="Possible retinal detachment, stroke, or serious eye condition",
        action="⚠️ See ophthalmologist or go to ER within 24 hours.",
        specialist="Ophthalmologist"
    ),
    RedFlag(
        symptom="New lump or mass, especially if growing or painful",
        urgency=UrgencyLevel.URGENT_24HR,
        reason="Needs evaluation to rule out cancer",
        action="⚠️ See doctor within 24-48 hours for evaluation and possible biopsy.",
        specialist="Primary Care → Oncologist or Surgeon"
    ),
    RedFlag(
        symptom="Black or bloody stools (melena or hematochezia)",
        urgency=UrgencyLevel.URGENT_24HR,
        reason="Possible GI bleeding from ulcer, polyp, or cancer",
        action="⚠️ See doctor within 24 hours. GI bleeding requires urgent evaluation.",
        specialist="Gastroenterologist"
    ),
    
    # SOON - Within 1 week
    RedFlag(
        symptom="Persistent pain lasting >2 weeks without improvement",
        urgency=UrgencyLevel.SOON_1WEEK,
        reason="Chronic pain may indicate underlying condition needing treatment",
        action="Schedule appointment within 1 week for evaluation.",
        specialist="Primary Care → Pain Specialist (depending on location)"
    ),
    RedFlag(
        symptom="New or changing mole (irregular border, color changes, growing)",
        urgency=UrgencyLevel.SOON_1WEEK,
        reason="Possible melanoma or skin cancer",
        action="See dermatologist within 1 week. Skin cancer is highly treatable if caught early.",
        specialist="Dermatologist"
    ),
    RedFlag(
        symptom="Persistent cough >3 weeks or worsening",
        urgency=UrgencyLevel.SOON_1WEEK,
        reason="Could be infection, asthma, COPD, or rarely lung cancer",
        action="See doctor within 1 week, especially if smoker or former smoker.",
        specialist="Primary Care → Pulmonologist"
    ),
]


# ============================================================================
# MEDICAL SPECIALTIES - Who to See for What
# ============================================================================

@dataclass
class MedicalSpecialty:
    name: str
    description: str
    treats_conditions: List[str]
    common_symptoms: List[str]
    when_to_see: str
    typical_tests: List[str]

MEDICAL_SPECIALTIES = {
    "endocrinologist": MedicalSpecialty(
        name="Endocrinologist",
        description="Hormone and metabolic disorders specialist",
        treats_conditions=[
            "Thyroid disorders (hypothyroidism, hyperthyroidism, Hashimoto's, Graves')",
            "Diabetes (Type 1, Type 2, prediabetes)",
            "Adrenal disorders (Addison's, Cushing's, adrenal fatigue)",
            "Pituitary disorders",
            "Metabolic syndrome",
            "PCOS (Polycystic Ovary Syndrome)",
            "Hormone imbalances",
            "Osteoporosis",
            "Growth disorders"
        ],
        common_symptoms=[
            "Unexplained weight gain or loss",
            "Extreme fatigue despite rest",
            "Heat or cold intolerance",
            "Hair loss (especially outer eyebrows)",
            "Irregular periods or fertility issues",
            "Excessive thirst or urination",
            "Mood swings or depression linked to hormones",
            "Low libido",
            "Brain fog and poor concentration",
            "Brittle bones or frequent fractures"
        ],
        when_to_see="If you suspect hormone imbalance, thyroid issues, diabetes, or metabolic problems. Especially if basic blood tests show abnormalities in TSH, glucose, or hormones.",
        typical_tests=["TSH, T3, T4, Thyroid antibodies", "Fasting glucose, HbA1c, insulin", "Cortisol", "Sex hormones (estrogen, testosterone, progesterone)", "DHEA, IGF-1"]
    ),
    
    "gastroenterologist": MedicalSpecialty(
        name="Gastroenterologist (GI Doctor)",
        description="Digestive system and gut health specialist",
        treats_conditions=[
            "IBS (Irritable Bowel Syndrome)",
            "IBD (Crohn's, Ulcerative Colitis)",
            "GERD (Acid Reflux)",
            "Celiac disease",
            "Food intolerances",
            "Liver disease (fatty liver, cirrhosis, hepatitis)",
            "Gallbladder disease",
            "Pancreatitis",
            "Ulcers",
            "Colon polyps or cancer screening"
        ],
        common_symptoms=[
            "Chronic bloating or gas",
            "Abdominal pain or cramping",
            "Diarrhea or constipation (especially alternating)",
            "Blood in stool",
            "Severe acid reflux or heartburn",
            "Nausea or vomiting",
            "Unexplained weight loss with digestive issues",
            "Food sensitivities or reactions",
            "Yellowing of skin (jaundice)",
            "Difficulty swallowing"
        ],
        when_to_see="If digestive issues persist >2-4 weeks, interfere with daily life, or if you have blood in stool, severe pain, or jaundice.",
        typical_tests=["Colonoscopy", "Endoscopy", "Stool tests", "Breath tests (SIBO, lactose)", "Liver function tests", "H. pylori test", "Celiac panel"]
    ),
    
    "cardiologist": MedicalSpecialty(
        name="Cardiologist",
        description="Heart and cardiovascular system specialist",
        treats_conditions=[
            "High blood pressure (hypertension)",
            "Coronary artery disease",
            "Heart failure",
            "Arrhythmias (irregular heartbeat)",
            "Heart valve problems",
            "Peripheral artery disease",
            "High cholesterol",
            "Cardiomyopathy"
        ],
        common_symptoms=[
            "Chest pain or pressure",
            "Shortness of breath",
            "Irregular or racing heartbeat (palpitations)",
            "Swelling in legs or feet",
            "Dizziness or fainting",
            "Fatigue with exertion",
            "High blood pressure readings"
        ],
        when_to_see="If you have chest pain, irregular heartbeat, family history of heart disease, or high blood pressure/cholesterol that's hard to control.",
        typical_tests=["EKG", "Echocardiogram", "Stress test", "Holter monitor", "Cardiac catheterization", "Lipid panel", "BNP"]
    ),
    
    "dermatologist": MedicalSpecialty(
        name="Dermatologist",
        description="Skin, hair, and nail specialist",
        treats_conditions=[
            "Acne",
            "Eczema and psoriasis",
            "Rosacea",
            "Skin cancer (melanoma, basal cell, squamous cell)",
            "Hair loss (alopecia)",
            "Nail disorders",
            "Fungal infections",
            "Warts and moles",
            "Aging skin concerns"
        ],
        common_symptoms=[
            "New or changing moles",
            "Persistent rash or itching",
            "Severe or cystic acne",
            "Hair loss or thinning",
            "Nail changes (discoloration, thickening)",
            "Suspicious skin lesions",
            "Chronic skin dryness or flaking",
            "Red, inflamed skin"
        ],
        when_to_see="For skin concerns that don't improve with over-the-counter treatments, any suspicious moles, severe acne, or hair loss.",
        typical_tests=["Skin biopsy", "Patch testing (allergies)", "Dermoscopy", "Fungal cultures"]
    ),
    
    "neurologist": MedicalSpecialty(
        name="Neurologist",
        description="Brain, spinal cord, and nervous system specialist",
        treats_conditions=[
            "Migraines and headaches",
            "Epilepsy and seizures",
            "Multiple sclerosis (MS)",
            "Parkinson's disease",
            "Neuropathy",
            "Stroke and TIA",
            "Dementia and Alzheimer's",
            "Brain tumors",
            "Movement disorders"
        ],
        common_symptoms=[
            "Severe or frequent headaches",
            "Numbness or tingling in extremities",
            "Weakness or paralysis",
            "Tremors or involuntary movements",
            "Seizures",
            "Memory problems or confusion",
            "Dizziness or vertigo",
            "Vision problems (double vision, etc.)"
        ],
        when_to_see="For severe headaches, numbness/tingling, seizures, memory issues, or any neurological symptoms.",
        typical_tests=["MRI or CT scan", "EEG", "EMG (nerve conduction)", "Lumbar puncture", "Neuropsych testing"]
    ),
    
    "rheumatologist": MedicalSpecialty(
        name="Rheumatologist",
        description="Autoimmune and joint disease specialist",
        treats_conditions=[
            "Rheumatoid arthritis",
            "Lupus (SLE)",
            "Fibromyalgia",
            "Sjogren's syndrome",
            "Ankylosing spondylitis",
            "Psoriatic arthritis",
            "Gout",
            "Vasculitis",
            "Polymyalgia rheumatica"
        ],
        common_symptoms=[
            "Joint pain and swelling (especially multiple joints)",
            "Morning stiffness >30 minutes",
            "Fatigue with joint pain",
            "Autoimmune symptoms (rashes, mouth sores)",
            "Muscle pain and weakness",
            "Unexplained fevers",
            "Raynaud's phenomenon (fingers turn white/blue in cold)"
        ],
        when_to_see="If joint pain persists >6 weeks, affects multiple joints, or if you suspect autoimmune disease.",
        typical_tests=["ANA (antinuclear antibody)", "Rheumatoid factor", "Anti-CCP", "ESR and CRP (inflammation)", "Joint X-rays or ultrasound"]
    ),
    
    "psychiatrist": MedicalSpecialty(
        name="Psychiatrist",
        description="Mental health and psychiatric medication specialist (MD)",
        treats_conditions=[
            "Depression (major depressive disorder)",
            "Anxiety disorders (GAD, panic, social anxiety)",
            "Bipolar disorder",
            "Schizophrenia",
            "PTSD",
            "OCD",
            "ADHD",
            "Eating disorders",
            "Substance use disorders"
        ],
        common_symptoms=[
            "Persistent sadness or hopelessness",
            "Anxiety or panic attacks",
            "Mood swings",
            "Difficulty concentrating",
            "Insomnia or hypersomnia",
            "Loss of interest in activities",
            "Suicidal thoughts",
            "Hallucinations or delusions",
            "Substance abuse"
        ],
        when_to_see="If mental health symptoms interfere with daily life, or if you need psychiatric medication management. For therapy without medication, see a psychologist or therapist.",
        typical_tests=["Psychiatric evaluation", "Mental status exam", "Screening questionnaires (PHQ-9, GAD-7)", "Sometimes: thyroid tests, vitamin B12, other labs to rule out medical causes"]
    ),
    
    "hematologist": MedicalSpecialty(
        name="Hematologist",
        description="Blood disorder specialist",
        treats_conditions=[
            "Anemia (iron deficiency, B12 deficiency, etc.)",
            "Clotting disorders (hemophilia, Factor V Leiden)",
            "Blood cancers (leukemia, lymphoma, myeloma)",
            "Thrombocytopenia (low platelets)",
            "Polycythemia (high red blood cells)",
            "Sickle cell disease",
            "Thalassemia"
        ],
        common_symptoms=[
            "Severe or persistent anemia",
            "Easy bruising or bleeding",
            "Frequent infections",
            "Swollen lymph nodes",
            "Bone pain",
            "Unexplained blood clots",
            "Fatigue with abnormal blood counts"
        ],
        when_to_see="If blood tests show significant abnormalities (very low hemoglobin, abnormal white cell count, etc.) or bleeding/clotting issues.",
        typical_tests=["CBC", "Iron panel", "B12 and folate", "Coagulation studies", "Bone marrow biopsy", "Flow cytometry"]
    ),
    
    "primary_care": MedicalSpecialty(
        name="Primary Care Physician (PCP)",
        description="Your first point of contact for general health concerns",
        treats_conditions=[
            "General health checkups",
            "Acute illnesses (colds, flu, infections)",
            "Chronic disease management (diabetes, hypertension)",
            "Preventive care (vaccines, screenings)",
            "Minor injuries",
            "Common skin issues",
            "Referrals to specialists"
        ],
        common_symptoms=[
            "General unwellness",
            "Fever or infection",
            "New health concern (unclear cause)",
            "Routine checkup needed",
            "Multiple symptoms (unclear which specialist)"
        ],
        when_to_see="Start here for most health concerns. Your PCP can evaluate and refer to specialists if needed.",
        typical_tests=["Basic blood work (CBC, CMP)", "Urinalysis", "Blood pressure", "Physical exam"]
    ),
}


# ============================================================================
# SYMPTOM TO SPECIALTY ROUTING
# ============================================================================

def route_to_specialist(symptoms: List[str], patient_context: Dict) -> List[Dict]:
    """
    Intelligent routing: Given symptoms, recommend which specialist(s) to see.
    
    Args:
        symptoms: List of patient symptoms
        patient_context: Additional context (age, sex, duration, severity)
    
    Returns:
        List of specialist recommendations with reasoning
    """
    
    recommendations = []
    
    # Symptom pattern matching to specialties
    symptom_routing = {
        # Endocrine symptoms
        ("fatigue", "weight_gain", "cold_intolerance", "hair_loss"): {
            "specialist": "endocrinologist",
            "reason": "Pattern suggests thyroid disorder (hypothyroidism)",
            "confidence": 0.85
        },
        ("weight_loss", "excessive_thirst", "frequent_urination"): {
            "specialist": "endocrinologist",
            "reason": "Pattern suggests diabetes",
            "confidence": 0.90
        },
        
        # GI symptoms
        ("bloating", "abdominal_pain", "diarrhea", "constipation"): {
            "specialist": "gastroenterologist",
            "reason": "Digestive symptoms suggest GI disorder (IBS, IBD, etc.)",
            "confidence": 0.80
        },
        
        # Cardiac symptoms
        ("chest_pain", "shortness_of_breath", "palpitations"): {
            "specialist": "cardiologist",
            "reason": "Cardiac symptoms require heart evaluation",
            "confidence": 0.95
        },
        
        # Skin symptoms
        ("rash", "skin_changes", "mole_changes"): {
            "specialist": "dermatologist",
            "reason": "Skin issues require dermatological evaluation",
            "confidence": 0.85
        },
        
        # Neurological symptoms
        ("headache", "numbness", "tingling", "weakness"): {
            "specialist": "neurologist",
            "reason": "Neurological symptoms suggest nervous system involvement",
            "confidence": 0.80
        },
        
        # Rheumatologic symptoms
        ("joint_pain", "multiple_joint_swelling", "morning_stiffness"): {
            "specialist": "rheumatologist",
            "reason": "Multiple joint involvement suggests autoimmune or inflammatory arthritis",
            "confidence": 0.85
        },
        
        # Mental health symptoms
        ("depression", "anxiety", "mood_swings", "panic_attacks"): {
            "specialist": "psychiatrist",
            "reason": "Mental health symptoms may benefit from psychiatric evaluation and medication",
            "confidence": 0.80
        },
    }
    
    # Check for pattern matches
    symptom_set = set(symptoms)
    for pattern, specialist_info in symptom_routing.items():
        if set(pattern).issubset(symptom_set):
            recommendations.append(specialist_info)
    
    # If no clear match, recommend starting with Primary Care
    if not recommendations:
        recommendations.append({
            "specialist": "primary_care",
            "reason": "Symptoms don't match a clear specialty pattern. Start with Primary Care for evaluation and potential referral.",
            "confidence": 0.70
        })
    
    return recommendations


# ============================================================================
# KNOWLEDGE BASE VALIDATION
# ============================================================================

def validate_recommendation_confidence(
    symptoms: List[str],
    assessment: Dict,
    patient_history: Optional[Dict] = None
) -> Dict:
    """
    Calculate confidence score for recommendations.
    
    Returns:
        {
            "confidence_score": 0.0-1.0,
            "reliability": "high" | "medium" | "low",
            "should_see_doctor": bool,
            "reason": str
        }
    """
    
    confidence_score = 0.5  # Start at neutral
    factors = []
    
    # Increase confidence if:
    # - Multiple consistent symptoms
    if len(symptoms) >= 3:
        confidence_score += 0.1
        factors.append("Multiple symptoms provide clearer pattern")
    
    # - Clear pattern match to known condition
    if assessment.get("pattern_match_strength", 0) > 0.8:
        confidence_score += 0.2
        factors.append("Strong pattern match to known condition")
    
    # - Patient history supports assessment
    if patient_history:
        confidence_score += 0.1
        factors.append("Patient history supports assessment")
    
    # Decrease confidence if:
    # - Vague symptoms
    vague_symptoms = ["tired", "feel_bad", "unwell"]
    if any(s in vague_symptoms for s in symptoms):
        confidence_score -= 0.2
        factors.append("Symptoms are vague and nonspecific")
    
    # - Red flags present
    if assessment.get("red_flags_present"):
        confidence_score = 0.3  # Low confidence, needs medical eval
        factors.append("Red flags require professional evaluation")
    
    # - Duration very short (<1 week)
    if assessment.get("duration_days", 7) < 7:
        confidence_score -= 0.1
        factors.append("Short duration makes assessment less certain")
    
    # Cap between 0 and 1
    confidence_score = max(0.0, min(1.0, confidence_score))
    
    # Determine reliability
    if confidence_score >= 0.75:
        reliability = "high"
    elif confidence_score >= 0.50:
        reliability = "medium"
    else:
        reliability = "low"
    
    # Should see doctor?
    should_see_doctor = (
        confidence_score < 0.60 or
        assessment.get("red_flags_present", False) or
        assessment.get("no_improvement_8weeks", False)
    )
    
    return {
        "confidence_score": round(confidence_score, 2),
        "reliability": reliability,
        "should_see_doctor": should_see_doctor,
        "factors": factors,
        "recommendation": _get_confidence_recommendation(confidence_score, reliability)
    }


def _get_confidence_recommendation(score: float, reliability: str) -> str:
    """Generate recommendation based on confidence"""
    
    if score >= 0.75:
        return (
            "High confidence in assessment. Recommendations are well-supported by symptom pattern. "
            "However, if symptoms persist or worsen, consult a healthcare professional."
        )
    elif score >= 0.50:
        return (
            "Moderate confidence in assessment. Recommendations are reasonable based on symptoms. "
            "Monitor your progress and see a doctor if no improvement in 4-6 weeks."
        )
    else:
        return (
            "Low confidence in assessment. Symptoms require professional medical evaluation. "
            "I recommend seeing a doctor for proper diagnosis. My suggestions are educational only."
        )


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'AGENT_CAPABILITIES',
    'MEDICAL_DISCLAIMER',
    'RED_FLAGS',
    'MEDICAL_SPECIALTIES',
    'SPECIALTIES',
    'UrgencyLevel',
    'route_to_specialist',
    'validate_recommendation_confidence',
]

# Alias for backward compatibility
SPECIALTIES = MEDICAL_SPECIALTIES
