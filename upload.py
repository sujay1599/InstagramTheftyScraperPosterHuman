import os
import logging
import random
import moviepy.editor as mp
from time import sleep
from datetime import datetime, timedelta
from utils import random_sleep, update_status, read_status, log_random_upload_times, sleep_with_progress_bar
import subprocess
from scrape import perform_human_actions
from rich.console import Console

console = Console()

DEFAULT_DESCRIPTIONS = [
""" AYYYYYY YOOOOOOO What in the world?!

The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.

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
    """
Here is a simple and delicious chocolate chip cookie recipe for you:

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
    """
    MmmmhhhGooood SOUP Soooopp,
    
Tomato Basil Soup

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
""",
    """    
    I JUST WANT TO GO FAST.......

🚗🔥 The Hellcat SRT: A Racing Legend Unleashed 🚀

📜 Here’s the scoop on the Hellcat SRT, an extraordinary racing beast known for its unmatched performance and aggressive styling.

Specifications:

Engine: 6.2-liter supercharged V8
Horsepower: Over 700 HP
Acceleration: 0 to 100 km/h in just 3.5 seconds
Top Speed: Exceeds 330 km/h
Price: Initially valued at around $1.8 million
Production: Limited to only three units
Performance and Power:

🏎 Video starts with the Hellcat SRT revving its engine, showcasing its raw power.

The Hellcat SRT is powered by a mighty 6.2-liter supercharged V8 engine, delivering a staggering 700+ horsepower. This incredible powertrain propels the car from 0 to 100 km/h in just 3.5 seconds, offering a thrilling driving experience.
🌪 The car speeding on a racetrack, highlighting its top speed.

With a mind-blowing top speed exceeding 330 km/h, the Hellcat SRT stands as a true testament to automotive engineering excellence. Its state-of-the-art aerodynamics and advanced stability systems ensure unmatched control and stability, especially during high-speed maneuvers.
🎯 Close-up shots of the car's aerodynamic design and stability systems.

Designed with cutting-edge aerodynamics, the Hellcat SRT slices through the air with precision, enhancing its performance on the track. Its advanced stability systems provide drivers with confidence and control, even at the highest speeds.
💎 Showcasing the luxurious interior and exterior design details.

Exclusivity and Luxury:

Initially valued at around $1.8 million, the Hellcat SRT stands as a pinnacle of exclusivity and luxury in the racing world. Every detail, from its luxurious interior to its striking exterior, reflects its high-end craftsmanship and design.
🌍 Highlighting the rarity and desirability of the Hellcat SRT among collectors.

Limited to only three units in production, the Hellcat SRT's rarity elevates its desirability, attracting racing aficionados and collectors worldwide. This limited production run makes owning a Hellcat SRT not just a dream, but a rare privilege.
🚀 Closing with the Hellcat SRT zooming off into the sunset, leaving a trail of dust.

From its breathtaking power to its unparalleled exclusivity, the Hellcat SRT is more than just a car; it’s a racing legend. Experience the ultimate in performance and luxury with the Hellcat SRT.
""" ,
    """
The Bugatti Veyron is a legendary supercar known for its exceptional performance and striking design.

It was first introduced in 2005 and quickly gained recognition as one of the most powerful and fastest cars in the world.🥇 
The Veyron is powered by an astonishing 8.0-liter, quad-turbocharged W16 engine, delivering an incredible amount of horsepower and torque.

With its aerodynamic body and sleek lines, the Bugatti Veyron exudes a sense of speed and elegance.🤯 
Its luxurious interior features high-quality materials and advanced technology, providing a comfortable and immersive driving experience.

As for the pricing, the Bugatti Veyron is a highly exclusive and limited-production vehicle, with a price tag that reflects its extraordinary performance and craftsmanship. 
The base price of a Bugatti Veyron can range from several million dollars to over ten million dollars,😨depending on various customization options and special editions. 
This makes it one of the most expensive and prestigious supercars in the world, reserved for a select few who can afford its exceptional engineering and luxury. 🎖️
""",
    """
👵 Grandma’s Famous Chocolate Chip Cookies 🍪

📜 Here’s the heartwarming story of my Grandma’s secret chocolate chip cookie recipe, a family tradition passed down through generations.

Ingredients:

1 cup (2 sticks) unsalted butter, softened
1 cup white sugar
1 cup packed brown sugar
2 large eggs
1 teaspoon vanilla extract
3 cups all-purpose flour
1 teaspoon baking soda
1/2 teaspoon baking powder
1/2 teaspoon salt
2 cups semisweet chocolate chips
Instructions:

🕒 Flashback to Grandma in the 1950s, mixing ingredients in her cozy kitchen.

Preheat your oven to 350°F (175°C) and line a baking sheet with parchment paper.
🥣 Grandma adding softened butter to a large mixing bowl.

In a large bowl, cream together the butter, white sugar, and brown sugar until smooth. The secret to Grandma’s cookies is in the perfect blend of sugars, making them irresistibly sweet and chewy.
🍳 Grandma cracking eggs and adding them to the mixture.

Beat in the eggs one at a time, ensuring each one is fully incorporated before adding the next. Stir in the vanilla extract, which adds that warm, comforting aroma we all love.
🥄 Mixing the dry ingredients in a separate bowl.

In a separate bowl, combine the flour, baking soda, baking powder, and salt. Gradually add this dry mixture to the wet ingredients, mixing until just blended. This step is crucial for that perfect dough consistency.
🍫 Grandma folding in chocolate chips with a smile.

Stir in the chocolate chips. Grandma always believed in using a generous amount of chocolate chips to make each bite a delightful experience.
🍪 Dropping rounded tablespoons of dough onto the baking sheet.

Drop rounded tablespoons of dough onto the prepared baking sheet. The dough balls should be evenly spaced to allow room for spreading.
🔥 Cookies baking in the oven, with a close-up of the golden edges.

Bake for 10 to 12 minutes in the preheated oven, or until the edges are golden brown. Allow cookies to cool on the baking sheet for 5 minutes before transferring to a wire rack to cool completely. The cooling process is essential to achieve the perfect texture.
❤️ Family members enjoying the cookies around the kitchen table, sharing laughter and stories.

📅 Every Saturday, we gather around the kitchen table, just like we did when we were kids, to enjoy Grandma’s delicious homemade cookies. These moments remind us of the love and joy she brought into our lives with her baking.

🏡 From our family to yours, we hope you enjoy these homemade chocolate chip cookies as much as we do. They’re more than just a treat; they’re a piece of our family history, filled with love and sweet memories.
"""
]

def build_description(original_description, use_original, custom_description, use_hashtags, hashtags_list, give_credit, profile_username):
    if not original_description:
        description = random.choice(DEFAULT_DESCRIPTIONS)
    else:
        description = original_description if use_original else (custom_description if custom_description else random.choice(DEFAULT_DESCRIPTIONS))

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
            console.print(f"[bold bright_green]Uploaded reel: {profile_username}_{reel_id} with description:\n{new_description}[/bold bright_green]")
        except Exception as e:
            console.print(f"[bold bright_red]Failed to upload reel {reel_id}: {e}[/bold bright_red]")
            continue

        console.print("[bold bright_green]Displaying dashboard after reel upload[/bold bright_green]")
        subprocess.run(["python", "dashboard.py"])

        if config['uploading']['add_to_story']:
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

        try:
            video = mp.VideoFileClip(media_path)
            video.reader.close()
            if video.audio:
                video.audio.reader.close_proc()
            logging.debug(f"Released video resources for reel {reel_id}")
        except Exception as e:
            console.print(f"[bold bright_red]Failed to release video resources for {reel_id}: {e}[/bold bright_red]")

        with open(log_filename, 'a') as log_file:
            log_file.write(f"{profile_username}_{reel_id}\n")
            logging.debug(f"Logged uploaded reel {profile_username}_{reel_id} to {log_filename}")

        uploaded_reels.add(f"{profile_username}_{reel_id}")

        status = read_status()
        status['reels_uploaded'].append(f"{profile_username}_{reel_id}")
        update_status(
            last_upload_time=datetime.now().timestamp(),
            next_upload_time=(datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])).timestamp(),
            reels_uploaded=status['reels_uploaded']
        )

        if config['uploading']['add_to_story']:
            update_status(
                last_story_upload_time=datetime.now().timestamp(),
                next_story_upload_time=(datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])).timestamp()
            )

        console.print(f"[bold blue3]Next upload will include reel: {reel_file}[/bold blue3]")

        sleep_time = random_sleep(10, 60, action="next upload", profile_reel_id=f"{profile_username}_{reel_id}")
        sleep_with_progress_bar(sleep_time)
        log_random_upload_times(sleep_time, f"{profile_username}_{reel_id}")

        next_upload_time = datetime.now() + timedelta(minutes=config['uploading']['upload_interval_minutes'])
        console.print(f"[bold blue3]Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}[/bold blue3]")
        console.print(f"[bold blue3]Waiting for {config['uploading']['upload_interval_minutes']} minutes before next upload[/bold blue3]")

        total_wait_time = config['uploading']['upload_interval_minutes'] * 60
        elapsed_time = 0

        while elapsed_time < total_wait_time:
            remaining_time = total_wait_time - elapsed_time
            interval = min(remaining_time, random.uniform(90, 545))
            sleep_with_progress_bar(interval)
            elapsed_time += interval

            if random.random() < 0.5:
                console.print("[bold yellow]Performing human-like actions during wait time[/bold yellow]")
                perform_human_actions(client, config.get('custom_tags'))
                next_upload_time = datetime.now() + timedelta(seconds=remaining_time - interval)
                console.print(f"[bold yellow]Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}[/bold yellow]")
                elapsed_minutes = elapsed_time // 60
                console.print(f"[bold yellow]Waiting for {config['uploading']['upload_interval_minutes'] - elapsed_minutes} minutes before next upload[/bold yellow]")
            else:
                elapsed_minutes = elapsed_time // 60
                console.print(f"[bold blue3]Waiting for {config['uploading']['upload_interval_minutes'] - elapsed_minutes} minutes before next upload[/bold blue3]")
                console.print(f"[bold blue3]Next upload at {(datetime.now() + timedelta(seconds=total_wait_time - elapsed_time)).strftime('%Y-%m-%d %H:%M:%S')}[/bold blue3]")

def get_unuploaded_reels(downloads_dir, scraped_reels, uploaded_reels):
    unuploaded_reels = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4'):
            reel_id = filename.split('_')[1].split('.')[0]
            reel_key = f"{filename.split('_')[0]}_{reel_id}"
            if reel_key not in uploaded_reels and reel_key not in scraped_reels:
                unuploaded_reels.append(filename)
    console.print(f"[bold bright_green]Found {len(unuploaded_reels)} unuploaded reels[/bold bright_green]")
    return unuploaded_reels
