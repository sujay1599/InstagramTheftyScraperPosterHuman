from cryptography.fernet import Fernet
from instagrapi import Client
import os
from rich.logging import RichHandler
import logging

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

def decrypt_credentials(config):
    key = config['key'].encode()
    cipher_suite = Fernet(key)
    username = cipher_suite.decrypt(config['instagram']['username'].encode()).decode()
    password = cipher_suite.decrypt(config['instagram']['password'].encode()).decode()
    return username, password

def login(client, username, password, session_file):
    if os.path.exists(session_file):
        try:
            client.load_settings(session_file)
            client.login(username, password)
            # Check session validity
            client.get_timeline_feed()
            logging.info(f"[bold blue]Logged in using session file - {username}[/bold blue]")
        except Exception as e:
            logging.error(f"[bold red]Failed to login using session file: {e}[/bold red]")
            _login_with_credentials(client, username, password, session_file)
    else:
        _login_with_credentials(client, username, password, session_file)

def _login_with_credentials(client, username, password, session_file):
    try:
        client.login(username, password)
        client.dump_settings(session_file)
        logging.info(f"[bold blue]Logged in using username and password, session file created - {username}[/bold blue]")
    except Exception as e:
        logging.error(f"[bold red]Username/password login failed: {e}[/bold red]")
        exit(1)

def main(config):
    client = Client()
    username, password = decrypt_credentials(config)
    session_file = 'session.json'
    
    # Load existing session or login
    login(client, username, password, session_file)
    
    # Ensure UUIDs are reused
    if os.path.exists(session_file):
        old_session = client.get_settings()
        client.set_uuids(old_session["uuids"])

    return client
