import logging
import random
import os
from time import sleep
from datetime import datetime, timedelta
from tqdm import tqdm
from rich.console import Console
from utils import update_status, read_status, random_sleep, sleep_with_progress_bar

console = Console()

def perform_human_actions(client, tags):
    if not tags:
        console.print(f"[bold bright_red]No tags provided for human-like actions.[/bold bright_red]")
        return
    
    random_tag = random.choice(tags)
    console.print(f"[bold yellow]Performing human-like actions on tag: {random_tag}[/bold yellow]")
    
    try:
        # Using hashtag_medias_recent_v1
        medias_recent = client.hashtag_medias_recent_v1(random_tag, amount=10)
        if medias_recent:
            console.print(f"[bold yellow]Media found using hashtag_medias_recent_v1.[/bold yellow]")
        
        # Using hashtag_medias_top_v1
        medias_top_v1 = client.hashtag_medias_top_v1(random_tag, amount=9)
        if medias_top_v1:
            console.print(f"[bold yellow]Media found using hashtag_medias_top_v1.[/bold yellow]")
        
        # Using hashtag_medias_top
        medias_top = client.hashtag_medias_top(random_tag, amount=9)
        if medias_top:
            console.print(f"[bold yellow]Media found using hashtag_medias_top.[/bold yellow]")
        
        # Combine all media lists and ensure no duplicates
        medias = list({media.pk: media for media in (medias_recent + medias_top_v1 + medias_top)}.values())

        if not medias:
            console.print(f"[bold bright_red]No media found for tag: {random_tag}[/bold bright_red]")
            return

        media = random.choice(medias)
        media_id = media.pk
        client.media_like(media_id)
        console.print(f"[bold yellow]Liked random media: {media_id} from tag: {random_tag}[/bold yellow]")
        
        sleep_time = random.uniform(5, 15)
        console.print(f"[bold yellow]Sleeping for {sleep_time:.2f} seconds to mimic human behavior.[/bold yellow]")
        sleep(sleep_time)
    except Exception as e:
        console.print(f"[bold red]Failed to perform human-like actions: {e}[/bold red]")
        
def scrape_reels(client, profile, num_reels, last_scrape_time, uploaded_reels, scraped_reels, tags):
    user_id = client.user_id_from_username(profile)
    reels = []
    new_scraped_reels = []

    for reel in client.user_clips(user_id, amount=num_reels):
        if reel.pk in uploaded_reels or reel.pk in scraped_reels:
            continue

        try:
            media_path = client.clip_download(reel.pk, folder='downloads')
            if media_path:
                description_path = os.path.join('downloads', f'{reel.pk}.txt')
                with open(description_path, 'w', encoding='utf-8') as f:
                    f.write(reel.caption_text or '')

                reels.append(reel)
                new_scraped_reels.append(reel.pk)

                if random.random() < 0.5:
                    perform_human_actions(client, tags)
                console.print(f"[bold bright_green]Scraped and saved reel: {reel.pk}[/bold bright_green]")
                
                sleep_time = random_sleep(10, 60, action="next reel scrape", profile_reel_id=f"{profile}_{reel.pk}")
                console.print(f"[bold bright_green]Sleeping for {sleep_time:.2f} seconds before next reel scrape.[/bold bright_green]")
                sleep_with_progress_bar(sleep_time)
                
                # Update status after each reel is scraped
                status = read_status()
                status['reels_scraped'].append(reel.pk)
                update_status(last_scrape_time=datetime.now().timestamp(), reels_scraped=status['reels_scraped'])
                
        except Exception as e:
            console.print(f"[bold red]Failed to scrape or save reel {reel.pk}: {e}[/bold red]")

    return reels
