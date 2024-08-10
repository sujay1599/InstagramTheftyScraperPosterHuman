Here is the updated README file for version 3.02:

---

### Updated README for InstagramTheftyScraperPosterHuman V3.02

# InstagramTheftyScraperPosterHumanV3.02
## 8/10/2024

### High-Level Changes in Version 3.02
- **Version Management**: Added a version management system where the version number and program details are read from a `version.txt` file, allowing easier updates and consistency across the project.
- **Enhanced Error Handling**: Improved error handling throughout the code to catch and log potential issues more effectively.
- **Session Management**: Further refinements in session handling to ensure seamless operation and reduced bot detection.
- **Optimized Logging**: Enhanced logging for better traceability and debugging, including more detailed logs for session handling and random wait times.
- **Code Refactoring**: Refactored various parts of the code to improve readability, modularity, and maintainability.

### CHANGE LOG:
## V3.02: [Enhanced Breakdown of Changes in InstagramTheftyScraperPosterHuman V3.02 vs InstagramTheftyScraperPosterHuman V3.0](https://github.com/sujay1599/InstagramTheftyScraperPosterHuman/wiki/Enhanced-Breakdown-of-Changes-in-InstagramTheftyScraperPosterHuman-V3.02-vs-InstagramTheftyScraperPosterHuman-V3.0)

InstagramTheftyScraperPosterHuman continues to evolve, adding new features and refining existing ones to improve the automation process, mimic human interactions more effectively, and enhance the overall user experience.

### Key Differences and Enhancements in Version 3.02

**auth.py:**
1. **Version Management**: Integrated version management to display the current version of the script upon execution.
2. **Error Handling**: Improved error handling during the session load and login processes.
3. **Session File Management**: Enhanced session file management to ensure session persistence across runs.

**config_setup.py:**
1. **Version Display**: Displays the current version of the script before starting the configuration process.
2. **Input Validation**: Improved input validation during the configuration setup to ensure correct data entry.

**main.py:**
1. **Version Management**: The version is now displayed at the start of the program, sourced from the `version.txt` file.
2. **Error Handling**: Enhanced error handling for the main loop, with better logging for unexpected issues.
3. **Session Management**: Further refined the session management process to reduce bot detection and handle session expirations gracefully.

**dashboard.py:**
1. **Version Display**: Now displays the current version of the program on the dashboard.
2. **Error Logging**: Improved error logging when reading and displaying dashboard data.

**utils.py:**
1. **File Management**: Enhanced file management functions to handle missing or corrupted files more gracefully.
2. **Version Handling**: Added utility functions for managing and displaying the program version.

**scrape.py:**
1. **Human-Like Actions**: Further refined human-like actions to improve mimicry of real user behavior.
2. **Logging Enhancements**: Improved logging during the scraping process for better traceability.

**upload.py:**
1. **Dashboard Integration**: The dashboard is now displayed after every successful upload to provide real-time feedback on the program's status.
2. **Error Handling**: Improved error handling during the upload process to catch and log issues more effectively.

## Features

### Core Features

- **Scraping Reels**: Scrapes reels from specified Instagram profiles.
- **Uploading Reels**: Uploads scraped reels with customizable descriptions and hashtags.
- **Human-like Actions**: Performs random actions like liking, commenting, and following to mimic human behavior.
- **Dashboard**: Displays detailed information about activities.
- **Anti-Bot Detection**: Implements random waits and actions to avoid detection.
- **Logging**: Logs all activities for better traceability and debugging.
- **Configurable Settings**: Uses a YAML configuration file for easy customization.

### New Features in InstagramTheftyScraperPosterHuman V3.02

- **Version Management**: The version is now managed centrally in a `version.txt` file and displayed across all scripts.
- **Enhanced Random Waits**: Improved the random wait mechanism to better simulate human behavior and avoid detection.
- **Improved Error Handling**: Enhanced error handling across all scripts for more robust operation and better logging.
- **Dashboard Integration**: The dashboard is now more integrated into the workflow, providing real-time feedback after each significant action.

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
   Follow the prompts to enter your configuration details. This will generate a `config.yaml` file with the necessary settings, including encrypted Instagram credentials, proxy settings, default descriptions, and comments.

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
  custom_descriptions:
    - "Custom description 1"
    - "Custom description 2"
    - "Custom description 3"
hashtags:
  use_hashtags: true
  hashtags_list: "example hashtags"
credit:
  give_credit: true
leave_comment: true
comments:
  - "Nice reel!"
  - "Great post!"
  - "Awesome!"
  - "Love it!"
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
proxy: http://proxyserver:port # Add your proxy address here if you use one
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
  - `use_original`: Set to `true` to use the original reel description. If `false`, custom descriptions will be used.
  - `custom_descriptions`: List of custom descriptions to use if `use_original` is `false`.
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
- **Proxy**: Optional proxy settings.

### Default Descriptions and Comments

The default descriptions and comments are used when the `use_original` option is set to `false` for descriptions and `

leave_comment` is set to `true`. During the configuration setup, users can input their own default descriptions and comments. These defaults will be used during the uploading and commenting processes, providing more flexibility and personalization for the user.

### Usage

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
   - Injects session IDs to the public session to maintain consistency.

#### config_setup.py

Generates the `config.yaml` configuration file with encrypted credentials. Also deletes any old status and log files to ensure a clean start.

1. **Version Display**:
   - Displays the current version of the program before starting the configuration process.

2. **Generating Key**:
   - Uses `cryptography.fernet.Fernet` to generate an encryption key.
   
3. **Encrypting Credentials**:
   - Encrypts the Instagram username and password using the generated key.
   
4. **Getting User Inputs**:
   - Prompts the user for various configuration details such as profiles to scrape, number of reels, intervals, proxy settings, default descriptions, and default comments.
   
5. **Creating and Saving Configuration**:
   - Creates a YAML configuration file with all the provided details and encrypted credentials.
   
6. **Deleting Old Files**:
   - Deletes old status and log files to ensure a clean setup.

#### dashboard.py

Displays a detailed dashboard of activities, showing the status of scraping, uploading, and human-like actions.

1. **Version Display**:
   - Displays the current version of the program on the dashboard.

2. **Dashboard Information**:
   - Displays the status of the last and next scrape, upload, and delete times.
   - Shows random wait times and other detailed logs.

#### input_helpers.py

Contains helper functions for getting user inputs during configuration setup.

1. **Input Functions**:
   - Functions to get and validate different types of user inputs, such as integers, booleans, and strings.

#### main.py

The main script that orchestrates the scraping, uploading, and human-like actions processes. It reads the configuration, manages the workflow, and ensures periodic actions are performed.

1. **Version Management**:
   - Displays the current version of the program at startup.

2. **Configuration and Initialization**:
   - Reads the `config.yaml` file to get the configuration settings.
   - Initializes logging and status files using utility functions from `utils.py`.

3. **Authentication**:
   - Uses `auth.py` to handle Instagram login. It checks for an existing session and uses it if available, otherwise, it performs a manual login and creates a new session, while keeping the UUIDs the same to reduce bot detection.

4. **Scraping Logic**:
   - Calls `scrape.py` to handle the scraping of Instagram reels.
   - Performs human-like actions using the `perform_human_actions` function, including liking and commenting on posts to reduce bot detection.

5. **Uploading Logic**:
   - Handles the uploading of scraped reels, including adding descriptions, hashtags, and crediting the original posters. This logic is found in `upload.py`.

6. **Logging and Random Waits**:
   - Implements random waits between actions to mimic human behavior and avoid detection.
   - Logs all activities for traceability and debugging purposes.

7. **Error Handling**:
   - Enhanced error handling to catch and log unexpected issues during execution.

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

2. **Dashboard Integration**:
   - The dashboard is now displayed after each upload to provide real-time feedback on the program's status.

3. **Error Handling**:
   - Improved error handling during the upload process to catch and log issues more effectively.

#### utils.py

Contains utility functions for logging, status management, random sleeps, and managing JSON files for random wait times:

1. **Logging and Status Management**:
   - Functions for reading and updating status files, logging uploads, and handling random wait times.

2. **Random Sleeps**:
   - Implements random wait periods between actions to reduce bot detection.
   - Logs the random wait times to `random-waits.json`.

3. **File Management**:
   - Functions to delete old status and log files to ensure a clean setup.

4. **Version Handling**:
   - Manages the program version and displays it across the different scripts.

### Anti-Bot Detection

The program includes several features to avoid detection by Instagram:
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

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### Disclaimer

This script is intended for educational and personal use only. Use it responsibly and ensure you comply with Instagram’s terms of service and guidelines.

--- 

This README reflects the new updates in version 3.02, including version management, enhanced error handling, and improved integration of the dashboard.