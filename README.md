# e-inkCalendar


 Run the following command in the RPi Terminal to open crontab.
```bash
sudo crontab -e
```
 Specifically, add the following command to crontab so that the MagInkCal Python script runs each time the RPi is booted up.
```bash
@reboot sleep 20; cd /home/pi/e-inkCalendar && sudo python3 main.py &
```