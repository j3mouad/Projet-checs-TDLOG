screen_width = 500
screen_height = 500
added_screen_width = 400
# Colors
# Define colors
white, grey, red, orange = (255, 255, 255), (128, 128, 128), (255, 0, 0), (255,165,0)
brown, light_brown, highlight_color = (118, 150, 86), (238, 238, 210), (200, 200, 0)
square_size = screen_width // 8
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 200, 100)  #green
button_hover_color = (150, 250, 150)  
square_size = screen_width // 8


# Colors
white, grey, red, orange = (255, 255, 255), (128, 128, 128), (255, 0, 0), (255,165,0)
brown, light_brown, highlight_color = (118, 150, 86), (238, 238, 210), (200, 200, 0)
black = (0, 0, 0)
button_color = (100, 200, 100)  # green
button_hover_color = (150, 250, 150)
screen_width = 500
screen_height = 500
added_screen_width = 400
square_size = screen_width // 8

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

