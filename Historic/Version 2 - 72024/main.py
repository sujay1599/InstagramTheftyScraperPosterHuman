print("="*80)
print("Created by: Sujay1599")
print("Program: InstgramTheftyScraperPosterHuman")
print("Working as of: 7/20/2024")
print("="*80)

import logging
import os
import random
from time import time, sleep
from tqdm import tqdm
from config_setup import load_config
from auth import login, decrypt_credentials
from instagrapi import Client
from scrape import scrape_reels, perform_human_actions
from upload import upload_reels_with_new_descriptions, get_unuploaded_reels, load_uploaded_reels
from utils import initialize_status_file, read_status, update_status, random_sleep, log_random_upload_times, log_random_waits, initialize_json_file, sleep_with_progress_bar, delete_old_reels
import subprocess
from rich.console import Console

console = Console()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

config = load_config()
logging.info("Loaded configuration")

INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD = decrypt_credentials(config)
logging.info("Decrypted Instagram credentials")

cl = Client()

login(cl, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, 'session.json')
logging.info("Logged in to Instagram")

def main():
    status = read_status()
    logging.info("Read initial status")

    uploaded_reels = load_uploaded_reels('upload_log.txt')
    logging.info(f"Loaded uploaded reels: {len(uploaded_reels)} reels")

    tags = config.get('custom_tags', [])

    while True:
        current_time = time()
        logging.debug(f"Current time: {current_time}")

        last_scrape_time = status.get('last_scrape_time', 0) or 0
        last_upload_time = status.get('last_upload_time', 0) or 0
        logging.debug(f"Last scrape time: {last_scrape_time}, Last upload time: {last_upload_time}")

        # Scraping logic
        if (current_time - last_scrape_time) >= 60 * 60:
            if config['scraping']['enabled']:
                for profile in config['scraping']['profiles'].split():
                    logging.info(f"Scraping profile: {profile}")
                    scraped_reels = scrape_reels(cl, profile, config['scraping']['num_reels'], last_scrape_time, uploaded_reels, status['reels_scraped'], tags)
                    status['reels_scraped'].extend(scraped_reels)
                    update_status(last_scrape_time=current_time, reels_scraped=status['reels_scraped'])
                    logging.info("Updated status after scraping")
                console.print("[bold navy_blue]Finished scraping reels from profiles[/bold navy_blue]")
                console.print("[bold navy_blue]Displaying dashboard before waiting phase[/bold navy_blue]")
                subprocess.run(["python", "dashboard.py"])

                # Randomly perform human-like actions
                if random.random() < 0.5:
                    perform_human_actions(cl, tags)
                wait_time = random_sleep(60, 90, action="uploading phase")
                console.print(f"[bold navy_blue]Waited for {wait_time:.2f} seconds before moving to the uploading phase[/bold navy_blue]")
                sleep_with_progress_bar(wait_time)

        # Uploading logic
        if (current_time - last_upload_time) >= config['uploading']['upload_interval_minutes'] * 60:
            if config['uploading']['enabled']:
                console.print("[bold purple4]Starting upload process[/bold purple4]")
                unuploaded_reels = get_unuploaded_reels('downloads', status['reels_scraped'], uploaded_reels)
                if not unuploaded_reels:
                    console.print("[bold purple4]No new reels to upload, initiating scraping protocol.[/bold purple4]")
                    for profile in config['scraping']['profiles'].split():
                        logging.info(f"Scraping profile: {profile}")
                        scraped_reels = scrape_reels(cl, profile, config['scraping']['num_reels'], last_scrape_time, uploaded_reels, status['reels_scraped'], tags)
                        status['reels_scraped'].extend(scraped_reels)
                        update_status(last_scrape_time=current_time, reels_scraped=status['reels_scraped'])
                        logging.info("Updated status after scraping")
                    console.print("[bold purple4]Finished scraping reels from profiles[/bold purple4]")
                    console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                    subprocess.run(["python", "dashboard.py"])
                else:
                    upload_reels_with_new_descriptions(cl, config, unuploaded_reels, uploaded_reels, 'upload_log.txt')
                    update_status(last_upload_time=current_time)
                    console.print("[bold purple4]Finished uploading reels[/bold purple4]")

                    # Randomly perform human-like actions
                    if random.random() < 0.5:
                        perform_human_actions(cl, tags)

                    console.print("[bold purple4]Displaying dashboard before waiting phase[/bold purple4]")
                    subprocess.run(["python", "dashboard.py"])

        # Randomly perform human-like actions during the waiting period
        if random.random() < 0.5:
            perform_human_actions(cl, tags)

        # Delete old reels based on the deletion interval
        delete_old_reels(config['deleting']['delete_interval_minutes'])

        sleep_with_progress_bar(60)
        logging.debug("Sleeping for 60 seconds before next iteration")

if __name__ == "__main__":
    main()
