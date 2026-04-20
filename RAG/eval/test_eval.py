# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import sys

# Ensure the RAG parent directory is on sys.path so 'rag_agent' is statically resolvable
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r"Pydantic serializer warnings*"
)


pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_eval_full_conversation():
    """Test the agent's basic ability on a few examples."""
    
    import contextlib

    BASE_DIR = pathlib.Path(__file__).parent
    old_path = BASE_DIR / "data/conversation.test.1.json"
    new_path = BASE_DIR / "data/conversation.test.1.evalset.json"
    
    # Auto-compile human readable JSON test fixtures into EvalSet schemas
    AgentEvaluator.migrate_eval_data_to_new_schema(
        old_eval_data_file=str(old_path),
        new_eval_data_file=str(new_path)
    )

    output_file = BASE_DIR / "eval.txt"
    
    with open(output_file, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        try:
            await AgentEvaluator.evaluate(
                agent_module="rag_agent.agent",
                eval_dataset_file_path_or_dir=str(
                    pathlib.Path(__file__).parent / "data/conversation.test.1.evalset.json"
                ),
                num_runs=1,
            )
        except AssertionError as e:
            print(str(e))
            raise e
