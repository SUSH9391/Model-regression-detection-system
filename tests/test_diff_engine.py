import os
import pytest
from src.contracts import EvalResult
from src.diff_engine import calculate_regression_delta, compute_accuracy

@pytest.fixture
def base_metrics():
    return {"category_match": 1.0, "latency": 0.1, "tokens_used": 50}

@pytest.fixture
def make_eval_result():
    def _make(case_id: str, match: float, status: str = "success") -> EvalResult:
        return EvalResult(
            test_case_id=case_id,
            status=status,
            output={"category": "billing", "summary": "test invoice info"},
            error=None,
            metrics={"category_match": match, "latency": 0.1, "tokens_used": 50}
        )
    return _make

def test_zero_regressions_is_pass(make_eval_result, monkeypatch):
    monkeypatch.setenv("WARN_THRESHOLD", "3.0")
    monkeypatch.setenv("FAIL_THRESHOLD", "8.0")
    
    baseline = [make_eval_result("1", 1.0), make_eval_result("2", 1.0)]
    current = [make_eval_result("1", 1.0), make_eval_result("2", 1.0)]
    
    delta = calculate_regression_delta(current, baseline)
    assert delta["status"] == "pass"
    assert delta["regressions_count"] == 0
    assert delta["accuracy_delta"] == 0.0

def test_five_percent_drop_is_warn(make_eval_result, monkeypatch):
    monkeypatch.setenv("WARN_THRESHOLD", "3.0")
    monkeypatch.setenv("FAIL_THRESHOLD", "8.0")
    
    # 20 cases in total -> 1 fail is a 5% drop
    baseline = [make_eval_result(str(i), 1.0) for i in range(20)]
    current = [make_eval_result(str(i), 1.0) for i in range(19)] + [make_eval_result("19", 0.0)]
    
    delta = calculate_regression_delta(current, baseline)
    assert delta["status"] == "warn"
    assert delta["regressions_count"] == 1
    assert delta["accuracy_delta"] == -5.0

def test_ten_percent_drop_is_fail(make_eval_result, monkeypatch):
    monkeypatch.setenv("WARN_THRESHOLD", "3.0")
    monkeypatch.setenv("FAIL_THRESHOLD", "8.0")
    
    # 10 cases in total -> 1 fail is a 10% drop
    baseline = [make_eval_result(str(i), 1.0) for i in range(10)]
    current = [make_eval_result(str(i), 1.0) for i in range(9)] + [make_eval_result("9", 0.0)]
    
    delta = calculate_regression_delta(current, baseline)
    assert delta["status"] == "fail"
    assert delta["regressions_count"] == 1
    assert delta["accuracy_delta"] == -10.0

def test_improvements_detected(make_eval_result, monkeypatch):
    monkeypatch.setenv("WARN_THRESHOLD", "3.0")
    monkeypatch.setenv("FAIL_THRESHOLD", "8.0")
    
    baseline = [make_eval_result("1", 0.0), make_eval_result("2", 1.0)]
    current = [make_eval_result("1", 1.0), make_eval_result("2", 1.0)]
    
    delta = calculate_regression_delta(current, baseline)
    assert delta["improvements_count"] == 1
    assert delta["regressions_count"] == 0
    assert delta["accuracy_delta"] == 50.0

def test_mismatched_ids_skipped(make_eval_result, monkeypatch):
    monkeypatch.setenv("WARN_THRESHOLD", "3.0")
    monkeypatch.setenv("FAIL_THRESHOLD", "8.0")
    
    # "2" is in current but not baseline; "1" is in baseline but not current
    baseline = [make_eval_result("1", 1.0)]
    current = [make_eval_result("2", 1.0)]
    
    delta = calculate_regression_delta(current, baseline)
    assert delta["regressions_count"] == 0
    assert delta["improvements_count"] == 0

def test_compute_accuracy_perfect(make_eval_result):
    results = [make_eval_result("1", 1.0), make_eval_result("2", 1.0)]
    assert compute_accuracy(results) == 1.0

def test_compute_accuracy_partial(make_eval_result):
    results = [make_eval_result("1", 1.0), make_eval_result("2", 0.0)]
    assert compute_accuracy(results) == 0.5
