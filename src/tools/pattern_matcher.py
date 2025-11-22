"""
Pattern Matching Tools
Core logic for identifying health patterns from user health profiles
"""

from src.tools.health_patterns import HEALTH_PATTERNS, get_all_patterns
from typing import Dict, List, Tuple

def match_health_patterns(health_profile: Dict) -> List[Dict]:
    """
    Match a user's health profile against known health patterns.
    
    Args:
        health_profile: Dict with keys like sleep_hours, mood_score, diet_type, exercise_mins, etc.
        
    Returns:
        List of matching patterns sorted by match confidence (highest first)
    """
    
    matches = []
    
    for pattern in get_all_patterns():
        # Calculate match score based on how many indicators are present
        indicators = pattern.get("indicators", [])
        severity_factors = pattern.get("severity_factors", {})
        
        match_score = 0.0
        indicators_matched = 0
        
        # Check each indicator
        for indicator in indicators:
            if _check_indicator_present(health_profile, indicator):
                match_score += 1.0
                indicators_matched += 1
        
        # Apply severity factors to increase match score
        for factor_key, factor_weight in severity_factors.items():
            if _check_severity_factor(health_profile, factor_key):
                match_score += factor_weight
        
        # Only include if we matched at least one indicator
        if indicators_matched > 0:
            confidence = indicators_matched / len(indicators) if indicators else 0
            matches.append({
                "pattern_id": pattern["id"],
                "pattern_name": pattern["name"],
                "match_score": match_score,
                "confidence": confidence,
                "indicators_matched": indicators_matched,
                "total_indicators": len(indicators),
                "explanation": pattern["explanation"],
                "recommendation": pattern["recommendation"],
                "timeline": pattern["timeline"]
            })
    
    # Sort by match score (highest first)
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Return top matches only
    return matches[:5]  # Top 5 matches


def _check_indicator_present(health_profile: Dict, indicator: str) -> bool:
    """Check if a health indicator is present in the user's profile"""
    
    indicator_checks = {
        "fatigue": lambda h: h.get("energy_level") == "low" or h.get("sleep_hours", 0) > 7,
        "low_mood": lambda h: h.get("mood_score", 5) < 5,
        "depression": lambda h: h.get("mood_score", 5) < 3,
        "anxiety": lambda h: h.get("anxiety_level", 0) > 5,
        "poor_sleep": lambda h: h.get("sleep_hours", 0) < 7,
        "brain_fog": lambda h: h.get("mental_clarity", 5) < 4,
        "weak_immune": lambda h: h.get("infections_per_year", 0) > 2,
        "muscle_weakness": lambda h: h.get("exercise_mins_per_week", 0) == 0,
        "weak_bones": lambda h: h.get("age", 30) > 50,
        "hair_loss": lambda h: h.get("hair_loss", False),
        "dry_skin": lambda h: h.get("skin_condition") == "dry",
        "joint_pain": lambda h: h.get("joint_pain", False),
        "muscle_tension": lambda h: h.get("muscle_tension", False),
        "irritability": lambda h: h.get("mood_score", 5) < 4,
        "mood_swings": lambda h: h.get("mood_stability", 5) < 3,
        "digestive_issues": lambda h: h.get("digestion", "normal") != "normal",
        "bloating": lambda h: h.get("bloating", False),
        "low_energy": lambda h: h.get("energy_level") == "low",
        "shortness_of_breath": lambda h: h.get("breathlessness", False),
        "dizziness": lambda h: h.get("dizziness", False),
        "weak_nails": lambda h: h.get("nail_health") == "poor",
        "pale_skin": lambda h: h.get("skin_tone") == "pale",
        "racing_heart": lambda h: h.get("heart_palpitations", False),
        "jittery": lambda h: h.get("jittery", False),
        "slow_wound_healing": lambda h: h.get("wound_healing") == "slow",
        "frequent_infections": lambda h: h.get("infections_per_year", 0) > 3,
        "afternoon_fatigue": lambda h: h.get("energy_pattern") == "crash_afternoon",
        "energy_crashes": lambda h: h.get("energy_pattern") == "crash_afternoon",
        "cravings": lambda h: h.get("sugar_cravings", False),
        "weight_gain": lambda h: h.get("recent_weight_change", "stable") == "gained",
        "slow_recovery": lambda h: h.get("exercise_recovery", "normal") == "slow",
        "headaches": lambda h: h.get("headaches", 0) > 2,
        "food_sensitivities": lambda h: h.get("food_sensitivities", False),
        "irregular_heartbeat": lambda h: h.get("heart_irregularities", False),
        "cold_sensitivity": lambda h: h.get("temperature_sensitivity") == "cold",
        "period_issues": lambda h: h.get("menstrual_regularity", "regular") != "regular",
        "low_libido": lambda h: h.get("libido", "normal") == "low",
        "slow_metabolism": lambda h: h.get("metabolism", "normal") == "slow",
        "tooth_issues": lambda h: h.get("tooth_health") == "poor",
    }
    
    if indicator in indicator_checks:
        try:
            return indicator_checks[indicator](health_profile)
        except:
            return False
    
    return False


def _check_severity_factor(health_profile: Dict, factor: str) -> bool:
    """Check if a severity factor is present"""
    
    factor_checks = {
        "sun_exposure_low": lambda h: h.get("sun_exposure", "moderate") == "low",
        "indoor_lifestyle": lambda h: h.get("lifestyle_type", "mixed") == "indoor",
        "dark_skin_tone": lambda h: h.get("skin_tone") == "dark",
        "diet_low_fish": lambda h: h.get("fish_intake", "moderate") == "low",
        "sleep_hours_low": lambda h: h.get("sleep_hours", 7) < 7,
        "stress_high": lambda h: h.get("stress_level", 5) > 6,
        "caffeine_high": lambda h: h.get("caffeine_cups_per_day", 0) > 3,
        "caffeine_after_2pm": lambda h: h.get("caffeine_after_2pm", False),
        "processed_diet": lambda h: h.get("diet_type", "mixed") == "processed",
        "vegetarian_diet": lambda h: h.get("diet_type", "mixed") == "vegetarian",
        "no_exercise": lambda h: h.get("exercise_mins_per_week", 0) == 0,
        "irregular_sleep": lambda h: h.get("sleep_consistency", "regular") == "irregular",
        "screen_before_bed": lambda h: h.get("screen_before_bed", False),
        "no_routine": lambda h: h.get("daily_routine", "structured") == "unstructured",
        "high_omega6_diet": lambda h: h.get("omega_ratio") == "high_omega6",
        "no_fish_intake": lambda h: h.get("fish_intake", "moderate") == "none",
        "low_protein_diet": lambda h: h.get("protein_intake", "moderate") == "low",
        "high_carb_diet": lambda h: h.get("carb_ratio", "moderate") == "high",
        "insufficient_protein": lambda h: h.get("protein_intake", "moderate") == "low",
        "high_sugar_intake": lambda h: h.get("sugar_intake", "moderate") == "high",
        "water_intake_low": lambda h: h.get("water_glasses_per_day", 8) < 6,
        "exercise_without_hydration": lambda h: h.get("exercise_hydration", "good") == "poor",
        "dry_climate": lambda h: h.get("climate", "temperate") == "dry",
        "antibiotic_history": lambda h: h.get("recent_antibiotics", False),
        "low_fiber": lambda h: h.get("fiber_intake", "moderate") == "low",
        "high_caffeine": lambda h: h.get("caffeine_cups_per_day", 0) > 3,
        "vitamin_d_deficiency": lambda h: h.get("sun_exposure", "moderate") == "low",
        "iodine_deficiency": lambda h: h.get("sea_vegetable_intake", "low") == "low",
        "selenium_deficiency": lambda h: h.get("brazil_nut_intake", "low") == "low",
        "female": lambda h: h.get("gender", "other") == "female",
        "age_over_50": lambda h: h.get("age", 0) > 50,
        "heavy_periods": lambda h: h.get("menstrual_flow", "normal") == "heavy",
        "alcohol_use": lambda h: h.get("alcohol_drinks_per_week", 0) > 2,
        "desk_job": lambda h: h.get("job_type", "mixed") == "desk",
        "high_screen_time": lambda h: h.get("screen_hours_per_day", 0) > 8,
        "low_fat_diet": lambda h: h.get("fat_intake", "moderate") == "low",
        "sedentary": lambda h: h.get("exercise_mins_per_week", 0) < 150,
        "vegetable_intake_low": lambda h: h.get("vegetable_servings_per_day", 0) < 3,
        "whole_food_intake_low": lambda h: h.get("processed_food_percentage", 50) > 70,
        "work_stress_high": lambda h: h.get("work_stress", 5) > 7,
        "no_relaxation": lambda h: h.get("relaxation_minutes_per_day", 0) < 10,
        "isolation": lambda h: h.get("social_connection", "good") == "poor",
        "dairy_free_diet": lambda h: h.get("dairy_intake", "regular") == "none",
    }
    
    if factor in factor_checks:
        try:
            return factor_checks[factor](health_profile)
        except:
            return False
    
    return False


def find_correlations(health_profile: Dict, matched_patterns: List[Dict]) -> List[Dict]:
    """
    Find correlations between health issues.
    
    For example: "Low sleep + low mood + poor magnesium = all connected"
    
    Args:
        health_profile: User's health profile
        matched_patterns: Patterns already identified
        
    Returns:
        List of correlation insights
    """
    
    correlations = []
    
    # Common correlation patterns
    if health_profile.get("sleep_hours", 0) < 7 and health_profile.get("mood_score", 5) < 5:
        correlations.append({
            "correlation": "Sleep ↔ Mood",
            "insight": "Poor sleep directly causes mood issues. This likely creates a cycle where bad mood leads to poor sleep.",
            "actions": ["Prioritize 7-9 hours sleep", "Focus on sleep quality first"]
        })
    
    if health_profile.get("exercise_mins_per_week", 0) == 0 and health_profile.get("energy_level") == "low":
        correlations.append({
            "correlation": "Exercise ↔ Energy",
            "insight": "Sedentary lifestyle causes low energy, which makes it harder to exercise. Breaking this cycle is key.",
            "actions": ["Start with 15-min walks", "Exercise boosts energy more than rest"]
        })
    
    if health_profile.get("diet_type") == "processed" and health_profile.get("mood_score", 5) < 5:
        correlations.append({
            "correlation": "Diet ↔ Mental Health",
            "insight": "Processed foods lack nutrients and spike inflammation, directly affecting mood. Gut health = mental health.",
            "actions": ["Add whole foods gradually", "Include omega-3 foods"]
        })
    
    if health_profile.get("caffeine_cups_per_day", 0) > 3 and health_profile.get("sleep_hours", 0) < 7:
        correlations.append({
            "correlation": "Caffeine ↔ Sleep",
            "insight": "High caffeine intake prevents deep sleep even if you 'fall asleep.' This is a major energy killer.",
            "actions": ["Cut caffeine by 2pm", "Gradually reduce total caffeine intake"]
        })
    
    if health_profile.get("stress_level", 5) > 6 and health_profile.get("energy_level") == "low":
        correlations.append({
            "correlation": "Stress ↔ Fatigue",
            "insight": "Chronic stress keeps cortisol elevated, which exhausts your body even at rest.",
            "actions": ["Add relaxation daily", "Meditation even 10 mins helps"]
        })
    
    return correlations


def score_deficiency_severity(health_profile: Dict) -> Dict:
    """
    Score overall health status and specific deficiency severity.
    
    Returns a score from 1-10 indicating overall health concern level.
    """
    
    severity_points = 0
    
    # Sleep score (max 2 points)
    sleep_hours = health_profile.get("sleep_hours", 0)
    if sleep_hours < 5:
        severity_points += 2
    elif sleep_hours < 7:
        severity_points += 1
    
    # Mood score (max 2 points)
    mood = health_profile.get("mood_score", 5)
    if mood < 3:
        severity_points += 2
    elif mood < 5:
        severity_points += 1
    
    # Exercise score (max 1.5 points)
    exercise = health_profile.get("exercise_mins_per_week", 0)
    if exercise == 0:
        severity_points += 1.5
    elif exercise < 150:
        severity_points += 0.75
    
    # Diet score (max 1.5 points)
    if health_profile.get("diet_type") == "processed":
        severity_points += 1.5
    elif health_profile.get("diet_type") != "whole_food":
        severity_points += 0.75
    
    # Stress score (max 1 point)
    stress = health_profile.get("stress_level", 5)
    if stress > 7:
        severity_points += 1
    elif stress > 5:
        severity_points += 0.5
    
    # Sun exposure (max 1 point)
    if health_profile.get("sun_exposure") == "low":
        severity_points += 1
    
    # Cap at 10
    overall_severity = min(severity_points, 10)
    
    return {
        "overall_severity": round(overall_severity, 1),
        "severity_level": "Critical" if overall_severity > 7 else "Moderate" if overall_severity > 4 else "Mild",
        "primary_concerns": [p for p in _identify_primary_concerns(health_profile)],
        "urgency": "High" if overall_severity > 7 else "Medium" if overall_severity > 4 else "Low"
    }


def _identify_primary_concerns(health_profile: Dict) -> List[str]:
    """Identify the user's primary health concerns"""
    concerns = []
    
    if health_profile.get("energy_level") == "low":
        concerns.append("Energy and fatigue")
    if health_profile.get("mood_score", 5) < 5:
        concerns.append("Mood and mental health")
    if health_profile.get("sleep_hours", 0) < 7:
        concerns.append("Sleep quality")
    if health_profile.get("exercise_mins_per_week", 0) == 0:
        concerns.append("Physical activity")
    if health_profile.get("anxiety_level", 0) > 5:
        concerns.append("Anxiety")
    if health_profile.get("digestion", "normal") != "normal":
        concerns.append("Digestive health")
    if health_profile.get("stress_level", 5) > 6:
        concerns.append("Chronic stress")
    
    return concerns[:3]  # Return top 3 concerns
