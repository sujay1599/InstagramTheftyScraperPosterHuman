import json
import os
import random
import logging
from datetime import datetime
from time import sleep


def random_sleep(min_time=5, max_time=30, action="", profile_reel_id=""):
    sleep_time = random.uniform(min_time, max_time)
    logging.info(f"Sleeping for {sleep_time:.2f} seconds before {action}.")
    log_random_waits(sleep_time, profile_reel_id)
    return sleep_time

def log_random_waits(sleep_time, profile_reel_id):
    random_waits_file = 'random-waits.json'
    initialize_json_file(random_waits_file)
    with open(random_waits_file, 'r') as f:
        random_waits = json.load(f)
    random_waits.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    with open(random_waits_file, 'w') as f:
        json.dump(random_waits, f)

def log_random_upload_times(sleep_time, profile_reel_id):
    random_upload_time_file = 'random-upload-times.json'
    initialize_json_file(random_upload_time_file)
    with open(random_upload_time_file, 'r') as f:
        random_times = json.load(f)
    random_times.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    with open(random_upload_time_file, 'w') as f:
        json.dump(random_times, f)

def initialize_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

def update_status(**kwargs):
    status_file = 'status.json'
    default_status = {
        "last_scrape_time": 0,
        "next_scrape_time": 0,
        "reels_scraped": [],
        "last_upload_time": 0,
        "next_upload_time": 0,
        "last_story_upload_time": 0,
        "next_story_upload_time": 0,
        "last_delete_time": 0,
        "random_upload_times": [],
        "random_waits": [],
        "next_file_to_upload": "N/A"
    }
    status = default_status.copy()
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status.update(json.load(f))
    
    status.update(kwargs)
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4, default=str)

def read_status():
    status_file = 'status.json'
    default_status = {
        "last_scrape_time": 0,
        "next_scrape_time": 0,
        "reels_scraped": [],
        "last_upload_time": 0,
        "next_upload_time": 0,
        "last_story_upload_time": 0,
        "next_story_upload_time": 0,
        "last_delete_time": 0,
        "random_upload_times": [],
        "random_waits": [],
        "next_file_to_upload": "N/A"
    }
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
            for key in ["last_scrape_time", "next_scrape_time", "last_upload_time", "next_upload_time", "last_story_upload_time", "next_story_upload_time", "last_delete_time"]:
                if status[key] is None:
                    status[key] = 0
                elif isinstance(status[key], str):
                    status[key] = datetime.strptime(status[key], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            return status
    return default_status

def initialize_status_file():
    status_file = 'status.json'
    default_status = {
        "last_scrape_time": 0,
        "next_scrape_time": 0,
        "reels_scraped": [],
        "last_upload_time": 0,
        "next_upload_time": 0,
        "last_story_upload_time": 0,
        "next_story_upload_time": 0,
        "last_delete_time": 0,
        "random_upload_times": [],
        "random_waits": [],
        "next_file_to_upload": "N/A"
    }
    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            json.dump(default_status, f, indent=4, default=str)

def sleep_with_progress_bar(duration):
    from tqdm import tqdm
    for _ in tqdm(range(int(duration)), desc="Sleeping", unit="s"):
        sleep(1)
