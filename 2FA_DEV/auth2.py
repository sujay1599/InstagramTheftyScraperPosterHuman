```python
import json
import yaml
import os
import logging
from cryptography.fernet import Fernet
import getpass
from instagrapi import Client
from rich.console import Console
from auth import perform_login, decrypt_credentials, generate_key, encrypt_credentials  

console = Console()

# Constants
SESSION_DIR = 'user_sessions'
CONFIG_DIR = 'configs'
KEY_FILE = 'key.key'  

# Set up logging
logging.basicConfig(
    filename="config_setup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

console.print(f"[bold green]Created session and config directories if not present[/bold green]")

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        logging.info(f"Generated new encryption key: {KEY_FILE}")
        return key

def get_user_credentials():
    key = load_or_generate_key()
    while True:
        username = input('Enter Instagram username: ').encode()
        password = getpass.getpass('Enter Instagram password: ').encode()
        client = Client()
        session_file = os.path.join(SESSION_DIR, f"{username.decode()}_session.json")
        if perform_login(client, username.decode(), password.decode(), session_file):
            logging.info(f"Login successful for user: {username.decode()}")
            console.print("[bold green]Login successful![/bold green]")
            encrypted_username, encrypted_password = encrypt_credentials(username, password, key)
            return encrypted_username, encrypted_password, username.decode()
        else:
            console.print("[bold red]Login failed. Please try again.[/bold red]")
            logging.error(f"Login failed for user: {username.decode()}")

def create_config(encrypted_username, encrypted_password, key, username):
    return {
        'instagram': {
            'username': encrypted_username,
            'password': encrypted_password,
        },
        'key': key.decode(),
        'proxy': input('Enter proxy server address (leave blank if not using proxy): '),
    }

def save_config(config, username):
    filename = os.path.join(CONFIG_DIR, f"{username}_config.yaml")
    with open(filename, 'w') as file:
        yaml.dump(config, file)
    console.print(f"[bold green]Configuration saved to {filename}[/bold green]")
    logging.info(f"Configuration saved to {filename}")

def main():
    key = load_or_generate_key()
    encrypted_username, encrypted_password, username = get_user_credentials()
    config = create_config(encrypted_username, encrypted_password, key, username)
    save_config(config, username)

if __name__ == "__main__":
    main()
