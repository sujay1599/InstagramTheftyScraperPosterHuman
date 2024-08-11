import yaml
from cryptography.fernet import Fernet
import getpass
import os
from input_helpers import get_input, get_boolean_input
from instagrapi import Client  # Correct import of Client class
from auth import perform_login, decrypt_credentials  # Import functions from auth.py
from default_comments import DEFAULT_COMMENTS
from default_descriptions import DEFAULT_DESCRIPTIONS
from rich.console import Console

console = Console()

# Constants
SESSION_DIR = 'user_sessions'
CONFIG_FILE = 'config.yaml'
DEFAULT_TAGS = [
    'instagram', 'instadaily', 'LikeForLike', 'FollowForFollow', 'viral',
    'trending', 'explorepage', 'love', 'photooftheday', 'instagood',
    'fashion', 'style', 'beauty', 'art', 'instamood', 'explore',
    'photography', 'travel', 'nature', 'happy', 'fun', 'picoftheday',
    'instalike', 'motivation', 'fitness', 'selfie', 'cute', 'food',
    'instafashion', 'lifestyle', 'smile', 'memes', 'dankmemes',
    'funnymemes', 'memestagram', 'funny', 'comedy', 'meme',
    'ootd', 'life', 'friends', 'summer', 'bhfyp', 'instaphoto',
    'inspiration', 'music', 'family', 'weekendvibes', 'sunset',
    'wanderlust', 'model', 'india', 'usa', 'goals'
]

# Ensure the session directory exists
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
    console.print(f"[bold green]Created directory for user sessions: {SESSION_DIR}[/bold green]")

def generate_key():
    return Fernet.generate_key()

def encrypt_credentials(username, password, key):
    cipher_suite = Fernet(key)
    encrypted_username = cipher_suite.encrypt(username).decode()
    encrypted_password = cipher_suite.encrypt(password).decode()
    return encrypted_username, encrypted_password

def get_user_credentials():
    """Prompt the user for Instagram credentials and validate by attempting login."""
    while True:
        username = input('Enter Instagram username: ').encode()
        password = getpass.getpass('Enter Instagram password: ').encode()
        
        # Check if the user has 2FA enabled
        two_fa_enabled = get_boolean_input('Is 2FA enabled on this account? (true/false): ')
        verification_code = None
        if two_fa_enabled:
            verification_code = input('Enter the 2FA verification code: ')

        # Initialize the Client object
        client = Client()
        client.delay_range = [1, 3]  # Mimic human behavior with delays between requests
        session_file = os.path.join(SESSION_DIR, f"{username.decode()}_session.json")

        # Use perform_login function from auth.py to attempt login and manage session
        if perform_login(client, username.decode(), password.decode(), session_file, verification_code):
            console.print("[bold green]Login successful![/bold green]")
            return username, password, two_fa_enabled
        else:
            console.print("[bold red]Login failed. Please try again.[/bold red]")

def create_scraping_config():
    """Create scraping configuration."""
    return {
        'enabled': get_boolean_input('Enable scraping? (true/false): '),
        'profiles': input('Enter profiles to scrape (space separated): '),
        'num_reels': get_input('Number of reels to scrape per profile: ', int),
        'scrape_interval_minutes': get_input('Interval between scrapes (minutes): ', int),
        'like_reels': get_boolean_input('Like scraped videos? (true/false): ')
    }

def create_uploading_config():
    """Create uploading configuration."""
    return {
        'enabled': get_boolean_input('Enable uploading? (true/false): '),
        'upload_interval_minutes': get_input('Interval between uploads (minutes): ', int),
        'add_to_story': get_boolean_input('Add to story? (true/false): ')
    }

def create_description_config():
    """Create description and hashtag configuration."""
    use_original_description = get_boolean_input('Use original description? (true/false): ')
    description_config = {'use_original': use_original_description}

    if use_original_description:
        description_config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if description_config['hashtags']['use_hashtags']:
            description_config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated, leave blank for default): ')
        
        description_config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }
    else:
        description_config['custom_description'] = input('Enter custom description (leave blank to use default descriptions): ')

        description_config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if description_config['hashtags']['use_hashtags']:
            description_config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated, leave blank for default): ')

        description_config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }

    return description_config

def create_config(encrypted_username, encrypted_password, key):
    """Create the main configuration dictionary."""
    config = {
        'instagram': {
            'username': encrypted_username,
            'password': encrypted_password,
            'original_username': encrypted_username
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
        'custom_tags': input(f'Enter custom tags (space separated, leave blank for default: {DEFAULT_TAGS}): ').split() or DEFAULT_TAGS
    }

    if config['leave_comment']:
        config['comments'] = input('Enter comments (comma separated): ').split(',')

    return config

def save_config(config, filename=CONFIG_FILE):
    """Save the configuration dictionary to a YAML file."""
    with open(filename, 'w') as file:
        yaml.dump(config, file)
    console.print(f"[bold green]Configuration saved to {filename}[/bold green]")

def delete_files(files):
    """Delete specified files if they exist."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            console.print(f"[bold yellow]Deleted {file}[/bold yellow]")

def load_config(config_file=CONFIG_FILE):
    """Load configuration from a YAML file."""
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def main():
    """Main function to generate configuration and manage session files."""
    key = generate_key()
    username, password, two_fa_enabled = get_user_credentials()
    encrypted_username, encrypted_password = encrypt_credentials(username, password, key)
    
    config = create_config(encrypted_username, encrypted_password, key)
    config['instagram']['original_username'] = username.decode()  # Add original username to config
    save_config(config)

    delete_files(['status.json', 'last_scraped_timestamp.txt', 'random-upload-times.json', 'random-waits.json'])

if __name__ == "__main__":
    main()
