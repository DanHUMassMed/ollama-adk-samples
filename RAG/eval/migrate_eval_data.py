from google.adk.evaluation.agent_evaluator import AgentEvaluator
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

old_path = BASE_DIR / "data/conversation.test.1.json"
new_path = BASE_DIR / "data/conversation.test.1.evalset.json"

AgentEvaluator.migrate_eval_data_to_new_schema(
    old_eval_data_file=str(old_path),
    new_eval_data_file=str(new_path)
)



print(f"✅ Migrated eval data written to {new_path}")
