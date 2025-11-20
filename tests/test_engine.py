import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def run_case(input_facts, expected_fact):
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)

    engine.facts.update(input_facts)

    engine.run()

    assert expected_fact in engine.facts, (
        f"Expected fact '{expected_fact}' not derived.\n"
        f"Input facts: {input_facts}\n"
        f"All derived facts: {sorted(engine.facts)}"
    )


def test_premium_ultrabook():
    input_facts = ["budget_high", "portable", "long_battery"]
    expected = "recommend:premium_ultrabook"
    run_case(input_facts, expected)


def test_budget_ultrabook_for_student():
    input_facts = ["budget_low", "portable", "office_only"]
    expected = "recommend:budget_ultrabook"
    run_case(input_facts, expected)


def test_midrange_gaming():
    input_facts = ["budget_medium", "gaming"]
    expected = "recommend:midrange_gaming_laptop"
    run_case(input_facts, expected)


def test_high_end_gaming():
    input_facts = ["budget_high", "gaming"]
    expected = "recommend:high_end_gaming_laptop"
    run_case(input_facts, expected)


def test_creative_work_ram_spec():
    input_facts = ["creative_work", "portable"]
    expected = "spec:ram_16_plus"
    run_case(input_facts, expected)


def test_creative_work_display_spec():
    input_facts = ["creative_work", "large_screen"]
    expected = "spec:display_15_plus_color_accurate"
    run_case(input_facts, expected)


def test_travel_battery_spec():
    input_facts = ["travel_often", "long_battery"]
    expected = "spec:battery_60wh_plus"
    run_case(input_facts, expected)


def test_macos_required_spec():
    input_facts = ["pref_os_macos"]
    expected = "spec:macos_required"
    run_case(input_facts, expected)


def test_ai_accel_spec():
    input_facts = ["needs_ai_accel"]
    expected = "spec:gpu_with_tensor_cores"
    run_case(input_facts, expected)


def test_linux_office_friendly_spec():
    input_facts = ["pref_os_linux", "office_only"]
    expected = "spec:linux_friendly_hw"
    run_case(input_facts, expected)
