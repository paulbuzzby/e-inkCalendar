# Work in Progress
# e-inkCalendar

This repo contains the code needed to drive a 7.5" e-ink display and act as a calendar. This project uses a battery powered (PiSugar2) Raspberry Pi Zero 2 WH (or install your own headers). Calendar events are retrived from Micrsoft Outlook.com.
The layout is based off how the Ios Outlook client shows calendar information. This felt like the best use for the 480x800 space available in the e-ink display.

This project was inspired by [MagInkCal](https://github.com/speedyg0nz/MagInkCal/blob/main/README.md) and some of his code does appear in this project. That project uses a much bigger e-ink display and they are a bit too expensive for me.

I created this project as a way to learn python and github while building something usful. The device is magentically attached to my kitchen fridge. Updates as 6am every morning to show me todays planned events along with as many future events that can fit on the page

## Hardware Required
- [Raspberry Pi Zero 2 WH](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) - Header pins are needed to connect to the E-Ink display. A Pi Zero 1 should also work
- [Waveshare 800×480 7.5inch E-Ink display HAT for Raspberry Pi](https://www.waveshare.com/7.5inch-e-paper-hat.htm) - Be careful as there is a version that also does red. While you will be able to make it work the driver code would need changing. Make sure you just buy the black and white display
- [PiSugar2 for Raspberry Pi Zero](https://www.pisugar.com/) ([Tindie](https://www.tindie.com/products/pisugar/pisugar2-battery-for-raspberry-pi-zero/)) - Provides the RTC and battery for this project

## How It Works
Through PiSugar2's web interface, the onboard RTC can be set to wake and trigger the RPi to boot up daily at a time of your preference. Upon boot, a cronjob on the RPi is triggered to run a Python script that fetches calendar events from Microsoft Calendar for the next few days, and formats them into the desired layout before displaying it on the E-Ink display. The RPi then shuts down to conserve battery. The calendar remains displayed on the E-Ink screen, because well, E-Ink...

Features of the calendar: 
- Battery life needs more testing but should last a couple of weeks. The Rpi zero 2 may be more power hungry than the Rpi zero. Retriving the calendar information takes the most amount of time. Maybe this can be optimised. I also have to force a wait command in the CronJob to make sure the system connects to the wifi
- Displays Day and date then lists start time and duration of events
- The calendar always starts from today and fills with as many events that will fit.
- Battery level is displayed in top right corner
- Timestamp of when the last update occured printed on the bottom left of screen

## Bugs

- Not sure how the system handles events spanning multiple days
- Currently only works against outlook.com calendars


## Setting Up Raspberry Pi Zero
1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a MicroSD Card. I recommend using the Raspberry Pi Imager. You can then pre-configure Wifi and other information. A great timesaver


 Run the following command in the RPi Terminal to open crontab.
```bash
sudo crontab -e
```
 Specifically, add the following command to crontab so that the Python script runs each time the RPi is booted up.
```bash
@reboot sleep 20; cd /home/pi/e-inkCalendar && sudo python3 main.py &
```

## Config file
Should look like

```json
{
    "icsURL": "",    
    "dayToCapture": 8,
    "shutdownOnUpdate":true
}
```