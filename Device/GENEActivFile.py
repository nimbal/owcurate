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

        # metadata stored in file header or related to entire file
        self.file_info = {          
            "serial_num": "",
            "device_type": "",
            "temperature_units": "",
            "measurement_frequency": "",
            "temp_frequency" : "",
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
            "number_of_pages": "",              # from header
            "pagecount" : None,                # count from datapacket
            "pagecount_match" : None,
            "samples" : None,
            "x-gain": 0,
            "x-offset": 0,
            "y-gain" : 0,
            "y-offset": 0,
            "z-gain": 0,
            "z-offset": 0,
            "volts": 0,
            "lux": 0}
            # ADD RANGE calculations
            # ADD SAMPLE RATES (TEMP DIFFERENT)

        # data read from file (may be partial pages and/or downsampled - see file_metadata)
        self.data = {
            "x" : [],
            "y" : [],
            "z" : [],
            "temperature" : [],
            "light" : [],
            "button" : [],
            "start_time": None,
            "sample_rate" : None,
            "temp_sample_rate" : None}

        self.remove_counter = 0

        self.drift_corrected = False

    def read(self, parse_data = True, start = 1, end = -1, downsample = 1,
             calibrate = True, correct_drift = False, update = True, quiet = False):

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
        self.file_info.update({
            "serial_num": self.header["Device Unique Serial Code"],
            "device_type": self.header["Device Type"],
            "temperature_units": self.header["Temperature Sensor Units"],
            "measurement_frequency": int(self.header["Measurement Frequency"].split(" ")[0]),
            "temp_frequency" : int(self.header["Measurement Frequency"].split(" ")[0]) / 300,
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
            "number_of_pages": int(self.header["Number of Pages"]),
            "x-gain": int(self.header["x gain"]),
            "x-offset": int(self.header["x offset"]),
            "y-gain": int(self.header["y gain"]),
            "y-offset": int(self.header["y offset"]),
            "z-gain": int(self.header["z gain"]),
            "z-offset": int(self.header["z offset"]),
            "volts": int(self.header["Volts"]),
            "lux": int(self.header["Lux"])
        })

        # get pagecount from data_packet

        # set match to true
        self.file_info["pagecount_match"] = True

        # get page counts
        pagecount = len(self.data_packet) / 10
        header_pagecount = self.file_info['number_of_pages']

        # check if pages read is an integer (lines read is multiple of 10)
        if not pagecount.is_integer():

            # set match to false and display warning
            self.file_info["pagecount_match"] = False
            print(f"****** WARNING: Pages read ({pagecount}) is not",
                  f"an integer, data may be corrupt.\n")

        # check if pages read matches header count
        if pagecount != header_pagecount:

            # set match to false and display warning
            self.file_info["pagecount_match"] = False
            print(f"****** WARNING: Pages read ({pagecount}) not equal to",
                  f"'Number of Pages' in header ({header_pagecount}).\n")

        # store pagecount as attribute
        self.file_info["pagecount"] = pagecount

        # cacluate number of samples
        self.file_info["samples"] = self.file_info["pagecount"] * 300

        #self.remove_counter = 0

        # parse data from hexadecimal
        if parse_data:
            self.parse_data(start = start, end = end, downsample = downsample, calibrate = calibrate,
                            correct_drift = correct_drift, update = update, quiet = quiet)

        if not quiet: print("Done reading file.")
    

    def parse_data(self, start = 1, end = -1, downsample = 1, calibrate = True,
                   correct_drift = False, update = True, quiet = False):

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

        pagecount = self.file_info["pagecount"]

        # check whether data has been read
        if (not self.header or self.data_packet is None
            or pagecount is None):

            print('****** WARNING: Cannot parse data because file has not',
                  'been read.\n')
            return

        if not quiet: print("Parsing data from hexadecimal ...")

        # store passed arguments before checking and modifying
        old_start = start
        old_end = end
        old_downsample = downsample

        # check start and end for acceptable values
        if start < 1: start = 1
        elif start > pagecount: start = round(pagecount)

        if end == -1 or end > pagecount: end = round(pagecount)
        elif end < start: end = start

        #check downsample for valid values
        if downsample < 1: downsample = 1
        elif downsample > 6: downsample = 6

        # get calibration variables
        if calibrate:
            x_offset = self.file_info["x-offset"]
            y_offset = self.file_info["y-offset"]
            z_offset = self.file_info["z-offset"]
            x_gain = self.file_info["x-gain"]
            y_gain = self.file_info["y-gain"]
            z_gain = self.file_info["z-gain"]
            volts = self.file_info["volts"]
            lux = self.file_info["lux"]
        
        # initialize lists to temporarily hold read data
        temp = []
        x = []
        y = []
        z = []
        light = []
        button = []

        total_pages = end - (start - 1)
        sample_rate = self.file_info['measurement_frequency']
        downsampled_rate = (sample_rate / downsample)
        meas_per_page = int(300 / downsample)

        # get start_time (time of first data point in view)
        start_time_line = self.data_packet[(start - 1) * 10 + 3]
        colon = start_time_line.index(':')
        start_time = start_time_line[colon + 1:]
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S:%f')

        # grab chunk of data from packet
        data_chunk = [self.data_packet[i]
                    for i in range((start - 1) * 10 + 9, end * 10, 10)]


        i = 0
        
        # loop through pages
        for data_line in data_chunk:

            i = i + 1

            # display progress
            if (i // 1000) * 1000 == i:
                if not quiet:
                    print("Current Progress: %f %%" % (100 * i / total_pages))

            # get temp from page header
            #temp.append(float(self.data_packet[(i * 10) + 5].split(":")[-1]))

            # loop through measurements in page
            for j in range(0, 300, downsample):

                # parse measurement from line and convert from hex to bin
                meas = data_line[j * 12 : (j + 1) * 12]
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


        # get all temp lines from data packet (1 per page)
        temp_chunk = [self.data_packet[i]
                      for i in range((start - 1) * 10 + 5, end * 10, 10)]

        # parse temp from temp lines and insert into dict
        for temp_line in temp_chunk:
            colon = temp_line.index(':')
            temp.append(float(temp_line[colon + 1:]))

        if not quiet: print("Storing parsed data ...")

        data= {"x" : np.array(x),
               "y" : np.array(y),
               "z" : np.array(z),
               "light" : np.array(light),
               "button" : np.array(button),
               "temperature" : np.array(temp),
               "start_time" : start_time,
               "sample_rate" : downsampled_rate,
               "temp_sample_rate" : self.file_info["temp_frequency"]}

        # update data attribute if requested
        if update: self.data = data

        # display message if start and end values were changed
        if old_start != start or old_end != end:
            print('****** WARNING: Start or end values were modified to fit',
                  'acceptable range.\n',
                  f'       Old range: {old_start} to {old_end}\n',
                  f'       New range: {start} to {end}\n')

        # display message downsample ratio was changed
        if old_downsample != downsample:
            print('****** WARNING: Downsample value was modified to fit',
                  'acceptable range.\n',
                  f'       Old value: {old_downsample}\n',
                  f'       New value: {downsample}\n')

        return data

        # correct clock drift if requested
        # if correct_drift: self.correct_drift(quiet = quiet)


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




