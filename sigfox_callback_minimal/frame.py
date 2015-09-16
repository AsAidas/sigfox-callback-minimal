__author__ = 'hbuyse'

import datetime

DELTA_TEMP = 123.5
BITS_PER_BYTE = 255
DIFF_TEMP = 30

dft = dict()

dft["data"] = "000000000000000000000000"
dft["device"] = "00000000"
dft["snr"] = "00.00"
dft["time"] = "0000000000"


class Frame(object):

    """
    Documentation of Frame
    """

    def __init__(self, d=dft):
        self._data = d["data"]
        self._device = d["device"]
        self._snr = float(d["snr"])
        self._timestamp = int(d["time"])

    def __repr__(self):
        d = {
            "data": self.get_data(),
            "device": self.get_device(),
            "snr": self.get_snr(),
            "timestamp": self.get_timestamp(),
            "date_of_frame": self.get_date_of_frame(),
            "time_of_frame": self.get_time_of_frame(),
            "alert_type": self.get_alert_type(),
            "alert_name": self.get_alert_name(),
            "temperature": self.get_temperature(),
            "latitude": self.get_latitude(),
            "longitude": self.get_longitude(),
            "altitude": self.get_altitude(),
            "sign_longitude": self.get_sign_longitude(),
            "sign_latitude": self.get_sign_latitude(),
            "sign_altitude": self.get_sign_altitude(),
            "satellites": self.get_satellites(),
            "precision": self.get_precision(),
            "battery": self.get_battery_state(),
        }

        return str(d)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def get_device(self):
        return self._device

    def set_device(self, device):
        self._device = device

    def get_snr(self):
        return self._snr

    def set_snr(self, snr):
        self._snr = snr

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def get_date_of_frame(self):
        return datetime.datetime.fromtimestamp(
            self._timestamp).strftime('%d/%m/%Y')

    def get_time_of_frame(self):
        return datetime.datetime.fromtimestamp(
            self._timestamp).strftime('%H:%M:%S')

    def get_alert_type(self):
        return int(self._data[0], 16)

    def get_alert_name(self):
        return int(self._data[0], 16)

    def get_temperature(self):
        return (
            (DELTA_TEMP * int(self._data[1:3], 16)) / BITS_PER_BYTE) - DIFF_TEMP

    def get_latitude(self):
        return int(self._data[3:9], 16)

    def get_longitude(self):
        return int(self._data[9:15], 16)

    def get_altitude(self):
        return int(self._data[15:18], 16)

    def get_sign_longitude(self):
        return (int(self._data[18:20], 16) >> 7) & 0b00000001

    def get_sign_latitude(self):
        return (int(self._data[18:20], 16) >> 6) & 0b00000001

    def get_sign_altitude(self):
        return (int(self._data[18:20], 16) >> 5) & 0b00000001

    def get_satellites(self):
        return (int(self._data[18:20], 16) >> 2) & 0b00000111

    def get_precision(self):
        return int(self._data[18:20], 16) & 0b0000011

    def get_battery_state(self):
        return (int(self._data[20:21], 16) >> 3) & 0b00000001

    def get_datas(self):
        d = {
            "data": self.get_data(),
            "device": self.get_device(),
            "snr": self.get_snr(),
            "timestamp": self.get_timestamp(),
            "date_of_frame": self.get_date_of_frame(),
            "time_of_frame": self.get_time_of_frame(),
            "alert_type": self.get_alert_type(),
            "alert_name": self.get_alert_name(),
            "temperature": self.get_temperature(),
            "latitude": self.get_latitude(),
            "longitude": self.get_longitude(),
            "altitude": self.get_altitude(),
            "sign_longitude": self.get_sign_longitude(),
            "sign_latitude": self.get_sign_latitude(),
            "sign_altitude": self.get_sign_altitude(),
            "satellites": self.get_satellites(),
            "precision": self.get_precision(),
            "battery": self.get_battery_state(),
        }

        return d
