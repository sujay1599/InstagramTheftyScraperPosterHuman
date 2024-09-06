import os
import logging
import random
import time
from datetime import datetime, timedelta
from time import sleep
import subprocess
from rich.console import Console
from utils import random_sleep, update_status, read_status, log_random_upload_times, sleep_with_progress_bar
from scrape import perform_human_actions
from default_descriptions import DEFAULT_DESCRIPTIONS
from auth import relogin  # Import the relogin function

console = Console()

def build_description(original_description, use_original, custom_description, use_hashtags, hashtags_list, give_credit, profile_username):
    """Build the description for the reel, including hashtags and credit to the original profile."""
    description = random.choice(DEFAULT_DESCRIPTIONS) if not original_description else (
        original_description if use_original else custom_description or random.choice(DEFAULT_DESCRIPTIONS)
    )
    
    if use_hashtags:
        description += f"\n{hashtags_list}"

    if give_credit:
        description += f"\nTaken from: @{profile_username}"

    return description

def load_uploaded_reels(log_filename):
    """Load reels that have already been uploaded from the log file."""
    uploaded_reels = set()
    if os.path.exists(log_filename):
        with open(log_filename, 'r') as log_file:
            uploaded_reels = set(line.strip() for line in log_file)
    return uploaded_reels

def upload_reels_with_new_descriptions(client, config, unuploaded_reels, uploaded_reels, log_filename, session_file):
    """Upload reels with new descriptions, handling re-login if necessary."""
    if not unuploaded_reels:
        console.print("[bold bright_red]No new reels to upload[/bold bright_red]")
        return
    
    for reel_file in unuploaded_reels:
        reel_id = reel_file.split('_')[1].split('.')[0]
        profile_username = reel_file.split('_')[0]
        media_path = os.path.join('downloads', reel_file)
        description_path = os.path.join('downloads', f'{reel_id}.txt')
        console.print(f"[bold bright_green]Preparing to upload reel {reel_id} from profile {profile_username}[/bold bright_green]")

        if not os.path.exists(media_path) or f"{profile_username}_{reel_id}" in uploaded_reels:
            console.print(f"[bold bright_red]Media file {media_path} not found or already uploaded. Skipping upload for reel: {reel_id}[/bold bright_red]")
            continue

        original_description = read_description(description_path, reel_id)

        # Safely get configurations with default values
        new_description = build_description(
            original_description,
            config.get('description', {}).get('use_original', False),
            config.get('description', {}).get('custom_description', ''),
            config.get('hashtags', {}).get('use_hashtags', False),
            config.get('hashtags', {}).get('hashtags_list', ''),
            config.get('credit', {}).get('give_credit', False),
            profile_username
        )
        logging.debug(f"Built new description for reel {reel_id}")

        # Attempt to upload the reel
        if not upload_reel(client, config, media_path, new_description, profile_username, reel_id, log_filename, session_file):
            continue

        # Optional story upload
        if config.get('uploading', {}).get('add_to_story', False):
            upload_to_story(client, media_path, new_description, profile_username, reel_id, config.get('uploading', {}).get('upload_interval_minutes', 10))

        # Update the uploaded reels log
        update_uploaded_reels(log_filename, profile_username, reel_id)

        # Perform random wait
        perform_random_wait(client, config, profile_username, reel_id)

def read_description(description_path, reel_id):
    """Read the original description from the description file."""
    if os.path.exists(description_path):
        with open(description_path, 'r', encoding='utf-8') as f:
            logging.debug(f"Read original description for reel {reel_id}")
            return f.read()
    return ""

def upload_reel(client, config, media_path, new_description, profile_username, reel_id, log_filename, session_file, retries=3):
    """Attempt to upload the reel, with retry logic in case of failure."""
    for attempt in range(retries):
        try:
            client.clip_upload(media_path, new_description)
            console.print(f"[bold bright_green]Uploaded reel: {profile_username}_{reel_id} with description:\n{new_description}[/bold bright_green]")
            
            # Update the uploaded reels in the status
            status = read_status()
            if 'reels_uploaded' not in status:
                status['reels_uploaded'] = []
            status['reels_uploaded'].append(f"{profile_username}_{reel_id}")
            
            update_status(
                last_upload_time=time.time(),
                next_upload_time=time.time() + config['uploading']['upload_interval_minutes'] * 60,
                reels_uploaded=status['reels_uploaded']  # Update reels_uploaded in status.json
            )

            # Log the uploaded reel in the log file
            update_uploaded_reels(log_filename, profile_username, reel_id)

            # Call the dashboard to display current status
            console.print("[bold blue3]Displaying dashboard after upload[/bold blue3]")
            subprocess.run(["python", "dashboard.py"])

            return True
        except Exception as e:
            console.print(f"[bold bright_red]Failed to upload reel {reel_id}: {e}[/bold bright_red]")
            if '400' in str(e) and attempt < retries - 1:  # Retry if it's a session issue
                console.print("[bold yellow]Re-login required, attempting to re-login...[/bold yellow]")
                relogin(client, config['instagram']['original_username'], config['instagram']['password'], session_file)
                continue  # Retry the upload after re-login
            else:
                console.print(f"[bold red]Max retries exceeded or unknown error occurred for reel {reel_id}. Skipping upload.[/bold red]")
                break
    return False

def upload_to_story(client, media_path, new_description, profile_username, reel_id, upload_interval_minutes):
    """Upload a reel to the Instagram story."""
    try:
        console.print(f"[bold bright_green]Preparing to upload reel {reel_id} to story[/bold bright_green]")
        story_wait_time = random_sleep(60, 180, action="story upload", profile_reel_id=f"{profile_username}_{reel_id}")
        console.print(f"[bold blue3]Waited for {story_wait_time:.2f} seconds before uploading reel {reel_id} to story[/bold blue3]")
        client.video_upload_to_story(media_path, new_description)
        console.print(f"[bold bright_green]Added reel: {profile_username}_{reel_id} to story[/bold bright_green]")
    except Exception as e:
        console.print(f"[bold bright_red]Failed to add reel {reel_id} to story: {e}[/bold bright_red]")
    console.print("[bold blue3]Displaying dashboard after story upload[/bold blue3]")
    subprocess.run(["python", "dashboard.py"])

def update_uploaded_reels(log_filename, profile_username, reel_id):
    """Log uploaded reels to the log file."""
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{profile_username}_{reel_id}\n")
        logging.debug(f"Logged uploaded reel {profile_username}_{reel_id} to {log_filename}")

def perform_random_wait(client, config, profile_username, reel_id):
    """Perform random wait between uploads and human-like actions."""
    sleep_time = random_sleep(10, 60, action="next upload", profile_reel_id=f"{profile_username}_{reel_id}")
    sleep_with_progress_bar(sleep_time)
    log_random_upload_times(sleep_time, f"{profile_username}_{reel_id}")

    next_upload_time = datetime.now() + timedelta(minutes=config.get('uploading', {}).get('upload_interval_minutes', 10))
    console.print(f"[bold blue3]Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}[/bold blue3]")
    console.print(f"[bold blue3]Waiting for {config.get('uploading', {}).get('upload_interval_minutes', 10)} minutes before next upload[/bold blue3]")

    total_wait_time = config.get('uploading', {}).get('upload_interval_minutes', 10) * 60
    elapsed_time = 0

    while elapsed_time < total_wait_time:
        remaining_time = total_wait_time - elapsed_time
        interval = min(remaining_time, random.uniform(90, 545))
        sleep_with_progress_bar(interval)
        elapsed_time += interval

        if random.random() < 0.01:
            console.print("[bold yellow]Performing human-like actions during wait time[/bold yellow]")
            perform_human_actions(client, config.get('custom_tags', []))
            next_upload_time = datetime.now() + timedelta(seconds=remaining_time - interval)
            console.print(f"[bold yellow]Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}[/bold yellow]")
            elapsed_minutes = elapsed_time // 60
            console.print(f"[bold yellow]Waiting for {config.get('uploading', {}).get('upload_interval_minutes', 10) - elapsed_minutes} minutes before next upload[/bold yellow]")
        else:
            elapsed_minutes = elapsed_time // 60
            console.print(f"[bold blue3]Waiting for {config.get('uploading', {}).get('upload_interval_minutes', 10) - elapsed_minutes} minutes before next upload[/bold blue3]")
            console.print(f"[bold blue3]Next upload at {(datetime.now() + timedelta(seconds=total_wait_time - elapsed_time)).strftime('%Y-%m-%d %H:%M:%S')}[/bold blue3]")

def get_unuploaded_reels(downloads_dir, scraped_reels, uploaded_reels):
    """Get the list of reels that have not been uploaded yet."""
    unuploaded_reels = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4'):
            reel_id = filename.split('_')[1].split('.')[0]
            reel_key = f"{filename.split('_')[0]}_{reel_id}"
            if reel_key not in uploaded_reels and reel_key not in scraped_reels:
                unuploaded_reels.append(filename)
    console.print(f"[bold bright_green]Found {len(unuploaded_reels)} unuploaded reels[/bold bright_green]")
    return unuploaded_reels
