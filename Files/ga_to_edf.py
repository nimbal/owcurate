# DAVID DING OCTOBER 30TH 2019
# Adam Vert January 2020


# ======================================== IMPORTS ========================================
from GENEActivFile import *
from file_naming import file_naming
import pyedflib
import datetime
import os, sys
import time

# ======================================== FUNCTIONS ========================================
def ga_to_edf(input_file_path, accelerometer_dir, temperature_dir, light_dir, button_dir, device_dir = "", device_edf = False, correct_drift=True, quiet=False):
    """
    The ga_to_edf is a function that takes a binary file provided by the GENEActiv device and converts it into an EDF format.

    Args:
        input_file_path: String
            Path to the binary GENEActiv file
        accelerometer_dir: String
            Directory accelerometer data will be outputted to. If empty inputted, will not output accelerometer.
        temperature_dir: String
            Directory temperature data will be outputted to. If empty inputted, will not output temperature.
        light_dir: String
            Directory light data will be outputted to. If empty string inputted, will not output light.
        button_dir: String
            Directory button data will be outputted to. If empty string inputted, will not output button.
        correct_drift: Bool
            Should the function correct the clock drift on the incoming data?
        quiet: Bool
            Silence the print function?


    Example(s):
        ga_to_edf(input_file_path,accelerometer_dir,temp_dir,button_dir)


    Requires:
        - Must have an integer entered for the subject ID parameter of the GENEActiv file.
        - If running from a windows computer must make the path compatible to Python standards by putting an r before your path.
          For example, input_file_path = r"C:\this\is\a\windows\path\file"

    Returns:
        EDF Files corresponding to above specifications
    """

    # Initialize GENEActiveFile class
    # if file does not exist then exit
    if not os.path.exists(input_file_path):
        print(f"****** WARNING: {input_file_path} does not exist.\n")
        return

    # Create GENEActivFile
    geneactivfile = GENEActivFile(input_file_path)

    # Read Binary File
    geneactivfile.read(correct_drift=correct_drift, quiet=quiet)

    # Create File Names
    file_names = file_naming(geneactivfile)
    accelerometer_file_name = file_names[0]
    temperature_file_name = file_names[1]
    light_file_name = file_names[2]
    button_file_name = file_names[3]


    # Create header values
    clock_drift = geneactivfile.file_info["clock_drift"]
    device_location = geneactivfile.file_info["device_location"]
    if device_location == '':  #  PyEDFlib can't recognize empty variables in header
        device_location = "aid"  # Todo: discuss what an appropriate name would be for this
    extract_time = geneactivfile.file_info["extract_time"]
    subject_id = geneactivfile.file_info["subject_id"]
    serial_num = geneactivfile.file_info["serial_num"]
    sex = geneactivfile.file_info["sex"]
    start_time = geneactivfile.file_info["start_time"]
    birthdate = datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")

    # Outputting Accelerometer Information
    if not quiet: print("Starting EDF Conversion.")
    if accelerometer_dir != "":
        edf_start_time = time.time()
        if not quiet: print("Building Accelerometer EDF...")
        accelerometer_full_path = os.path.join(accelerometer_dir, accelerometer_file_name)
        accelerometer_file = pyedflib.EdfWriter(accelerometer_full_path, 3)
        accelerometer_file.setHeader({"technician": "",
                                      "recording_additional": str(clock_drift),  # Using this to hold the clock drift variable, for encoding reasons needs to be a string
                                      "patientname": device_location, # Using this to hold the body location variable
                                      "patient_additional": str(extract_time), # Using this to hold the extract_time variable
                                      "patientcode": subject_id,
                                      "equipment": serial_num,
                                      "admincode": "",
                                      "gender": sex,
                                      "startdate": start_time,
                                      "birthdate": birthdate})

        accelerometer_file.setSignalHeader(0, {"label": "x", "dimension": geneactivfile.file_info['accelerometer_units'],
                                               "sample_rate": geneactivfile.data['sample_rate'],
                                               "physical_max":geneactivfile.file_info["accelerometer_physical_max"],
                                               "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(1, {"label": "y", "dimension": geneactivfile.file_info['accelerometer_units'],
                                               "sample_rate": geneactivfile.data['sample_rate'],
                                               "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                               "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(2, {"label": "z", "dimension": geneactivfile.file_info['accelerometer_units'],
                                               "sample_rate": geneactivfile.data['sample_rate'],
                                               "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                               "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.writeSamples([geneactivfile.data['x'], geneactivfile.data['y'], geneactivfile.data['z']])
        accelerometer_file.close()
        if not quiet: print("Seconds to make Accelerometer EDF:", time.time() - edf_start_time)

    if temperature_dir != "":
        edf_start_time = time.time()
        if not quiet: print("Building Temperature EDF...")
        temperature_full_path = os.path.join(temperature_dir, temperature_file_name)
        temperature_file = pyedflib.EdfWriter(temperature_full_path, 1)
        temperature_file.setHeader({"technician": "",
                                      "recording_additional": str(clock_drift),  # Using this to hold the clock drift variable, for encoding reasons needs to be a string
                                      "patientname": device_location, # Using this to hold the body location variable
                                      "patient_additional": str(extract_time), # Using this to hold the extract_time variable
                                      "patientcode": subject_id,
                                      "equipment": serial_num,
                                      "admincode": "",
                                      "gender": sex,
                                      "startdate": start_time,
                                      "birthdate": birthdate})

        temperature_file.setSignalHeader(0, {"label": "temperature", "dimension": geneactivfile.file_info['temperature_units'], "sample_rate": 1, #Actual sample rate = 0.25
                                             "physical_max": geneactivfile.file_info["temperature_physical_max"],
                                             "physical_min": geneactivfile.file_info["temperature_physical_min"],
                                             "digital_max": 32767, "digital_min": -32768,
                                             "prefilter": "pre1", "transducer": "trans1"})

        temperature_file.setDatarecordDuration(400000) #This makes the time per data record from 1 second to 4 making the sample rate 0.25
        temperature_file.writeSamples([np.array(geneactivfile.data['temperature'])])
        temperature_file.close()
        if not quiet: print("Seconds to make Temperature EDF:", time.time() - edf_start_time)

    if light_dir != "":
        edf_start_time = time.time()
        if not quiet: print("Building Light EDF...")
        light_full_path = os.path.join(light_dir, light_file_name)
        light_file = pyedflib.EdfWriter(light_full_path, 1)
        light_file.setHeader({"technician": "",
                                      "recording_additional": str(clock_drift),  # Using this to hold the clock drift variable, for encoding reasons needs to be a string
                                      "patientname": device_location, # Using this to hold the body location variable
                                      "patient_additional": str(extract_time), # Using this to hold the extract_time variable
                                      "patientcode": subject_id,
                                      "equipment": serial_num,
                                      "admincode": "",
                                      "gender": sex,
                                      "startdate": start_time,
                                      "birthdate": birthdate})

        light_file.setSignalHeader(0, {"label": "light", "dimension": geneactivfile.file_info['light_units'],
                                       "sample_rate": geneactivfile.data['sample_rate'],
                                       "physical_max": geneactivfile.file_info["light_physical_max"],
                                       "physical_min": geneactivfile.file_info["light_physical_min"],
                                       "digital_max": 32767, "digital_min": -32768,
                                       "prefilter": "pre1", "transducer": "trans1"})

        light_file.writeSamples([np.array(geneactivfile.data["light"])])
        light_file.close()
        if not quiet: print("Seconds to make Light EDF:", time.time() - edf_start_time)
    if button_dir != "":
        edf_start_time = time.time()
        if not quiet: print("Building Button EDF...")
        button_full_path = os.path.join(button_dir, button_file_name)
        button_file = pyedflib.EdfWriter(button_full_path, 1)
        button_file.setHeader({"technician": "",
                                      "recording_additional": str(clock_drift),  # Using this to hold the clock drift variable, for encoding reasons needs to be a string
                                      "patientname": device_location, # Using this to hold the body location variable
                                      "patient_additional": str(extract_time), # Using this to hold the extract_time variable
                                      "patientcode": subject_id,
                                      "equipment": serial_num,
                                      "admincode": "",
                                      "gender": sex,
                                      "startdate": start_time,
                                      "birthdate": birthdate})

        button_file.setSignalHeader(0, {"label": "button ", "dimension": "", "sample_rate": geneactivfile.data['sample_rate'],
                                        "physical_max": 1,  # Must state physical min and max explicitly in the event that no button is pressed
                                        "physical_min": 0,
                                        "digital_max": 32767, "digital_min": -32768,
                                        "prefilter": "pre1", "transducer": "trans1"})

        button_file.writeSamples([np.array(geneactivfile.data["button"])])
        button_file.close()
        if not quiet: print("Seconds to make Button EDF:", time.time() - edf_start_time)
    if device_edf: device_ga_to_edf(geneactivfile, device_dir, quiet)

    if not quiet: print("EDF Conversion Complete.")

#
def device_ga_to_edf(geneactivfile, device_output_dir, quiet=False):


    # File Name
    file_names = file_naming(geneactivfile)
    device_file_name = file_names[4]

    # Create header values
    clock_drift = geneactivfile.file_info["clock_drift"]
    device_location = geneactivfile.file_info["device_location"]
    extract_time = geneactivfile.file_info["extract_time"]
    subject_id = geneactivfile.file_info["subject_id"]
    serial_num = geneactivfile.file_info["serial_num"]
    sex = geneactivfile.file_info["sex"]
    start_time = geneactivfile.file_info["start_time"]
    birthdate = datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")

    if not quiet: print("Building Device EDF...")
    edf_start_time = time.time()
    device_full_path = os.path.join(device_output_dir, device_file_name)
    device_file = pyedflib.EdfWriter(device_full_path, 6)
    device_file.setDatarecordDuration(400000)  # This allows the proper sample rate for temperature (0.25hz) by having a datarecord be 4 seconds, so all frequencyies are multiplied by 4
    device_file.setHeader({"technician": "",
                                      "recording_additional": str(clock_drift),  # Using this to hold the clock drift variable, for encoding reasons needs to be a string
                                      "patientname": device_location, # Using this to hold the body location variable
                                      "patient_additional": str(extract_time), # Using this to hold the extract_time variable
                                      "patientcode": subject_id,
                                      "equipment": serial_num,
                                      "admincode": "",
                                      "gender": sex,
                                      "startdate": start_time,
                                      "birthdate": birthdate})


    # Accelerometer Parameters
    device_file.setSignalHeader(0, {"label": "x", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate']*4,
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    device_file.setSignalHeader(1, {"label": "y", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate']*4,
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    device_file.setSignalHeader(2, {"label": "z", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate']*4,
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    # Temperature Parameter
    device_file.setSignalHeader(3, {"label": "temperature", "dimension": geneactivfile.file_info['temperature_units'], "sample_rate": 1,
                                    "physical_max": geneactivfile.file_info["temperature_physical_max"],
                                    "physical_min": geneactivfile.file_info["temperature_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    # Light Parameter
    device_file.setSignalHeader(4, {"label": "light", "dimension": geneactivfile.file_info['light_units'],
                                    "sample_rate": geneactivfile.data['sample_rate']*4,
                                    "physical_max": geneactivfile.file_info["light_physical_max"],
                                    "physical_min": geneactivfile.file_info["light_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    # Button Parameter
    device_file.setSignalHeader(5, {"label": "button ", "dimension": "", "sample_rate": geneactivfile.data['sample_rate']*4,
                                    "physical_max": 1,  # Must state physical min and max explicitly in the event that no button is pressed
                                    "physical_min": 0,
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    device_file.writeSamples(
        [geneactivfile.data['x'], geneactivfile.data['y'], geneactivfile.data['z'], geneactivfile.data['temperature'], geneactivfile.data["light"], geneactivfile.data["button"]])
    device_file.close()
    if not quiet: print("Seconds to make Device EDF:", time.time() - edf_start_time)


def edf_integrity_check(edf_path, binary_path):
    """
    to verify that the data in the edf and bin files are the same
    """

    geneactivfile = GENEActivFile(binary_path)
    geneactivfile.read()

    # get EDF data
    edf_data = pyedflib.EdfReader(edf_path)
    clock_drift = edf_data.getRecordingAdditional()
    body_location = edf_data.getPatientName()
    extraction_time = edf_data.getPatientAdditional()
    subject_id = edf_data.getPatientCode()
    serial_num = edf_data.getEquipment()
    start_date = edf_data.getStartdatetime()
    print("Clock Drift: ", clock_drift)
    print("Body Location: ", body_location)
    print("Extraction Time: ", extraction_time)
    print("Subject ID: ", subject_id)
    print("Serial Number: ", serial_num)
    print("Start Date: ", start_date)


    print("")
    print("")

    # Get binary file data
    bin_clock_drift = geneactivfile.file_info["clock_drift"]
    bin_body_location = geneactivfile.file_info["device_location"]
    bin_extraction_time = geneactivfile.file_info["extract_time"]
    bin_subject_id = geneactivfile.file_info["subject_id"]
    bin_serial_num = geneactivfile.file_info["serial_num"]
    bin_start_date = geneactivfile.file_info["start_time"]
    print("Bin Clock Drift: ", bin_clock_drift)
    print("Bin Body Location: ", bin_body_location)
    print("Bin Extraction Time: ", bin_extraction_time)
    print("Bin Subject ID: ", bin_subject_id)
    print("Bin Serial Number: ", bin_serial_num)
    print("Bin Start Date: ", bin_start_date)

    # Compare data
    bad_match = 0
    if str(clock_drift) != str(bin_clock_drift):
        print("**WARNING, clock_drift VALUES DON'T MATCH")
        print("EDF CLOCK DRIFT: ", clock_drift)
        print("BIN CLOCK DRIFT: ", bin_clock_drift)
        bad_match += 1

    if str(body_location) != str(bin_body_location.replace("_", " ")):
        print("**WARNING, body_location VALUES DON'T MATCH")
        print("EDF BODY LOCATION: ", body_location)
        print("BIN BODY LOCATION: ", bin_body_location)
        bad_match += 1

    if str(extraction_time) != str(bin_extraction_time):
        print("**WARNING, extraction_time VALUES DON'T MATCH")
        print("EDF EXTRACTION TIME: ", extraction_time)
        print("BIN EXTRACTION TIME: ", bin_extraction_time)
        bad_match += 1

    if str(subject_id) != str(bin_subject_id):
        print("**WARNING, subject_id VALUES DON'T MATCH")
        print("EDF SUBJECT ID: ", subject_id)
        print("BIN SUBJECT ID: ", bin_subject_id)
        bad_match += 1

    if str(serial_num) != str(bin_serial_num):
        print("**WARNING, serial_num VALUES DON'T MATCH")
        print("EDF SERIAL NUMBER: ", subject_id)
        print("BIN SERIAL NUMBER: ", bin_subject_id)
        bad_match += 1

    if str(start_date + datetime.timedelta(0,0.5)) != str(bin_start_date):
        print("**WARNING, start_date VALUES DON'T MATCH")
        print("EDF START DATE: ", start_date)
        print("BIN START DATE: ", bin_start_date)
        bad_match += 1

    if bad_match ==0: print("NO ERRORS")


    print("Test Complete with ", bad_match, "bad matches.")
