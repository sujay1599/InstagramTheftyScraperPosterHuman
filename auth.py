import json
import os
import logging
from instagrapi import Client
from cryptography.fernet import Fernet
from rich.console import Console

console = Console()

def generate_key():
    return Fernet.generate_key()

def encrypt_credentials(username, password, key):
    cipher_suite = Fernet(key)
    encrypted_username = cipher_suite.encrypt(username.encode()).decode()
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_username, encrypted_password

def decrypt_credentials(config):
    key = config['key'].encode()
    cipher_suite = Fernet(key)
    decrypted_username = cipher_suite.decrypt(config['instagram']['username'].encode()).decode()
    decrypted_password = cipher_suite.decrypt(config['instagram']['password'].encode()).decode()
    return decrypted_username, decrypted_password

def save_session(client, filename='session.json'):
    settings = client.get_settings()
    with open(filename, 'w') as f:
        json.dump(settings, f)
    console.print(f"[bold blue]Session file created/updated: {filename}[/bold blue]")

def load_session(client, filename='session.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            settings = json.load(f)
        client.set_settings(settings)
        return True
    return False

def login(client, username, password, session_file='session.json'):
    if load_session(client, session_file):
        try:
            client.get_timeline_feed()
            console.print("[bold blue]Logged in using session file[/bold blue]")
            return
        except Exception as e:
            console.print(f"[bold red]Failed to login using session file: {e}[/bold red]")

    try:
        client.login(username, password)
        client.set_timezone_offset(-21600)  # Set CST (Chicago) timezone offset
        save_session(client, session_file)
        console.print(f"[bold blue]Logged in using username and password, session file created - {username}[/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Failed to login using username and password: {e}[/bold red]")

def update_session_file(client, session_file='session.json'):
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        session_data['authorization_data'] = {
            'ds_user_id': client.user_id,
            'sessionid': client.sessionid
        }
        session_data['cookies'] = client.cookie_dict
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=4)
        console.print("[bold blue]Session file updated with user ds_user_id and cookies.[/bold blue]")

def relogin(client, username, password, session_file='session.json'):
    console.print("[bold blue]Attempting to re-login to Instagram...[/bold blue]")
    client.relogin()
    client.set_timezone_offset(-21600)  # Ensure timezone offset is set during re-login
    update_session_file(client, session_file)
    console.print("[bold blue]Re-login successful and session file updated.[/bold blue]")

if __name__ == "__main__":
    config = {
        'key': 'your_generated_key_here',
        'instagram': {
            'username': 'your_encrypted_username_here',
            'password': 'your_encrypted_password_here'
        }
    }
    username, password = decrypt_credentials(config)
    client = Client()
    login(client, username, password)
    update_session_file(client)
