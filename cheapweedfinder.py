import os
import json
from functions import dutchrequest, janerequest, clear
# Purpose: Find the best deals on weed using requests and simple math
# Author: cat-thats-fat
# Date: 10-04-2024
# Version: 3.0.0
# Current Task: Rewrite interface
# To-Do:
#     Clean up all the code
#     Add documentation

def main(config):

    filters = {
        "categories": ["Flower", "Pre-Rolls", "Vaporizer", "Concentrates"],
        "strains": ['Sativa', "Indica", "Hybrid", "No Preference"]
    }

    clear()

    print("Cheap Weed Finder \n")
    print(f"Current Category: {filters['categories'][config["choices"]["category"]]}")
    print(f"Current Strain: {filters['strains'][config["choices"]["strain"]]} \n")
    print("1. Search")
    print("2. Change search parameters")
    print("3. Save & Exit \n")
    choice = int(input("Enter choice: "))

    if choice == 1:
        
        clear()

        print("Cheap Weed Finder \n")
        print("Progress:")
        
        output = {}

        count = 0

        dispos = len(config["dutchIDS"]) + len(config["janeIDS"])

        # search dutchie IDS
        for dispo in config["dutchIDS"]:
            info = config["dutchIDS"][dispo]
            output[dispo] = dutchrequest(info, config)
            count += 1
            print(f"Sites searched: {count}/{dispos}")
        
        for dispo in config["janeIDS"]:
            info = config["janeIDS"][dispo]
            output[dispo] = janerequest(info, config)
            count += 1
            print(f"Sites searched: {count}/{dispos}")

        with open("output.json", "w") as f:
            json.dump(output, f, indent=6)
            f.close
        print("Search complete and results saved.")
        input("Press enter to return home...")
        main(config)
            
            


    elif choice == 2:
        
        clear()

        print("Cheap Weed Finder")
        print("Change Parameters")
        print()
        print("Categories: Flower(1), Pre-Rolls(2), Vaporizers(3), Concentrate(4)")
        print("Strains: Sativa(1), Indica(2), Hybrid(3), No Preference(4)")
        print()
        config["choices"]["category"] = int(input("Which category would you like to search for?")) - 1
        config["choices"]["strain"] = int(input("Which strain would you like to search for?")) - 1
        input("Changes saved, press enter to return home...")
        main(config)

    elif choice == 3:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
            f.close

        clear()
        exit()

def setup():
    clear()

    if not os.path.exists("config.json"):
        print("Welcome to Cheap Weed Finder by cat-thats-fat")
        print("It appears to be your first time using CWF as the config file cannot be found.")
        config_template = {
            "choices": {
                "category": 0,
                "strain": 0
            },
            "dutchIDS": {
                "DISPENSARY NAME": {
                    "id": "R3PL4C3_TH15_W1TH_TH3_1D",
                    "discount": 420
                },
            },
            "janeIDS": {
                "DISPENSARY NAME": {
                    "id": "1234",
                    "discount": 420
                },
            }
        }

        with open("config.json", "w") as f:
            json.dump(config_template, f, indent=4)
            f.close
        print("Config file created")
        print("Fill in the config file, follow the instructions in the readme to find the IDS.")
        input("Press enter to exit....")
        exit()

if __name__ == "__main__":
    setup()

    with open("config.json", "r") as f:
        config = json.load(f)
        f.close()

    main(config)
