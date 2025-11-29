"""
Agent evaluation and metrics tracking
Measures agent performance, confidence, and quality
"""

import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AgentType(Enum):
    """Types of agents in the system"""
    INTAKE = "intake"
    DIAGNOSTIC = "diagnostic"
    SPECIALTY_ROUTER = "specialty_router"
    KNOWLEDGE = "knowledge"
    ROOT_CAUSE = "root_cause"
    RECOMMENDER = "recommender"
    ORCHESTRATOR = "orchestrator"
    CHAT = "chat"

@dataclass
class AgentMetrics:
    """Metrics for a single agent execution"""
    agent_type: str
    execution_time: float  # seconds
    input_length: int  # character count
    output_length: int
    confidence_score: float  # 0.0-1.0
    success: bool
    error_message: Optional[str] = None
    timestamp: str = ""
    
    def to_dict(self):
        return asdict(self)

class EvaluationTracker:
    """Tracks metrics across agent pipeline"""
    
    def __init__(self):
        self.metrics: List[AgentMetrics] = []
        self.session_id = f"session_{int(time.time())}"
    
    def record_agent_execution(
        self,
        agent_type: AgentType,
        input_text: str,
        output_text: str,
        execution_time: float,
        confidence_score: float,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AgentMetrics:
        """Record metrics for one agent execution"""
        
        metric = AgentMetrics(
            agent_type=agent_type.value,
            execution_time=execution_time,
            input_length=len(input_text),
            output_length=len(output_text),
            confidence_score=confidence_score,
            success=success,
            error_message=error_message,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        self.metrics.append(metric)
        return metric
    
    def get_pipeline_stats(self) -> Dict:
        """Calculate statistics across entire pipeline"""
        if not self.metrics:
            return {}
        
        successful = [m for m in self.metrics if m.success]
        failed = [m for m in self.metrics if not m.success]
        
        total_time = sum(m.execution_time for m in self.metrics)
        avg_confidence = sum(m.confidence_score for m in successful) / len(successful) if successful else 0
        
        return {
            "session_id": self.session_id,
            "total_agents_executed": len(self.metrics),
            "successful_agents": len(successful),
            "failed_agents": len(failed),
            "success_rate": (len(successful) / len(self.metrics)) * 100,
            "total_pipeline_time": total_time,
            "average_agent_time": total_time / len(self.metrics),
            "average_confidence": avg_confidence,
            "avg_input_length": sum(m.input_length for m in self.metrics) / len(self.metrics),
            "avg_output_length": sum(m.output_length for m in self.metrics) / len(self.metrics),
        }
    
    def get_agent_stats(self, agent_type: AgentType) -> Dict:
        """Get stats for a specific agent type"""
        agent_metrics = [m for m in self.metrics if m.agent_type == agent_type.value]
        
        if not agent_metrics:
            return {}
        
        return {
            "agent": agent_type.value,
            "executions": len(agent_metrics),
            "avg_execution_time": sum(m.execution_time for m in agent_metrics) / len(agent_metrics),
            "avg_confidence": sum(m.confidence_score for m in agent_metrics) / len(agent_metrics),
            "success_rate": (sum(1 for m in agent_metrics if m.success) / len(agent_metrics)) * 100,
        }
    
    def export_metrics(self, filepath: str):
        """Export all metrics to JSON file"""
        data = {
            "session_id": self.session_id,
            "pipeline_stats": self.get_pipeline_stats(),
            "individual_metrics": [m.to_dict() for m in self.metrics],
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def print_report(self):
        """Print human-readable metrics report"""
        stats = self.get_pipeline_stats()
        
        print("\n" + "=" * 80)
        print("📊 AGENT PIPELINE PERFORMANCE REPORT")
        print("=" * 80)
        print(f"Session ID: {self.session_id}")
        print(f"\nExecution Summary:")
        print(f"  Total Agents Executed: {stats.get('total_agents_executed')}")
        print(f"  Successful: {stats.get('successful_agents')}")
        print(f"  Failed: {stats.get('failed_agents')}")
        print(f"  Success Rate: {stats.get('success_rate', 0):.1f}%")
        print(f"\nTiming:")
        print(f"  Total Pipeline Time: {stats.get('total_pipeline_time', 0):.2f}s")
        print(f"  Average Per Agent: {stats.get('average_agent_time', 0):.2f}s")
        print(f"\nQuality Metrics:")
        print(f"  Average Confidence: {stats.get('average_confidence', 0):.2f}")
        print(f"  Avg Input Length: {int(stats.get('avg_input_length', 0))} chars")
        print(f"  Avg Output Length: {int(stats.get('avg_output_length', 0))} chars")
        
        print(f"\nPer-Agent Breakdown:")
        for agent_type in AgentType:
            agent_stats = self.get_agent_stats(agent_type)
            if agent_stats:
                print(f"\n  {agent_stats['agent'].upper()}")
                print(f"    Executions: {agent_stats['executions']}")
                print(f"    Avg Time: {agent_stats['avg_execution_time']:.2f}s")
                print(f"    Confidence: {agent_stats['avg_confidence']:.2f}")
                print(f"    Success Rate: {agent_stats['success_rate']:.1f}%")
        
        print("\n" + "=" * 80)

# Global tracker instance
_tracker = EvaluationTracker()

def get_tracker() -> EvaluationTracker:
    """Get the global evaluation tracker"""
    return _tracker

def track_agent_execution(
    agent_type: AgentType,
    input_text: str,
    output_text: str,
    execution_time: float,
    confidence_score: float = 0.8,
    success: bool = True,
    error_message: Optional[str] = None
) -> AgentMetrics:
    """Convenience function to track agent execution using global tracker"""
    return _tracker.record_agent_execution(
        agent_type=agent_type,
        input_text=input_text,
        output_text=output_text,
        execution_time=execution_time,
        confidence_score=confidence_score,
        success=success,
        error_message=error_message
    )
