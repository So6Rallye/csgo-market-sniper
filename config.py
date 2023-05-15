import time
from typing import Any, Dict, List, Optional

import yaml


def load_config() -> Optional[Dict[str, Any]]:
    """
    Loads configuration file (config.yaml), extracts and validates the necessary information.

    Returns:
    dict: A dictionary containing configuration parameters including a nested list of skin dictionaries with their details
          (float, pattern, price, pages, url, sort_by_float), and a proxy configuration dictionary.
          Returns None if any skin's URL is not provided.
    """

    # Inform the user that the configuration file is being loaded
    print("Loading configuration file...")
    time.sleep(1)

    # Open and load the configuration file
    with open('settings/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Extract the skins configuration
    skins_config: List[Dict[str, str]] = config.get('skins')

    # If no skins are provided, inform the user and return None
    if not skins_config:
        print("No skins provided. Add skins to settings/config.yaml and rerun.\nExiting...")
        return None

    # For each skin in the configuration file, process the pattern
    for skin in skins_config:
        # If a pattern is provided as a string, split it into a list
        pattern = skin.get('pattern')
        if pattern and isinstance(pattern, str):
            skin['pattern'] = pattern.split(', ')

    # Inform the user of the number of skins loaded
    print(f"Loaded {len(skins_config)} skins!")
    time.sleep(1)

    # Define default timeouts
    default_timeouts = {
        'per_skin': 2,
        'per_page': 2,
        'after_server_error': 10,
        'after_too_many_requests': 60
    }

    # If no timeouts are provided, use the default values
    timeouts: Dict[str, int] = config.get('timeouts', default_timeouts)

    # Check for each timeout in defaults
    for timeout in default_timeouts:
        # If a timeout is not provided or zero, set to default and inform the user
        if not timeouts.get(timeout):
            timeouts[timeout] = default_timeouts[timeout]
            print(f"Timeout '{timeout}' not provided. Using default value of {default_timeouts[timeout]} seconds...")
            time.sleep(1)

    # Warn if per_skin or per_page timeouts are zero
    if timeouts['per_skin'] == 0 or timeouts['per_page'] == 0:
        print("Warning: Timeout values of 0 seconds are not recommended. This may cause you to get rate limited.")
        time.sleep(1)

    # Update config with actual timeouts
    config['timeouts'] = timeouts

    # If no proxy is provided, inform the user
    if not config.get('proxy_url'):
        print("No proxy provided. Continuing without a proxy...")
        time.sleep(1)

    return config