import pytest
from unittest.mock import Mock
import backlog_gen_v2 as v2  # Minimal Diff: Point to v2 module

# --- Fixtures ---

@pytest.fixture
def standard_mock_llm():
    """Arrange: Mock for successful happy-path scenarios."""
    mock = Mock(spec=v2.OllamaLLM)
    mock.generate.side_effect = [
        "Epic Title\n\nAcceptance Criteria:\n1. AC1\n2. AC2\n3. AC3",
        "Feature 1\n\nAcceptance Criteria:\n1. AC1\n2. AC2\n3. AC3"
    ]
    return mock

@pytest.fixture
def empty_mock_llm():
    """Arrange: Mock for boundary scenarios."""
    mock = Mock(spec=v2.OllamaLLM)
    mock.generate.return_value = "Default Output"
    return mock

@pytest.fixture
def prompts():
    return {"epic": "Requirement: {input}", "feature": "Context: {input}"}

# --- Tests ---

def test_pipeline_output_structure(standard_mock_llm, prompts):
    result = v2.run_pipeline("Req", prompts, standard_mock_llm)
    # Minimal Diff: Verify shared state keys instead of hardcoded dict keys
    assert "requirement" in result
    assert "epic" in result
    assert "features" in result

def test_pipeline_data_chaining(standard_mock_llm, prompts):
    requirement = "Constraint: Exactly 3 features"
    v1_output = v2.run_pipeline(requirement, prompts, standard_mock_llm)
    
    # Minimal Diff: Verify requirement PERSISTS in the second call (State check)
    second_call_input = standard_mock_llm.generate.call_args_list[1][0][0]
    assert requirement in second_call_input
    assert "Epic Title" in second_call_input

def test_acceptance_criteria_presence(standard_mock_llm, prompts):
    result = v2.run_pipeline("Req", prompts, standard_mock_llm)
    assert "1. AC1" in result["epic"] and "1. AC1" in result["features"]

def test_pipeline_handles_empty_requirement(empty_mock_llm, prompts):
    result = v2.run_pipeline("", prompts, empty_mock_llm)
    assert result["requirement"] == ""
    assert result["epic"] == "Default Output"