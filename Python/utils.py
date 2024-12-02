def has_non_empty_list(map_data):
    """
    Checks if a dictionary has any value that is a non-empty list.

    :param map_data: dict
        The dictionary to check.
    :return: bool
        True if any value is a non-empty list, False otherwise.
    """
    
    for value in map_data.values():
        if isinstance(value, list) and len(value) > 0:
            return True
    return False
import random

def get_random_value(data):
    """
    Selects a random value from a non-empty random list in the given dictionary.

    Args:
        data (dict): A dictionary where keys are tuples of integers, and values are lists.

    Returns:
        A random value from a random non-empty list in the dictionary.
        Returns None if all lists are empty or the dictionary is empty.
    """
    # Get all keys in the dictionary
    keys = list(data.keys())
    
    while keys:  # Repeat until keys are exhausted
        # Select a random key
        random_key = random.choice(keys)
        random_list = data[random_key]

        # Check if the list is non-empty
        if random_list:
            return random_key,random.choice(random_list)  # Return random value from the list

        # Remove the key with the empty list and continue
        keys.remove(random_key)

    # If no non-empty list is found, return None
    return None

