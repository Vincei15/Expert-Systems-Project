from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def ask_yes_no(prompt: str) -> bool:
    answer = input(prompt).strip().lower()
    return answer.startswith("y")


def collect_initial_facts():
    facts = []

    # Budget 
    budget = input("What is your budget? (low/medium/high): ").strip().lower()
    if budget in {"low", "medium", "high"}:
        facts.append(f"budget_{budget}")

    # Usage 
    if ask_yes_no("Is portability important? (y/n): "):
        facts.append("portable")

    if ask_yes_no("Do you need long battery life? (y/n): "):
        facts.append("long_battery")

    if ask_yes_no("Is this mainly for gaming? (y/n): "):
        facts.append("gaming")

    if ask_yes_no("Is this mainly for creative work (photo/video/design)? (y/n): "):
        facts.append("creative_work")

    if ask_yes_no("Is this mostly for office / web / documents only? (y/n): "):
        facts.append("office_only")

    if ask_yes_no("Do you travel often with your laptop? (y/n): "):
        facts.append("travel_often")

    if ask_yes_no("Do you prefer a large screen (15\" or bigger)? (y/n): "):
        facts.append("large_screen")

    # OS 
    os_pref = input("Preferred OS? (windows/macos/linux/none): ").strip().lower()
    if os_pref == "windows":
        facts.append("pref_os_windows")
    elif os_pref == "macos":
        facts.append("pref_os_macos")
    elif os_pref == "linux":
        facts.append("pref_os_linux")

    # AI needs
    if ask_yes_no("Do you need AI acceleration / heavy ML workloads? (y/n): "):
        facts.append("needs_ai_accel")

    return facts


def main():
    rules = load_rules(KB_PATH)

    engine = ForwardChainingEngine(rules)

    initial_facts = collect_initial_facts()
    engine.facts.update(initial_facts)

    engine.run()

    results = engine.conclusions()

    for rec in results["recommendations"]:
        print(f"> Recommendation: {rec}")
        full_fact = f"recommend:{rec}"
        fired = next(
            (step for step in engine.trace if step["consequent"] == full_fact),
            None,
        )
        if fired is not None:
            print(f"> Explanation: derived from rule '{fired['rule'].name}'")

    if results["specs"]:
        print("\n> Suggested specs:")
        for spec in results["specs"]:
            print(f"  - {spec}")

    if engine.trace:
        print("\nRules fired (in order):")
        for step in engine.trace:
            print(f"- {step['rule'].name} -> {step['consequent']}")
    else:
        print("\nNo rules fired. Try different answers or expand the knowledge base.")


if __name__ == "__main__":
    main()
