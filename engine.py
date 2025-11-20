from dataclasses import dataclass
from typing import List, Set, Dict, Any


@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:

    def __init__(self, rules: List[Rule]):
        self.rules: List[Rule] = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def can_fire(self, rule: Rule) -> bool:      
        if not all(ant in self.facts for ant in rule.antecedents):
            return False

        if rule.consequent in self.facts:
            return False

        return True

    def run(self) -> None:
        while True:
            applicable = [r for r in self.rules if self.can_fire(r)]

            if not applicable:
                break

            applicable.sort(key=lambda r: r.priority, reverse=True)
            rule_to_fire = applicable[0]

            facts_before = set(self.facts)

            self.facts.add(rule_to_fire.consequent)

            self.trace.append(
                {
                    "rule": rule_to_fire,
                    "consequent": rule_to_fire.consequent,
                    "facts_before": facts_before,
                    "facts_after": set(self.facts),
                }
            )

    def conclusions(self) -> Dict[str, List[str]]:
        recommendations: List[str] = []
        specs: List[str] = []
        other: List[str] = []

        for fact in self.facts:
            if fact.startswith("recommend:"):
                recommendations.append(fact.split(":", 1)[1])
            elif fact.startswith("spec:"):
                specs.append(fact.split(":", 1)[1])
            else:
                other.append(fact)

        recommendations.sort()
        specs.sort()
        other.sort()

        return {
            "recommendations": recommendations,
            "specs": specs,
            "other_facts": other,
        }
