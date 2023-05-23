import requests
import json
from uptime_kuma_api import UptimeKumaApi
from uptime_kuma_api import UptimeKumaException
from uptime_kuma_api import MonitorType

# Your details
uptimerobot_api_key = 'UPTIMEROBOT-API-KEY'  # your UptimeRobot API key
uptimekuma_protocol = 'https'  # http or https
uptimekuma_url = '127.0.0.1:3001'  # domain or IP address of your Uptime Kuma instance
uptimekuma_username = 'admin'  # your Uptime Kuma username
uptimekuma_password = 'password'  # your Uptime Kuma password

# Options
skip_paused_monitors = False  # skip paused monitors
expire_notification = False  # send notification when monitor expires (HTTPS monitors only)
start_clean = False  # clean all monitors from Uptime Kuma before syncing

# Uptime Kuma API login
uptimerobot_offset = 0
api = UptimeKumaApi(f'{uptimekuma_protocol}://{uptimekuma_url}')
api.login(uptimekuma_username, uptimekuma_password)


# Clean monitors from Uptime Kuma API
def clean_uptimekuma_monitors():
    """
    Cleans monitors from Uptime Kuma API.
    """
    print('Cleaning monitors from Uptime Kuma API.')
    monitors = api.get_monitors()
    for monitor in monitors:
        api.delete_monitor(monitor['id'])
        print(f"Monitor '{monitor['name']}' deleted from Uptime Kuma.")
    print('Done cleaning monitors from Uptime Kuma API.')

# Fetch monitors from UptimeRobot API
def fetch_uptimerobot_monitors():
    """
    Fetches monitor data from UptimeRobot API.
    Returns a list of monitors.
    """
    monitor_url = "https://api.uptimerobot.com/v2/getMonitors"

    payload = f"api_key={uptimerobot_api_key}&format=json&logs=1&offset={uptimerobot_offset}"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", monitor_url, data=payload, headers=headers)
    data = json.loads(response.text)

    if data['stat'] == 'ok':
        return data['monitors']
    else:
        raise Exception('Failed to fetch monitors from UptimeRobot API.')


# Sync monitor to Uptime Kuma API
def sync_monitor_to_uptimekuma(monitor):
    """
    Syncs a monitor to Uptime Kuma API.
    """

    # Check if monitor already exists in Uptime Kuma
    if check_if_monitor_exists(monitor):
        print(f"Monitor '{monitor['friendly_name']}' already exists in Uptime Kuma.")
        return

    # Skip paused monitors
    if skip_paused_monitors and monitor['status'] == 0:
        print(f"Monitor '{monitor['friendly_name']}' is paused and will be skipped.")
        return

    # Add PORT monitor
    if monitor['type'] == 4:
        try:
            api.add_monitor(
                type=MonitorType.PORT,
                name=monitor['friendly_name'],
                url=monitor['url'],
                interval=monitor['interval'],
                hostname=monitor['url'],
                port=monitor['port'],
            )
            print(f"Monitor '{monitor['friendly_name']}' added to Uptime Kuma with type PORT.")
        except UptimeKumaException as e:
            print(f"Monitor '{monitor['friendly_name']}' failed to sync to Uptime Kuma.")
            print(e)

            return

    # Add HTTP monitor
    elif monitor['type'] == 1:
        try:
            api.add_monitor(
                type=MonitorType.HTTP,
                name=monitor['friendly_name'],
                url=monitor['url'],
                hostname=monitor['url'],
                interval=monitor['interval'],
                expireNotification=expire_notification,
            )
            print(f"Monitor '{monitor['friendly_name']}' added to Uptime Kuma with type HTTP.")
        except UptimeKumaException as e:
            print(f"Monitor '{monitor['friendly_name']}' failed to sync to Uptime Kuma.")
            print(e)

    # Add KEYWORD monitor
    elif monitor['type'] == 2:
        try:
            if monitor['keyword_type'] == 1:
                flip = True
            else:
                flip = False
            api.add_monitor(
                type=MonitorType.KEYWORD,
                name=monitor['friendly_name'],
                url=monitor['url'],
                hostname=monitor['url'],
                interval=monitor['interval'],
                keyword=monitor['keyword_value'],
                upsideDown=flip,
            )
            print(f"Monitor '{monitor['friendly_name']}' added to Uptime Kuma with type KEYWORD.")
        except UptimeKumaException as e:
            print(f"Monitor '{monitor['friendly_name']}' failed to sync to Uptime Kuma.")
            print(e)

    # Add PING monitor
    elif monitor['type'] == 3:
        try:
            api.add_monitor(
                type=MonitorType.PING,
                name=monitor['friendly_name'],
                hostname=monitor['url'],
                url=monitor['url'],
                interval=monitor['interval'],
            )
            print(f"Monitor '{monitor['friendly_name']}' added to Uptime Kuma with type PING.")
        except UptimeKumaException as e:
            print(f"Monitor '{monitor['friendly_name']}' failed to sync to Uptime Kuma.")
            print(e)

    else:
        print(f"Monitor '{monitor['friendly_name']}' has an unsupported type.")
        return


# Check if monitor already exists in Uptime Kuma
def check_if_monitor_exists(monitor):
    """
    Checks if a monitor already exists in Uptime Kuma.
    Returns True if monitor exists, False if not.
    """
    monitors = api.get_monitors()
    for m in monitors:
        if m['name'] == monitor['friendly_name']:
            return True
    return False


# Clean monitors from Uptime Kuma API
if start_clean:
    clean_uptimekuma_monitors()
    print('Done cleaning monitors from Uptime Kuma API.')

# Fetch monitors from UptimeRobot API
print('Fetching monitors from UptimeRobot API.')
monitors = fetch_uptimerobot_monitors()
print(f'Fetched {len(monitors)} monitors from UptimeRobot API.')
# When there are 50 monitors, there are more monitors to fetch, limit is 50, keep going until there are no more monitors to fetch
if len(monitors) == 50:
    uptimerobot_offset += 50
    print(f'Fetching monitors from UptimeRobot API with offset {uptimerobot_offset}.')
    monitors += fetch_uptimerobot_monitors()
if len(monitors) == 100:
    uptimerobot_offset += 50
    print(f'Fetching monitors from UptimeRobot API with offset {uptimerobot_offset}.')
    monitors += fetch_uptimerobot_monitors()
if len(monitors) == 150:
    uptimerobot_offset += 50
    print(f'Fetching monitors from UptimeRobot API with offset {uptimerobot_offset}.')
    monitors += fetch_uptimerobot_monitors()


print(f'Fetched {len(monitors)} monitors from UptimeRobot API.')

# Sync each monitor to Uptime Kuma API
print('Syncing monitors to Uptime Kuma API.')
for monitor in monitors:
    sync_monitor_to_uptimekuma(monitor)
print('Done syncing monitors to Uptime Kuma API.')

# Quit program
print('Done!')
