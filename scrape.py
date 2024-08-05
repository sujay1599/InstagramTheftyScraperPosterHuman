import logging
import random
import os
from time import sleep
from datetime import datetime
from tqdm import tqdm
from rich.console import Console
from utils import update_status, read_status, random_sleep, sleep_with_progress_bar
from default_comments import DEFAULT_COMMENTS

console = Console()

def perform_human_actions(client, tags):
    if not tags:
        console.print(f"[bold bright_red]No tags provided for human-like actions.[/bold bright_red]")
        return
    
    random_tag = random.choice(tags)
    console.print(f"[bold yellow]Performing human-like actions on tag: {random_tag}[/bold yellow]")
    
    actions = [
        lambda tag: client.hashtag_medias_recent_v1(tag, amount=10),
        lambda tag: client.hashtag_medias_top_v1(tag, amount=9),
        lambda tag: client.hashtag_medias_top(tag, amount=9)
    ]
    
    try:
        action = random.choice(actions)
        medias = action(random_tag)
        
        if medias:
            console.print(f"[bold yellow]Media found using {action.__name__}.[/bold yellow]")
            media = random.choice(medias)
            media_id = media.pk
            
            # Randomly like or unlike media
            if random.random() < 0.5:
                if client.media_likers(media_id).usernames:
                    client.media_unlike(media_id)
                    console.print(f"[bold yellow]Unliked random media: {media_id} from tag: {random_tag}.[/bold yellow]")
                else:
                    client.media_like(media_id)
                    console.print(f"[bold yellow]Liked random media: {media_id} from tag: {random_tag}.[/bold yellow]")
            else:
                client.media_like(media_id)
                console.print(f"[bold yellow]Liked random media: {media_id} from tag: {random_tag}.[/bold yellow]")
            
            # Random follow/unfollow
            if random.random() < 0.1:
                user_to_follow = media.user.pk
                if client.user_following(client.user_id).get(user_to_follow):
                    client.user_unfollow(user_to_follow)
                    console.print(f"[bold yellow]Unfollowed user: {user_to_follow}.[/bold yellow]")
                else:
                    client.user_follow(user_to_follow)
                    console.print(f"[bold yellow]Followed user: {user_to_follow}.[/bold yellow]")

            # Random comments
            if random.random() < 0.1:
                comment_text = random.choice(DEFAULT_COMMENTS)
                client.media_comment(media_id, comment_text)
                console.print(f"[bold yellow]Commented on media: {media_id} with text: {comment_text}.[/bold yellow]")
            
            # Randomly view stories
            if random.random() < 0.1:
                stories = client.user_stories(user_to_follow)
                if stories:
                    story_to_view = random.choice(stories)
                    client.story_seen(story_to_view.id)
                    console.print(f"[bold yellow]Viewed story: {story_to_view.id}.[/bold yellow]")

            sleep_time = random.uniform(5, 15)
            console.print(f"[bold yellow]Sleeping for {sleep_time:.2f} seconds to mimic human behavior.[/bold yellow]")
            sleep(sleep_time)
        else:
            console.print(f"[bold bright_red]No media found for tag: {random_tag}.[/bold bright_red]")
    except Exception as e:
        console.print(f"[bold red]Failed to perform human-like actions: {e}.[/bold red]")
        logging.error(f"Failed to perform human-like actions: {e}")

def scrape_reels(client, profile, num_reels, last_scrape_time, uploaded_reels, scraped_reels, tags):
    user_id = client.user_id_from_username(profile)
    reels = []
    new_scraped_reels = []

    for reel in client.user_clips(user_id, amount=num_reels):
        reel_id_str = str(reel.pk)  # Ensure reel_id is treated as a string
        profile_reel_id = f"{profile}_{reel_id_str}"
        if profile_reel_id in uploaded_reels or profile_reel_id in scraped_reels:
            continue

        try:
            media_path = client.clip_download(reel.pk, folder='downloads')
            if media_path:
                description_path = os.path.join('downloads', f'{reel_id_str}.txt')
                with open(description_path, 'w', encoding='utf-8') as f:
                    f.write(reel.caption_text or '')

                reels.append(reel)
                new_scraped_reels.append(profile_reel_id)

                if random.random() < 0.01:  # Perform human-like actions 1% of the time
                    perform_human_actions(client, tags)
                console.print(f"[bold bright_green]Scraped and saved reel: {profile_reel_id}.[/bold bright_green]")
                
                sleep_time = random_sleep(10, 60, action="next reel scrape", profile_reel_id=profile_reel_id)
                console.print(f"[bold bright_green]Sleeping for {sleep_time:.2f} seconds before next reel scrape.[/bold bright_green]")
                sleep_with_progress_bar(sleep_time)
                
                # Update status after each reel is scraped
                status = read_status()
                status['reels_scraped'].append(profile_reel_id)
                update_status(last_scrape_time=datetime.now().timestamp(), reels_scraped=status['reels_scraped'])
                
        except Exception as e:
            console.print(f"[bold red]Failed to scrape or save reel {profile_reel_id}: {e}.[/bold red]")
            logging.error(f"Failed to scrape or save reel {profile_reel_id}: {e}")

    return new_scraped_reels
