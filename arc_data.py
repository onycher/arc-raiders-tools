import json

from pathlib import Path
from typing import Any

from constants import ITEM_DATA_PATH, WORKBENCH_DATA_PATH, QUEST_DATA_PATH


class ArcData:
    """Class to handle ARC data loading and querying."""

    def __init__(self) -> None:
        """Initialize ArcData by loading JSON data."""
        self.items: list[dict[str, Any]] = self._load_json(ITEM_DATA_PATH)
        self.hideout_modules: list[dict[str, Any]] = self._load_json(
            WORKBENCH_DATA_PATH
        )
        self.quests: list[dict[str, Any]] = self._load_json(QUEST_DATA_PATH)

    @staticmethod
    def _load_json(path: Path) -> list[dict[str, Any]]:
        """Load JSON data from the given path."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_deps(
        self, item_id: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Get dependencies for the given item ID from quests and hideout modules.

        Args:
            item_id: The ID of the item.

        Returns:
            A tuple of (quest_deps, hideout_deps).
        """
        quest_deps = [
            {
                "name": quest["name"],
                "trader": quest["trader"],
                "count": requirement.get("count", 1),
            }
            for quest in self.quests
            if "requirements" in quest
            for requirement in quest["requirements"]
            if "links" in requirement
            for link in requirement["links"]
            if link["id"].strip() == item_id
        ]
        hideout_deps = [
            {
                "name": hideout_module["name"],
                "tier": hideout_levels["tier"],
                "count": required_item_id["count"],
            }
            for hideout_module in self.hideout_modules
            for hideout_levels in hideout_module["tiers"]
            if "requiredItems" in hideout_levels
            for required_item_id in hideout_levels["requiredItems"]
            if required_item_id["itemId"] == item_id
        ]
        return quest_deps, hideout_deps
