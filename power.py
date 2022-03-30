import subprocess
import logging

class PowerHelper:
#https://github.com/PiSugar/pisugar-power-manager-rs#unix-domain-socket--webscoket--tcp
    def __init__(self):
        self.logger = logging.getLogger('eInkCalendar')

    def get_battery(self):
        # start displaying on eink display
        # command = ['echo "get battery" | nc -q 0 127.0.0.1 8423']
        battery_float = -1
        try:
            ps = subprocess.Popen(('echo', 'get battery'), stdout=subprocess.PIPE)
            result = subprocess.check_output(('nc', '-q', '0', '127.0.0.1', '8423'), stdin=ps.stdout)
            ps.wait()
            result_str = result.decode('utf-8').rstrip()
            battery_level = result_str.split()[-1]
            battery_float = float(battery_level)
            #battery_level = "{:.3f}".format(battery_float)
        except (ValueError, subprocess.CalledProcessError) as e:
            self.logger.info('Invalid battery output')
        return battery_float

    def set_next_boot_datetime(self, datetime):
        # TODO: For directly scheduling next boot instead of using PiSugar's web interface
        # Currently, it can be done manually through the PiSugar web interface
        return True

    def get_RTC_time(self) : 
        RTCDateTimeStr = ''
        try:
            ps = subprocess.Popen(('echo', 'get rtc_time'), stdout=subprocess.PIPE)
            result = subprocess.check_output(('nc', '-q', '0', '127.0.0.1', '8423'), stdin=ps.stdout)
            ps.wait()
            result_str = result.decode('utf-8').rstrip()
            RTCDateTimeStr = result_str.split()[-1]
        except subprocess.CalledProcessError:
            self.logger.info('Invalid command')

        return RTCDateTimeStr

    def sync_time(self):
        # To sync PiSugar RTC and Pi with web time
        try:
            ps = subprocess.Popen(('echo', 'rtc_web'), stdout=subprocess.PIPE)
            result = subprocess.check_output(('nc', '-q', '0', '127.0.0.1', '8423'), stdin=ps.stdout)
            ps.wait()
        except subprocess.CalledProcessError:
            self.logger.info('Invalid time sync command')