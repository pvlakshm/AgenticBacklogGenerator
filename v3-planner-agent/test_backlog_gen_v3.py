import pytest
from unittest.mock import Mock
import backlog_gen_v3 as v3  # Minimal Diff: Point to v3 module

# --- Fixtures ---

@pytest.fixture
def standard_mock_llm():
    """Arrange: Mock for successful happy-path scenarios."""
    mock = Mock(spec=v3.OllamaLLM)
    # Restored to identical v1/v2 sample strings
    mock.generate.side_effect = [
        "Epic Title\n\nAcceptance Criteria:\n1. AC1\n2. AC2\n3. AC3",
        "Feature 1\n\nAcceptance Criteria:\n1. AC1\n2. AC2\n3. AC3"
    ]
    return mock

@pytest.fixture
def empty_mock_llm():
    """Arrange: Mock for boundary scenarios."""
    mock = Mock(spec=v3.OllamaLLM)
    mock.generate.return_value = "Default Output"
    return mock

@pytest.fixture
def prompts():
    # Minimal Diff: Added planner_system key for v3 orchestration
    return {
        "planner_system": "You are a Project Orchestrator. Do not ask for confirmation.",
        "epic": "Requirement: {input}",
        "feature": "Context: {input}"
    }

# --- Tests ---

def test_pipeline_uses_system_prompt(standard_mock_llm, prompts):
    """Act & Assert: Verify v3 passes the orchestration policy to the system role."""
    v3.run_pipeline("Req", prompts, standard_mock_llm)
    
    # Capture the keyword arguments sent to the generate method
    _, kwargs = standard_mock_llm.generate.call_args_list[0]
    assert kwargs["system_prompt"] == prompts["planner_system"]

def test_pipeline_output_structure(standard_mock_llm, prompts):
    result = v3.run_pipeline("Req", prompts, standard_mock_llm)
    assert "requirement" in result
    assert "epic" in result
    assert "features" in result # Matches plural requirement

def test_pipeline_execution_history(standard_mock_llm, prompts):
    """Act & Assert: Verify the agent tracks its dynamic execution path."""
    result = v3.run_pipeline("Req", prompts, standard_mock_llm)
    
    assert "history" in result
    assert result["history"] == ["epic", "features"]

def test_pipeline_handles_empty_requirement(empty_mock_llm, prompts):
    result = v3.run_pipeline("", prompts, empty_mock_llm)
    assert result["requirement"] == ""
    assert result["epic"] == "Default Output"