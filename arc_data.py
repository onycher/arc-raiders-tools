import json

from pathlib import Path
from typing import Any

from constants import (
    ITEM_DATA_PATH,
    WORKBENCH_DATA_PATH,
    QUEST_DATA_PATH,
    PROJECTS_DATA_PATH,
)


class ArcData:
    """Class to handle ARC data loading and querying."""

    def __init__(self) -> None:
        """Initialize ArcData by loading JSON data."""
        self.items: list[dict[str, Any]] = self._load_json(ITEM_DATA_PATH)
        self.hideout_modules: list[dict[str, Any]] = self._load_json(
            WORKBENCH_DATA_PATH
        )
        self.quests: list[dict[str, Any]] = self._load_json(QUEST_DATA_PATH)
        self.projects: list[dict[str, Any]] = self._load_json(PROJECTS_DATA_PATH)

    @staticmethod
    def _load_json(path: Path) -> list[dict[str, Any]]:
        """Load JSON data from the given path."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_deps(
        self, item_id: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Get dependencies for the given item ID from quests, hideout modules, and projects.

        Args:
            item_id: The ID of the item.

        Returns:
            A tuple of (quest_deps, hideout_deps, project_deps).
        """
        quest_deps = [
            {
                "name": quest["name"],
                "trader": quest["trader"],
                "count": required_item.get("quantity", 1),
            }
            for quest in self.quests
            if "requiredItemIds" in quest
            for required_item in quest["requiredItemIds"]
            if required_item["itemId"].strip() == item_id
        ]
        hideout_deps = [
            {
                "name": hideout_module["name"],
                "tier": hideout_level["level"],
                "count": required_item["quantity"],
            }
            for hideout_module in self.hideout_modules
            for hideout_level in hideout_module["levels"]
            if "requirementItemIds" in hideout_level
            for required_item in hideout_level["requirementItemIds"]
            if required_item["itemId"] == item_id
        ]
        project_deps = [
            {
                "name": project["name"],
                "phase": phase["phase"],
                "phase_name": phase["name"],
                "count": required_item["quantity"],
            }
            for project in self.projects
            for phase in project.get("phases", [])
            for required_item in phase.get("requirementItemIds", [])
            if required_item["itemId"] == item_id
        ]
        return quest_deps, hideout_deps, project_deps
