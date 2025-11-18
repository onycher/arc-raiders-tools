from pathlib import Path

# Image processing constants
TEMPLATE_IMAGE_PATH = "actions.png"

# Data paths - new layout uses per-entity JSON files in directories
ITEMS_DIR = Path("arcraiders-data/items")
HIDEOUT_DIR = Path("arcraiders-data/hideout")
QUESTS_DIR = Path("arcraiders-data/quests")
PROJECTS_DATA_PATH = Path("arcraiders-data/projects.json")

# Backwards-compatible aliases for existing code
# Previously these pointed to single large JSON files; now they refer to
# directories or specific files while keeping the old names so existing
# imports continue to work.
ITEM_DATA_PATH = ITEMS_DIR  # Previously: arcraiders-data/items.json
WORKBENCH_DATA_PATH = HIDEOUT_DIR / "workbench.json"  # Previously: hideoutModules.json
QUEST_DATA_PATH = QUESTS_DIR  # Previously: arcraiders-data/quests.json

# Hotkey
HOTKEY_COMBINATION = "<ctrl>+<alt>+s"
