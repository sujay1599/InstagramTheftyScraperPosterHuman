# InstagramTheftyScraperPosterHumanV2.1

## See Changes Here: [Enhanced Breakdown of Changes in InstagramTheftyScraperPosterHuman V2.1 vs InstagramTheftyScraperPosterHuman V2 ](https://github.com/sujay1599/InstagramTheftyScraperPosterHuman/wiki/Changes-V2-to-V2.1)

InstagramTheftyScraperPosterHuman is an advanced tool for automating the process of scraping, uploading, and managing Instagram reels. This tool builds upon previous versions, introducing several enhancements and new functionalities to improve automation, human-like interactions, and bot detection prevention.

### Key Differences and Enhancements

**auth.py:**
1. **Logging Enhancements**: Uses `rich.console.Console` for more detailed logging.
2. **Session Handling**: Improved session management with `save_session`, `load_session`, and `update_session_file` functions.
3. **Time Zone Setting**: Sets CST (Chicago) time zone during login.
4. **Enhanced Re-login**: Adds `relogin` function for better session handling.
5. **Modular Code**: More modular with separate functions for session handling.

**main.py:**
1. **Configuration Validation**: Ensures required keys in the `scraping` section.
2. **Session Management**: Improved with `perform_login`, `update_session_file`, and `relogin` functions.
3. **Rate Limit Handling**: Adds `handle_rate_limit` function with retries and exponential backoff.
4. **Delay Range**: Sets a delay range for human-like behavior.
5. **Proxy Support**: Adds support for proxies.
6. **Error Handling**: More robust error handling with detailed logging.

**utils.py:**
1. **Enhanced Logging**: Improved logging messages for better clarity.
2. **Session Management**: Ensures better handling of session files.
3. **Functionality Additions**: Minor updates to align with other enhanced functionalities.

**scrape.py:**
1. **Human-Like Actions**: Randomly selects actions from a list of lambda functions.
2. **Media Handling**: Simplifies the process by performing actions directly on media.
3. **Logging Enhancements**: Improved logging messages.
4. **Scraping Logic**: Uses `profile_reel_id` for uniqueness.
5. **Error Handling**: More detailed logging for exceptions.

**upload.py:**
1. **Default Descriptions**: Adds branding messages for social media accounts.
2. **Human-Like Actions**: More seamlessly integrated with improved logging.
3. **Description Building**: Enhanced with additional branding messages.
4. **Dashboard Display**: Displays the dashboard after each upload.
5. **Resource Management**: Improved logging for resource management.
6. **Loop Logic**: Maintains the waiting period logic with random sleep intervals.

## Features

### Core Features

- **Scraping Reels**: Scrapes reels from specified Instagram profiles.
- **Uploading Reels**: Uploads scraped reels with customizable descriptions and hashtags.
- **Human-like Actions**: Performs random actions like liking, commenting, and following to mimic human behavior.
- **Dashboard**: Displays detailed information about activities.
- **Anti-Bot Detection**: Implements random waits and actions to avoid detection.
- **Logging**: Logs all activities for better traceability and debugging.
- **Configurable Settings**: Uses a YAML configuration file for easy customization.

### New Features in InstagramTheftyScraperPosterHuman

- **Enhanced Random Waits**: Added random waits between scraping, liking, commenting, and uploading actions to better simulate human behavior and reduce the risk of detection by Instagram.
- **Logging of Random Waits**: Logged random wait times into a separate file (`random-waits.json`) for better tracking and debugging.
- **Detailed Logging of Comments**: The program now logs the actual comments posted on each reel for better traceability.
- **Improved Error Handling**: Enhanced error handling and logging to capture JSONDecodeError and other exceptions, making the script more robust.
- **Improved Dashboard**: Updated dashboard to display detailed information about scraping, uploading, and random wait times, as well as the next file to be uploaded.
- **Human-like Interactions**: Performs random human-like actions during waiting periods, including liking and commenting on random posts from popular hashtags.
- **Auto Restart Scraping**: Automatically initiates the scraping process when there are no more videos left to upload in the downloads directory.

## Requirements

- Python 3.6+
- Required Python packages (specified in `requirements.txt`)

### Install Required Packages

You can install all the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sujay1599/InstagramTheftyScraperPosterHuman.git
   cd InstagramTheftyScraperPosterHuman
   ```

2. Install the required packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Run `config_setup.py` to create the `config.yaml` file:
   ```bash
   python config_setup.py
   ```
   Follow the prompts to enter your configuration details. This will generate a `config.yaml` file with the necessary settings, including encrypted Instagram credentials.

### Configuration

The `config.yaml` file will be generated by running `config_setup.py`. It includes the following settings:

```yaml
instagram:
  username: ENCRYPTED_USERNAME
  password: ENCRYPTED_PASSWORD
key: ENCRYPTION_KEY
scraping:
  enabled: true
  profiles: profile1 profile2
  num_reels: 10
  scrape_interval_minutes: 60
  like_reels: true
uploading:
  enabled: true
  upload_interval_minutes: 30
  add_to_story: true
description:
  use_original: true
  custom_description: ""
hashtags:
  use_hashtags: true
  hashtags_list: "example hashtags"
credit:
  give_credit: true
leave_comment: true
comments:
  - "Nice reel!"
  - "Great post!"
deleting:
  delete_interval_minutes: 1440
custom_tags:
  - instagram
  - instadaily
  - LikeForFollow
  - LikesForLikes
  - LikeForLikes
  - FollowForFollow
  - LikeForLike
  - FollowForFollowBack
  - FollowBack
  - FollowMe
  - instalike
  - comment
  - follow
  - memes
  - funnymemes
  - memestagram
  - dankmemes
  - memelord
  - instamemes
  - instagood
  - love
  - photooftheday
  - picoftheday
  - likeforlikes
  - likes
  - followme
  - photography
  - beautiful
  - fashion
  - smile
  - me
  - followforfollowback
  - l
  - likeforfollow
  - myself
  - likeforlike
  - bhfyp
  - f
  - followback
  - followers
  - followforfollow
  - style
  - photo
  - happy
  - instamood
  - nature
  - trending
  - art
  - india
  - viral
  - explore
  - model
  - travel
```

### Configuration Details

- **Instagram Credentials**: Provide your Instagram username and password. These will be encrypted and stored securely.
- **Scraping Settings**:
  - `enabled`: Set to `true` to enable scraping.
  - `profiles`: Space-separated list of Instagram profiles to scrape reels from.
  - `num_reels`: Number of reels to scrape per profile.
  - `scrape_interval_minutes`: Interval in minutes between scraping sessions.
- **Uploading Settings**:
  - `enabled`: Set to `true` to enable uploading.
  - `upload_interval_minutes`: Interval in minutes between uploads.
  - `add_to_story`: Set to `true` to add reels to your Instagram story.
- **Description Settings**:
  - `use_original`: Set to `true` to use the original reel description. If `false`, you will be prompted to enter a custom description.
  - `custom_description`: The custom description to use if `use_original` is `false`.
- **Hashtags Settings**:
  - `use_hashtags`: Set to `true` to use hashtags in the reel descriptions.
  - `hashtags_list`: List of hashtags to include in the reel descriptions (if `use_hashtags` is `true`).
- **Credit Settings**:
  - `give_credit`: Set to `true` to give credit to the original poster in the reel descriptions.
- **Deleting Settings**:
  - `delete_interval_minutes`: Interval in minutes between deletions.
- **Comments**:
  - `leave_comment`: Set to `true` to leave comments on scraped videos.
  - `comments`: List of comments to leave if `leave_comment` is `true`.
- **Custom Tags**: List of custom tags for human-like actions.

## Usage

Run the script:

```bash
python main.py
```

This will start the process of scraping, uploading, and performing human-like actions as configured in the `config.yaml` file.

### Detailed Breakdown of Files

#### auth.py

Handles Instagram authentication and session management:

1. **Decryption of Credentials**:
   - Decrypts stored Instagram credentials using a generated key.
   
2. **Login Management**:
   - Manages login sessions, checking for an active session first and creating a new one if necessary.
   - Uses `instagrapi` to handle the authentication process.
  
   - S![image](https://github.com/user-attachments/assets/4ddc09a9-df1b-4f01-8204-ef1e5e5d3885)


#### config_setup.py

Generates the `config.yaml` configuration file with encrypted credentials. Also deletes any old status and log files to ensure a clean start.

1. **Generating Key**:
   - Uses `cryptography.fernet.Fernet` to generate an encryption key.
   
2. **Encrypting Credentials**:
   - Encrypts the Instagram username and password using the generated key.
   
3. **Getting User Inputs**:
   - Prompts the user for various configuration details such as profiles to scrape, number of reels, and intervals.
   
4. **Creating and Saving Configuration**:
   - Creates a YAML configuration file with all the provided details and encrypted credentials.
   
5. **Deleting Old Files**:
   - Deletes old status and log files to ensure a clean setup.

#### dashboard.py

Displays a detailed dashboard of activities, showing the status of scraping, uploading, and human-like actions.

1. **Dashboard Information**:
   - Displays the status of the last and next scrape, upload, and delete times.
   - Shows random wait times and other detailed logs.

#### input_helpers.py

Contains helper functions for getting user inputs during configuration setup.

1. **Input Functions**:
   - Functions to get and validate different types of user inputs, such as integers, booleans, and strings.

#### main.py

The main script that orchestrates the scraping, uploading, and human-like actions processes. It reads the configuration, manages the workflow, and ensures periodic actions are performed.

1. **Configuration and Initialization**:
   - Reads the `config.yaml` file to get the configuration settings.
   - Initializes logging and status files using utility functions from `utils.py`.

2. **Authentication**:
   - Uses `auth.py` to handle Instagram login. It checks for an existing session and uses it if available, otherwise, it performs a manual login and creates a new session, while keeping the UUIDs the same to reduce bot detection.

3. **Scraping Logic**:
   - Calls `scrape.py` to handle the scraping of Instagram reels.
   - Performs human-like actions using the `perform_human_actions` function, including Sliking and commenting on posts to reduce bot detection.
        - ![image](https://github.com/user-attachments/assets/a0e8585c-cc07-4170-a2f5-426aeffaf3b2)

4. **Uploading Logic**:
   - Handles the uploading of scraped reels, including adding descriptions, hashtags, and crediting the original posters. This logic is found in `upload.py`.
      -    ![image](https://github.com/user-attachments/assets/ed0752bf-f8e5-4401-a0ec-9663014a8b86)
      -    ![image](https://github.com/user-attachments/assets/052cd0df-c7bc-4544-a418-a18d4aba4f4a)



5. **Logging and Random Waits**:
   - Implements random waits between actions to mimic human behavior and avoid detection.
   - Logs all activities for traceability and debugging purposes.
      - ![image](https://github.com/user-attachments/assets/2bb3f567-b676-41d6-b094-b3f02085f8f5)
      - ![image](https://github.com/user-attachments/assets/5ae6d148-1764-418b-bac1-2c3fd6d84f60)

#### scrape.py

Handles scraping of Instagram reels and performing human-like actions:

1. **Scraping Functionality**:
   - Scrapes reels from specified Instagram profiles.
   - Implements human-like interactions such as liking and commenting on random posts from popular hashtags to mimic human behavior.

2. **Human-like Actions**:
   - The `perform_human_actions` function simulates human interactions by performing random actions during waiting periods, including liking and commenting on random posts.

#### upload.py

Handles the uploading of scraped reels:

1. **Uploading Mechanism**:
   - Uploads reels with customizable descriptions, hashtags, and credits.
   - Supports adding reels to Instagram stories if configured.

2. **Default Descriptions**:
   - Uses predefined default descriptions if custom descriptions are not provided.

3. **Logging Uploads**:
   - Logs the upload activities and tracks the uploaded reels.

#### utils.py

Contains utility functions for logging, status management, random sleeps, and managing JSON files for random wait times:

1. **Logging and Status Management**:
   - Functions for reading and updating status files, logging uploads, and handling random wait times.

2. **Random Sleeps**:
   - Implements random wait periods between actions to reduce bot detection.
   - Logs the random wait times to `random-waits.json`.

3. **File Management**:
   - Functions to delete old status and log files to ensure a clean setup.

### Anti-Bot Detection

The program includes several features to avoid detection by Instagram:
   ![image](https://github.com/user-attachments/assets/50fc5988-8f71-4fbe-a39b-6efb40df31f2)
- **Random Waits**: Implements random waits between actions to mimic human behavior.
- **Human-like Actions**: Performs random actions like liking, commenting, and following during the waiting periods.
- **Detailed Logging**: Logs all activities for better traceability and debugging.

### Logging

The script maintains several log files to track activities and debug issues:

- **upload_log.txt**: Keeps track of uploaded reels.
- **status.json**: Tracks the last action times and other status information.
- **random-upload-times.json**: Logs the random sleep times between uploads.
- **random-waits.json**: Logs the random wait times between various actions.

### Dashboard

Run the dashboard script to view detailed information about scraping, uploading activities, and random wait times:

```bash
python dashboard.py
```
![image](https://github.com/user-attachments/assets/12d495a7-8115-4e3d-8a86-a635b8a79682)

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### Disclaimer

This script is intended for educational and personal use only. Use it responsibly and ensure you comply with Instagram’s terms of service and guidelines.
