"""
Health Patterns Database
20 common health issue patterns with indicators, causes, and recommendations
"""

HEALTH_PATTERNS = [
    {
        "id": 1,
        "name": "Vitamin D Deficiency",
        "indicators": ["fatigue", "low_mood", "depression", "weak_bones", "muscle_weakness"],
        "severity_factors": {
            "sun_exposure_low": 2.0,
            "indoor_lifestyle": 1.5,
            "dark_skin_tone": 1.5,
            "diet_low_fish": 1.0
        },
        "explanation": (
            "You spend most time indoors, limiting sun exposure. Vitamin D is synthesized from "
            "sunlight UV-B rays. Without sufficient sun exposure, vitamin D levels drop. "
            "Low vitamin D causes: fatigue, mood issues, weak immune function, poor bone health."
        ),
        "recommendation": {
            "supplement": "Vitamin D3",
            "dose": "2000-4000 IU",
            "timing": "With breakfast",
            "lifestyle": "Get 15-20 minutes of sunlight daily, preferably in morning"
        },
        "timeline": "3-4 weeks to feel improvement"
    },
    
    {
        "id": 2,
        "name": "Magnesium Deficiency",
        "indicators": ["poor_sleep", "anxiety", "muscle_tension", "low_mood", "irritability"],
        "severity_factors": {
            "sleep_hours_low": 2.0,
            "stress_high": 1.5,
            "caffeine_high": 1.5,
            "processed_diet": 1.0
        },
        "explanation": (
            "Poor sleep combined with high stress depletes magnesium, your body's relaxation mineral. "
            "High caffeine intake blocks magnesium absorption. Without enough magnesium, your nervous "
            "system stays activated, making sleep difficult and anxiety worse."
        ),
        "recommendation": {
            "supplement": "Magnesium Glycinate",
            "dose": "300-400mg",
            "timing": "At bedtime, away from calcium-rich foods",
            "lifestyle": "Reduce caffeine after 2pm, practice relaxation 30 mins before bed"
        },
        "timeline": "1-2 weeks for sleep improvement"
    },
    
    {
        "id": 3,
        "name": "B Vitamin Deficiency (Energy)",
        "indicators": ["fatigue", "brain_fog", "low_energy", "mood_issues", "weak_immune"],
        "severity_factors": {
            "processed_diet": 2.0,
            "vegetarian_diet": 1.5,
            "high_stress": 1.5,
            "no_exercise": 1.0
        },
        "explanation": (
            "Your diet is high in processed foods which are stripped of B vitamins during manufacturing. "
            "B vitamins are essential for converting food into energy. Without enough B vitamins, your "
            "mitochondria (energy factories) can't produce ATP efficiently, leading to constant fatigue."
        ),
        "recommendation": {
            "supplement": "B-Complex or B12 Methylcobalamin (if vegetarian)",
            "dose": "500-1000 mcg B12, or complete B-complex daily",
            "timing": "Morning with breakfast",
            "lifestyle": "Add whole grains, leafy greens, eggs to diet"
        },
        "timeline": "2-3 weeks for energy boost"
    },
    
    {
        "id": 4,
        "name": "Iron Deficiency (Low Energy)",
        "indicators": ["fatigue", "shortness_of_breath", "dizziness", "weak_nails", "pale_skin"],
        "severity_factors": {
            "vegetarian_diet": 2.0,
            "female": 1.5,  # Women lose blood monthly
            "heavy_periods": 2.0,
            "low_protein_diet": 1.5
        },
        "explanation": (
            "Iron is essential for carrying oxygen in your blood. Low iron means your cells don't get "
            "enough oxygen, causing fatigue. This is especially common in vegetarians (plant iron is "
            "less absorbable) and women with heavy periods."
        ),
        "recommendation": {
            "supplement": "Iron (Ferrous Bisglycinate or Heme Iron)",
            "dose": "15-25mg daily",
            "timing": "Morning on empty stomach, 2 hours before food",
            "lifestyle": "Eat iron-rich foods: red meat, spinach, beans. Take with Vitamin C for better absorption"
        },
        "timeline": "4-6 weeks for energy improvement"
    },
    
    {
        "id": 5,
        "name": "Zinc Deficiency (Weak Immunity)",
        "indicators": ["frequent_infections", "slow_wound_healing", "weak_immune", "hair_loss", "brain_fog"],
        "severity_factors": {
            "high_stress": 2.0,
            "vegetarian_diet": 1.5,
            "high_carb_diet": 1.0,
            "alcohol_use": 1.5
        },
        "explanation": (
            "Zinc is critical for immune function, wound healing, and brain function. Stress increases "
            "zinc excretion. Plant-based diets have less available zinc. Without enough zinc, your immune "
            "system weakens and you get sick more often."
        ),
        "recommendation": {
            "supplement": "Zinc Glycinate",
            "dose": "15-30mg daily",
            "timing": "With a meal",
            "lifestyle": "Reduce stress with meditation, eat shellfish/red meat for natural zinc"
        },
        "timeline": "2-3 weeks for immune improvement"
    },
    
    {
        "id": 6,
        "name": "Caffeine Sensitivity",
        "indicators": ["anxiety", "racing_heart", "sleep_disruption", "jittery", "digestive_issues"],
        "severity_factors": {
            "caffeine_intake_high": 2.0,
            "caffeine_after_2pm": 2.0,
            "sleep_hours_low": 1.5,
            "baseline_anxiety": 1.0
        },
        "explanation": (
            "Caffeine blocks adenosine receptors in your brain, which normally signal tiredness. "
            "Even small amounts of caffeine after 2pm can disrupt sleep 8+ hours later. Poor sleep "
            "makes you dependent on more caffeine, creating a vicious cycle."
        ),
        "recommendation": {
            "supplement": "L-Theanine (optional, calms caffeine)",
            "dose": "100-200mg with coffee if needed",
            "timing": "N/A",
            "lifestyle": "Cut off all caffeine by 2pm. Gradually reduce total caffeine intake over 1 week"
        },
        "timeline": "3-5 days to feel effects"
    },
    
    {
        "id": 7,
        "name": "Blood Sugar Dysregulation (Energy Crashes)",
        "indicators": ["afternoon_fatigue", "energy_crashes", "mood_swings", "cravings", "brain_fog"],
        "severity_factors": {
            "high_carb_diet": 2.0,
            "no_exercise": 1.5,
            "high_stress": 1.0,
            "insufficient_protein": 1.5
        },
        "explanation": (
            "High-carb meals without protein cause blood sugar spikes and crashes. When blood sugar "
            "crashes, your body releases stress hormones (adrenaline, cortisol) causing fatigue and "
            "mood swings. This creates cravings for more sugar to boost energy again."
        ),
        "recommendation": {
            "supplement": "Chromium (optional, aids glucose control)",
            "dose": "200-400 mcg daily",
            "timing": "Before meals",
            "lifestyle": "Add protein to every meal, reduce refined carbs, eat slowly, move after meals"
        },
        "timeline": "3-5 days for stabilized energy"
    },
    
    {
        "id": 8,
        "name": "Sleep Deprivation (Systemic Impact)",
        "indicators": ["fatigue", "low_mood", "weak_immune", "weight_gain", "poor_memory"],
        "severity_factors": {
            "sleep_hours_low": 2.0,
            "irregular_sleep": 1.5,
            "screen_before_bed": 1.0,
            "no_routine": 1.0
        },
        "explanation": (
            "When you sleep less than 7 hours, your entire body suffers: immune system weakens, "
            "metabolism slows, mood tanks, memory suffers. Sleep is when your brain detoxifies and "
            "hormones regulate. Chronic sleep deprivation is linked to every major disease."
        ),
        "recommendation": {
            "supplement": "Magnesium (see pattern 2), Melatonin (if extremely sleep deprived)",
            "dose": "0.5-3mg melatonin 30 mins before bed",
            "timing": "30 minutes before target sleep time",
            "lifestyle": "Set consistent bedtime, dim lights 2 hours before bed, no screens 1 hour before"
        },
        "timeline": "1-2 weeks for noticeable sleep improvement"
    },
    
    {
        "id": 9,
        "name": "Omega-3 Deficiency (Mood & Inflammation)",
        "indicators": ["depression", "low_mood", "joint_pain", "dry_skin", "brain_fog"],
        "severity_factors": {
            "processed_diet": 2.0,
            "vegetarian_diet": 1.5,
            "no_fish_intake": 1.5,
            "high_omega6_diet": 1.0
        },
        "explanation": (
            "Omega-3 fats are building blocks for your brain and reduce inflammation. Modern diets are "
            "high in omega-6 (vegetable oils) and low in omega-3, causing systemic inflammation. This "
            "manifests as joint pain, brain fog, and depression."
        ),
        "recommendation": {
            "supplement": "Omega-3 (Fish Oil or Algae for vegetarians)",
            "dose": "1000-2000mg EPA+DHA daily",
            "timing": "With meals (fat-soluble)",
            "lifestyle": "Eat fatty fish 2-3x/week (salmon, sardines, mackerel) or add flaxseeds"
        },
        "timeline": "3-4 weeks for mood improvement"
    },
    
    {
        "id": 10,
        "name": "Chronic Stress (Cortisol Dysregulation)",
        "indicators": ["anxiety", "weight_gain", "insomnia", "weak_immune", "mood_swings"],
        "severity_factors": {
            "work_stress_high": 2.0,
            "no_exercise": 1.5,
            "poor_sleep": 1.5,
            "no_relaxation": 1.0
        },
        "explanation": (
            "Chronic stress keeps cortisol elevated 24/7. High cortisol causes: belly fat storage, "
            "muscle loss, poor sleep, weak immunity, anxiety. Unlike acute stress (which is survivable), "
            "chronic stress damages your health without recovery time."
        ),
        "recommendation": {
            "supplement": "Magnesium (pattern 2), Ashwagandha (stress adaptogen)",
            "dose": "300-500mg Ashwagandha daily",
            "timing": "With meals",
            "lifestyle": "Exercise 30 mins daily, meditate 10 mins daily, set work boundaries, take breaks"
        },
        "timeline": "2-3 weeks for stress reduction"
    },
    
    {
        "id": 11,
        "name": "Sedentary Lifestyle (Deconditioning)",
        "indicators": ["low_energy", "weight_gain", "poor_mood", "weak_immune", "early_aging"],
        "severity_factors": {
            "no_exercise": 3.0,
            "desk_job": 1.5,
            "sleep_issues": 1.0,
            "high_screen_time": 1.0
        },
        "explanation": (
            "Movement is medicine. Without exercise, your muscles atrophy, cardiovascular system weakens, "
            "mood plummets, and aging accelerates. Exercise improves every health marker: energy, sleep, "
            "mood, immunity, metabolism."
        ),
        "recommendation": {
            "supplement": "None required (exercise is the medicine)",
            "dose": "N/A",
            "timing": "N/A",
            "lifestyle": "Start with 20-30 mins walking daily, progress to strength training 2-3x/week"
        },
        "timeline": "1-2 weeks for energy boost, 8 weeks for visible changes"
    },
    
    {
        "id": 12,
        "name": "Processed Food Diet (Nutrient Deficiency)",
        "indicators": ["fatigue", "brain_fog", "weak_immune", "digestive_issues", "mood_issues"],
        "severity_factors": {
            "processed_diet_high": 2.0,
            "vegetable_intake_low": 1.5,
            "whole_food_intake_low": 1.5,
            "sugar_intake_high": 1.0
        },
        "explanation": (
            "Processed foods are stripped of nutrients and filled with additives. Your body doesn't "
            "recognize these as food, so nutrition is poor and inflammation is high. This creates "
            "deficiency in multiple micronutrients simultaneously."
        ),
        "recommendation": {
            "supplement": "High-quality multivitamin as temporary bridge",
            "dose": "Daily quality multivitamin",
            "timing": "With breakfast",
            "lifestyle": "Progressively replace processed foods with whole foods: vegetables, fruits, meat, fish"
        },
        "timeline": "2-3 weeks for noticeable improvement"
    },
    
    {
        "id": 13,
        "name": "Protein Deficiency (Low Energy & Muscle Loss)",
        "indicators": ["low_energy", "muscle_weakness", "hair_loss", "weak_immune", "slow_recovery"],
        "severity_factors": {
            "low_protein_intake": 2.0,
            "vegetarian_diet": 1.0,
            "no_exercise": 1.0,
            "high_carb_diet": 1.0
        },
        "explanation": (
            "Protein is needed to build and maintain muscle, which is your metabolic engine. Low protein "
            "causes muscle loss, slower metabolism, weak immunity, and poor recovery. Your body needs "
            "0.8-1g protein per pound of goal body weight."
        ),
        "recommendation": {
            "supplement": "Whey or Plant-Based Protein Powder (if struggling to hit targets)",
            "dose": "20-40g per serving, 1-2 servings daily",
            "timing": "After workouts or with meals",
            "lifestyle": "Add protein to every meal: eggs, fish, meat, legumes, dairy"
        },
        "timeline": "2-4 weeks for energy improvement"
    },
    
    {
        "id": 14,
        "name": "Dehydration (Fatigue & Brain Fog)",
        "indicators": ["fatigue", "headaches", "brain_fog", "dry_skin", "dark_urine"],
        "severity_factors": {
            "water_intake_low": 2.0,
            "high_caffeine": 1.0,
            "exercise_without_hydration": 1.5,
            "dry_climate": 1.0
        },
        "explanation": (
            "70% of your body is water. Even 2% dehydration impairs cognitive function and energy. "
            "Many people mistake dehydration for hunger or fatigue. Caffeine accelerates dehydration."
        ),
        "recommendation": {
            "supplement": "Electrolyte powder (optional, if exercising heavily)",
            "dose": "Follow package instructions",
            "timing": "During/after workouts",
            "lifestyle": "Drink 8-10 glasses of water daily. Drink before you're thirsty. Add electrolytes if sweating"
        },
        "timeline": "1-2 days to feel improvement"
    },
    
    {
        "id": 15,
        "name": "Gut Health Issues (Inflammation & Poor Absorption)",
        "indicators": ["digestive_issues", "bloating", "low_energy", "weak_immune", "food_sensitivities"],
        "severity_factors": {
            "processed_diet": 2.0,
            "antibiotic_history": 1.5,
            "high_stress": 1.0,
            "low_fiber": 1.5
        },
        "explanation": (
            "Your gut is your second brain and immune system. Poor diet and stress damage the gut lining, "
            "allowing bacteria to leak (leaky gut). This causes inflammation, poor nutrient absorption, "
            "and immune dysfunction."
        ),
        "recommendation": {
            "supplement": "Probiotics + Prebiotic Fiber",
            "dose": "10-50 billion CFU probiotics daily",
            "timing": "Morning on empty stomach or evening",
            "lifestyle": "Add fermented foods (yogurt, sauerkraut, kombucha), eat fiber (vegetables, fruits, whole grains)"
        },
        "timeline": "3-4 weeks for digestive improvement"
    },
    
    {
        "id": 16,
        "name": "Calcium Deficiency (Bones & Nerves)",
        "indicators": ["muscle_cramps", "bone_weakness", "tooth_issues", "anxiety", "irregular_heartbeat"],
        "severity_factors": {
            "dairy_free_diet": 1.5,
            "vitamin_d_deficiency": 2.0,  # Vitamin D needed for calcium absorption
            "high_caffeine": 1.0,
            "age_over_50": 1.5
        },
        "explanation": (
            "Calcium is essential for strong bones, muscle function, and nerve transmission. Without "
            "vitamin D, calcium isn't absorbed well. If calcium is low, your body pulls it from bones, "
            "leading to osteoporosis."
        ),
        "recommendation": {
            "supplement": "Calcium Citrate + Vitamin D3 together",
            "dose": "800-1000mg Calcium, 2000 IU Vitamin D daily",
            "timing": "With meals, separate from iron/zinc by 2 hours",
            "lifestyle": "Eat dairy (milk, yogurt, cheese) or leafy greens, get weight-bearing exercise"
        },
        "timeline": "4-8 weeks for bone strengthening"
    },
    
    {
        "id": 17,
        "name": "Thyroid Issues (Slow Metabolism)",
        "indicators": ["fatigue", "weight_gain", "cold_sensitivity", "dry_skin", "low_mood"],
        "severity_factors": {
            "iodine_deficiency": 2.0,
            "selenium_deficiency": 1.5,
            "high_stress": 1.0,
            "female": 1.0
        },
        "explanation": (
            "Your thyroid regulates metabolism, energy, and temperature. It needs iodine and selenium. "
            "Without these, your metabolism slows, you gain weight even with diet, and feel perpetually "
            "tired. This is especially common in women."
        ),
        "recommendation": {
            "supplement": "Iodine (kelp) + Selenium",
            "dose": "100-150 mcg Iodine, 200 mcg Selenium daily",
            "timing": "With meals",
            "lifestyle": "Eat fish, shellfish, seaweed. Get thyroid function tested (TSH, Free T3, Free T4)"
        },
        "timeline": "4-6 weeks for metabolism boost"
    },
    
    {
        "id": 18,
        "name": "Inflammation (Joint Pain & General Malaise)",
        "indicators": ["joint_pain", "muscle_soreness", "low_energy", "brain_fog", "mood_issues"],
        "severity_factors": {
            "processed_diet": 2.0,
            "sedentary_lifestyle": 1.5,
            "high_stress": 1.5,
            "high_sugar_intake": 1.0
        },
        "explanation": (
            "Chronic inflammation is the root of most modern diseases. It's caused by poor diet (seed oils, "
            "sugar), sedentary lifestyle, and stress. This manifests as joint pain, brain fog, and fatigue."
        ),
        "recommendation": {
            "supplement": "Omega-3 (pattern 9), Turmeric (Curcumin)",
            "dose": "500-1000mg Curcumin with black pepper (enhances absorption)",
            "timing": "With meals (fat-soluble)",
            "lifestyle": "Eliminate seed oils, reduce sugar, add anti-inflammatory foods (fatty fish, berries, greens), exercise"
        },
        "timeline": "2-3 weeks for pain reduction"
    },
    
    {
        "id": 19,
        "name": "Hormonal Imbalance (Women)",
        "indicators": ["mood_swings", "period_issues", "fatigue", "weight_gain", "low_libido"],
        "severity_factors": {
            "high_stress": 2.0,
            "poor_sleep": 1.5,
            "low_fat_diet": 1.0,
            "sedentary": 1.0
        },
        "explanation": (
            "Hormones regulate mood, energy, metabolism, and reproduction. Chronic stress and poor sleep "
            "dysregulate cortisol, which throws off estrogen and progesterone balance. This manifests as "
            "mood swings, irregular periods, and weight gain."
        ),
        "recommendation": {
            "supplement": "Magnesium (pattern 2), Vitamin B6 (supports progesterone)",
            "dose": "400mg Magnesium, 50-100mg B6 daily",
            "timing": "Morning and evening",
            "lifestyle": "Reduce stress (meditation, yoga), improve sleep (7-9 hours), eat healthy fats"
        },
        "timeline": "1-3 menstrual cycles for normalization"
    },
    
    {
        "id": 20,
        "name": "Mental Health Challenges (Mood & Anxiety)",
        "indicators": ["depression", "anxiety", "low_motivation", "brain_fog", "poor_focus"],
        "severity_factors": {
            "high_stress": 2.0,
            "poor_sleep": 2.0,
            "no_exercise": 1.5,
            "isolation": 1.5
        },
        "explanation": (
            "Mental health is tied to physical health. Poor sleep, stress, lack of exercise, isolation, "
            "and nutritional deficiencies all contribute to depression and anxiety. This is not just "
            "'mental' - it's biochemical."
        ),
        "recommendation": {
            "supplement": "Omega-3 (pattern 9), Magnesium (pattern 2), Vitamin D (pattern 1)",
            "dose": "See individual patterns",
            "timing": "See individual patterns",
            "lifestyle": "Exercise 30 mins daily, meditate 10 mins daily, connect with people, get sunlight, improve sleep, consider therapy"
        },
        "timeline": "2-4 weeks for mood improvement"
    }
]

def get_pattern_by_id(pattern_id: int) -> dict:
    """Get a specific health pattern by ID"""
    for pattern in HEALTH_PATTERNS:
        if pattern["id"] == pattern_id:
            return pattern
    return None

def get_all_patterns() -> list:
    """Get all health patterns"""
    return HEALTH_PATTERNS

def get_pattern_names() -> list:
    """Get list of all pattern names"""
    return [p["name"] for p in HEALTH_PATTERNS]
