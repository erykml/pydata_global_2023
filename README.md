# Classifying Legendary Pokémon

A demo project showcasing experiment tracking capabilities of DVC.
The example is built on the case of classifying Pokémon as legendary.

## Known limitations
* Generation is based on Pokédex number. That does not reflect regional forms (Galarian, Alolan, etc.), Mega Evolutions, etc.
* Until generation 8 (incl.), the legendary classification consisted of the following: Sub-Legendary Pokémon | Legendary Pokémon | Mythical Pokémon. We treat them all as legendary for the sake of this exercise.
* From generation 9 onwards, the legendary classification is slightly different, that is, there are groups called: Sub-Legendary Pokémon | Ultra Beasts | Paradox Pokémon | Restricted Legendary Pokémon | Mythical Pokémon. For example, Ultra Beasts are now a separate class and are not considered Legendary.

## References
* https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420/?select=pokedex_%28Update_04.21%29.csv
* https://pokemondb.net/pokedex/all
* https://www.serebii.net/pokemon/legendary.shtml
* https://www.serebii.net/pokemon/specialpokemon.shtml

Icons:
* https://www.flaticon.com/free-icon/csv_9159105
* https://www.flaticon.com/free-icon/cloud_3222791