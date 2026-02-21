#!/usr/bin/env python
"""One-off script to update use_resource_oriented_design rule."""
import json
from pathlib import Path

path = Path(__file__).parent.parent / "bots/story_bot/behaviors/code/rules/use_resource_oriented_design.json"
with open(path) as f:
    d = json.load(f)

d["description"] = (
    "Code must use resource-oriented, object-oriented design. Use object-oriented classes "
    "(singular or collection) with responsibilities that encapsulate logic over manager/doer/loader "
    "patterns. Maximize encapsulation through collaborator relationships. Logic belongs on the "
    "resource that owns the data; do not implement it on a parent that wraps."
)

d["do"] = {
    "description": "Use resource-oriented classes; put logic on the resource that owns the data",
    "guidance": [
        {
            "description": "Use resource-oriented classes instead of managers. Create object-oriented classes, encapsulate logic in classes, use collection classes (Behaviors, Holdings) as properties of domain objects.",
            "example": [
                "class Portfolio:",
                "    @property",
                "    def holdings(self) -> Holdings: ...",
                "class Holdings:",
                "    def get_many_positions(self) -> List[Position]: ...",
            ],
        },
        {
            "description": "Put logic on the resource that owns the data. Behavior-level data belongs on Behavior; action-level data belongs on Action. Bot delegates to them. For simple storage use properties; for logic (load, validate, persist) use methods.",
            "example": [
                "class Behavior:",
                "    @property",
                "    def special_instructions(self) -> Optional[str]: ...",
                "    @special_instructions.setter",
                "    def special_instructions(self, value: str): ...",
                "class Action:",
                "    @property",
                "    def special_instructions(self) -> Optional[str]: ...",
                "    @special_instructions.setter",
                "    def special_instructions(self, value: str): ...",
            ],
        },
    ],
}

d["dont"] = {
    "description": "Do not create manager/loader classes; do not wrap logic on parent when it belongs to child",
    "guidance": [
        {
            "description": "Do not create manager/loader classes. Do not separate loading logic from domain concepts.",
            "example": [
                "class PortfolioManager:",
                "    def get_holdings(self, client_id, account_id): ...",
                "class HoldingsLoader:",
                "    def load_holdings(self, client_id, account_id): ...",
            ],
        },
        {
            "description": "Do not wrap: parent implementing logic that belongs to child. Do not implement storage/retrieval on Bot when the data belongs to Behavior or Action.",
            "example": [
                "class Bot:",
                "    def set_behavior_special_instructions(self, behavior_name, text): ...",
                "    def set_action_special_instructions(self, behavior_name, action_name, text): ...",
                "    def get_behavior_special_instructions(self, behavior_name): ...",
                "    def get_action_special_instructions(self, behavior_name, action_name): ...",
            ],
        },
    ],
}

if "examples" in d:
    del d["examples"]

with open(path, "w") as f:
    json.dump(d, f, indent=2)

print("Updated rule")
