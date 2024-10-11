# InstagramTheftyScraperPosterHuman - Version 3.2.2

## Overview

**InstagramTheftyScraperPosterHuman** is a bot designed for automating the scraping, posting, and management of Instagram reels with added features to simulate human-like actions. This tool enables scraping reels from specified Instagram profiles, uploading them with customizable descriptions and hashtags, and mimicking real user behaviors like liking, following, and commenting on posts.

Here's the updated README file reflecting the version update and highlighting the loop error fix:

---

# InstagramTheftyScraperPosterHuman - Version 3.2.2

## Overview

**InstagramTheftyScraperPosterHuman** is a bot designed for automating the scraping, posting, and management of Instagram reels with added features to simulate human-like actions. This tool enables scraping reels from specified Instagram profiles, uploading them with customizable descriptions and hashtags, and mimicking real user behaviors like liking, following, and commenting on posts.

## Version 3.2.2 - October 10th, 2024

### Key Features and Enhancements

1. **Bug Fix - Loop Error During Scraping**:
   - Fixed a loop error that caused the bot to get stuck during the scraping phase when encountering specific profiles.

2. **Version Control and Cleanup**:
   - The bot now reflects version **3.2.2** and includes improved error handling and better retry mechanisms for the scraping loop.

3. **Session and Configuration Management**:
   - Sessions and configuration files are stored in dedicated directories (`user_sessions/` and `configs/`), making multi-account management seamless.
   - Credentials are securely encrypted using **Fernet** encryption and saved in YAML configuration files.

4. **Human-Like Behavior Simulation**:
   - Refined human-like behaviors such as random interactions (likes, comments, follows) to avoid detection.
   - Reels are scraped at intervals, with human-like delays and randomized actions, simulating natural usage patterns.

5. **Rate Limit Handling**:
   - Enhanced handling of Instagram rate limits and re-logins when required. The bot employs exponential backoff and session re-authentication to ensure stable performance.

6. **File Management and Logging**:
   - All relevant logs (e.g., scraping and uploading activities) are saved in `config_setup.log`, making it easier to debug and track the bot's actions.
   - Improved management of session cookies and automatic initialization of necessary JSON files (`status.json`, `random-upload-times.json`).

7. **Scraping and Uploading**:
   - **Scrape reels**: Reels are scraped from profiles at user-defined intervals. New scraping methods ensure no duplicates and better media handling.
   - **Uploading reels**: The bot now uploads reels with customizable descriptions, hashtags, and optional Instagram Story uploads.

8. **Dashboard**:
   - The bot includes a dashboard that provides real-time updates on scraping, uploading, and bot status.

---

## Why Version 3.2.2 is Better Than 3.2.1

1. **Loop Error Fix**:
   - Fixed an issue where the bot would get stuck in an infinite loop during the scraping phase if a specific profile caused errors. This fix ensures smoother and more stable operation.

2. **Streamlined Codebase**:
   - In version **3.2.2**, we improved error handling and session management, reducing the likelihood of the bot getting stuck or failing during crucial operations.

3. **Improved Human-like Actions**:
   - Version **3.2.2** enhanced the timing and randomization of human-like actions, making the bot’s behavior even more realistic.

4. **Better Error Handling**:
   - The latest version includes improved error handling during scraping and uploading processes. Errors are now logged more clearly, and the bot retries certain actions before giving up, enhancing stability.

5. **Enhanced Session Management**:
   - Updates in `auth.py` and `config_setup.py` have improved session management. Now, the bot better handles session cookies, ensuring that session information is retained between restarts. Re-login functionality has also been enhanced to prevent disruptions caused by expired sessions.

6. **Rate Limit Handling**:
   - The new version refines rate limit handling, ensuring smoother operations even when Instagram enforces rate limits. With exponential backoff and retry mechanisms, **3.2.2** is more robust in handling rate-limited scenarios.

7. **Configurable Deletion Intervals**:
   - Version **3.2.2** provides more flexibility with the option to configure reel deletion intervals, ensuring that old reels are deleted on time, keeping storage usage under control.

8. **Optimized Uploading Logic**:
   - The bot now incorporates retries during reel uploads in case of failure. With the improved `upload.py`, re-login attempts are made seamlessly when required, reducing downtime caused by session expiration.

9. **User Experience and Feedback**:
   - Visual feedback during scraping, uploading, and random wait periods has been improved. The progress bar feature now gives users a clearer idea of the bot’s current actions and status, making it more user-friendly.

---

## Installation

### Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/sujay1599/InstagramTheftyScraperPosterHuman.git
cd InstagramTheftyScraperPosterHuman
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Configuration Setup

```bash
python config_setup.py
```

The setup process will guide you through entering your Instagram credentials and configuring scraping, uploading, and other settings.

### 4. Run the Bot

Once the configuration is complete, you can run the bot:

```bash
python main.py
```

## Configuration

The bot’s configuration is stored in a `USERNAME_config.yaml` file, generated after running the `config_setup.py` script. This file holds settings for Instagram credentials, scraping, uploading, descriptions, and more.

### Example `USERNAME_config.yaml`:

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
hashtags:
  use_hashtags: true
  hashtags_list: "#hashtag1 #hashtag2"
credit:
  give_credit: true
leave_comment: true
comments:
  - "Nice reel!"
  - "Great post!"
deleting:
  delete_interval_minutes: 1440
custom_tags:
  - tag1
  - tag2
proxy: http://proxyserver:port  # Optional: Add your proxy server address
```

## Logging

Logs are saved in the `config_setup.log` file and include:

- Login attempts and results.
- Reels scraped and uploaded.
- Any errors encountered during scraping or uploading.

## CLI Arguments

You can reuse an existing configuration by passing the `--reuse-config` argument:

```bash
python config_setup.py --reuse-config
```

This will load an existing configuration if available, allowing for faster setup.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact

For any issues or contributions, feel free to msg me!
## Installation

### Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/sujay1599/InstagramTheftyScraperPosterHuman.git
cd InstagramTheftyScraperPosterHuman
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Configuration Setup

```bash
python config_setup.py
```

The setup process will guide you through entering your Instagram credentials and configuring scraping, uploading, and other settings.

### 4. Run the Bot

Once the configuration is complete, you can run the bot:

```bash
python main.py
```

## Configuration

The bot’s configuration is stored in a `USERNAME_config.yaml` file, generated after running the `config_setup.py` script. This file holds settings for Instagram credentials, scraping, uploading, descriptions, and more.

### Example `USERNAME_config.yaml`:

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
hashtags:
  use_hashtags: true
  hashtags_list: "#hashtag1 #hashtag2"
credit:
  give_credit: true
leave_comment: true
comments:
  - "Nice reel!"
  - "Great post!"
deleting:
  delete_interval_minutes: 1440
custom_tags:
  - tag1
  - tag2
proxy: http://proxyserver:port  # Optional: Add your proxy server address
```

## Logging

Logs are saved in the `config_setup.log` file and include:

- Login attempts and results.
- Reels scraped and uploaded.
- Any errors encountered during scraping or uploading.

## CLI Arguments

You can reuse an existing configuration by passing the `--reuse-config` argument:

```bash
python config_setup.py --reuse-config
```

This will load an existing configuration if available, allowing for faster setup.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact

For any issues or contributions, feel free to msg me!
