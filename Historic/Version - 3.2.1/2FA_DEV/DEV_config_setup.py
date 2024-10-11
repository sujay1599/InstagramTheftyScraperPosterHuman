import json
import yaml
import os
import logging
from cryptography.fernet import Fernet
import getpass
from instagrapi import Client
from rich.console import Console
from auth import perform_login, decrypt_credentials, generate_key, encrypt_credentials  # Functions from auth.py
from input_helpers import get_input, get_boolean_input
from default_comments import DEFAULT_COMMENTS
from default_descriptions import DEFAULT_DESCRIPTIONS

console = Console()

# Constants
SESSION_DIR = 'user_sessions'
CONFIG_DIR = 'configs'
KEY_FILE = 'key.key'  # Encryption key storage

DEFAULT_TAGS = [
    '1min', 'LongerVideos', 'swifttok', 'FallGuysMoments', 
    'MakeupInspo', 'PaTiChallenge', 'ForYourPride', 'ohno', 
    'anime', 'FilmTok', 'Fashionista', 'ShoppingTherapy', 
    'BeautyDay', 'SportsPhotography', 'EntertainmentNews',
    'GreenEnergy', 'EcoFriendly', 'MentalHealthMatters', 'DigitalArt', 'TravelGoals'
]

# Set up logging
logging.basicConfig(
    filename="config_setup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Ensure the session and config directories exist
os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

console.print(f"[bold green]Created session and config directories if not present[/bold green]")

# Encryption key management
def load_or_generate_key():
    """Load encryption key from file, or generate a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        logging.info(f"Generated new encryption key: {KEY_FILE}")
        return key

# Prompt user for Instagram credentials and validate login
def get_user_credentials():
    """Prompt user for Instagram credentials and validate login via auth.py."""
    key = load_or_generate_key()
    while True:
        username = input('Enter Instagram username: ').encode()
        password = getpass.getpass('Enter Instagram password: ').encode()

        # Initialize the Client object
        client = Client()
        client.delay_range = [1, 3]  # Mimic human behavior
        session_file = os.path.join(SESSION_DIR, f"{username.decode()}_session.json")

        # Perform login using auth.py's function
        if perform_login(client, username.decode(), password.decode(), session_file):
            logging.info(f"Login successful for user: {username.decode()}")
            console.print("[bold green]Login successful![/bold green]")
            encrypted_username, encrypted_password = encrypt_credentials(username, password, key)
            return encrypted_username, encrypted_password, username.decode()  # Return decoded username for file naming
        else:
            console.print("[bold red]Login failed. Please try again.[/bold red]")
            logging.error(f"Login failed for user: {username.decode()}")

# Create scraping configuration
def create_scraping_config():
    """Create and return scraping configuration."""
    return {
        'enabled': get_boolean_input('Enable scraping? (true/false): '),
        'profiles': input('Enter Instagram profiles to scrape (space-separated): '),
        'num_reels': get_input('Number of reels to scrape per profile: ', int),
        'scrape_interval_minutes': get_input('Interval between scrapes (minutes): ', int),
        'like_reels': get_boolean_input('Like scraped videos? (true/false): ')
    }

# Create uploading configuration
def create_uploading_config():
    """Create and return uploading configuration."""
    return {
        'enabled': get_boolean_input('Enable uploading? (true/false): '),
        'upload_interval_minutes': get_input('Interval between uploads (minutes): ', int),
        'add_to_story': get_boolean_input('Add to story? (true/false): ')
    }

# Create description and hashtag configuration
def create_description_config():
    """Create and return description configuration."""
    use_original_description = get_boolean_input('Use original description? (true/false): ')
    description_config = {'use_original': use_original_description}

    if use_original_description:
        description_config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if description_config['hashtags']['use_hashtags']:
            description_config['hashtags']['hashtags_list'] = input('Enter hashtags (space-separated, leave blank for default): ')
        
        description_config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }
    else:
        description_config['custom_description'] = input('Enter custom description (leave blank to use default descriptions): ')
        description_config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if description_config['hashtags']['use_hashtags']:
            description_config['hashtags']['hashtags_list'] = input('Enter hashtags (space-separated, leave blank for default): ')

        description_config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }

    return description_config

# Create the full configuration file
def create_config(encrypted_username, encrypted_password, key, username):
    """Create the main configuration file."""
    config = {
        'instagram': {
            'username': encrypted_username,
            'password': encrypted_password,
        },
        'key': key.decode(),
        'scraping': create_scraping_config(),
        'uploading': create_uploading_config(),
        'proxy': input('Enter proxy server address (leave blank if not using proxy): '),
        'description': create_description_config(),
        'leave_comment': get_boolean_input('Leave comment on scraped videos? (true/false): '),
        'deleting': {
            'delete_interval_minutes': get_input('Interval between deletions (minutes): ', int)
        },
        'custom_tags': input(f'Enter custom tags (space-separated, leave blank for default: {DEFAULT_TAGS}): ').split() or DEFAULT_TAGS
    }

    if config['leave_comment']:
        config['comments'] = input('Enter comments (comma-separated): ').split(',')

    return config

def save_config(config, username, filename=None):
    """Save the configuration dictionary to a YAML file."""
    if filename is None:
        filename = os.path.join(CONFIG_DIR, f"{username}_config.yaml")  # Save config for specific user

    try:
        with open(filename, 'w') as file:
            yaml.dump(config, file)
        console.print(f"[bold green]Configuration saved to {filename}[/bold green]")
        logging.info(f"Configuration saved to {filename}")
    except Exception as e:
        console.print(f"[bold red]Failed to save configuration: {e}[/bold red]")
        logging.error(f"Failed to save configuration: {e}")
# Save configuration to a YAML file, using the username to differentiate files

def load_config(username, filename=None):
    """Load the configuration from a YAML file."""
    if filename is None:
        filename = os.path.join(CONFIG_DIR, f"{username}_config.yaml")  # Use the config for specific user

    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                config = yaml.safe_load(file)
            console.print(f"[bold green]Configuration loaded from {filename}[/bold green]")
            return config
        except Exception as e:
            console.print(f"[bold red]Failed to load configuration: {e}[/bold red]")
            logging.error(f"Failed to load configuration: {e}")
            raise
    else:
        console.print(f"[bold red]Configuration file {filename} not found. Run config_setup.py first.[/bold red]")
        raise FileNotFoundError(f"Configuration file {filename} not found.")

# Main function to set up the config
def main():
    """Main function to gather credentials, create, and save configuration."""
    key = load_or_generate_key()
    encrypted_username, encrypted_password, username = get_user_credentials()
    config = create_config(encrypted_username, encrypted_password, key, username)
    save_config(config, username)

if __name__ == "__main__":
    main()
