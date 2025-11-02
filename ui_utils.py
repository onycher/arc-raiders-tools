from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import Any

from arc_data import ArcData


def print_item_info(console: Console, item_data: dict[str, Any], data: ArcData) -> None:
    """
    Print item information to the console with enhanced styling.

    Args:
        console: The Rich console instance.
        item_data: The item data dictionary.
        data: The ArcData instance.
    """
    console.clear()
    quest_data, hideout_data = data.get_deps(item_data["id"])

    # Build content list
    content = []

    # Item header
    item_text = Text(f"{item_data['name']}: {item_data['value']}$", style="bold green")
    content.append(item_text)

    # Quest table
    if quest_data:
        quest_table = Table(
            title="[bold blue]Quests[/bold blue]",
            title_style="bold blue",
            header_style="bold cyan",
            border_style="blue",
            show_header=True,
            show_lines=True,
        )
        quest_table.add_column("Name", style="white", no_wrap=True)
        quest_table.add_column("Trader", style="white")
        quest_table.add_column("Count", style="yellow", justify="right")
        for q in quest_data:
            quest_table.add_row(q["name"], q["trader"], str(q["count"]))
        content.append(quest_table)

    # Hideout table
    if hideout_data:
        hideout_table = Table(
            title="[bold magenta]Hideout Modules[/bold magenta]",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="magenta",
            show_header=True,
            show_lines=True,
        )
        hideout_table.add_column("Name", style="white", no_wrap=True)
        hideout_table.add_column("Tier", style="white", justify="center")
        hideout_table.add_column("Count", style="yellow", justify="right")
        for h in hideout_data:
            hideout_table.add_row(h["name"], str(h["tier"]), str(h["count"]))
        content.append(hideout_table)

    # If no data
    if not quest_data and not hideout_data:
        no_data_text = Text("No dependencies found for this item.", style="italic red")
        content.append(no_data_text)

    # Create panel
    panel = Panel(
        Group(*content),
        title="[bold green]🤖 ARK Raiders Item Info[/bold green]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
