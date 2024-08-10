import json
import os
import logging
import time
from instagrapi import Client
from cryptography.fernet import Fernet
from rich.console import Console
from instagrapi.exceptions import LoginRequired, PrivateError

console = Console()
logger = logging.getLogger()

# Define the directory for user sessions
SESSION_DIR = 'user_sessions'

# Ensure the session directory exists
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
    logger.info(f"Created directory for user sessions: {SESSION_DIR}")

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

def save_session(client, session_file):
    settings = client.get_settings()
    settings['last_login'] = time.time()
    with open(session_file, 'w') as f:
        json.dump(settings, f, indent=4)
    console.print(f"[bold blue]Session file created/updated: {session_file}[/bold blue]")
    logger.info(f"Session file created/updated: {session_file}")

def load_session(client, session_file):
    if os.path.exists(session_file):
        client.load_settings(session_file)
        console.print(f"[bold blue]Loaded session from {session_file}[/bold blue]")
        logger.info(f"Loaded session from {session_file}")
        return True
    return False

def perform_login(client, username, password, session_file, verification_code=None):
    """Handles logging in with or without 2FA enabled."""
    if load_session(client, session_file):
        try:
            client.login(username, password)
            client.get_timeline_feed()  # Ensure session is still valid
            console.print("[bold blue]Logged in using session file[/bold blue]")
            logger.info("Logged in using session file")
            client.login_flow()  # Simulate real user behavior after login
            return True
        except LoginRequired:
            console.print("[bold red]Session is invalid, logging in with username and password[/bold red]")
            logger.warning("Session is invalid, logging in with username and password")
            return login_with_credentials(client, username, password, session_file, verification_code)
    else:
        return login_with_credentials(client, username, password, session_file, verification_code)

def login_with_credentials(client, username, password, session_file, verification_code=None):
    try:
        if verification_code:
            client.login(username, password, verification_code=verification_code)
        else:
            client.login(username, password)
        
        client.set_timezone_offset(-21600)  # Set CST (Chicago) timezone offset
        client.inject_sessionid_to_public()  # Inject sessionid to public session
        save_session(client, session_file)
        console.print(f"[bold blue]Logged in using username and password, session file created - {username}[/bold blue]")
        logger.info(f"Logged in using username and password, session file created - {username}")
        client.login_flow()  # Simulate real user behavior after login
        return True
    except Exception as e:
        console.print(f"[bold red]Failed to login using username and password: {e}[/bold red]")
        logger.error(f"Failed to login using username and password: {e}")
        return False

def relogin(client, session_file):
    console.print("[bold blue]Attempting to re-login to Instagram...[/bold blue]")
    logger.info("Attempting to re-login to Instagram")
    try:
        client.relogin()
        client.set_timezone_offset(-21600)  # Ensure timezone offset is set during re-login
        save_session(client, session_file)
        console.print("[bold blue]Re-login successful and session file updated.[/bold blue]")
        logger.info("Re-login successful and session file updated")
        client.login_flow()  # Simulate real user behavior after login
        return True
    except Exception as e:
        console.print(f"[bold red]Failed to re-login: {e}[/bold red]")
        logger.error(f"Failed to re-login: {e}")
        return False

def login_by_sessionid(client, sessionid, session_file):
    try:
        client.login_by_sessionid(sessionid)
        client.inject_sessionid_to_public()
        client.set_timezone_offset(-21600)  # Set CST (Chicago) timezone offset
        save_session(client, session_file)
        console.print(f"[bold blue]Logged in using sessionid, session file created - {sessionid}[/bold blue]")
        logger.info(f"Logged in using sessionid, session file created - {sessionid}")
        client.login_flow()  # Simulate real user behavior after login
        return True
    except Exception as e:
        console.print(f"[bold red]Failed to login using sessionid: {e}[/bold red]")
        logger.error(f"Failed to login using sessionid: {e}")
        return False

def update_session_file(client, session_file):
    save_session(client, session_file)

if __name__ == "__main__":
    import time
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from a .env file

    config = {
        'key': os.getenv('ENCRYPTION_KEY'),  # Load key from environment variable
        'instagram': {
            'username': os.getenv('ENCRYPTED_USERNAME'),
            'password': os.getenv('ENCRYPTED_PASSWORD'),
            'original_username': os.getenv('INSTAGRAM_USERNAME')  # Load original username
        }
    }
    username, password = decrypt_credentials(config)
    session_file = os.path.join(SESSION_DIR, f"{config['instagram']['original_username']}_session.json")
    client = Client()
    client.delay_range = [1, 3]  # Mimic human behavior with delays between requests
    perform_login(client, username, password, session_file)
    update_session_file(client, session_file)
