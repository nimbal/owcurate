
# ======================================== IMPORTS ========================================
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join


class GENEActiv():
    def __init__(self, path):
        self.file = path
        self.file_name = path.split("/")[-1],
        self.working_directory = path.split("/")[:-1]
        self.metadata = {
            "serial_num": "",
            "device_type": "",
            "temperature_units": "",
            "measurement_frequency": "",
            "measurement_period": "",
            "start_time": "",
            "study_centre": "",
            "study_code": "",
            "investigator_id": "",
            "exercise_type": "",
            "config_id": "",
            "config_time": "",
            "config_notes": "",
            "extract_id": "",
            "extract_time": "",
            "extract_notes": "",
            "device_location": "",
            "subject_id": "",
            "date_of_birth": "",
            "sex": "",
            "height": "",
            "weight": "",
            "handedness_code": "",
            "subject_notes": "",
            "number_of_pages": ""
        }
        self.calibration_info = {
            "x-gain": 0,
            "x-offset": 0,
            "y-gain" : 0,
            "y-offset": 0,
            "z-gain": 0,
            "z-offset": 0,
            "volts": 0,
            "lux": 0
        }

        self.error_corrected = False
        self.time_shifted = False
        self.x = None
        self.y = None
        self.z = None
        self.temperature = None
        self.light = None
        self.button = None
        self.samples = 0
        self.remove_counter = 0

    def read_from_raw(self, quiet=False, parsehex=True):

        def twos_comp(val, bits):
            """ This method calculates the twos complement value of the current bit
            Args:
                val: bin
                    Bits to be processed (Binary)
                bits: int
                    Total number of bits in the operation

            Returns:
                Integer value resulting from the twos compliment operation
            """
            if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                val = val - (1 << bits)  # compute negative value
            return val

        def process_curr(raw_hex, offsets, gains, volts, lux):
            """ This method processes the current line of "page" of data as defined by GENEActiv

            Args:
                raw_hex: str
                    String of Hexadecimal data to be parsed as per their descriptors
                offsets: tuple
                    Stores the offsets for the three channels in a tuple (x, y, z)
                gains: tuple
                    Stores the gains for the three channels in a tuple (x, y, z)

            Returns:
                list of tuples : Each tuple will contain (x, y, z) samples for that time

            """
            returned_array = []
            x_offset, y_offset, z_offset = offsets
            x_gain, y_gain, z_gain = gains

            for i in range(300):
                curr = bin(int(raw_hex[i * 12: (i + 1) * 12], 16))[2:]
                curr = curr.zfill(48)
                x_comp = curr[0:12]
                y_comp = curr[12:24]
                z_comp = curr[24:36]
                light = curr[36:46]           # TODO: These variables are not used, not sure if they will be used
                button = int(curr[46], 2)
                res = int(curr[47], 2)

                # run the twos component value on each composition which starts in binary form
                x_comp = twos_comp(int(x_comp, 2), 12)
                y_comp = twos_comp(int(y_comp, 2), 12)
                z_comp = twos_comp(int(z_comp, 2), 12)
                light = twos_comp(int(light, 2), 10)

                # run the modifiers as prescribed in the GENEActiv documentation
                x_comp = (x_comp * 100 - x_offset) / x_gain
                y_comp = (y_comp * 100 - y_offset) / y_gain
                z_comp = (z_comp * 100 - z_offset) / z_gain
                light = (light * lux) / volts

                returned_array.append((x_comp, y_comp, z_comp, light, button))

            return returned_array

        # Variable Declaration and Initialization

        lines = None
        header_packet = None
        data_packet = None
        bin_file = None
        header = {}

        # Getting input
        print("Opening %s" % self.file)
        bin_file = open(self.file, "r", encoding="utf-8")
        lines = np.array([line[:-1] for line in bin_file.readlines()])
        bin_file.close()
        print("Done reading, parsing Header Information")

        # Parsing Input
        header_packet = lines[:59]
        data_packet = lines[59:]

        # Getting Data from the header
        for line in header_packet:
            try:
                colon = line.index(":")
                header[line[:colon]] = (line[colon + 1:].rstrip('\x00').rstrip())
            except ValueError:
                pass

        # Extracting and saving relevant information from header dictionary
        # UPDATING HEADER DICTIONARY
        self.metadata.update({
            # "visit_num": int(self.file.split("_")[3]),
            "serial_num": header["Device Unique Serial Code"],
            "device_type": header["Device Type"],
            "temperature_units": header["Temperature Sensor Units"],
            "measurement_frequency": int(header["Measurement Frequency"].split(" ")[0]),
            "measurement_period": int(header["Measurement Period"].split(" ")[0]),
            "start_time": datetime.datetime.strptime(data_packet[3][10:], "%Y-%m-%d %H:%M:%S:%f"),
            "study_centre": header["Study Centre"],
            "study_code": header["Study Code"],
            "investigator_id": header["Investigator ID"],
            "exercise_type": header["Exercise Type"],
            "config_id": header["Config Operator ID"],
            "config_time": datetime.datetime.strptime(header["Config Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "config_notes": header["Config Notes"],
            "extract_id": header["Extract Operator ID"],
            "extract_time": datetime.datetime.strptime(header["Extract Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "extract_notes": header["Extract Notes"],
            "time_shift": float(header["Extract Notes"].split(" ")[-1][:-2]),
            "device_location": header["Device Location Code"],
            "subject_id": int(header["Subject Code"]),
            "date_of_birth": header["Date of Birth"],
            "sex": header["Sex"],
            "height": header["Height"],
            "weight": header['Weight'],
            "handedness_code": header["Handedness Code"],
            "subject_notes": header["Subject Notes"],
            "number_of_pages": int(header["Number of Pages"])
        })
        self.calibration_info.update({
            "x-gain": int(header["x gain"]),
            "x-offset": int(header["x offset"]),
            "y-gain": int(header["y gain"]),
            "y-offset": int(header["y offset"]),
            "z-gain": int(header["z gain"]),
            "z-offset": int(header["z offset"]),
            "volts": int(header["Volts"]),
            "lux": int(header["Lux"])
        })

        self.samples = self.metadata["number_of_pages"] * 300
        self.remove_counter = 0

        print("Done Reading Header Information")

        if parsehex:
            if not quiet:
                print("Reading and parsing hexadecimal")

            # Appending relevant information from parsed hexadecimal data
            temps = []
            x = []
            y = []
            z = []
            light = []
            button = []
            for i in range(self.metadata["number_of_pages"]):
                if (i // 1000) * 1000 == i:
                    if not quiet:
                        print("Current Progress: %f %%" % (100 * i / self.metadata["number_of_pages"]))
                curr_chunk = process_curr(data_packet[(i * 10) + 9], (self.calibration_info["x-offset"],
                                                                      self.calibration_info["y-offset"],
                                                                      self.calibration_info["z-offset"]),
                                          (self.calibration_info["x-gain"],
                                           self.calibration_info["y-gain"],
                                           self.calibration_info["z-gain"]),
                                          self.calibration_info["volts"],
                                          self.calibration_info["lux"])
                temps.append(float(data_packet[(i * 10) + 5].split(":")[-1]))
                x.extend([curr_chunk[j][0] for j in range(300)])
                y.extend([curr_chunk[j][1] for j in range(300)])
                z.extend([curr_chunk[j][2] for j in range(300)])
                light.extend([curr_chunk[j][3] for j in range(300)])
                button.extend([curr_chunk[j][4] for j in range(300)])

            self.x = np.array(x)
            self.y = np.array(y)
            self.z = np.array(z)
            self.light = np.array(light)
            self.button = np.array(button)
            self.temperature = np.array(temps)

    def calculate_time_shift(self, force=False):
        if (self.time_shifted and force) or (not self.time_shifted):
            self.remove_counter = abs(self.samples / (self.metadata["time_shift"] * self.metadata["frequency"]))
            if self.metadata["time_shift"] > 0:
                # We need to remove every nth value (n = remove_counter)
                self.x = np.delete(self.x,
                                   [(self.remove_counter * i) for i in range(int(len(self.x) / self.remove_counter))])
                self.y = np.delete(self.y,
                                   [(self.remove_counter * i) for i in range(int(len(self.y) / self.remove_counter))])
                self.z = np.delete(self.z,
                                   [(self.remove_counter * i) for i in range(int(len(self.z) / self.remove_counter))])

            else:
                # We need to add a 0 value every remove_counter indices
                self.x = np.insert(self.x,
                                   [(self.remove_counter * i) for i in range(int(len(self.x) / self.remove_counter))], 0)
                self.y = np.insert(self.y,
                                   [(self.remove_counter * i) for i in range(int(len(self.y) / self.remove_counter))], 0)
                self.z = np.insert(self.z,
                                   [(self.remove_counter * i) for i in range(int(len(self.z) / self.remove_counter))], 0)
        else:
            print("Times have already been shifted. To shift again, run with param force=True")

    def PDFSummary(self):

        return 0




