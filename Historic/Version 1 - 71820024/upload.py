import os
import logging
import random
import moviepy.editor as mp
from time import sleep
from datetime import datetime, timedelta
from utils import random_sleep, update_status, log_random_upload_times, sleep_with_progress_bar
import subprocess
from scrape import perform_human_actions
from tqdm import tqdm

DEFAULT_DESCRIPTIONS = [
    """The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.

Here is a comprehensive overview of its key features and specifications:

Tesla Cybertruck Overview

Design and Structure

• Exterior: The Cybertruck has a distinctive, angular, stainless steel exoskeleton design for durability and passenger protection. It features ultra-hard 30X cold-rolled stainless steel and armored glass.

• Dimensions: Approximately 231.7 inches long, 79.8 inches wide, and 75 inches tall, with a 6.5-foot cargo bed.

Performance and Variants

• Single Motor RWD:
◦ 0-60 mph: ~6.5 seconds
◦ Range: ~250 miles
◦ Towing Capacity: 7,500 pounds
• Dual Motor AWD:
◦ 0-60 mph: ~4.5 seconds
◦ Range: ~300 miles
◦ Towing Capacity: 10,000 pounds
• Tri-Motor AWD:
◦ 0-60 mph: ~2.9 seconds
◦ Range: ~500 miles
◦ Towing Capacity: 14,000 pounds
""",
    """Here is a simple and delicious chocolate chip cookie recipe for you:

Ingredients:
- 1 cup (2 sticks) unsalted butter, softened
- 1 cup white sugar
- 1 cup packed brown sugar
- 2 large eggs
- 1 teaspoon vanilla extract
- 3 cups all-purpose flour
- 1 teaspoon baking soda
- 1/2 teaspoon baking powder
- 1/2 teaspoon salt
- 2 cups semisweet chocolate chips

Instructions:
1. Preheat your oven to 350°F (175°C) and line a baking sheet with parchment paper.
2. In a large bowl, cream together the butter, white sugar, and brown sugar until smooth.
3. Beat in the eggs one at a time, then stir in the vanilla.
4. In a separate bowl, combine the flour, baking soda, baking powder, and salt. Gradually add this dry mixture to the wet ingredients, mixing until just blended.
5. Stir in the chocolate chips.
6. Drop rounded tablespoons of dough onto the prepared baking sheet.
7. Bake for 10 to 12 minutes in the preheated oven, or until the edges are golden brown. Allow cookies to cool on baking sheet for 5 minutes before transferring to a wire rack to cool completely.

Enjoy your delicious homemade chocolate chip cookies!
""",
    """Tomato Basil Soup

Ingredients:
- 2 tbsp olive oil
- 1 large onion, chopped
- 4 cloves garlic, minced
- 2 cans (28 ounces each) crushed tomatoes
- 3 cups vegetable broth
- 1 cup heavy cream
- 1 tsp sugar
- Salt and black pepper to taste
- 1 cup fresh basil leaves, chopped
- Grated Parmesan cheese for garnish (optional)

Instructions:
1. Heat the olive oil in a large pot over medium heat. Add the chopped onion and sauté until softened, about 5 minutes.
2. Add the minced garlic and cook for an additional 1-2 minutes until fragrant.
3. Pour in the crushed tomatoes and vegetable broth, stirring to combine.
4. Bring the mixture to a boil, then reduce the heat and let it simmer for 20 minutes, allowing the flavors to meld.
5. Stir in the heavy cream and sugar, and season with salt and black pepper to taste.
6. Use an immersion blender to puree the soup until smooth. Alternatively, carefully transfer the soup in batches to a blender and puree.
7. Stir in the chopped basil leaves and simmer for another 5 minutes.
8. Serve hot, garnished with grated Parmesan cheese if desired. Enjoy with crusty bread or a grilled cheese sandwich.
"""
]

def build_description(original_description, use_original, custom_description, use_hashtags, hashtags_list, give_credit, profile_username):
    if not original_description:
        description = random.choice(DEFAULT_DESCRIPTIONS)
    else:
        description = original_description if use_original else custom_description

    if use_hashtags:
        description += f"\n{hashtags_list}"

    if give_credit:
        description += f"\nTaken from: @{profile_username}"

    return description

def load_uploaded_reels(log_filename):
    uploaded_reels = set()
    if os.path.exists(log_filename):
        with open(log_filename, 'r') as log_file:
            uploaded_reels = set(line.strip() for line in log_file)
    return uploaded_reels

def upload_reels_with_new_descriptions(client, config, unuploaded_reels, uploaded_reels, log_filename):
    if not unuploaded_reels:
        logging.info("No new reels to upload")
        return
    for reel_file in unuploaded_reels:
        reel_id = reel_file.split('_')[1].split('.')[0]
        profile_username = reel_file.split('_')[0]
        media_path = os.path.join('downloads', reel_file)
        description_path = os.path.join('downloads', f'{reel_id}.txt')
        logging.info(f"Preparing to upload reel {reel_id} from profile {profile_username}")

        if not os.path.exists(media_path) or f"{profile_username}_{reel_id}" in uploaded_reels:
            logging.info(f"Media file {media_path} not found or already uploaded. Skipping upload for reel: {reel_id}")
            continue

        if os.path.exists(description_path):
            with open(description_path, 'r', encoding='utf-8') as f:
                original_description = f.read()
                logging.debug(f"Read original description for reel {reel_id}")
        else:
            original_description = ""

        new_description = build_description(
            original_description,
            config['description']['use_original'],
            config['description'].get('custom_description', ''),
            config['hashtags']['use_hashtags'],
            config['hashtags'].get('hashtags_list', ''),
            config['credit']['give_credit'],
            profile_username
        )
        logging.debug(f"Built new description for reel {reel_id}")

        try:
            client.clip_upload(media_path, new_description)
            logging.info(f"Uploaded reel: {profile_username}_{reel_id} with description:\n{new_description}")
        except Exception as e:
            logging.error(f"Failed to upload reel {reel_id}: {e}")
            continue

        # Call the dashboard display function after each upload
        logging.info("Displaying dashboard after reel upload")
        subprocess.run(["python", "dashboard.py"])

        if config['uploading']['add_to_story']:
            try:
                logging.info(f"Preparing to upload reel {reel_id} to story")
                story_wait_time = random_sleep(60, 180, action="story upload", profile_reel_id=f"{profile_username}_{reel_id}")  # Increased wait time before uploading to story
                logging.info(f"Waited for {story_wait_time:.2f} seconds before uploading reel {reel_id} to story")
                client.video_upload_to_story(media_path, new_description)
                logging.info(f"Added reel: {profile_username}_{reel_id} to story")
            except Exception as e:
                logging.error(f"Failed to add reel {reel_id} to story: {e}")

            # Call the dashboard display function after each story upload
            logging.info("Displaying dashboard after story upload")
            subprocess.run(["python", "dashboard.py"])

        try:
            video = mp.VideoFileClip(media_path)
            video.reader.close()
            if video.audio:
                video.audio.reader.close_proc()
            logging.debug(f"Released video resources for reel {reel_id}")
        except Exception as e:
            logging.error(f"Failed to release video resources for {reel_id}: {e}")

        with open(log_filename, 'a') as log_file:
            log_file.write(f"{profile_username}_{reel_id}\n")
            logging.debug(f"Logged uploaded reel {profile_username}_{reel_id} to {log_filename}")

        uploaded_reels.add(f"{profile_username}_{reel_id}")

        update_status(
            last_upload_time=datetime.now().timestamp(),
            next_upload_time=(datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])).timestamp(),
            reels_uploaded=[f"{profile_username}_{reel_id}"]  # Track uploaded reels
        )

        if config['uploading']['add_to_story']:
            update_status(
                last_story_upload_time=datetime.now().timestamp(),
                next_story_upload_time=(datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])).timestamp()
            )

        logging.info(f"Next upload will include reel: {reel_file}")

        sleep_time = random_sleep(10, 60, action="next upload", profile_reel_id=f"{profile_username}_{reel_id}")
        sleep_with_progress_bar(sleep_time)
        log_random_upload_times(sleep_time, f"{profile_username}_{reel_id}")

        next_upload_time = datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])
        logging.info(f"Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Waiting for {config['uploading']['upload_interval_minutes']} minutes before next upload")

        total_wait_time = config['uploading']['upload_interval_minutes'] * 60
        elapsed_time = 0

        while elapsed_time < total_wait_time:
            remaining_time = total_wait_time - elapsed_time
            interval = min(remaining_time, random.uniform(90, 545))  # Pause every 1 to 5 minutes
            sleep_with_progress_bar(interval)
            elapsed_time += interval

            if random.random() < 0.5:
                logging.info("Performing human-like actions during wait time")
                perform_human_actions(client, config.get('custom_tags'))
                next_upload_time = datetime.now() + timedelta(seconds=remaining_time - interval)
                logging.info(f"Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}")
                elapsed_minutes = elapsed_time // 60
                logging.info(f"Waiting for {config['uploading']['upload_interval_minutes'] - elapsed_minutes} minutes before next upload")
    
    
        # Print the waiting time after each interval
            elapsed_minutes = elapsed_time // 60
            logging.info(f"Waiting for {config['uploading']['upload_interval_minutes'] - elapsed_minutes} minutes before next upload")

def get_unuploaded_reels(downloads_dir, scraped_reels, uploaded_reels):
    unuploaded_reels = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4'):
            reel_id = filename.split('_')[1].split('.')[0]
            reel_key = f"{filename.split('_')[0]}_{reel_id}"
            if reel_key not in uploaded_reels and reel_key not in scraped_reels:
                unuploaded_reels.append(filename)
    logging.info(f"Found {len(unuploaded_reels)} unuploaded reels")
    return unuploaded_reels
