import json
import os
import random
import logging
from rich.console import Console
from datetime import datetime
from time import sleep

console = Console()

def random_sleep(min_time=5, max_time=30, action="", profile_reel_id=""):
    sleep_time = random.uniform(min_time, max_time)
    logging.info(f"Sleeping for {sleep_time:.2f} seconds before {action}.")
    log_random_waits(sleep_time, profile_reel_id)
    return sleep_time

def log_random_waits(sleep_time, profile_reel_id):
    random_waits_file = 'random-waits.json'
    initialize_json_file(random_waits_file, default=[])
    with open(random_waits_file, 'r') as f:
        random_waits = json.load(f)
    random_waits.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    with open(random_waits_file, 'w') as f:
        json.dump(random_waits, f, indent=4)
    console.print(f"[bold green]Logged random wait: {sleep_time:.2f} seconds for {profile_reel_id}[/bold green]")

def log_random_upload_times(sleep_time, profile_reel_id):
    random_upload_time_file = 'random-upload-times.json'
    initialize_json_file(random_upload_time_file, default=[])
    with open(random_upload_time_file, 'r') as f:
        random_times = json.load(f)
    random_times.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    with open(random_upload_time_file, 'w') as f:
        json.dump(random_times, f, indent=4)
    console.print(f"[bold green]Logged random upload time: {sleep_time:.2f} seconds for {profile_reel_id}[/bold green]")

def initialize_json_file(file_path, default):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default, f, indent=4)
        console.print(f"[bold green]Created new JSON file: {file_path}[/bold green]")

def update_status(**kwargs):
    status_file = 'status.json'
    status = read_status()
    status.update(kwargs)
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4, default=str)
    console.print("[bold green]Updated status file.[/bold green]")

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
        "next_file_to_upload": "N/A",
        "reels_uploaded": []
    }
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
            for key in ["last_scrape_time", "next_scrape_time", "last_upload_time", "next_upload_time", "last_story_upload_time", "next_story_upload_time", "last_delete_time"]:
                if status[key] is None:
                    status[key] = 0
                elif isinstance(status[key], str):
                    status[key] = datetime.strptime(status[key], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            console.print("[bold green]Loaded existing status file.[/bold green]")
            return status
    console.print("[bold yellow]No existing status file found, using default status.[/bold yellow]")
    return default_status

def initialize_status_file():
    status_file = 'status.json'
    if not os.path.exists(status_file):
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
            "next_file_to_upload": "N/A",
            "reels_uploaded": []
        }
        with open(status_file, 'w') as f:
            json.dump(default_status, f, indent=4, default=str)
        console.print("[bold green]Initialized new status file.[/bold green]")

def sleep_with_progress_bar(duration):
    from tqdm import tqdm
    console.print(f"[bold blue]Sleeping for {duration} seconds.[/bold blue]")
    for _ in tqdm(range(int(duration)), desc="Sleeping", unit="s"):
        sleep(1)
    console.print("[bold blue]Finished sleeping.[/bold blue]")

def delete_old_reels(delete_interval_minutes):
    status = read_status()
    last_delete_time = status.get('last_delete_time', 0) or 0
    current_time = datetime.now().timestamp()

    if (current_time - last_delete_time) >= delete_interval_minutes * 60:
        console.print("[bold blue]Starting the deletion process...[/bold blue]")
        delete_uploaded_files()
        console.print("[bold blue]Deletion process completed.[/bold blue]")

def delete_uploaded_files():
    upload_log = read_upload_log()
    if not upload_log:
        console.print("[bold yellow]No files to delete.[/bold yellow]")
        return

    deleted_files = []
    for log_entry in upload_log:
        file_prefix = log_entry
        for extension in ['.mp4', '.txt', '.mp4.jpg']:
            file_path = os.path.join('downloads', file_prefix + extension)
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_path)
                console.print(f"[bold green]Deleted file:[/bold green] {file_path}")

    if deleted_files:
        update_status(last_delete_time=datetime.now().timestamp())
        console.print(f"[bold green]Updated status with last delete time: {datetime.now()}[/bold green]")
    else:
        console.print("[bold yellow]No matching files found to delete.[/bold yellow]")

def read_upload_log():
    log_file = 'upload_log.txt'
    if not os.path.exists(log_file):
        console.print("[bold red]Upload log file not found.[/bold red]")
        return []
    with open(log_file, 'r') as f:
        uploads = f.readlines()
    return [upload.strip() for upload in uploads]
