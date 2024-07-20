import yaml
from cryptography.fernet import Fernet
import getpass
import os
from input_helpers import get_input, get_boolean_input

def generate_key():
    return Fernet.generate_key()

def encrypt_credentials(username, password, key):
    cipher_suite = Fernet(key)
    encrypted_username = cipher_suite.encrypt(username).decode()
    encrypted_password = cipher_suite.encrypt(password).decode()
    return encrypted_username, encrypted_password

def get_user_credentials():
    username = input('Enter Instagram username: ').encode()
    password = getpass.getpass('Enter Instagram password: ').encode()
    return username, password

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
        }
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
        config['description']['custom_description'] = input('Enter custom description: ')
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

    config['custom_tags'] = input('Enter custom tags (space separated, leave blank for default): ').split()

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
    save_config(config)

    delete_files(['status.json', 'last_scraped_timestamp.txt', 'random-upload-times.json'])

if __name__ == "__main__":
    main()
