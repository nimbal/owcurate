# DAVID DING OCTOBER 30TH 2019
# Adam Vert January 2020


# ======================================== IMPORTS ========================================
from GENEActivFile import *
from file_naming import file_naming
import pyedflib
import datetime
import os


# ======================================== FUNCTIONS ========================================
def ga_to_edf(input_file_path, accelerometer_dir, temperature_dir, light_dir, button_dir ,correct_drift=True, quiet=False):
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
          For example, input_file_path=r"C:\this\is\a\windows\path\file"

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

    # Outputting Accelerometer Information
    if not quiet: print("Starting EDF Conversion.")
    if accelerometer_dir != "":
        if not quiet: print("Building Accelerometer EDF...")
        accelerometer_full_path = os.path.join(accelerometer_dir, accelerometer_file_name)
        accelerometer_file = pyedflib.EdfWriter(accelerometer_full_path, 3)
        accelerometer_file.setHeader({"technician": "",
                                      "recording_additional": "",
                                      "patientname": "",
                                      "patient_additional": "",
                                      "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                                      "equipment": "GENEActiv",  # Body Location
                                      "device_location": geneactivfile.file_info["device_location"],
                                      "admincode": "",
                                      "gender": geneactivfile.file_info["sex"],
                                      "startdate": geneactivfile.file_info["start_time"],
                                      "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")})

        accelerometer_file.setSignalHeader(0, {"label": "x", "dimension": geneactivfile.file_info['accelerometer_units'],
                                               "sample_rate": geneactivfile.data['sample_rate'],
                                               # Todo: Reference back to GENEActivFile header (FOR ALL)
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

    if temperature_dir != "":
        if not quiet: print("Building Temperature EDF...")
        temperature_full_path = os.path.join(temperature_dir, temperature_file_name)
        temperature_file = pyedflib.EdfWriter(temperature_full_path, 1)
        temperature_file.setHeader({"technician": "",
                                    "recording_additional": "",
                                    "patientname": "",
                                    "patient_additional": "",
                                    "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                                    "equipment": "GENEActiv",
                                    "admincode": "",
                                    "gender": geneactivfile.file_info["sex"],
                                    "startdate": geneactivfile.file_info["start_time"],
                                    "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")})

        temperature_file.setSignalHeader(0, {"label": "temperature", "dimension": geneactivfile.file_info['temperature_units'], "sample_rate": 4,
                                             # TODO: sample_rate value should be 0.25 (sample rate/300) but it is restricted to integers
                                             "physical_max": geneactivfile.file_info["temperature_physical_max"],
                                             "physical_min": geneactivfile.file_info["temperature_physical_min"],
                                             "digital_max": 32767, "digital_min": -32768,
                                             "prefilter": "pre1", "transducer": "trans1"})

        #temperature_file.writeSamples([np.array(np.repeat(geneactivfile.data['temperature'], 4))])  #If you want the temperture to be synced with other sensors
        temperature_file.writeSamples([np.array(geneactivfile.data['temperature'])])
        temperature_file.close()

    if light_dir != "":
        if not quiet: print("Building Light EDF...")
        light_full_path = os.path.join(light_dir, light_file_name)
        light_file = pyedflib.EdfWriter(light_full_path, 1)
        light_file.setHeader({"technician": "",
                              "recording_additional": "",
                              "patientname": "",
                              "patient_additional": "",
                              "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                              "equipment": "GENEActiv",
                              "admincode": "",
                              "gender": geneactivfile.file_info["sex"],
                              "startdate": geneactivfile.file_info["start_time"],
                              "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")})

        light_file.setSignalHeader(0, {"label": "light", "dimension": geneactivfile.file_info['light_units'],
                                       "sample_rate": geneactivfile.data['sample_rate'],
                                       "physical_max": geneactivfile.file_info["light_physical_max"],
                                       "physical_min": geneactivfile.file_info["light_physical_min"],
                                       "digital_max": 32767, "digital_min": -32768,
                                       "prefilter": "pre1", "transducer": "trans1"})

        light_file.writeSamples([np.array(geneactivfile.data["light"])])
        light_file.close()

    if button_dir != "":
        if not quiet: print("Building Button EDF...")
        button_full_path = os.path.join(button_dir, button_file_name)
        button_file = pyedflib.EdfWriter(button_full_path, 1)
        button_file.setHeader({"technician": "",
                               "recording_additional": "",
                               "patientname": "",
                               "patient_additional": "",
                               "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                               "equipment": "GENEActiv",
                               "admincode": "",
                               "gender": geneactivfile.file_info["sex"],
                               "startdate": geneactivfile.file_info["start_time"],
                               "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"],
                                                                       "%Y-%m-%d")})

        button_file.setSignalHeader(0, {"label": "button ", "dimension": "", "sample_rate": geneactivfile.data['sample_rate'],
                                        "physical_max": 1,  # Must state physical min and max explicitly in the event that no button is pressed
                                        "physical_min": 0,
                                        "digital_max": 32767, "digital_min": -32768,
                                        "prefilter": "pre1", "transducer": "trans1"})

        button_file.writeSamples([np.array(geneactivfile.data["button"])])
        button_file.close()
    if not quiet: print("EDF Conversion Complete.")

def device_ga_to_edf(input_file_path, device_output_dir, correct_drift=True, quiet=False):


    # Create GENEActivFile
    geneactivfile = GENEActivFile(input_file_path)

    # Read Binary File
    geneactivfile.read(correct_drift=correct_drift, quiet=quiet)

    # File Name
    file_names = file_naming(geneactivfile)
    device_file_name = file_names[4]

    if not quiet: print("Building Device EDF...")
    device_full_path = os.path.join(device_output_dir, device_file_name)
    device_file = pyedflib.EdfWriter(device_full_path, 6)
    device_file.setHeader({"technician": "",
                           "recording_additional": "",
                           "patientname": "",
                           "patient_additional": "",
                           "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                           "equipment": "GENEActiv",  # Body Location
                           "device_location": geneactivfile.file_info["device_location"],
                           "admincode": "",
                           "gender": geneactivfile.file_info["sex"],
                           "startdate": geneactivfile.file_info["start_time"],
                           "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"], "%Y-%m-%d")})

    # Accelerometer Parameters
    device_file.setSignalHeader(0, {"label": "x", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate'],
                                    # Todo: Reference back to GENEActivFile header (FOR ALL)
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    device_file.setSignalHeader(1, {"label": "y", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate'],
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    device_file.setSignalHeader(2, {"label": "z", "dimension": geneactivfile.file_info['accelerometer_units'],
                                    "sample_rate": geneactivfile.data['sample_rate'],
                                    "physical_max": geneactivfile.file_info["accelerometer_physical_max"],
                                    "physical_min": geneactivfile.file_info["accelerometer_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    print(int(geneactivfile.file_info["temperature_frequency"]))
    # Temperature Parameter
    device_file.setSignalHeader(3, {"label": "temperature", "dimension": geneactivfile.file_info['temperature_units'], "sample_rate": 1,  # TODO: This value should be 0.25 (sample rate/300) but it is restricted to integers
                                    "physical_max": geneactivfile.file_info["temperature_physical_max"],
                                    "physical_min": geneactivfile.file_info["temperature_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    # Light Parameter
    device_file.setSignalHeader(4, {"label": "light", "dimension": geneactivfile.file_info['light_units'],
                                    "sample_rate": geneactivfile.data['sample_rate'],
                                    "physical_max": geneactivfile.file_info["light_physical_max"],
                                    "physical_min": geneactivfile.file_info["light_physical_min"],
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    # Button Parameter
    device_file.setSignalHeader(5, {"label": "button ", "dimension": "", "sample_rate": geneactivfile.data['sample_rate'],
                                    "physical_max": 1,  # Must state physical min and max explicitly in the event that no button is pressed
                                    "physical_min": 0,
                                    "digital_max": 32767, "digital_min": -32768,
                                    "prefilter": "pre1", "transducer": "trans1"})

    temperature_x4 = np.repeat(geneactivfile.data['temperature'], 4)

    device_file.writeSamples(
        [geneactivfile.data['x'], geneactivfile.data['y'], geneactivfile.data['z'], temperature_x4, geneactivfile.data["light"], geneactivfile.data["button"]])
    device_file.close()
    print("Device Wide EDF Conversion Complete")
