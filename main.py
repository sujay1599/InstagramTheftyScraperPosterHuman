import logging
import os
import random
import json
from time import time, sleep
from tqdm import tqdm
from config_setup import load_config
from auth import login, decrypt_credentials
from instagrapi import Client
from scrape import scrape_reels, perform_human_actions
from upload import upload_reels_with_new_descriptions, get_unuploaded_reels, load_uploaded_reels
from utils import initialize_status_file, read_status, update_status, random_sleep, log_random_upload_times, log_random_waits, initialize_json_file
import subprocess

DEFAULT_TAGS = [
    'instagram', 'instadaily', 'LikeForFollow', 'LikesForLikes', 'LikeForLikes', 
    'FollowForFollow', 'LikeForLike', 'FollowForFollowBack', 'FollowBack', 
    'FollowMe', 'instalike', 'comment', 'follow', 'memes', 'funnymemes', 
    'memestagram', 'dankmemes', 'memelord', 'instamemes'
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the downloads directory exists
downloads_dir = 'downloads'
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)
    logging.info(f"Created directory: {downloads_dir}")

# Delete old files if they exist
for file in ['status.json', 'last_scraped_timestamp.txt', 'random-upload-times.json', 'random-waits.json']:
    if os.path.exists(file):
        os.remove(file)
        logging.info(f"Deleted {file}")

# Initialize files
initialize_status_file()
logging.info("Initialized status file")

# Initialize random-upload-times.json and random-waits.json
initialize_json_file('random-upload-times.json')
initialize_json_file('random-waits.json')

config = load_config()
logging.info("Loaded configuration")

INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD = decrypt_credentials(config)
logging.info("Decrypted Instagram credentials")

cl = Client()

login(cl, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, 'session.json')
logging.info("Logged in to Instagram")

def sleep_with_progress_bar(duration):
    for _ in tqdm(range(int(duration)), desc="Sleeping", unit="s"):
        sleep(1)

def main():
    status = read_status()
    logging.info("Read initial status")

    uploaded_reels = load_uploaded_reels('upload_log.txt')
    logging.info(f"Loaded uploaded reels: {len(uploaded_reels)} reels")

    custom_tags = config.get('custom_tags', [])
    tags = custom_tags if custom_tags else DEFAULT_TAGS

    while True:
        current_time = time()
        logging.debug(f"Current time: {current_time}")

        last_scrape_time = status.get('last_scrape_time', 0) or 0
        last_upload_time = status.get('last_upload_time', 0) or 0
        logging.debug(f"Last scrape time: {last_scrape_time}, Last upload time: {last_upload_time}")

        if (current_time - last_scrape_time) >= 60 * 60:
            if config['scraping']['enabled']:
                for profile in config['scraping']['profiles'].split():
                    logging.info(f"Scraping profile: {profile}")
                    scraped_reels = scrape_reels(cl, profile, config['scraping']['num_reels'], last_scrape_time, uploaded_reels, status['reels_scraped'])
                    status['reels_scraped'].extend(scraped_reels)
                    update_status(last_scrape_time=current_time, reels_scraped=status['reels_scraped'])
                    logging.info("Updated status after scraping")
                logging.info("Finished scraping reels from profiles")
                logging.info("Displaying dashboard before waiting phase")
                subprocess.run(["python", "dashboard.py"])

                # Randomly perform human-like actions
                if random.random() < 0.5:
                    perform_human_actions(cl, tags)
                wait_time = random_sleep(60, 90, action="uploading phase")  # Increased wait time before moving to uploading
                logging.info(f"Waited for {wait_time:.2f} seconds before moving to the uploading phase")
                sleep_with_progress_bar(wait_time)

        if (current_time - last_upload_time) >= config['uploading']['upload_interval_minutes'] * 60:
            if config['uploading']['enabled']:
                logging.info("Starting upload process")
                unuploaded_reels = get_unuploaded_reels('downloads', status['reels_scraped'], uploaded_reels)
                upload_reels_with_new_descriptions(cl, config, unuploaded_reels, uploaded_reels, 'upload_log.txt')
                update_status(last_upload_time=current_time)
                logging.info("Finished uploading reels")

                # Randomly perform human-like actions
                if random.random() < 0.5:
                    perform_human_actions(cl, tags)

                logging.info("Displaying dashboard before waiting phase")
                subprocess.run(["python", "dashboard.py"])

        # Randomly perform human-like actions during the waiting period
        if random.random() < 0.5:
            perform_human_actions(cl, tags)

        sleep_with_progress_bar(60)
        logging.debug("Sleeping for 60 seconds before next iteration")

if __name__ == "__main__":
    main()
