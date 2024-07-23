print("="*80)
print("Created by: Sujay1599")
print("Program: InstgramTheftyScraperPosterHuman")
print("Working as of: 7/20/2024")
print("="*80)

import logging
import os
import random
import time
from time import time, sleep
from tqdm import tqdm
from config_setup import load_config
from auth import login, decrypt_credentials, update_session_file, relogin
from instagrapi import Client
from scrape import scrape_reels, perform_human_actions
from upload import upload_reels_with_new_descriptions, get_unuploaded_reels, load_uploaded_reels
from utils import initialize_status_file, read_status, update_status, random_sleep, log_random_upload_times, log_random_waits, initialize_json_file, sleep_with_progress_bar, delete_old_reels
import subprocess
from rich.console import Console

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Ensure the downloads directory exists
downloads_dir = 'downloads'
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)
    logging.info(f"Created directory: {downloads_dir}")

# Initialize files
initialize_status_file()
logging.info("Initialized status file")

# Initialize random-upload-times.json and random-waits.json
initialize_json_file('random-upload-times.json', default=[])
initialize_json_file('random-waits.json', default=[])

# Load configuration
config = load_config()
logging.info("Loaded configuration")

# Validate configuration
required_scraping_keys = ['profiles', 'num_reels', 'scrape_interval_minutes']
for key in required_scraping_keys:
    if key not in config['scraping']:
        logging.error(f"Missing required configuration key: scraping.{key}")
        exit(1)

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

# Function to perform login with retries
def perform_login(client, username, password, session_file):
    try:
        login(client, username, password, session_file)
    except Exception as e:
        console.print(f"[bold red]Login failed: {e}. Retrying after waiting.[/bold red]")
        sleep(300)  # Sleep for 5 minutes before retrying
        relogin(client, username, password, session_file)

# Perform initial login
perform_login(cl, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, 'session.json')
update_session_file(cl, 'session.json')
logging.info("Logged in to Instagram")

# Ensure UUIDs and timezone offset are reused if available
if os.path.exists('session.json'):
    old_session = cl.get_settings()
    if "uuids" in old_session:
        cl.set_uuids(old_session["uuids"])
    if "timezone_offset" in old_session:
        cl.set_timezone_offset(old_session["timezone_offset"])
else:
    # Set timezone offset to CST (Chicago) if session is not available
    cl.set_timezone_offset(-21600)

def handle_rate_limit(client, func, *args, **kwargs):
    retries = 5
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if '429' in str(e) or 'login_required' in str(e):  # Rate limit or login required error
                sleep_time = min(2 ** attempt, 300)  # Exponential backoff up to 5 minutes
                console.print(f"Rate limit or login required. Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                relogin(client, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, 'session.json')
            else:
                raise e
    raise Exception("Max retries exceeded")

# Main loop
def main():
    # Load status
    status = read_status()

    # Set initial values for the main loop
    last_upload_time = status.get('last_upload_time', 0)
    last_scrape_time = status.get('last_scrape_time', 0)
    reels_scraped = status.get('reels_scraped', [])

    # Define tags from the configuration
    tags = config.get('custom_tags', [])

    while True:
        current_time = time()
        
        # Check if it's time to scrape reels
        if current_time - last_scrape_time >= config['scraping']['scrape_interval_minutes'] * 60:
            try:
                profiles = config['scraping']['profiles'].split()
                uploaded_reels = load_uploaded_reels('upload_log.txt')  # Initialize uploaded_reels here
                for profile in profiles:
                    try:
                        scraped_reels = handle_rate_limit(cl, scrape_reels, cl, profile, config['scraping']['num_reels'], last_scrape_time, uploaded_reels, reels_scraped, tags)
                        reels_scraped.extend(scraped_reels)
                        update_status(last_scrape_time=current_time, reels_scraped=reels_scraped)
                        logging.info("Updated status after scraping")
                    except Exception as e:
                        logging.error(f"Error scraping profile {profile}: {e}")
                        console.print(f"[bold red]Error scraping profile {profile}: {e}[/bold red]")

                console.print("[bold purple4]Finished scraping reels from profiles[/bold purple4]")
                console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                subprocess.run(["python", "dashboard.py"])
            except Exception as e:
                logging.error(f"Error in scraping loop: {e}")
                console.print(f"[bold red]Error in scraping loop: {e}[/bold red]")
        
        # Check if it's time to upload reels
        uploaded_reels = load_uploaded_reels('upload_log.txt')  # Ensure uploaded_reels is initialized
        unuploaded_reels = get_unuploaded_reels('downloads', reels_scraped, uploaded_reels)
        
        if current_time - last_upload_time >= config['uploading']['upload_interval_minutes'] * 60:
            try:
                handle_rate_limit(cl, upload_reels_with_new_descriptions, cl, config, unuploaded_reels, uploaded_reels, 'upload_log.txt')
                update_status(last_upload_time=current_time)
                console.print("[bold purple4]Finished uploading reels[/bold purple4]")

                # Randomly perform human-like actions
                if random.random() < 0.5:
                    perform_human_actions(cl, tags)

                console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                subprocess.run(["python", "dashboard.py"])
            except Exception as e:
                logging.error(f"Error in upload loop: {e}")
                console.print(f"[bold red]Error in upload loop: {e}[/bold red]")
        
        # Randomly perform human-like actions during the waiting period
        if random.random() < 0.5:
            perform_human_actions(cl, tags)

        # Delete old reels based on the deletion interval
        delete_old_reels(config['deleting']['delete_interval_minutes'])

        sleep_with_progress_bar(60)
        logging.debug("Sleeping for 60 seconds before next iteration")

if __name__ == "__main__":
    main()
