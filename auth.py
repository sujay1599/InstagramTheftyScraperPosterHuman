from cryptography.fernet import Fernet
from instagrapi import Client
import os
import logging

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
            logging.info("Logged in using session file")
        except Exception as e:
            logging.error(f"Failed to login using session file: {e}")
            _login_with_credentials(client, username, password, session_file)
    else:
        _login_with_credentials(client, username, password, session_file)

def _login_with_credentials(client, username, password, session_file):
    try:
        client.login(username, password)
        client.dump_settings(session_file)
        logging.info("Logged in using username and password, session file created")
    except Exception as e:
        logging.error(f"Username/password login failed: {e}")
        exit(1)
