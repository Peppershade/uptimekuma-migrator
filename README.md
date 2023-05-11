# Uptime Kuma Monitor Importer

This script allows you to sync/import monitors from UptimeRobot to Uptime Kuma using the Uptime Kuma API.

## Supported Monitor Types
While Uptime Kuma supports a wide range of monitor types, this script currently only supports the following monitor types:
### HTTP(s)
- Friendly Name
- URL
- Monitoring Interval
- Hostname

### Ping
- Friendly Name
- URL
- Monitoring Interval
- Hostname

### Keyword
- Friendly Name
- URL
- Monitoring Interval
- Hostname
- Keyword

### Port
- Friendly Name
- URL
- Monitoring Interval
- Hostname
- Port

## Prerequisites

Before running the script, make sure you have the following information:

- UptimeRobot API key: Obtain this from your UptimeRobot account.
- Uptime Kuma credentials: You need the protocol (http or https), URL or IP address of your Uptime Kuma instance, username, and password.

## Installation

1. Clone this repository or download the script to your local machine.

2. Install the required dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```


3. Update the following variables in the script:

- `uptimerobot_api_key`: Replace `'UPTIMEROBOT-API-KEY'` with your UptimeRobot API key.
- `uptimekuma_protocol`: Set this to `'http'` or `'https'` depending on the protocol used by your Uptime Kuma instance.
- `uptimekuma_url`: Replace `'127.0.0.1:3001'` with the domain or IP address of your Uptime Kuma instance.
- `uptimekuma_username`: Replace `'admin'` with your Uptime Kuma username.
- `uptimekuma_password`: Replace `'password'` with your Uptime Kuma password.
- `skip_paused_monitors`: Set this to `True` if you want to skip syncing paused monitors.
- `start_clean`: Set this to `True` if you want to clean all existing monitors from Uptime Kuma before syncing.

## Usage

To run the script, execute the following command:

```python sync.py```


The script will perform the following steps:

1. Fetch monitors from UptimeRobot API.
2. Sync each monitor to Uptime Kuma API.
3. Print status messages and errors for each monitor sync.

Please note that the script will print verbose output during the process.

## Notes

- The script uses the `requests` library to make API requests, so make sure it is installed before running the script.
- The `uptime_kuma_api` module is required for interacting with the Uptime Kuma API. Make sure it is present in the same directory as the script.

## License

This script is released under the [MIT License](LICENSE).

