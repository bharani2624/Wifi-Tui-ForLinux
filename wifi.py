import curses as c
import subprocess as sp
def wifi_list():
    result=sp.run(['nmcli','-t','-f','SSID,SECURITY','dev','wifi'],capture_output=True,text=True)
    networks=result.stdout.strip().split('\n')
    seen=set()
    filtered_networks=[net for net in networks if net and not (net in seen or seen.add(net))]

    return filtered_networks
def connectToWifi(ssid,password=None):
    if password:
        sp.run(['nmcli','device','wifi','connect',ssid,'password',password])
    else:
        sp.run(['nmcli','device','wifi','connect',ssid])
def tui(stdscr):
    c.curs_set(0)
    stdscr.clear()
    WifiList=wifi_list()
    selected=0

    while True:
        stdscr.clear()
        stdscr.addstr(0,0,"Networks Available:")
        for i,wifi in enumerate(WifiList):
            if i == selected:
                stdscr.addstr(i+1,0,f"⭐{wifi}",c.A_REVERSE)
            else:
                stdscr.addstr(i+1,0,f" {wifi}")
        key=stdscr.getch()
        if key == c.KEY_UP and selected > 0:
            selected -= 1
        elif key == c.KEY_DOWN and selected < len(WifiList) - 1:
            selected += 1
        elif key == ord('\n'):
            ssid=WifiList[selected].split(":")[0]
            stdscr.addstr(len(WifiList)+2,0,f"Connecting To {ssid}")
            stdscr.refresh()

            stdscr.addstr(len(WifiList)+3,0,f"Enter The Password 🔐(leave blank for open network): ")
            c.echo()
            password = stdscr.getstr(len(WifiList)+4,0).decode('utf-8')
            c.noecho()
            connectToWifi(ssid,password if password else None)
            break
        stdscr.refresh()
c.wrapper(tui)
