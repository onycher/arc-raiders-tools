import json
from pathlib import Path
from typing import Any

from constants import (
    HIDEOUT_DIR,
    ITEMS_DIR,
    PROJECTS_DATA_PATH,
    QUESTS_DIR,
)


class ArcData:
    """Class to handle ARC data loading and querying."""

    def __init__(self) -> None:
        """Initialize ArcData by loading JSON data."""
        # New data layout uses many per-entity JSON files instead of single large files.
        self.items: list[dict[str, Any]] = self._load_dir(ITEMS_DIR)
        self.hideout_modules: list[dict[str, Any]] = self._load_dir(HIDEOUT_DIR)
        self.quests: list[dict[str, Any]] = self._load_dir(QUESTS_DIR)
        self.projects: list[dict[str, Any]] = self._load_json(PROJECTS_DATA_PATH)

    @staticmethod
    def _load_json(path: Path) -> list[dict[str, Any]]:
        """Load JSON data from a single JSON file path."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _load_dir(path: Path) -> list[dict[str, Any]]:
        """
        Load JSON data from all .json files in a directory into a single list.

        Each JSON file may contain either:
        - a single object, or
        - a list of objects

        In the first case, the object is appended; in the second, the list is
        extended into the combined result.
        """
        data: list[dict[str, Any]] = []
        for json_path in sorted(path.glob("*.json")):
            with open(json_path, "r", encoding="utf-8") as file:
                obj = json.load(file)
                if isinstance(obj, list):
                    data.extend(obj)
                else:
                    data.append(obj)
        return data

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
        # Quests: where this item is REQUIRED (turn‑in), via requiredItemIds
        quest_deps = [
            {
                "name": quest.get("name", {}).get("en", "<no name>"),
                "trader": quest.get("trader"),
                "count": required_item.get("quantity", 1),
            }
            for quest in self.quests
            for required_item in quest.get("requiredItemIds", [])
            if str(required_item.get("itemId", "")).strip() == str(item_id).strip()
        ]

        # Hideout: where this item is required to upgrade modules (requirementItemIds)
        hideout_deps = [
            {
                "name": hideout_module.get("name", {}).get("en", "<no name>"),
                "tier": hideout_level.get("level", 0),
                "count": required_item.get("quantity", 1),
            }
            for hideout_module in self.hideout_modules
            for hideout_level in hideout_module.get("levels", [])
            for required_item in hideout_level.get("requirementItemIds", [])
            if required_item.get("itemId") == item_id
        ]

        # Projects: where this item is required in project phases
        project_deps = [
            {
                "name": project.get("name", {}).get("en", "<no name>"),
                "phase": phase.get("phase"),
                "phase_name": phase.get("name", {}).get("en", "<no phase name>"),
                "count": required_item.get("quantity", 1),
            }
            for project in self.projects
            for phase in project.get("phases", [])
            for required_item in phase.get("requirementItemIds", [])
            if required_item.get("itemId") == item_id
        ]

        return quest_deps, hideout_deps, project_deps
