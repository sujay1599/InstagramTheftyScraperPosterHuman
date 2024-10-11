# Main function that handles scraping, uploading, and other bot tasks.

# This function contains the main loop of the bot, which scrapes reels from
# Instagram profiles, uploads them to TikTok, and performs human-like actions
# to mimic a real user. The function also handles rate limits and re-logins
# if needed, with exponential backoff.

# The function also displays a dashboard after each scraping and uploading
# phase, which shows the current status of the bot.

# Note: This function runs indefinitely until an error occurs or the user
# manually stops the program with Ctrl+C.
#V3.2.2

import logging
import os
import random
import time
from time import sleep as time_sleep
from config_setup import load_config  # This should now be correct in config_setup.py
from auth import perform_login, update_session_file, decrypt_credentials, relogin, Client, inject_cookies
from scrape import scrape_reels, perform_human_actions, display_version_info
from upload import upload_reels_with_new_descriptions, get_unuploaded_reels, load_uploaded_reels
from utils import (
    initialize_status_file, read_status, update_status, random_sleep,
    log_random_upload_times, log_random_waits, initialize_json_file,
    sleep_with_progress_bar, delete_old_reels
)
import subprocess
from rich.console import Console
import signal
import sys
import json

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Signal handler to catch keyboard interrupts
def signal_handler(sig, frame):
    console.print("\n[bold red]KeyboardInterrupt detected! Exiting gracefully...[/bold red]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Ensure the downloads directory exists
downloads_dir = 'downloads'
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)
    logging.info(f"Created directory: {downloads_dir}")

# Initialize necessary JSON files
if not os.path.exists('status.json'):
    initialize_status_file()
    logging.info("Initialized status file")

if not os.path.exists('random-upload-times.json'):
    initialize_json_file('random-upload-times.json', default=[])
    logging.info("Created new random-upload-times.json file")

if not os.path.exists('random-waits.json'):
    initialize_json_file('random-waits.json', default=[])
    logging.info("Created new random-waits.json file")

# Function to get the latest JSON session file created by config_setup.py
def get_latest_json_file(directory):
    try:
        json_files = [
            f for f in os.listdir(directory)
            if f.endswith('_session.json') and os.path.isfile(os.path.join(directory, f))
        ]
        if not json_files:
            raise FileNotFoundError("No JSON session files found in the directory.")
        
        # Sort the files by modification time, with the most recent first
        json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
        
        # Return the full path to the most recent JSON file
        return os.path.join(directory, json_files[0])
    except Exception as e:
        logging.error(f"Error finding JSON session file: {e}")
        return None

# Load configuration
try:
    # Automatically select the most recent session file and config file
    session_directory = './user_sessions/'  # Adjust this path to your actual session directory
    latest_json_file = get_latest_json_file(session_directory)
    
    if latest_json_file:
        # Extract the username from the filename (e.g., username_session.json -> username)
        filename = os.path.basename(latest_json_file)
        if '_session.json' in filename:
            last_username = filename.replace('_session.json', '')
            logging.info(f"Extracted username '{last_username}' from session file name.")
        else:
            raise ValueError("Session file name does not follow the expected format 'username_session.json'.")
        
        # Load the configuration for this user
        config = load_config(last_username)
        logging.info(f"Loaded configuration for user: {last_username} from session file: {latest_json_file}")
    else:
        raise FileNotFoundError("No JSON session files available to load.")
    
    # Verify that the corresponding config file exists
    config_file = os.path.join('configs', f"{last_username}_config.yaml")
    if not os.path.exists(config_file):
        logging.error(f"Config file {config_file} not found. Please run config_setup.py first to generate the configuration file.")
        raise FileNotFoundError(f"Config file {config_file} not found")
    
except (FileNotFoundError, ValueError) as e:
    console.print(f"[bold red]Error: {e}. Make sure to run config_setup.py first to generate the configuration file.[/bold red]")
    sys.exit(1)

# Validate configuration
required_scraping_keys = ['profiles', 'num_reels', 'scrape_interval_minutes']
for key in required_scraping_keys:
    if key not in config.get('scraping', {}):
        logging.error(f"Missing required configuration key: scraping.{key}")
        console.print(f"[bold red]Missing required configuration key: scraping.{key}[/bold red]")
        sys.exit(1)

# Decrypt Instagram credentials
INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD = decrypt_credentials(config)
logging.info("Decrypted Instagram credentials")

# Initialize Instagram client
cl = Client()

# Set delay range to mimic human behavior
cl.delay_range = [2, 5]

# Set proxy if available in configuration
proxy = config.get('proxy')
if proxy:
    cl.set_proxy(proxy)

# Perform initial login
session_file = os.path.join('user_sessions', f"{INSTAGRAM_USERNAME}_session.json")
perform_login(cl, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, session_file)
update_session_file(cl, session_file)
logging.info("Logged in to Instagram")

# Inject cookies for public requests (if needed)
inject_cookies(cl, session_file)

def handle_rate_limit(client, func, *args, **kwargs):
    """Handle rate limits and re-login if needed, with exponential backoff."""
    retries = 5
    for attempt in range(retries):
        try:
            console.print(f"[bold blue]Attempting call {attempt+1}/{retries}[/bold blue]")
            return func(*args, **kwargs)
        except Exception as e:
            console.print(f"[bold red]Error on attempt {attempt+1}/{retries}[/bold red]")
            console.print(f"Error message: {e}")
            if '429' in str(e) or 'login_required' in str(e):  # Rate limit or login required error
                sleep_time = min(2 ** attempt, 300)  # Exponential backoff up to 5 minutes
                console.print(f"Rate limit or login required. Retrying in {sleep_time} seconds...")
                time_sleep(sleep_time)
                console.print(f"[bold yellow]Re-logging in after attempt {attempt+1}[/bold yellow]")
                relogin(client, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, session_file)
            else:
                logging.error(f"Error: {e}")
                raise e
    raise Exception("Max retries exceeded")

def main():
    try:
        display_version_info()  # Display version control information
        # Load status
        status = read_status()
        # Set initial values for the main loop
        last_upload_time = status.get('last_upload_time', 0)
        last_scrape_time = status.get('last_scrape_time', 0)
        reels_scraped = set(status.get('reels_scraped', []))  # Use set to ensure uniqueness
        # Define tags from the configuration
        tags = config.get('custom_tags', [])
        default_comments = config.get('comments', [])
        default_descriptions = config.get('description', {}).get('custom_descriptions', [])
        
        while True:
            current_time = time.time()
            # Check if it's time to scrape reels
            if current_time - last_scrape_time >= config['scraping']['scrape_interval_minutes'] * 60:
                try:
                    profiles = config['scraping']['profiles'].split()
                    uploaded_reels = load_uploaded_reels('upload_log.txt')
                    for profile in profiles:
                        try:
                            # Scrape reels from the given profile
                            scraped_reels = handle_rate_limit(
                                cl,
                                scrape_reels,
                                cl,
                                profile,
                                config['scraping']['num_reels'],
                                last_scrape_time,
                                uploaded_reels,
                                list(reels_scraped),
                                tags
                            )
                            reels_scraped.update(scraped_reels)  # Update set with new scraped reels
                            # Update status after scraping
                            update_status(last_scrape_time=current_time, reels_scraped=list(reels_scraped))  # Convert back to list for JSON
                            logging.info("Updated status after scraping")
                        except Exception as e:
                            logging.error(f"Error scraping profile {profile}: {e}")
                            # Corrected closing tag from '}' to ']'
                            console.print(f"[bold red]Error scraping profile {profile}: {e}[/bold red]")
                    console.print("[bold purple4]Finished scraping reels from profiles[/bold purple4]")
                    console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                    subprocess.run(["python", "dashboard.py"])
                except Exception as e:
                    logging.error(f"Error in scraping loop: {e}")
                    # Corrected closing tag from '}' to ']'
                    console.print(f"[bold red]Error in scraping loop: {e}[/bold red]")

            # Check if it's time to upload reels
            uploaded_reels = load_uploaded_reels('upload_log.txt')
            unuploaded_reels = get_unuploaded_reels('downloads', list(reels_scraped), uploaded_reels)
            if current_time - last_upload_time >= config['uploading']['upload_interval_minutes'] * 60:
                try:
                    # Check if there are any unuploaded reels
                    if not unuploaded_reels:
                        console.print("[bold yellow]No new reels to upload. Restarting scraping...[/bold yellow]")
                        continue  # Restart the scraping process

                    # Proceed to upload if there are unuploaded reels
                    handle_rate_limit(
                        cl,
                        upload_reels_with_new_descriptions,
                        cl,
                        config,
                        unuploaded_reels,
                        uploaded_reels,
                        'upload_log.txt',
                        session_file
                    )
                    # Update status after uploading
                    update_status(last_upload_time=current_time)
                    console.print("[bold purple4]Finished uploading reels[/bold purple4]")
                    # Randomly perform human-like actions
                    if random.random() < 0.01:
                        perform_human_actions(cl, tags)
                    console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                    subprocess.run(["python", "dashboard.py"])
                except Exception as e:
                    logging.error(f"Error in upload loop: {e}")
                    # Corrected closing tag from '}' to ']'
                    console.print(f"[bold red]Error in upload loop: {e}[/bold red]")

            # Randomly perform human-like actions during the waiting period
            if random.random() < 0.01:
                perform_human_actions(cl, tags)

            # Delete old reels based on the deletion interval
            try:
                delete_old_reels(config['deleting']['delete_interval_minutes'], config)
            except Exception as e:
                logging.error(f"Error in deletion process: {e}")
                # Corrected closing tag from '}' to ']'
                console.print(f"[bold red]Error in deletion process: {e}[/bold red]")

            sleep_with_progress_bar(60)
            logging.debug("Sleeping for 60 seconds before next iteration")
    
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting program...[/bold red]")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        # Corrected closing tag from '}' to ']'
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
