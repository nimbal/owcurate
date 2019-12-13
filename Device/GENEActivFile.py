# Authors:  David Ding
#           Kit Beyer


# ======================================== IMPORTS ========================================
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join

## == ISSUES =============================================



# ======================================== GENEActivFile CLASS ========================================
class GENEActivFile:
    def __init__(self, file_path):

        self.file_path = file_path
        self.header = {}
        self.data_packet = None
        #self.error_corrected = False # NOT SURE WHAT THIS IS FOR

        self.file_metadata = {
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
            "number_of_pages": ""}
        
        self.calibration_info = {
            "x-gain": 0,
            "x-offset": 0,
            "y-gain" : 0,
            "y-offset": 0,
            "z-gain": 0,
            "z-offset": 0,
            "volts": 0,
            "lux": 0}

        self.data = {
            "x" : [],
            "y" : [],
            "z" : [],
            "temperature" : [],
            "light" : [],
            "button" : []}

        self.samples = 0
        self.remove_counter = 0

        self.drift_corrected = False

    def read(self, parse_data = True, calibrate = True, correct_drift = False, quiet = False):

        '''
        read_from_raw reads a raw GENEActiv .bin file
        Args:
            parse_data: Bool
                Whether or not to parse the hexadecimal (as opposed to only returning header information)
            quiet: Bool
                Whether or not to print additional information
                TODO: Figure out how to change this into -v command

        Returns:

        '''

        # Read GENEActiv .bin file
        if not quiet: print("Reading %s ..." % self.file_path)
        bin_file = open(self.file_path, "r", encoding="utf-8")
        lines = np.array([line[:-1] for line in bin_file.readlines()])
        bin_file.close()

        # Separate header and data packets
        header_packet = lines[:59]
        self.data_packet = lines[59:]

        # Parse header into header dict
        if not quiet: print("Parsing header information ...")
        for line in header_packet:
            try:
                colon = line.index(":")
                self.header[line[:colon]] = line[colon + 1:].rstrip('\x00').rstrip()
            except ValueError:
                pass

        # Extract and format relevant metadata from header
        self.file_metadata.update({
            "serial_num": self.header["Device Unique Serial Code"],
            "device_type": self.header["Device Type"],
            "temperature_units": self.header["Temperature Sensor Units"],
            "measurement_frequency": int(self.header["Measurement Frequency"].split(" ")[0]),
            "measurement_period": int(self.header["Measurement Period"].split(" ")[0]), #???????
            "start_time": datetime.datetime.strptime(self.data_packet[3][10:], "%Y-%m-%d %H:%M:%S:%f"),
            "study_centre": self.header["Study Centre"],
            "study_code": self.header["Study Code"],
            "investigator_id": self.header["Investigator ID"],
            "exercise_type": self.header["Exercise Type"],
            "config_id": self.header["Config Operator ID"],
            "config_time": datetime.datetime.strptime(self.header["Config Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "config_notes": self.header["Config Notes"],
            "extract_id": self.header["Extract Operator ID"],
            "extract_time": datetime.datetime.strptime(self.header["Extract Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "extract_notes": self.header["Extract Notes"],
            "time_shift": float(self.header["Extract Notes"].split(" ")[3][:-2].replace(",", "")),
            "device_location": self.header["Device Location Code"],
            "subject_id": (int(self.header["Subject Code"]) if self.header["Subject Code"] is not "" else 0),
            "date_of_birth": self.header["Date of Birth"],
            "sex": self.header["Sex"],
            "height": self.header["Height"],
            "weight": self.header['Weight'],
            "handedness_code": self.header["Handedness Code"],
            "subject_notes": self.header["Subject Notes"],
            "number_of_pages": int(self.header["Number of Pages"])
        })
        self.calibration_info.update({
            "x-gain": int(self.header["x gain"]),
            "x-offset": int(self.header["x offset"]),
            "y-gain": int(self.header["y gain"]),
            "y-offset": int(self.header["y offset"]),
            "z-gain": int(self.header["z gain"]),
            "z-offset": int(self.header["z offset"]),
            "volts": int(self.header["Volts"]),
            "lux": int(self.header["Lux"])
        })

        self.samples = self.file_metadata["number_of_pages"] * 300
        self.remove_counter = 0

        # parse data from hexadecimal
        if parse_data:
            self.parse_data(calibrate = calibrate, correct_drift = correct_drift, quiet = quiet)

        if not quiet: print("Done reading file.")
    

    def parse_data(self, calibrate = True, correct_drift = False, quiet = False):

        def twos_comp(val, bits):
            """ This method calculates the twos complement value of the current bit
            Args:
                val: bin
                    Bits to be processed (Binary)
                bits: int
                    Total number of bits in the operation

            Returns:
                page_data: Integer value resulting from the twos compliment operation
            """
            if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                val = val - (1 << bits)  # compute negative value
            return val


        if not quiet: print("Parsing data from hexadecimal ...")

        # get calibration variables
        if calibrate:
            x_offset = self.calibration_info["x-offset"]
            y_offset = self.calibration_info["y-offset"]
            z_offset = self.calibration_info["z-offset"]
            x_gain = self.calibration_info["x-gain"]
            y_gain = self.calibration_info["y-gain"]
            z_gain = self.calibration_info["z-gain"]
            volts = self.calibration_info["volts"]
            lux = self.calibration_info["lux"]
        
        # initialize lists to temporarily hold read data
        temp = []
        x = []
        y = []
        z = []
        light = []
        button = []

        start = 1
        end = self.file_metadata["number_of_pages"]

        # loop through pages
        for i in range(end):

            # display progress
            if (i // 1000) * 1000 == i:
                if not quiet:
                    print("Current Progress: %f %%" % (100 * i / end))

            # get temp from page header
            temp.append(float(self.data_packet[(i * 10) + 5].split(":")[-1]))

            # get page data hex line
            page_hex = self.data_packet[(i * 10) + 9]

            # loop through measurements in page
            for j in range(300):

                # parse measurement from line and convert from hex to bin
                meas = page_hex[j * 12 : (j + 1) * 12]
                meas = bin(int(meas, 16))[2:]
                meas = meas.zfill(48)

                # parse each signal from measurement and convert to int
                meas_x = int(meas[0:12], 2)
                meas_y = int(meas[12:24], 2)
                meas_z = int(meas[24:36], 2)
                meas_light = int(meas[36:46], 2)
                meas_button = int(meas[46], 2)
                # res = int(curr[47], 2) - NOT USED

                # use twos complement to get signed integer for accelerometer data
                meas_x = twos_comp(meas_x, 12)
                meas_y = twos_comp(meas_y, 12)
                meas_z = twos_comp(meas_z, 12)
                #light = twos_comp(light, 10) # NOT NEEDED, not a signed integer? TEST TO SEE IF THIS FIXES HIGH VALUES??

                # calibrate data if requrested
                if calibrate:
                    meas_x = (meas_x * 100 - x_offset) / x_gain
                    meas_y = (meas_y * 100 - y_offset) / y_gain
                    meas_z = (meas_z * 100 - z_offset) / z_gain
                    meas_light = (meas_light * lux) / volts

                # append measurement to data list
                x.append(meas_x)
                y.append(meas_y)
                z.append(meas_z)
                light.append(meas_light)
                button.append(meas_button)
                

        if not quiet: print("Storing parsed data ...")

        # convert data to numpy arrays and store in data dictionary attribute
        self.data["x"] = np.array(x)
        self.data["y"] = np.array(y)
        self.data["z"] = np.array(z)
        self.data["light"] = np.array(light)
        self.data["button"] = np.array(button)
        self.data["temperature"] = np.array(temp)

        # correct clock drift if requested
        if correct_drift: self.correct_drift(quiet = quiet)


    def correct_drift(self, force = False, quiet = False):

        '''
        calculate_time_shift adds one null sample (or deletes one sample) every X number of samples
        X is determined through the GENEActiv Clock Drift measurement
        Args:
            force: bool
                If time shift has already been done, the time_shifted will be True.
                force is an optional parameter that neglects that and will shift regardless

        Returns:

        '''
        if (self.drift_corrected and force) or (not self.drift_corrected):
            self.remove_counter = abs(self.samples / (self.file_metadata["time_shift"] * self.file_metadata["measurement_frequency"]))

            if not quiet: print("Correcting clock drift ...")

            if self.metadata["time_shift"] > 0:
                # We need to remove every nth value (n = remove_counter)
                self.x = np.delete(self.x,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.x) / self.remove_counter))])

                self.y = np.delete(self.y,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.y) / self.remove_counter))])

                self.z = np.delete(self.z,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.z) / self.remove_counter))])

                self.light = np.delete(self.light,
                                       [int(self.remove_counter * i) for i in
                                        range(int(len(self.light) / self.remove_counter))])

                self.button = np.delete(self.button,
                                        [int(self.remove_counter * i) for i in
                                         range(int(len(self.button) / self.remove_counter))])

            else:
                # We need to add a 0 value every remove_counter indices
                self.x = np.insert(self.x,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.x) / self.remove_counter))], 0)

                self.y = np.insert(self.y,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.y) / self.remove_counter))], 0)

                self.z = np.insert(self.z,
                                   [int(self.remove_counter * i) for i in
                                    range(int(len(self.z) / self.remove_counter))], 0)

                self.light = np.insert(self.light,
                                       [int(self.remove_counter * i) for i in
                                        range(int(len(self.light) / self.remove_counter))], 0)

                self.button = np.insert(self.button,
                                        [int(self.remove_counter * i) for i in
                                         range(int(len(self.button) / self.remove_counter))], 0)
            self.drift_corrected = True

            # CORRECT SAMPLE COUNTER AFTER DRIFT CORRECTION
            
        else:
            print("Times have already been shifted. To shift again, run with param force=True")

    def PDFSummary(self):

        return 0




