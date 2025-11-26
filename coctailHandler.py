def calc_abv(cocktail, abv_table, dilution):
    total_ml = 0
    total_alcohol_ml = 0.0

    for item in cocktail["ingredients"]:
        amount = item["amount"]
        if amount is None:
            continue
        name = item["name"].lower()
        total_ml += amount
        if name in abv_table:
            abv = abv_table[name] / 100
            total_alcohol_ml += amount * abv

    if total_ml == 0:
        return 0.0

    method = cocktail.get("method", "").lower()
    dil = dilution.get(method, 0.0)
    diluted_ml = total_ml * (1 + dil)

    return round((total_alcohol_ml / diluted_ml) * 100, 1)

def show_all_cocktails(cocktails):
    print("\n--- Cocktail List ---")
    for idx, c in enumerate(cocktails, start=1):
        print(f"{idx}) {c['name']} ({c['base']}, {c.get('style', 'n/a')})")

def add_cocktail(cocktails):
    print("\n--- Add your cocktail ---")
    name = input("Cocktail name: ").strip()
    base = input("Base spirit: ").strip().lower()
    glass = input("Glass type (rocks, coupe, highball, etc): ").strip()
    method = input("Method (shake, stir, build, blend, no_dilution): ").strip().lower()
    style = input(
        "Style (classic, modern classic, tiki, highball, spritz, coffee, sours, "
        "dessert, long drink, aperitivo, shitty classic): "
    ).strip().lower()

    ingredients = []
    print("Enter ingredients one by one.")
    print("Format: name,ml   or   name   (for no amount)")
    print("Enter empty line when finished.\n")

    while True:
        line = input("Ingredient: ").strip()
        if line == "":
            break

        if "," in line:
            ing_name, ing_amount = line.split(",", 1)
            ing_name = ing_name.strip()
            ing_amount = ing_amount.strip()
            try:
                ing_amount = int(ing_amount)
            except ValueError:
                ing_amount = None
        else:
            ing_name = line
            ing_amount = None

        ingredients.append({"name": ing_name, "amount": ing_amount})

    cocktails.append(
        {
            "name": name,
            "base": base,
            "glass": glass,
            "method": method,
            "style": style,
            "ingredients": ingredients,
        }
    )

    data = {"cocktails": cocktails}
    with open("CocktailSpecs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Cocktail '{name}' added!")

def find_by_ingredient(cocktails, abv_table, dilution_calc):
    ing = input("\nIngredient: ").strip().lower()

    matches = []
    for c in cocktails:
        for item in c["ingredients"]:
            if ing in item["name"].lower():
                matches.append(c)
                break

    if not matches:
        print(f"No cocktails found with '{ing}'.")
        return

    print(f"\nCocktails containing '{ing}':")
    for idx, c in enumerate(matches, start=1):
        print(f"{idx}) {c['name']} - {calc_abv(c, abv_table, dilution_calc)}% ABV ({c.get('style', 'n/a')})")

    num_str = input("\nChoose cocktail number for details (or Enter to cancel): ").strip()
    if num_str == "":
        return

    try:
        num = int(num_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= num <= len(matches)):
        print("No cocktail with this number.")
        return

    c = matches[num - 1]
    show_cocktail_details(c, abv_table, dilution_calc)

def show_cocktails_by_style(cocktails, abv_table, dilution_calc):
    styles = sorted({c.get("style") for c in cocktails if c.get("style")})

    if not styles:
        print("No styles defined yet.")
        return

    print("\n--- Available styles ---")
    for idx, s in enumerate(styles, start=1):
        print(f"{idx}) {s}")

    num_str = input("\nChoose style number (or Enter to cancel): ").strip()
    if num_str == "":
        return

    try:
        num = int(num_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= num <= len(styles)):
        print("No such style.")
        return

    chosen_style = styles[num - 1]
    matches = [c for c in cocktails if c.get("style") == chosen_style]

    if not matches:
        print(f"No cocktails with style '{chosen_style}'.")
        return

    print(f"\nCocktails with style '{chosen_style}':")
    for idx, c in enumerate(matches, start=1):
        print(f"{idx}) {c['name']} - {calc_abv(c, abv_table, dilution_calc)}% ABV ({c['base']})")

    num_str = input("\nChoose cocktail number for details (or Enter to cancel): ").strip()
    if num_str == "":
        return

    try:
        num = int(num_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= num <= len(matches)):
        print("No such cocktail.")
        return

    c = matches[num - 1]
    show_cocktail_details(c, abv_table, dilution_calc)

def show_cocktails_sorted_by_abv(cocktails, abv_table, dilution_calc):
    print("\n--- Cocktails sorted by strength (ABV, high → low) ---")
    sorted_list = sorted(
        cocktails,
        key=lambda cocktail: calc_abv(cocktail, abv_table, dilution_calc),
        reverse=True
    )

    for idx, c in enumerate(sorted_list, start=1):
        print(f"{idx}) {c['name']} - {calc_abv(c, abv_table, dilution_calc)}% ABV ({c['base']}, {c.get('style', 'n/a')})")

    num_str = input("\nChoose cocktail number for details (or Enter to cancel): ").strip()
    if num_str == "":
        return

    try:
        num = int(num_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= num <= len(sorted_list)):
        print("No such cocktail.")
        return

    c = sorted_list[num - 1]
    show_cocktail_details(c, abv_table, dilution_calc)

def show_cocktail_details(c, abv_table, dilution_calc):
    print("\n--- Cocktail details ---")
    print(f"Name:   {c['name']}")
    print(f"Base:   {c['base']}")
    print(f"Style:  {c.get('style', 'n/a')}")
    print(f"Glass:  {c.get('glass', 'n/a')}")
    print(f"Method: {c.get('method', 'n/a')}")
    print(f"ABV:    {calc_abv(c, abv_table, dilution_calc)}%")
    print("Ingredients:")
    for item in c["ingredients"]:
        if item["amount"] is None:
            print(f" - {item['name']}")
        else:
            print(f" - {item['name']}: {item['amount']} ml")

def suggest_by_base(cocktails, abv_table, dilution_calc):
    bases = sorted({c["base"] for c in cocktails})
    print("\nChoose base spirit:")
    for idx, b in enumerate(bases, start=1):
        print(f"{idx}) {b}")

    num_str = input("\nEnter number (or Enter to cancel): ").strip()
    if num_str == "":
        return

    try:
        num = int(num_str)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= num <= len(bases)):
        print("No such base.")
        return

    base = bases[num - 1]

    matches = []
    for cocktail in cocktails:
        if cocktail["base"] == base:
            matches.append(cocktail)

    if not matches:
        print("No cocktails with this base.")
        return

    print(f"\nCocktails with base '{base}':")
    for idx, c in enumerate(matches, start=1):
        print(f"{idx}) {c['name']} - {calc_abv(c, abv_table, dilution_calc)}% ABV ({c.get('style', 'n/a')})")

    choice = input("\nChoose cocktail number for details (or Enter to cancel): ").strip()
    if choice == "":
        return

    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid number.")
        return

    if not (1 <= choice_num <= len(matches)):
        print("No such cocktail.")
        return

    c = matches[choice_num - 1]
    show_cocktail_details(c, abv_table, dilution_calc)
