import json
import os
import random
import logging
import time
from rich.console import Console
from datetime import datetime
from time import sleep

console = Console()

def random_sleep(min_time=5, max_time=30, action="", profile_reel_id=""):
    """Sleep for a random amount of time between `min_time` and `max_time`, and log the wait."""
    sleep_time = random.uniform(min_time, max_time)
    logging.info(f"Sleeping for {sleep_time:.2f} seconds before {action}.")
    log_random_waits(sleep_time, profile_reel_id)
    sleep(sleep_time)  # Perform the actual sleep
    return sleep_time

def log_random_waits(sleep_time, profile_reel_id):
    """Log random wait times to a JSON file."""
    random_waits_file = 'random-waits.json'
    initialize_json_file(random_waits_file, default=[])
    
    with open(random_waits_file, 'r') as f:
        random_waits = json.load(f)
        
    random_waits.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    
    with open(random_waits_file, 'w') as f:
        json.dump(random_waits, f, indent=4)
        
    console.print(f"[bold green]Logged random wait: {sleep_time:.2f} seconds for {profile_reel_id}[/bold green]")

def log_random_upload_times(sleep_time, profile_reel_id):
    """Log random upload times to a JSON file."""
    random_upload_time_file = 'random-upload-times.json'
    initialize_json_file(random_upload_time_file, default=[])
    
    with open(random_upload_time_file, 'r') as f:
        random_times = json.load(f)
    
    random_times.append({'time': sleep_time, 'profile_reel_id': profile_reel_id})
    
    with open(random_upload_time_file, 'w') as f:
        json.dump(random_times, f, indent=4)
        
    console.print(f"[bold green]Logged random upload time: {sleep_time:.2f} seconds for {profile_reel_id}[/bold green]")

def initialize_json_file(file_path, default):
    """Create a JSON file with a default structure if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default, f, indent=4)
        console.print(f"[bold green]Created new JSON file: {file_path}[/bold green]")

def update_status(**kwargs):
    """Update the status file with provided keyword arguments, merging lists where necessary."""
    status_file = 'status.json'
    status = read_status()

    # Update the status dictionary with the provided keyword arguments
    for key, value in kwargs.items():
        if key in status and isinstance(status[key], list) and isinstance(value, list):
            # Merge lists and ensure no duplicates
            combined_list = list(set(status[key] + value))
            status[key] = combined_list
        else:
            status[key] = value  # Overwrite or add new key-value pairs

    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4, default=str)
    console.print("[bold green]Updated status file.[/bold green]")

def read_status():
    """Read the status from the JSON file, creating it with default values if necessary."""
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
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            for key in ["last_scrape_time", "next_scrape_time", "last_upload_time", "next_upload_time", 
                        "last_story_upload_time", "next_story_upload_time", "last_delete_time"]:
                if isinstance(status.get(key), str):
                    status[key] = datetime.strptime(status[key], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            console.print("[bold green]Loaded existing status file.[/bold green]")
            return status
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[bold red]Error reading status file: {e}. Using default status.[/bold red]")
    else:
        console.print("[bold yellow]No existing status file found, using default status.[/bold yellow]")
    
    return default_status

def initialize_status_file():
    """Create the status file with default values if it doesn't exist."""
    status_file = 'status.json'
    if not os.path.exists(status_file):
        default_status = read_status()  # Use default status from `read_status`
        with open(status_file, 'w') as f:
            json.dump(default_status, f, indent=4, default=str)
        console.print("[bold green]Initialized new status file.[/bold green]")

def sleep_with_progress_bar(duration):
    """Sleep for `duration` seconds, showing a progress bar."""
    from tqdm import tqdm
    interval = 10  # Set the interval to 10 seconds
    total_intervals = int(duration) // interval  # Number of full intervals
    remainder = int(duration) % interval  # Remaining time after full intervals

    console.print(f"[bold blue]Sleeping for {duration:.2f} seconds in 10-second intervals.[/bold blue]")
    
    for _ in tqdm(range(total_intervals), desc="Sleeping", unit="interval", ncols=100):
        sleep(interval)
    
    if remainder > 0:
        sleep(remainder)
        tqdm.write(f"Finished sleeping additional {remainder} seconds.")

    console.print("[bold blue]Finished sleeping.[/bold blue]")

def delete_old_reels(delete_interval_minutes, config):
    """Delete old reels that have been uploaded, based on the configured interval."""
    status = read_status()
    last_delete_time = status.get('last_delete_time', 0) or 0
    current_time = datetime.now().timestamp()

    if (current_time - last_delete_time) >= delete_interval_minutes * 60:
        console.print("[bold blue]Starting the deletion process...[/bold blue]")
        delete_uploaded_files(config)
        console.print("[bold blue]Deletion process completed.[/bold blue]")

def delete_uploaded_files(config):
    """Delete media files that have already been uploaded, logging any deleted files."""
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
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    console.print(f"[bold green]Deleted file:[/bold green] {file_path}")
                except Exception as e:
                    console.print(f"[bold red]Error deleting file {file_path}: {e}[/bold red]")

    if deleted_files:
        # Update status after successful deletion
        update_status(
            last_delete_time=time.time(),
            next_deletion_time=time.time() + config['deleting']['delete_interval_minutes'] * 60
        )
        console.print(f"[bold green]Updated status with last delete time: {datetime.now()}[/bold green]")
    else:
        console.print("[bold yellow]No matching files found to delete.[/bold yellow]")

def read_upload_log():
    """Read the upload log to determine which files have been uploaded."""
    log_file = 'upload_log.txt'
    if not os.path.exists(log_file):
        console.print("[bold red]Upload log file not found.[/bold red]")
        return []
    with open(log_file, 'r') as f:
        uploads = f.readlines()
    return [upload.strip() for upload in uploads]
