def show_library(library):
    """Show library folders and items (spirits, syrups, balance, methods, acids, cordials, etc.)."""
    if not library:
        print("Library is empty.")
        return

    sections = list(library.keys())

    print("\n--- Library folders ---")
    for idx, key in enumerate(sections, start=1):
        print(f"{idx}) {key}")

    sec_str = input("\nChoose folder number (or Enter to cancel): ").strip()
    if sec_str == "":
        return

    try:
        sec_num = int(sec_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= sec_num <= len(sections)):
        print("No such folder.")
        return

    section_key = sections[sec_num - 1]
    items_dict = library[section_key]

    if not items_dict:
        print("This folder is empty for now.")
        return

    item_names = list(items_dict.keys())

    print(f"\n--- {section_key} ---")
    for idx, name in enumerate(item_names, start=1):
        info = items_dict[name]
        if section_key == "syrups":
            cat = "syrup"
        else:
            cat = info.get("category", "n/a")
        print(f"{idx}) {name} ({cat})")

    item_str = input("\nChoose item number for details (or Enter to cancel): ").strip()
    if item_str == "":
        return

    try:
        item_num = int(item_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= item_num <= len(item_names)):
        print("No such item.")
        return

    name = item_names[item_num - 1]
    info = items_dict[name]

    print("\n--- Library item ---")
    print(f"Name:      {name}")
    if section_key == "syrups":
        print("Category:  syrup")
    else:
        print(f"Category:  {info.get('category', 'n/a')}")

    desc = info.get("description", "")
    if desc:
        print(f"Description: {desc}")

    # Old version:
    # if "ratio" in info:
    #     print(f"Ratio:     {info['ratio']}")
    # if "brix" in info:
    #     print(f"Brix:      {info['brix']}")
    # if "usage" in info:
    #     print(f"Usage:     {info['usage']}")
    # if "history" in info:
    #     print(f"History:     {info['history']}")

    # Search for key-value in info Object (one recipy from BarLibrary) and show every available value
    for key, value in info.items():
        print(f"{key:10}: {value}")

    sensory = info.get("sensory")
    if sensory:
        print(f"Sensory:   {sensory}")

    bar_tips = info.get("bar_tips")
    if bar_tips:
        print(f"Bar tips:  {bar_tips}")

    safety = info.get("safety")
    if safety:
        print(f"Safety:    {safety}")

    stock_solution = info.get("stock_solution")
    if stock_solution:
        print(f"Stock solution: {stock_solution}")

    example_applications = info.get("example_applications")
    if example_applications:
        print(f"Examples:  {example_applications}")

    note = info.get("note") or info.get("notes")
    if note:
        print(f"Notes:     {note}")

    recipe = info.get("recipe")
    if recipe:
        print(f"Recipe:    {recipe}")
