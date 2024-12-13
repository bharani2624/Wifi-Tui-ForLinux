#!/bin/bash

wifi_list=$(nmcli -t -f SSID dev wifi )

# Show menu
ssid=$(whiptail --title "Available WiFi Networks" --menu "Select a network:" 20 50 10 $(echo "$wifi_list" | awk '{print NR " " $0}') 3>&1 1>&2 2>&3)

[ $? -ne 0 ] && exit

# Ask for password
password=$(whiptail --title "WiFi Password" --passwordbox "Enter password for $ssid (leave blank for open network):" 10 50 3>&1 1>&2 2>&3)

# Connect to WiFi
if [ -z "$password" ]; then
    nmcli dev wifi connect "$ssid"
else
    nmcli dev wifi connect "$ssid" password "$password"
fi

whiptail --msgbox "Connected to $ssid!" 6 40
