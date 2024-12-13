#!/bin/bash

# Get WiFi list
wifi_list=$(nmcli -t -f SSID dev wifi | awk '!seen[$0]++')

# Show WiFi list in dialog
ssid=$(dialog --menu "Available WiFi Networks" 20 50 10 $(echo "$wifi_list" | awk '{print NR " " $0}') 3>&1 1>&2 2>&3)

# Exit if user cancels
[ $? -ne 0 ] && exit

# Ask for password
password=$(dialog --inputbox "Enter password for $ssid (leave blank for open network)" 10 50 3>&1 1>&2 2>&3)

# Connect to WiFi
if [ -z "$password" ]; then
    nmcli dev wifi connect "$ssid"
else
    nmcli dev wifi connect "$ssid" password "$password"
fi

# Notify user
dialog --msgbox "Connected to $ssid!" 6 40

