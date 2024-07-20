import logging
import random
import os
from time import sleep
from datetime import datetime, timedelta
from tqdm import tqdm
from utils import update_status, random_sleep

DEFAULT_TAGS = [
    "instagram", "instadaily", "LikeForFollow", "LikesForLikes", "LikeForLikes", 
    "FollowForFollow", "LikeForLike", "FollowForFollowBack", "FollowBack", 
    "FollowMe", "instalike", "comment", "follow"
]

def perform_human_actions(client, custom_tags=None):
    tags = custom_tags if custom_tags else DEFAULT_TAGS
    random_tag = random.choice(tags)
    logging.info(f"Performing human-like actions on tag: {random_tag}")
    try:
        feed = client.hashtag_feed(random_tag)
        if 'sections' in feed:
            media_items = []
            for section in feed['sections']:
                media_items.extend(section.get('layout_content', {}).get('medias', []))
            
            if not media_items:
                logging.warning(f"No media items found in sections for tag: {random_tag}")
                return

            media = random.choice(media_items)['media']
            media_id = media['pk']
            client.media_like(media_id)
            logging.info(f"Liked random media: {media_id} from tag: {random_tag}")
        else:
            logging.warning(f"No sections found in feed for tag: {random_tag}")
            return

        sleep_time = random.uniform(5, 15)
        logging.info(f"Sleeping for {sleep_time:.2f} seconds to mimic human behavior.")
        sleep(sleep_time)
    except Exception as e:
        logging.error(f"Failed to perform human-like actions: {e}")

def scrape_reels(client, profile, num_reels, last_scrape_time, uploaded_reels, scraped_reels):
    user_id = client.user_id_from_username(profile)
    reels = []
    all_downloaded_reels = []

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
                all_downloaded_reels.append(f"{profile}_{reel.pk}")

                if random.random() < 0.5:
                    perform_human_actions(client)
                logging.info(f"Scraped and saved reel: {reel.pk}")
                
                # Update status after each successful scrape
                update_status(
                    last_scrape_time=datetime.now().timestamp(),
                    next_scrape_time=(datetime.now() + timedelta(minutes=60)).timestamp(),
                    reels_scraped=all_downloaded_reels
                )

                sleep_time = random_sleep(10, 60, action="next reel scrape", profile_reel_id=f"{profile}_{reel.pk}")
                logging.info(f"Sleeping for {sleep_time:.2f} seconds before next reel scrape.")
        except Exception as e:
            logging.error(f"Failed to scrape or save reel {reel.pk}: {e}")

    update_status(
        last_scrape_time=datetime.now().timestamp(),
        next_scrape_time=(datetime.now() + timedelta(minutes=60)).timestamp(),
        reels_scraped=all_downloaded_reels
    )

    return reels
