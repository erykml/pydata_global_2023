import requests
from bs4 import BeautifulSoup
import pandas as pd
from constants import LEGEND_LIST, PARADOX_LIST, DATA_RAW_DIR
from utils import get_generation, remove_repeated_words
import os

POKEDB_URL = "https://pokemondb.net/pokedex/all"

# Send a GET request to the URL
response = requests.get(POKEDB_URL)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing Pokémon data
    table = soup.find("table", {"id": "pokedex"})

    # Extract data from the table
    pokemon_data = []

    for row in table.find_all("tr")[1:]:  # Skip the header row
        columns = row.find_all("td")

        # extract name and number - we will need them for other things as well
        name = columns[1].text.strip()
        name_cleaned = (
            name.split(" ")[0]
            if (" " in name and name not in PARADOX_LIST and "Iron" not in name)
            else name
        )
        pokedex_number = int(columns[0].text.strip())

        # append to list
        pokemon_data.append(
            {
                "Pokedex Number": pokedex_number,
                "Name": remove_repeated_words(name),
                "Types": columns[2].text.strip(),
                "Total": columns[3].text.strip(),
                "HP": columns[4].text.strip(),
                "Attack": columns[5].text.strip(),
                "Defense": columns[6].text.strip(),
                "Sp. Atk": columns[7].text.strip(),
                "Sp. Def": columns[8].text.strip(),
                "Speed": columns[9].text.strip(),
                "Legendary": any(name_cleaned in name for name in LEGEND_LIST),
                "Generation": get_generation(pokedex_number),
            }
        )

    pokedex_df = pd.DataFrame(pokemon_data)

    # additional processing
    pokedex_df[["Type 1", "Type 2"]] = pokedex_df["Types"].str.split(expand=True)
    pokedex_df = pokedex_df.drop("Types", axis=1)
    pokedex_df["Mega Evolution"] = pokedex_df["Name"].str.contains(r"Mega|Primal")

    # save data
    pokedex_df.to_csv(os.path.join(DATA_RAW_DIR, "pokedex.csv"), index=None)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
