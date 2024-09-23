# InstagramTheftyScraperPosterHuman - Version 3.2.0

## Overview

InstagramTheftyScraperPosterHuman is a bot designed to automate the scraping, posting, and management of Instagram reels with added functionality to mimic human-like actions. It allows users to scrape reels from various profiles, upload them with custom descriptions and tags, and even simulate interactions such as liking, following, and commenting.

This project focuses on automation while implementing safety measures like random actions and delays to prevent detection by Instagram’s anti-bot mechanisms.

## Version 3.2.0 - September 5, 2024

### New Features and Enhancements

1. **Version Control Integration**
   - Added a `version.txt` file to manage version control, allowing the program to display information such as the creator, version number, and the last known working date at startup.
   - Example format for `version.txt`:
     ```json
     {
         "created_by": "Sujay1599",
         "program_name": "InstagramTheftyScraperPosterHuman",
         "version": "3.2.0",
         "working_as_of": "2024-09-05"
     }
     ```

2. **Load Configuration Based on User Session**
   - New configuration loading based on the last username entered in the session, allowing for multi-account management with individual `config.yaml` files.

3. **Improved Cookie Injection**
   - Enhanced the cookie injection feature during Instagram login to avoid public request failures. Cookies from the session file are now properly loaded and injected to support public requests.

4. **Human-like Behavior Simulation**
   - Refined the `perform_human_actions()` function to include randomized human-like behaviors such as liking, following/unfollowing, and commenting on posts.
   - Improved the `random_sleep()` function to log wait times, adding more randomness and realism to the bot's actions.

5. **Enhanced Error Handling and Logging**
   - Added comprehensive logging across all functions to track execution, errors, and specific actions like waits and deletions.
   - Improved error handling in functions like `scrape_reels()` and `handle_rate_limit()` to manage issues like rate limits and failed scrapes/upload attempts gracefully.

6. **Progress Feedback**
   - Integrated a progress bar during sleep intervals with the `sleep_with_progress_bar()` function to provide visual feedback during long-running operations.

7. **File Management and Initialization**
   - Implemented automatic initialization for JSON files such as `status.json` using `initialize_json_file()` and `initialize_status_file()` to ensure they are properly set up with default values.
   - Enhanced file cleanup with functions like `delete_old_reels()` and `delete_uploaded_files()` to manage storage efficiently by deleting old or unnecessary files.

8. **Session and Configuration File Management**
   - Session files are now saved in the `user_sessions` directory, allowing each user to have a separate session file that maintains their login state.
   - Configuration files (`config.yaml`) are saved in the `configs` directory, allowing for easy management of multiple configurations for different users.
   - The `config_setup.log` file tracks all activities during the configuration process, including login attempts and encryption key generation.

---

### Why Version 3.2.0 is Better Than the Previous Versions

#### 1. **Enhanced User Experience for Multi-Account Management**
   - Version 3.2.0 introduces individual `config.yaml` files and session files per user, simplifying multi-account management. Users can now manage multiple Instagram accounts more efficiently, without mixing up configurations or login states.
   - Each user’s session is preserved in the `user_sessions` directory, and configuration files are saved in the `configs` directory. This was not available in previous versions, making this release far more flexible for users who manage multiple accounts.

#### 2. **Improved Stability with Cookie Injection**
   - The new cookie injection system reduces public request failures that were an issue in earlier versions. By injecting cookies from the session file into the client, the bot can maintain the session across both private and public requests, leading to a smoother experience and fewer login issues.
   - This enhancement reduces the frequency of re-authentication attempts, significantly improving the bot’s stability and reliability compared to older versions.

#### 3. **Better Rate Limit Handling**
   - Version 3.2.0 includes refined rate limit handling, allowing the bot to handle Instagram’s rate limits more gracefully. Instead of stopping the bot after a rate limit hit, the program now backs off with exponential delays and retries, reducing the chances of being blocked.
   - Previous versions were less capable of handling rate limits effectively, which could lead to unexpected crashes or blocked accounts.

#### 4. **More Realistic Human-Like Behavior**
   - Human-like actions such as liking, following, and commenting are much more randomized and realistic in this version. The improved `perform_human_actions()` function simulates real user interactions better, further lowering the bot’s detectability.
   - This new version adds a layer of protection against Instagram’s anti-bot measures that older versions lacked, making it safer to use.

#### 5. **Progress and Feedback Improvements**
   - A new progress bar feature during long-running sleep intervals provides users with visual feedback, making it easier to monitor the bot’s actions in real-time. This feature was not present in earlier versions, enhancing the overall user experience.
   - Additionally, comprehensive logging provides more transparency into the bot’s internal operations, making it easier for users to debug issues or understand the bot’s actions.

#### 6. **File Management and Cleanup**
   - The new version offers better file management, with automatic initialization for crucial files (`status.json`, `random-waits.json`, `random-upload-times.json`). Old or unnecessary media files are also deleted automatically, ensuring the program runs efficiently without accumulating excess storage.
   - Version 3.2.0 manages these files far more effectively compared to previous versions, where manual intervention was often required.

---

### Installation

#### Prerequisites
- **Python 3.9+**
- **pip** (Python package manager)

#### 1. Clone the Repository:
```bash
git clone https://github.com/sujay1599/InstagramTheftyScraperPosterHuman.git
cd InstagramTheftyScraperPosterHuman
```

#### 2. Install the Required Packages:
```bash
pip install -r requirements.txt
```

#### 3. Run the Configuration Setup:
To generate the `config.yaml` file, run:
```bash
python config_setup.py
```
Follow the prompts to enter your configuration details. This will generate a `config.yaml` file with the necessary settings, including encrypted Instagram credentials, proxy settings, default descriptions, and comments.

### Configuration

The `config.yaml` file will be generated by running `config_setup.py`. It includes the following settings:

- **Session files**: Stored in the `user_sessions` directory. Each session is saved with the username as the filename.
- **Configuration files**: Stored in the `configs` directory. Each user's configuration file is saved under their username.
- **Log file**: Configuration activities are logged in the `config_setup.log` file for debugging and tracking purposes.

Here’s an example of what the `config.yaml` file might look like:

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
proxy: http://proxyserver:port # Add your proxy address here if you use one
```

### How to Update to Version 3.2.0

1. **Re-clone the Repository**  
   Pull the latest version of the program by re-cloning the repository:
   ```bash
   git clone https://github.com/sujay1599/InstagramTheftyScraperPosterHuman.git
   cd InstagramTheftyScraperPosterHuman
   ```

2. **Validate the Update**  
   After cloning, check the `version.txt` file to ensure you are using the latest version:
   ```bash
   cat version.txt
   ```

   The file should contain:
   ```json
   {
       "created_by": "Sujay1599",
       "program_name": "InstagramTheftyScraperPosterHuman",
       "version": "3.2.0",
       "working_as_of": "2024-09-05"
   }
   ```

3. **Review and Update `config.yaml`**  
   Ensure your `config.yaml` file is updated and configured to your requirements. You can generate a new one if needed by running:
   ```bash
   python config_setup.py
   ```

4. **Run the Program**  
   After validating the update and configuring settings, run the program as usual to start using the new features:
   ```bash
   python

 main.py
   ```

### Known Issues

- **Rate Limit Handling**: The program now has improved rate limit handling, but it’s still possible to encounter rate limits if the bot is run too frequently. Adjust the scrape/upload intervals in `config.yaml` to mitigate this.
- **Duplication Check**: The new status management should prevent duplicates in `reels_scraped`, but if you encounter any issues, ensure the status file is properly initialized and updated.

### File Management Locations

- **Session Files**: `user_sessions/` directory. Each user’s session file is named after their Instagram username.
- **Configuration Files**: `configs/` directory. Each user’s configuration file is saved under their username.
- **Log Files**: `config_setup.log` is created in the root directory to track configuration activities.

### License

This project is licensed under the MIT License.

### Contact
For any issues or contributions, feel free to contact the creator:  
**Sujay1599** - sujay1599@github.com