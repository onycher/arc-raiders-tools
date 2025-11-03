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
    quest_data, hideout_data, project_data = data.get_deps(item_data["id"])

    # Build content list
    content = []

    # Item header
    value = item_data.get("value", "N/A")
    value_str = f"{value}$" if value != "N/A" else value
    item_text = Text(f"{item_data['name']}: {value_str}", style="bold green")
    content.append(item_text)

    # Recycles Into table
    recycles_into = item_data.get("recyclesInto", {})
    if recycles_into and isinstance(recycles_into, dict):
        recycles_table = Table(
            title="[bold yellow]Recycles Into[/bold yellow]",
            title_style="bold yellow",
            header_style="bold cyan",
            border_style="yellow",
            show_header=True,
            show_lines=True,
        )
        recycles_table.add_column("Item", style="white", no_wrap=True)
        recycles_table.add_column("Quantity", style="yellow", justify="right")
        for item_id, quantity in recycles_into.items():
            recycles_table.add_row(item_id.replace("_", " ").title(), str(quantity))
        content.append(recycles_table)

    # Salvages Into table
    salvages_into = item_data.get("salvagesInto", {})
    if salvages_into and isinstance(salvages_into, dict):
        salvages_table = Table(
            title="[bold cyan]Salvages Into[/bold cyan]",
            title_style="bold cyan",
            header_style="bold cyan",
            border_style="cyan",
            show_header=True,
            show_lines=True,
        )
        salvages_table.add_column("Item", style="white", no_wrap=True)
        salvages_table.add_column("Quantity", style="cyan", justify="right")
        for item_id, quantity in salvages_into.items():
            salvages_table.add_row(item_id.replace("_", " ").title(), str(quantity))
        content.append(salvages_table)

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

    # Project table
    if project_data:
        project_table = Table(
            title="[bold red]Projects[/bold red]",
            title_style="bold red",
            header_style="bold cyan",
            border_style="red",
            show_header=True,
            show_lines=True,
        )
        project_table.add_column("Project", style="white", no_wrap=True)
        project_table.add_column("Phase", style="white", justify="center")
        project_table.add_column("Phase Name", style="white")
        project_table.add_column("Count", style="yellow", justify="right")
        for p in project_data:
            project_table.add_row(
                p["name"], str(p["phase"]), p["phase_name"], str(p["count"])
            )
        content.append(project_table)

    # If no data at all
    if (
        not quest_data
        and not hideout_data
        and not project_data
        and not recycles_into
        and not salvages_into
    ):
        no_data_text = Text(
            "No dependencies or crafting info found for this item.", style="italic red"
        )
        content.append(no_data_text)

    # Create panel
    panel = Panel(
        Group(*content),
        title="[bold green]🤖 ARC Raiders Item Info[/bold green]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
