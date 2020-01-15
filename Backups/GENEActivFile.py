# Authors:  David Ding
#           Kit Beyer


# ======================================== IMPORTS ========================================
import numpy as np
import datetime
import os
import shutil
import fpdf
import matplotlib.pyplot as plt
import matplotlib.style as mstyle
import matplotlib.dates as mdates

mstyle.use('fast')




# ======================================== GENEActivFile CLASS ========================================
class GENEActivFile:

    def __init__(self, file_path):

        self.file_path = file_path
        self.header = {}
        self.data_packet = None

        # metadata stored in file header or related to entire file
        self.file_info = {
            "serial_num" : None,
            "device_type" : None,
            "temperature_units" : None,
            "measurement_frequency" : None,
            "temp_frequency" : None,
            "measurement_period" : None,
            "start_time" : None,
            "study_centre" : None,
            "study_code" : None,
            "investigator_id" : None,
            "exercise_type" : None,
            "config_id" : None,
            "config_time" : None,
            "config_notes" : None,
            "extract_id" : None,
            "extract_time" : None,
            "extract_notes" : None,
            "clock_drift" : None,
            "clock_drift_rate" : None,
            "device_location": None,
            "subject_id": None,
            "date_of_birth": None,
            "sex": None,
            "height": None,
            "weight": None,
            "handedness_code": None,
            "subject_notes": None,
            "number_of_pages": None,              # from header
            "pagecount" : None,                # count from datapacket
            "pagecount_match" : None,
            "samples" : None,
            "x_gain": None,
            "x_offset": None,
            "y_gain" : None,
            "y_offset": None,
            "z_gain": None,
            "z_offset": None,
            "volts": None,
            "lux": None,
            "x_min" : None,
            "y_min" : None,
            "z_min" : None,
            "x_max" : None,
            "y_max" : None,
            "z_max" : None,
            "light_min" : None,
            "light_max" : None}

        # data read from file (may be partial pages and/or downsampled - see file_metadata)
        self.data = {
            "x" : [],
            "y" : [],
            "z" : [],
            "temperature" : [],
            "light" : [],
            "button" : [],
            "start_page" : None,
            "end_page" : None,
            "start_time" : None,
            "sample_rate" : None,
            "temp_sample_rate" : None}


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

        # if file does not exist then exit
        if not os.path.exists(self.file_path):

            print(f"****** WARNING: {self.file_path} does not exist.\n")
            return

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
            "serial_num" : self.header["Device Unique Serial Code"],
            "device_type" : self.header["Device Type"],
            "temperature_units" : self.header["Temperature Sensor Units"],
            "measurement_frequency" : int(self.header["Measurement Frequency"].split(" ")[0]),
            "temp_frequency" : int(self.header["Measurement Frequency"].split(" ")[0]) / 300,
            "measurement_period" : int(self.header["Measurement Period"].split(" ")[0]), #???????
            "start_time" : datetime.datetime.strptime(self.data_packet[3][10:], "%Y-%m-%d %H:%M:%S:%f"),
            "study_centre" : self.header["Study Centre"],
            "study_code" : self.header["Study Code"],
            "investigator_id" : self.header["Investigator ID"],
            "exercise_type" : self.header["Exercise Type"],
            "config_id" : self.header["Config Operator ID"],
            "config_time" : datetime.datetime.strptime(self.header["Config Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "config_notes" : self.header["Config Notes"],
            "extract_id" : self.header["Extract Operator ID"],
            "extract_time" : datetime.datetime.strptime(self.header["Extract Time"], "%Y-%m-%d %H:%M:%S:%f"),
            "extract_notes" : self.header["Extract Notes"],
            "clock_drift" : float(self.header["Extract Notes"].split(" ")[3][:-2].replace(",", "")),
            "device_location" : self.header["Device Location Code"],
            "subject_id" : self.header["Subject Code"],
            "date_of_birth" : self.header["Date of Birth"],
            "sex" : self.header["Sex"],
            "height" : self.header["Height"],
            "weight" : self.header['Weight'],
            "handedness_code" : self.header["Handedness Code"],
            "subject_notes" : self.header["Subject Notes"],
            "number_of_pages" : int(self.header["Number of Pages"]),
            "x_gain" : int(self.header["x gain"]),
            "x_offset" : int(self.header["x offset"]),
            "y_gain" : int(self.header["y gain"]),
            "y_offset" : int(self.header["y offset"]),
            "z_gain" : int(self.header["z gain"]),
            "z_offset" : int(self.header["z offset"]),
            "volts" : int(self.header["Volts"]),
            "lux" : int(self.header["Lux"]),
            "x_min" : (-204800 - int(self.header['x offset'])) / int(self.header['x gain']),
            "y_min" : (-204800 - int(self.header['y offset'])) / int(self.header['y gain']),
            "z_min" : (-204800 - int(self.header['z offset'])) / int(self.header['z gain']),
            "x_max" : (204700 - int(self.header['x offset'])) / int(self.header['x gain']),
            "y_max" : (204700 - int(self.header['y offset'])) / int(self.header['y gain']),
            "z_max" : (204700 - int(self.header['z offset'])) / int(self.header['z gain']),
            "light_min" : 0 * int(self.header['Lux']) / int(self.header['Volts']),
            "light_max" : 1023 * int(self.header['Lux']) / int(self.header['Volts'])})

        # calculate pagecount from data_packet

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

        #calculate clock drift rate
        total_seconds = (self.file_info["extract_time"] - self.file_info["config_time"]).total_seconds()
        self.file_info["clock_drift_rate"] = self.file_info["clock_drift"] / total_seconds

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
        if not self.header or self.data_packet is None or pagecount is None:

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
            x_offset = self.file_info["x_offset"]
            y_offset = self.file_info["y_offset"]
            z_offset = self.file_info["z_offset"]
            x_gain = self.file_info["x_gain"]
            y_gain = self.file_info["y_gain"]
            z_gain = self.file_info["z_gain"]
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

            i += 1

            # display progress
            if (i // 1000) * 1000 == i:
                if not quiet:
                    print("Current Progress: %f %%" % (100 * i / total_pages))

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

        data = {"x" : np.array(x),
                "y" : np.array(y),
                "z" : np.array(z),
                "light" : np.array(light),
                "button" : np.array(button),
                "temperature" : np.array(temp),
                "start_page" : start,
                "end_page" : end,
                "start_time" : start_time,
                "sample_rate" : downsampled_rate,
                "temp_sample_rate" : self.file_info["temp_frequency"]}

         # correct clock drift
        if correct_drift:

            if not quiet: print("Correcting clock drift ...")

            adjust_rate = abs(1 / self.file_info["clock_drift_rate"])
            time_to_start = (data["start_time"] - self.file_info["config_time"]).total_seconds()
            adjust_start = int(time_to_start * data["sample_rate"] * abs(self.file_info["clock_drift_rate"]))
            adjust_start_temp = int(time_to_start * data["temp_sample_rate"] * abs(self.file_info["clock_drift_rate"]))

            if self.file_info["clock_drift_rate"] > 0: #if drift is positive then remove extra samples


                for key in ["x", "y", "z", "light", "button", "temperature"]:

                    # delete data from each signal
                    data[key] = np.delete(data[key],
                                          [round(adjust_rate * (i + 1)) for i in
                                           range(int(len(data[key]) / adjust_rate))])


                    # delete data from start of each signal to account for time from config to start
                    if key is "temperature":
                        data[key] = np.delete(data[key], range(adjust_start_temp))
                    else:
                        data[key] = np.delete(data[key], range(adjust_start))


            else: #else add samples

                for key in ["x", "y", "z", "light", "button", "temperature"]:

                    # insert data into each signal
                    data[key] = np.insert(data[key],
                                          [round(adjust_rate * (i + 1)) for i in
                                           range(int(len(data[key]) / adjust_rate))], 0)


                    # insert data into start of each signal to account for time from config to start
                    if key is "temperature":
                        data[key] = np.insert(data[key], 0, [0] * adjust_start_temp)
                    else:
                        data[key] = np.insert(data[key], 0, [0] * adjust_start)


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

    def create_pdf(self, pdf_folder, window_hours = 4, downsample = 5,
                   correct_drift = False, quiet = False):

        '''creates a pdf summary of the file
        Parameters
        ----------
        pdf_folder : str
            path to folder where pdf will be stored
        window_hours : int
            number of hours to display on each page (default = 4) -- if hour occurs
            in the middle of a data page then time displayed on each pdf page may
            be slightly less than the number of hours specified
        downsample : int
            factor by which to downsample (range: 1-6, default = 5)
        correct_drift: bool
            should sample rate be adjusted for clock drift? (default = False)
        
        Returns
        -------
        pdf_path : str
            path to pdf file created
        '''

        # check whether data has been read
        if not self.header or self.data_packet is None or self.file_info["pagecount"] is None:
            print("****** WARNING: Cannot view data because file has not",
                  "been read.")
            return

        if not quiet: print("Creating PDF summary ...")

        # get filenames and paths     
        bin_name = os.path.basename(self.file_path)

        base_name = os.path.splitext(bin_name)[0]

        pdf_name = base_name + ".pdf"
        pdf_path = os.path.join(pdf_folder, pdf_name)

        png_folder = os.path.join(pdf_folder, "temp", "")

        # adjust sample rate for clock drift?
        sample_rate = self.file_info["measurement_frequency"]

        # calculate pages per plot
        window_pages = round((window_hours * 60 * 60 * sample_rate) / 300)
        window_sequence = range(1, round(self.file_info["pagecount"]), window_pages)
        #window_sequence = range(1, window_pages*6, window_pages)

        # CREATE PLOTS ------

        if not quiet: print("Generating plots ...")

        # define date locators and formatters
        #hours = mdates.HourLocator()
        #hours_fmt = mdates.DateFormatter('%H:%M')

        # set plot parameters

        # each accel axis has a different min and max based on the digital range
        # and the offset and gain values (-8 to 8 stated in the header is just
        # a minimum range, actual range is slightly larger)

        accel_min = min([self.file_info["x_min"],
                         self.file_info["y_min"],
                         self.file_info["z_min"]])
        accel_max = max([self.file_info["x_max"],
                         self.file_info["y_max"],
                         self.file_info["z_max"]])
        accel_range = accel_max - accel_min
        accel_buffer = accel_range * 0.1

        light_min = self.file_info["light_min"]
        light_max = self.file_info["light_max"]
        light_range = light_max - light_min
        light_buffer = light_range * 0.1

        yaxis_lim = [[accel_min - accel_buffer, accel_max + accel_buffer],
                    [accel_min - accel_buffer, accel_max + accel_buffer],
                    [accel_min - accel_buffer, accel_max + accel_buffer],
                    [light_min - light_buffer, light_max + light_buffer],
                    [-0.01, 1],
                    [9.99, 40.01]]

        yaxis_ticks = [[-8, 0, 8],
                       [-8, 0, 8],
                       [-8, 0, 8],
                       [0, 10000, 20000, 30000],
                       [0, 1],
                       [10, 20, 30, 40]]

        yaxis_units = [self.header["Accelerometer Units"],
                       self.header["Accelerometer Units"],
                       self.header["Accelerometer Units"],
                       self.header["Light Meter Units"],
                       "",
                       self.header["Temperature Sensor Units"]]

        yaxis_lines = [[self.file_info["x_min"], 0, self.file_info["x_max"]],
                       [self.file_info["y_min"], 0, self.file_info["y_max"]],
                       [self.file_info["z_min"], 0, self.file_info["z_max"]],
                       [light_min, light_max]]


        line_color = ["b", "g", "r", "c", "m", "y"]

        plt.rcParams["lines.linewidth"] = 0.25
        plt.rcParams["figure.figsize"] = (6, 7.5)
        plt.rcParams["figure.subplot.top"] = 0.92
        plt.rcParams["figure.subplot.bottom"] = 0.06
        plt.rcParams["font.size"] = 8

        # create temp folder to store .png files
        if not os.path.exists(png_folder): os.mkdir(png_folder)

        # loop through time windows to create separate plot for each
        for start_index in window_sequence:

            # get data for current window
            end_index = start_index + window_pages - 1
            plot_data = self.parse_data(start = start_index,
                                        end = end_index,
                                        downsample = downsample,
                                        update = False,
                                        correct_drift = correct_drift,
                                        quiet = quiet)

            # format start and end date for current window
            time_format = "%b %-d, %Y (%A) @ %H:%M:%S.%f"
            window_start = plot_data["start_time"]
            window_start_txt = window_start.strftime(time_format)[:-3]

            window_end = window_start + datetime.timedelta(hours = window_hours)
            window_end_txt = window_end.strftime(time_format)[:-3]

            # initialize figure with subplots
            fig, ax = plt.subplots(6, 1)

            # insert date range as plot title
            fig.suptitle(f'{window_start_txt} to {window_end_txt}',
                         fontsize = 8, y = 0.96)

            # initialize subplot index
            subplot_index = 0

            # loop through subplots and generate plot
            for key in ["x", "y", "z", "light", "button", "temperature"]:

                # plot signal
                ax[subplot_index].plot(plot_data[key],
                                       color = line_color[subplot_index])

                # remove box around plot
                ax[subplot_index].spines["top"].set_visible(False)
                ax[subplot_index].spines["bottom"].set_visible(False)
                ax[subplot_index].spines["right"].set_visible(False)

##                # set axis ticks and labels
##                ax[subplot_index].xaxis.set_major_locator(hours)
##                ax[subplot_index].xaxis.set_major_formatter(hours_fmt)
##                if subplot_index != 5:
##                    ax[subplot_index].set_xticklabels([])

                ax[subplot_index].set_yticks(yaxis_ticks[subplot_index])
                units = yaxis_units[subplot_index]
                ax[subplot_index].set_ylabel(f'{key} ({units})')


##                # set vertical lines on plot at hours
##                ax[subplot_index].grid(True, 'major', 'x',
##                                       color = 'k', linestyle = '--')

                # set horizontal lines on plot at zero and limits
                if subplot_index < 4:
                    for yline in yaxis_lines[subplot_index]:
                        ax[subplot_index].axhline(y = yline, color = 'grey',
                                                  linestyle = '-')

                # set axis limits
                ax[subplot_index].set_ylim(yaxis_lim[subplot_index])
##                ax[subplot_index].set_xlim(window_start,
##                                           window_start +
##                                           dt.timedelta(hours = 4))

                # increment to next subplot
                subplot_index += 1

            # save figure as .png and close
            png_file = 'plot_' + f'{start_index:09d}' + '.png'
            fig.savefig(os.path.join(png_folder, png_file))
            plt.close(fig)


        # CREATE PDF ------

        if not quiet: print("Building PDF ...")

        # HEADER PAGE ----------------

        # initialize pdf
        pdf = fpdf.FPDF(format = 'letter')

        # add first page and print file name at top
        pdf.add_page()
        pdf.set_font("Courier", size = 16)
        pdf.cell(200, 10, txt = bin_name, ln = 1, align = 'C', border = 0)

        # set font for header info
        pdf.set_font("Courier", size = 12)
        header_text = '\n'

        # find length of longest key in header
        key_length = max(len(key) for key in self.header.keys()) + 1

        # create text string for header information
        for key, value in self.header.items():
            header_text = header_text + f"{key:{key_length}}:  {value}\n"

        # print header to pdf
        pdf.multi_cell(200, 5, txt = header_text, align = 'L')

        # PLOT DATA PAGES -------------

        # list all .png files in temp folder
        png_files = os.listdir(png_folder)
        png_files.sort()

        # loop through .png files to add to pdf
        for png_file in png_files:

            # create full .png file path
            png_path = os.path.join(png_folder, png_file)

            # add page and set font
            pdf.add_page()
            pdf.set_font("Courier", size = 16)

            # print file_name as header
            pdf.cell(0, txt = bin_name, align = 'C')
            pdf.ln()

            # insert .png plot into pdf
            pdf.image(png_path, x = 1, y = 13, type = 'png')

        # SAVE PDF AND DELETE PNGS --------------

        if not quiet: print("Cleaning up ...")

        # save pdf file
        pdf.output(pdf_path)

        # delete temp .png files
        shutil.rmtree(png_folder)

        if not quiet: print("Done creating PDF summary ...")

        return pdf_path
