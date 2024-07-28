import os
import json
from rich.console import Console
from rich.table import Table
from datetime import datetime

print("="*80)
print("Created by: Sujay1599")
print("Program: InstgramTheftyScraperPosterHuman")
print("Working as of: 7/20/2024")
print("="*80)

status_file = 'status.json'
log_file = 'upload_log.txt'
random_upload_time_file = 'random-upload-times.json'
random_waits_file = 'random-waits.json'
downloads_dir = 'downloads'
console = Console()

def read_json_file(file_path):
    if not os.path.exists(file_path):
        console.print(f"[bold red]{file_path} not found.[/bold red]")
        return []
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        console.print(f"[bold red]Error reading {file_path}: {e}[/bold red]")
        return []

def read_text_file(file_path):
    if not os.path.exists(file_path):
        console.print(f"[bold red]{file_path} not found.[/bold red]")
        return []
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except Exception as e:
        console.print(f"[bold red]Error reading {file_path}: {e}[/bold red]")
        return []

def get_file_counts():
    if not os.path.exists(downloads_dir):
        console.print("[bold red]Downloads directory not found.[/bold red]")
        return 0, [], 0, 0
    total_files = [f for f in os.listdir(downloads_dir) if f.endswith('.mp4')]
    uploaded_files = read_text_file(log_file)
    uploaded_files_set = set(uploaded_files)
    unuploaded_files = [f for f in total_files if f not in uploaded_files_set]
    folder_size = sum(os.path.getsize(os.path.join(downloads_dir, f)) for f in total_files) / (1024 * 1024)
    return len(total_files), uploaded_files, len(unuploaded_files), folder_size

def format_time(timestamp):
    if not timestamp or timestamp == 'None':
        return "N/A"
    try:
        return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Invalid timestamp"

def display_dashboard():
    status = read_json_file(status_file)
    if not status:
        return

    uploads = read_text_file(log_file)
    random_upload_times = read_json_file(random_upload_time_file)
    random_waits = read_json_file(random_waits_file)
    total_files, uploaded_files, unuploaded_files, folder_size = get_file_counts()

    console.print("=" * 80, justify="left")
    console.print("[bold yellow]Instagram Thefty Poster Dashboard[/bold yellow]", justify="left")
    console.print("=" * 80, justify="left")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Scrape Status", justify="center")
    table.add_column("Upload Status", justify="center")

    table.add_row(
        f"Last Scrape Time: {format_time(status.get('last_scrape_time'))}\nNext Scrape Time: {format_time(status.get('next_scrape_time'))}",
        f"Last Upload Time: {format_time(status.get('last_upload_time'))}\nNext Upload Time: {format_time(status.get('next_upload_time'))}"
    )
    console.print(table)

    file_table = Table(show_header=True, header_style="bold magenta")
    file_table.add_column("Metric", justify="center")
    file_table.add_column("Value", justify="center")

    file_table.add_row("Total .mp4 Files", str(total_files))
    file_table.add_row("Uploaded .mp4 Files", str(len(uploaded_files)))
    file_table.add_row("Unuploaded .mp4 Files", str(unuploaded_files))
    file_table.add_row("Downloads Folder Size (MB)", f"{folder_size:.2f}")

    console.print(file_table)

    console.print("[bold]Last 10 Uploads[/bold]")
    for upload in uploads[-10:]:
        console.print(f"- {upload}")

    console.print("[bold]Reels Scraped[/bold]")
    for reel in status.get('reels_scraped', []):
        console.print(f"- {reel}")

    console.print("[bold]Random Upload Times[/bold]")
    for item in random_upload_times[-10:]:
        if isinstance(item, dict):
            time_record = item.get('time', 'N/A')
            profile_reel_id = item.get('profile_reel_id', 'N/A')
            console.print(f"- {time_record} seconds for {profile_reel_id}")
        else:
            console.print(f"- {item}")

    console.print("[bold]Random Wait Times[/bold]")
    for item in random_waits[-10:]:
        if isinstance(item, dict):
            time_record = item.get('time', 'N/A')
            profile_reel_id = item.get('profile_reel_id', 'N/A')
            console.print(f"- {time_record} seconds for {profile_reel_id}")
        else:
            console.print(f"- {item}")

    table2 = Table(show_header=True, header_style="bold magenta")
    table2.add_column("Story Upload Status", justify="center")
    table2.add_column("Deletion Status", justify="center")

    table2.add_row(
        f"Last Story Upload Time: {format_time(status.get('last_story_upload_time'))}\nNext Story Upload Time: {format_time(status.get('next_story_upload_time'))}",
        f"Last Deletion Time: {format_time(status.get('last_delete_time'))}\nNext Deletion Time: {format_time(status.get('next_deletion_time'))}"
    )
    console.print(table2)

    next_file = status.get('next_file_to_upload', 'N/A')
    console.print(f"[bold]Next File to Upload:[/bold] {next_file}")

if __name__ == "__main__":
    display_dashboard()
