import logging
import random
import os
from time import sleep
from datetime import datetime, timedelta
from utils import update_status, random_sleep, sleep_with_progress_bar

def perform_human_actions(client, tags):
    random_tag = random.choice(tags)
    logging.info(f"Performing human-like actions on tag: {random_tag}")
    try:
        medias = client.hashtag_medias_recent_v1(random_tag, amount=20)
        if not medias:
            logging.warning(f"No media items found for tag: {random_tag}")
            return

        media = random.choice(medias)
        client.media_like(media.pk)
        logging.info(f"Liked random media: {media.pk} from tag: {random_tag}")

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
                    perform_human_actions(client, profile)
                logging.info(f"Scraped and saved reel: {reel.pk}")
                
                # Update status after each successful scrape
                update_status(
                    last_scrape_time=datetime.now().timestamp(),
                    next_scrape_time=(datetime.now() + timedelta(minutes=60)).timestamp(),
                    reels_scraped=all_downloaded_reels
                )

                sleep_time = random_sleep(10, 60, action="next reel scrape", profile_reel_id=f"{profile}_{reel.pk}")
                logging.info(f"Sleeping for {sleep_time:.2f} seconds before next reel scrape.")
                sleep_with_progress_bar(sleep_time)
        except Exception as e:
            logging.error(f"Failed to scrape or save reel {reel.pk}: {e}")

    if not reels:
        logging.info("No new reels scraped.")

    update_status(
        last_scrape_time=datetime.now().timestamp(),
        next_scrape_time=(datetime.now() + timedelta(minutes=60)).timestamp(),
        reels_scraped=all_downloaded_reels
    )

    return reels
