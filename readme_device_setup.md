#Setup ODYSSEY
Ubuntu 22.04
Python3.10.6

#Enable ssh:
```bash
sudo apt update
sudo apt install openssh-server
```
Check SSH server status: ```sudo systemctl status ssh```
Get IP address: ```ip a```


#Enable RDP:
```bash
sudo apt install xrdp
```

Check RDP server status: ```sudo systemctl status xrdp```
If it is not running you might need to turn off Ubuntu's native RDP (which is less convenient than xrdp)
