#!/usr/bin/env python2
import curses as c
import subprocess as sp

def wifi_list():
    result = sp.run(['nmcli', '-t', '-f', 'SSID,SECURITY', 'dev', 'wifi'], 
                    capture_output=True, text=True)
    networks = result.stdout.strip().split('\n')
    seen = set()
    filtered_networks = [net for net in networks if net and not (net in seen or seen.add(net))]
    return filtered_networks

def connect_to_wifi(ssid, password=None):
    """Connect to a Wi-Fi network."""
    try:
        if password:
            sp.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], check=True)
        else:
            sp.run(['nmcli', 'device', 'wifi', 'connect', ssid], check=True)
    except sp.CalledProcessError:
        pass

def tui(stdscr):
    c.curs_set(0)
    stdscr.clear()

    wifi_list_data = wifi_list()
    if not wifi_list_data:
        stdscr.addstr(0, 0, "No Wi-Fi networks found.")
        stdscr.refresh()
        stdscr.getch()
        return

    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Networks Available:")
        for i, wifi in enumerate(wifi_list_data):
            ssid,security = wifi.split(':') #security is used to store the values after the , in split
            display_line = ssid 
            if i == selected:
                stdscr.addstr(i + 1, 0, f"⭐ {display_line}", c.A_REVERSE)
            else:
                stdscr.addstr(i + 1, 0, f"  {display_line}")

        key = stdscr.getch()
        if key == ord('q' or 'Q'):
            stdscr.addstr(len(wifi_list_data)+6,0,f"Exitting............")
            return 
        if key == c.KEY_UP and selected > 0:
            selected -= 1
        elif key == c.KEY_DOWN and selected < len(wifi_list_data) - 1:
            selected += 1
        elif key == ord('\n'):
            ssid = wifi_list_data[selected].split(":")[0]
            stdscr.addstr(len(wifi_list_data) + 2, 0, f"Connecting to {ssid}...")
            stdscr.refresh()

            stdscr.addstr(len(wifi_list_data) + 3, 0, "Enter the password 🔐 (leave blank for open network): ")
            c.echo()
            password = stdscr.getstr(len(wifi_list_data) + 4, 0).decode('utf-8')
            c.noecho()

            connect_to_wifi(ssid, password if password else None)
            stdscr.addstr(len(wifi_list_data) + 5, 0, f"Attempted connection to {ssid}. Press any key to exit.")
            stdscr.refresh()
            stdscr.getch()
            break

        stdscr.refresh()

c.wrapper(tui)
