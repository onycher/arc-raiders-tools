import json
import mss
import pytesseract
import cv2
import numpy as np
from pynput import keyboard
from rich.console import Console
from rich.table import Table
from rich.text import Text


def find_popup(image):
    template = cv2.imread("actions.png")

    template_h, template_w = template.shape[:2]
    image_h, image_w = image.shape[:2]

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    seed_point = (top_left[0], top_left[1] + template_h - 1)

    mask = np.zeros((image_h + 2, image_w + 2), np.uint8)

    lo_diff = (10, 10, 10)
    up_diff = (10, 10, 10)

    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (1 << 8)

    cv2.floodFill(image, mask, seed_point, 0, lo_diff, up_diff, flags)

    filled_mask = mask[1:-1, 1:-1]
    rows, cols = np.where(filled_mask == 1)

    if rows.size > 0 and cols.size > 0:
        # Find the bounding box of the filled area
        y_min = np.min(rows)
        y_max = np.max(rows)
        x_min = np.min(cols)
        x_max = np.max(cols)

        final_cropped_image = image[y_min : y_max + 1, x_min : x_max + 1]
        return final_cropped_image
    else:
        return None


def capture_screen():
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[1])

    img_np = np.array(sct_img)
    screenshot = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
    return screenshot
    # pil_img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
    # return pil_img


class ArcData:
    def __init__(self):
        with open("Arc-Data-Compendium/src/data/items/itemData.json", "r") as file:
            self.items = json.load(file)
        with open(
            "Arc-Data-Compendium/src/data/workbenches/workbenchData.json", "r"
        ) as file:
            self.hideout_modules = json.load(file)
        with open("Arc-Data-Compendium/src/data/quests/questData.json", "r") as file:
            self.quests = json.load(file)

    def get_deps(self, item):
        # items = [
        #     item["id"]
        #     for item in self.items
        #     if item["name"].lower() == item_name.lower()
        #
        # ]
        # if len(items) == 0:
        #     raise ValueError(f"No item found with name '{item_name}'")
        # item = items[0].strip()
        # print(f"item: {item}")

        quest_deps = []
        for quest in self.quests:
            if "requirements" in quest:
                for requirement in quest["requirements"]:
                    if "links" in requirement:
                        for link in requirement["links"]:
                            if link["id"].strip() == item:
                                quest_deps.append(
                                    {
                                        "name": quest["name"],
                                        "trader": quest["trader"],
                                        "count": requirement["count"]
                                        if "count" in requirement
                                        else 1,
                                    }
                                )
        hideout_deps = []
        for hideout_module in self.hideout_modules:
            for hideout_levels in hideout_module["tiers"]:
                if "requiredItems" in hideout_levels:
                    for required_item_id in hideout_levels["requiredItems"]:
                        if required_item_id["itemId"] == item:
                            hideout_deps.append(
                                {
                                    "name": hideout_module["name"],
                                    "tier": hideout_levels["tier"],
                                    "count": required_item_id["count"],
                                }
                            )
        return quest_deps, hideout_deps


data = ArcData()
console = Console()


def on_hotkey_activate():
    screen = capture_screen()
    popup = find_popup(screen)
    text = pytesseract.image_to_string(popup)
    for line in text.splitlines():
        item = line.strip().lower().replace(" ", "_")
        if all([i["id"] != item for i in data.items]):
            continue
        item_data = [i for i in data.items if i["id"] == item][0]
        try:
            print_item_info(item_data)
            break
        except Exception as e:
            raise e
    else:
        print(f"Item not found: {item}")


def print_item_info(item_data):
    console.clear()
    t = Text(f"{item_data['name']}: {item_data['value']}$")
    t.stylize("frame")
    console.print(t, style="frame")
    quest_data, hideout_data = data.get_deps(item_data["id"])
    quest_table = Table(title="Quests")
    quest_table.add_column("Name")
    quest_table.add_column("Trader")
    quest_table.add_column("Count")
    for q in quest_data:
        quest_table.add_row(q["name"], q["trader"], str(q["count"]))
    if quest_data:
        console.print(quest_table)
    hideout_table = Table(title="Hideout")
    hideout_table.add_column("Name")
    hideout_table.add_column("Tier")
    hideout_table.add_column("Count")
    for h in hideout_data:
        hideout_table.add_row(h["name"], str(h["tier"]), str(h["count"]))
    if hideout_data:
        console.print(hideout_table)


# def on_hotkey_release():
#     print("Hotkey released")


def main():
    try:
        with keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": on_hotkey_activate}) as h:
            h.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    except Exception as e:
        print(f"An error occurred: {e}")
    # image = cv2.imread("image.png")
    # popup = find_popup(image)
    # text = pytesseract.image_to_string(popup)
    # item = text.split("\n")[1].strip()
    # print(item)
    # print(data.get_deps(item))


if __name__ == "__main__":
    main()
