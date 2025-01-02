
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



