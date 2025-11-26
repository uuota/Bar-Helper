# Bar Helper App — with styles, ABV, glass, method and Library
import json
import barLibruaryHandler
import coctailHandler


def show_menu():
    print("\n=== BAR HELPER ===")
    print("1) Show all cocktails")
    print("2) Suggest cocktails by base spirit")
    print("3) Add your own cocktail")
    print("4) Find cocktails by ingredient")
    print("5) Show cocktails by style")
    print("6) Show cocktails sorted by strength (ABV)")
    print("7) Library")
    print("8) Exit")

# How to scale app with load json function
# def load_json(file_path):
#     with open(file_path) as f:
#         file = json.load(f)
#         if file:
#             return file
#         return None
#
# Usability in main():
# 	jsons_to_load = {
#         'cocktails': 'CocktailSpecs.json',
#         'abv_table': 'AbvTable.json',
#         'dilution_calc': 'DilutionCalk.json',
#         'bar_library': 'BarLibrary.json'
#     }
#
#     data = {}
#
#
#     for key, my_file in jsons_to_load.items():
#         if key == 'cocktails':
#             data_from_json = load_json(my_file)
#             data[key] = data_from_json['cocktails']
#         data[key] = load_json(my_file)
#
#     cocktails = data['cocktails']
#     abv_table = data['abv_table']
#     dilution_calc = data['dilution_calc']
#     bar_library = data['bar_library']

def main():
    with open('CocktailSpecs.json') as f:
        d = json.load(f)
        cocktails = d["cocktails"]

    with open('AbvTable.json') as f:
        abv_table = json.load(f)

    with open('DilutionCalk.json') as f:
        dilution_calc = json.load(f)

    with open('BarLibrary.json') as f:
        bar_library = json.load(f)

    while True:
        show_menu()
        choice = input("\nChoose option: ").strip()

        if choice == "1":
            coctailHandler.show_all_cocktails(cocktails)
        elif choice == "2":
            coctailHandler.suggest_by_base(cocktails, abv_table, dilution_calc)
        elif choice == "3":
            coctailHandler.add_cocktail(cocktails)
        elif choice == "4":
            coctailHandler.find_by_ingredient(cocktails, abv_table, dilution_calc)
        elif choice == "5":
            coctailHandler.show_cocktails_by_style(cocktails, abv_table, dilution_calc)
        elif choice == "6":
            coctailHandler.show_cocktails_sorted_by_abv(cocktails, abv_table, dilution_calc)
        elif choice == "7":
            barLibruaryHandler.show_library(bar_library)
        elif choice == "8":
            print("Goodbye, bartender!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()