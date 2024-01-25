# DroneDeploy TIFF Downloader

## Overview
This Python script automates the downloading of TIFF images from DroneDeploy sites. It leverages the Selenium WebDriver to interact with web pages, performing tasks such as clicking buttons, checking checkboxes, and entering text programmatically. The script supports processing multiple links from a text file and handles each link sequentially.

## Prerequisites
- Python 3.x
- Selenium WebDriver
- Google Chrome or Chromium browser
- ChromeDriver executable that matches the version of your Chrome browser

## Setup
1. **Google Chrome User Data**: The script uses a specific Google user data directory to maintain session information. Ensure that the `USER_GOOGLE_ACCOUNT_ADDRESS` variable in the script points to your Google Chrome user data directory.
2. **ChromeDriver**: Download and place the ChromeDriver executable in your system PATH or specify its location in the script.

## Configuration
- **Links File (`LINK_TXT`)**: Specify the path to the text file containing the DroneDeploy site URLs.
- **Output Files**: The script logs processed links and errors to specific files (`PROCESSED_LINK_TXT`, `ERROR_TXT`). Ensure these files exist or the script can create them in the specified directory.

## Usage
1. Update the `LINK_TXT` file with the DroneDeploy site URLs you wish to download TIFF images from.
2. Run the script using Python: `python your_script_name.py`
3. The script will open a Chrome browser window, navigate to each URL, and perform the necessary steps to download the TIFF images.

## Error Handling
- The script logs any errors encountered during execution to the `ERROR_TXT` file. If the script cannot navigate to a page, click a button, or find an element, it logs the error along with the URL and a description.

## Note
- The script is configured to run in headless mode. To watch the script execute in real-time, you can comment out the headless option in the `chrome_options` configuration.

## Disclaimer
This script is for educational purposes. Please ensure you have the proper rights to download images from DroneDeploy sites.

## License

Enjoy automating your DroneDeploy downloads!
