import yaml
from cryptography.fernet import Fernet
import getpass
import os
from input_helpers import get_input, get_boolean_input
from auth import perform_login, decrypt_credentials, Client
from default_comments import DEFAULT_COMMENTS
from default_descriptions import DEFAULT_DESCRIPTIONS

print("="*80)
print("Created by: Sujay1599")
print("Program: InstgramTheftyScraperPosterHuman")
print("Version:3.0")
print("Working as of: 8/5/2024")
print("="*80)

DEFAULT_TAGS = [
    'instagram', 'instadaily', 'LikeForFollow', 'LikesForLikes', 'LikeForLikes', 
    'FollowForFollow', 'LikeForLike', 'FollowForFollowBack', 'FollowBack', 
    'FollowMe', 'instalike', 'comment', 'follow', 'memes', 'funnymemes', 
    'memestagram', 'dankmemes', 'memelord', 'instamemes', 'instagood', 'love', 
    'photooftheday', 'picoftheday', 'likeforlikes', 'likes', 'followme', 
    'photography', 'beautiful', 'fashion', 'smile', 'me', 'followforfollowback', 
    'l', 'likeforfollow', 'myself', 'likeforlike', 'bhfyp', 'f', 'followback', 
    'followers', 'followforfollow', 'style', 'photo', 'happy', 'instamood', 
    'nature', 'trending', 'art', 'india', 'viral', 'explore', 'model', 'travel'
]

SESSION_DIR = 'user_sessions'

# Ensure the session directory exists
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
    print(f"Created directory for user sessions: {SESSION_DIR}")

def generate_key():
    return Fernet.generate_key()

def encrypt_credentials(username, password, key):
    cipher_suite = Fernet(key)
    encrypted_username = cipher_suite.encrypt(username).decode()
    encrypted_password = cipher_suite.encrypt(password).decode()
    return encrypted_username, encrypted_password

def get_user_credentials():
    while True:
        username = input('Enter Instagram username: ').encode()
        password = getpass.getpass('Enter Instagram password: ').encode()
        
        # Try logging in with the provided credentials
        client = Client()
        client.delay_range = [1, 3]  # Mimic human behavior with delays between requests
        session_file = os.path.join(SESSION_DIR, f"{username.decode()}_session.json")
        
        if perform_login(client, username.decode(), password.decode(), session_file):
            print("Login successful!")
            return username, password
        else:
            print("Login failed. Please try again.")

def create_config(encrypted_username, encrypted_password, key):
    config = {
        'instagram': {
            'username': encrypted_username,
            'password': encrypted_password
        },
        'key': key.decode(),
        'scraping': {
            'enabled': get_boolean_input('Enable scraping? (true/false): '),
            'profiles': input('Enter profiles to scrape (space separated): '),
            'num_reels': get_input('Number of reels to scrape per profile: ', int),
            'scrape_interval_minutes': get_input('Interval between scrapes (minutes): ', int),
            'like_reels': get_boolean_input('Like scraped videos? (true/false): ')
        },
        'uploading': {
            'enabled': get_boolean_input('Enable uploading? (true/false): '),
            'upload_interval_minutes': get_input('Interval between uploads (minutes): ', int),
            'add_to_story': get_boolean_input('Add to story? (true/false): ')
        },
        'proxy': input('Enter proxy server address (leave blank if not using proxy): '),
        'description': {
            'use_original': get_boolean_input('Use original description? (true/false): '),
            'custom_descriptions': input('Enter custom descriptions (comma separated, leave blank for default): ').split(',') or []
        },
        'comments': input('Enter default comments (comma separated): ').split(',') or []
    }

    use_original_description = get_boolean_input('Use original description? (true/false): ')
    config['description'] = {
        'use_original': use_original_description
    }

    if use_original_description:
        config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if config['hashtags']['use_hashtags']:
            config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated, leave blank for default): ')
        
        config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }
    else:
        custom_description = input('Enter custom description (leave blank to use default descriptions): ')
        config['description']['custom_description'] = custom_description

        config['hashtags'] = {
            'use_hashtags': get_boolean_input('Add hashtags? (true/false): ')
        }
        if config['hashtags']['use_hashtags']:
            config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated, leave blank for default): ')

        config['credit'] = {
            'give_credit': get_boolean_input('Give credit? (true/false): ')
        }

    config['leave_comment'] = get_boolean_input('Leave comment on scraped videos? (true/false): ')
    if config['leave_comment']:
        config['comments'] = input('Enter comments (comma separated): ').split(',')

    config['deleting'] = {
        'delete_interval_minutes': get_input('Interval between deletions (minutes): ', int)
    }

    config['custom_tags'] = input(f'Enter custom tags (space separated, leave blank for default: {DEFAULT_TAGS}): ').split() or DEFAULT_TAGS

    return config

def save_config(config, filename='config.yaml'):
    with open(filename, 'w') as file:
        yaml.dump(config, file)
    print(f'Configuration saved to {filename}')

def delete_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f'Deleted {file}')

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def main():
    key = generate_key()
    username, password = get_user_credentials()
    encrypted_username, encrypted_password = encrypt_credentials(username, password, key)
    
    config = create_config(encrypted_username, encrypted_password, key)
    config['instagram']['original_username'] = username.decode()  # Add original username to config
    save_config(config)

    delete_files(['status.json', 'last_scraped_timestamp.txt', 'random-upload-times.json', 'random-waits.json'])

if __name__ == "__main__":
    main()