import logging
import sys

import pytesseract  # type: ignore
from pynput import keyboard
from rich.console import Console

from arc_data import ArcData
from constants import HOTKEY_COMBINATION
from image_utils import capture_screen, find_popup
from ui_utils import print_item_info

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def on_hotkey_activate(data: ArcData, console: Console) -> None:
    """
    Handle the hotkey activation: capture screen, find popup, extract text, and print item info.

    Args:
        data: The ArcData instance.
        console: The Rich console instance.
    """
    try:
        screen = capture_screen()
        popup = find_popup(screen)
        if popup is None:
            logging.warning("Popup not found in screenshot.")
            return
        text = str(pytesseract.image_to_string(popup))  # type: ignore
        item_id = ""
        for line in text.splitlines():
            item_id = line.strip().lower().replace(" ", "_")
            if item_id == "":
                continue
            if not any(i["id"].startswith(item_id) for i in data.items):
                continue
            item_data = next(i for i in data.items if i["id"].startswith(item_id))
            print_item_info(console, item_data, data)
            return
        logging.info(f"Item not found: {item_id}")
    except Exception as e:
        logging.error(f"An error occurred during hotkey activation: {e}")


def quit_app(console: Console) -> None:
    """Quit the application."""
    console.print("[bold red]Exiting ARC Raiders Tool. Goodbye![/bold red]")
    logging.info("Quit hotkey pressed.")
    sys.exit(0)


def main() -> None:
    """Main function to set up hotkeys and run the application."""
    data = ArcData()
    console = Console()
    try:
        with keyboard.GlobalHotKeys(
            {
                HOTKEY_COMBINATION: lambda: on_hotkey_activate(data, console),
                "<ctrl>+q": lambda: quit_app(console),
            }
        ) as h:
            h.join()
    except KeyboardInterrupt:
        console.print("[bold red]Exiting ARC Raiders Tool. Goodbye![/bold red]")
        logging.info("Keyboard interrupt detected.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
