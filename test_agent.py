from src.orchestrator import HealthAgentOrchestrator
orchestrator = HealthAgentOrchestrator()
result = orchestrator.run_consultation('I have fatigue and weight gain')
print('Specialist:', result['stages']['specialty_router']['recommendation'])
print('Confidence:', result['overall_confidence'])
