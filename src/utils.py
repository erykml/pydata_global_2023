from collections import Counter
import yaml


def get_generation(pokedex_number):
    if 1 <= pokedex_number <= 151:
        return 1
    elif 152 <= pokedex_number <= 251:
        return 2
    elif 252 <= pokedex_number <= 386:
        return 3
    elif 387 <= pokedex_number <= 493:
        return 4
    elif 494 <= pokedex_number <= 649:
        return 5
    elif 650 <= pokedex_number <= 721:
        return 6
    elif 722 <= pokedex_number <= 809:
        return 7
    elif 810 <= pokedex_number <= 906:
        return 8
    elif 907 <= pokedex_number <= 1010:
        return 9
    else:
        return None


def remove_repeated_words(input_string):
    words = input_string.split()
    word_counts = Counter(words)

    # Remove repeated instances of words
    unique_words = []
    for word in words:
        if word_counts[word] > 1:
            word_counts[word] -= 1
        else:
            unique_words.append(word)

    # Construct the resulting string
    result_string = " ".join(unique_words)

    return result_string


def load_params(file_path="params.yaml"):
    with open(file_path, "r") as stream:
        try:
            params = yaml.safe_load(stream)
            return params
        except yaml.YAMLError as e:
            print(f"Error loading YAML file {file_path}: {e}")
            return None
