from functions import dutchrequest, maryrequest, sorter, os, json
from config import dutchIDS, janeIDS, path

# Purpose: send a request to the inputed dispensaries and then extract data from the response and sort it.
# Author: cat-thats-fat
# Date: 10-04-2024
# Version: 2.2
# Current Task: Add support for iheartjane
# To-Do:
#     Create menu option for finding a store's ID given a link to the store
#     Create menu option to add/remove stores

filters = {
    "category": ["Flower", "Vaporizers", "Pre-Rolls", "Concentrate"],
    "strainType": ["Sativa", "Indica", "Hybrid", "No Preference"],
}
# first is type second is cate
currentchoice = [0, 0]

def home(currentchoice):
    os.system('cls' if os.name == 'nt' else 'clear')
    main(currentchoice)

def main(currentchoice):

    cate = filters["category"][currentchoice[0]]
    type = filters["strainType"][currentchoice[1]]

    print("Cheap Weed Finder")
    print()
    print(f"Current parameters: \n  Category: {cate} \n  Type: {type}")
    print()
    print("1. Change search parameters")
    print("2. Search")
    print("3. View store(s) and change discounts")
    print("3. Exit")

    choice = int(input(">"))

    if choice == 1:
        print("Change Search Parameters")
        print()
        print("Available Categories: Flower(1), Vaporizers(2), Pre-rolls(3), Concentrate(4)")
        print()
        print("Strain types: Sativa(1), Indica(2), Hybrid(3), No Preference(4)")
        print()

        currentchoice[0] = int(input("Enter the category you'd like to search: ")) - 1
        currentchoice[1] = int(input("Enter the type of strain you'd like to search: ")) - 1
        home(currentchoice)

    elif choice == 2:

        os.system('cls' if os.name == 'nt' else 'clear')
        count = 1
        print("Requesting Data")

        output = {}

        # Loop through the IDs and request the data
        if len(dutchIDS) > 0:
            for name, info in dutchIDS.items():
                output[name] = (dutchrequest(info, currentchoice))
                print(f"{count}/{len(dutchIDS)} stores searched")
                count += 1
            print("Search Complete")

        # write the output
        with open(f"{path}/output.json", "w") as f:
            json.dump(output, f, indent=4)
            f.close()

        print("Results Saved.")
        input("Press enter to exit...")

    elif choice == 3:

        print("Cheap Weed Finder")
        print()
        print("Current Dispenaries:")
        print()
        for name in dutchIDS:
            print(name)
            print(f"Discount: {dutchIDS[name]["discount"]}")
        print()
        print("1. Change Discount")
        print("2. Return Home")
        print(">")
        choice = input()

        if choice == 1:

            print("Change Dispensarie discounts:")
            print()
            for store in dutchIDS:
                print(store)
                print(f"Current Discount: dutchIDS[store]["discount"]")
                print("Enter new discount:")
                discount = input
        elif choice == 2:
            home()


    elif choice == 4:
        exit()


main(currentchoice)
