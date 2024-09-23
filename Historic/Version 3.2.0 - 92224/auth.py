import json
import logging
import os
from instagrapi import Client
from cryptography.fernet import Fernet
from rich.console import Console

console = Console()

def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()

def encrypt_credentials(username, password, key):
    """Encrypt the username and password using the provided key."""
    cipher_suite = Fernet(key)
    encrypted_username = cipher_suite.encrypt(username).decode()
    encrypted_password = cipher_suite.encrypt(password).decode()
    return encrypted_username, encrypted_password

def decrypt_credentials(config):
    """Decrypt Instagram credentials from the config."""
    key = config['key'].encode()
    cipher_suite = Fernet(key)
    decrypted_username = cipher_suite.decrypt(config['instagram']['username'].encode()).decode()
    decrypted_password = cipher_suite.decrypt(config['instagram']['password'].encode()).decode()
    return decrypted_username, decrypted_password

def perform_login(client, username, password, session_file):
    """Login to Instagram using instagrapi Client."""
    if os.path.exists(session_file):
        try:
            client.load_settings(session_file)
            client.login(username, password)
            console.print("[bold green]Logged in using existing session file[/bold green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Failed to log in using session file: {e}[/bold red]")
            os.remove(session_file)
            return perform_login(client, username, password, session_file)
    else:
        try:
            client.login(username, password)
            client.dump_settings(session_file)
            console.print("[bold green]Successfully logged in and session saved[/bold green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Login failed: {e}[/bold red]")
            return False

def update_session_file(client, session_file):
    """Update the session file with the latest session details."""
    try:
        client.dump_settings(session_file)
        logging.info(f"Session file updated: {session_file}")
    except Exception as e:
        logging.error(f"Failed to update session file: {e}")

def inject_cookies(client, session_file):
    """Inject cookies from session to client."""
    try:
        with open(session_file, 'r') as f:
            settings = json.load(f)
        client.set_settings(settings)
        logging.info("Cookies injected successfully")
    except Exception as e:
        logging.error(f"Failed to inject cookies: {e}")

def relogin(client, username, password, session_file):
    """Re-login to Instagram, handling rate limits or session issues."""
    try:
        client.relogin()
        update_session_file(client, session_file)
        console.print(f"[bold green]Re-logged in successfully[/bold green]")
    except Exception as e:
        logging.error(f"Re-login failed: {e}")
        console.print(f"[bold red]Re-login failed: {e}. Attempting fresh login...[/bold red]")
        perform_login(client, username, password, session_file)
