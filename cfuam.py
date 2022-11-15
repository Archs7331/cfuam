# Credits to Pog for cf API help and Xplode for sneding his feet hh
import requests
import psutil
import os
import time
import toml

config = toml.load('config.toml')

url = "https://api.cloudflare.com/client/v4/zones//firewall/rules"
expid = config.get('cloudflare').get('expid')
firewallid = config.get('cloudflare').get('firewallid')
email = config.get('cloudflare').get('email')
apikey = config.get('cloudflare').get('apikey')
maxcpu = float(config.get('settings').get('cpumax'))
sleeptime = int(config.get('settings').get('sleep'))
uam = int(config.get('settings').get('uamtime'))
reqdebug = config.get('settings').get('reqdebug')

payload = [
    {
        "id": firewallid,
        "paused": False,
        "description": "simple",
        "action": "challenge",
        "filter": {"id": expid}
    }
]
headers = {
    "cookie": "Cookie",
    "X-Auth-Email": email,
    "X-Auth-Key": apikey,
    "Content-Type": "application/json"
}

payload2 = [
    {
        "id": firewallid,
        "paused": True,
        "description": "simple",
        "action": "challenge",
        "filter": {"id": expid}
    }
]
headers2 = {
    "cookie": "Cookie",
    "X-Auth-Email": email,
    "X-Auth-Key": apikey,
    "Content-Type": "application/json"
}

def main(url,expid,firewallid,email,apikey,payload,payload2,headers,headers2,maxcpu,sleeptime,uam,reqdebug):
    while (True):
        hide = "\033[?251"
        cpuload = psutil.cpu_percent()

        os.system("clear")
        print(f"current cpu load: {cpuload} | Max cpu load: {maxcpu}")

        time.sleep(sleeptime)

        if cpuload > float(maxcpu):
            enableuam = requests.request("PUT", url, json=payload, headers=headers)
            if reqdebug == True:
                print(enableuam.text)
            else:
                print(f"\x1b[1;31m[ATTACK] Max CPU Reached, Enabling UAM For {uam}\x1b[0;0m")
            time.sleep(uam)
            disableuam = requests.request("PUT", url, json=payload2, headers=headers2)

main(url,expid,firewallid,email,apikey,payload,payload2,headers,headers2,maxcpu,sleeptime,uam,reqdebug)
