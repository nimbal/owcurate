# DAVID DING OCTOBER 30TH 2019
# Adam Vert January 2020


# ======================================== IMPORTS ========================================
from GENEActivFile import *
import pyedflib


# ======================================== FUNCTIONS ========================================
def ga_to_edf(input_file_path, accel_dir, temperature_dir, light_dir, button_dir, correct_drift=True, quiet=False):
    """
    The ga_to_edf is a function that takes a binary file provided by the GENEActiv device and converts it into an EDF format.

    Args:
        input_file_path: String
            Path to the binary GENEActiv file
        accel_dir: String
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
        ga_to_edf(input_file_path,accel_dir,temp_dir,button_dir)


    Requires:
        - Must have an integer entered for the subject ID parameter of the GENEActiv file.
        - If running from a windows computer must make the path compatible to Python standards by putting an r before your path.
          For example, input_file_path=r"C:\this\is\a\windows\path\file"

```    Returns:
        EDF Files corresponding to above specifications
    """


    # Initialize GENEActiveFile class
    geneactivfile = GENEActivFile(input_file_path)

    # Read Binary File
    geneactivfile.read(geneactivfile, correct_drift=correct_drift, quiet=quiet)

    # Outputting Accelerometer Information
    if not quiet: print("Starting EDF Conversion.")
    if accel_dir != "":
        if not quiet: print("Building Accelerometer EDF...")
        accel_dir = os.path.abspath(accel_dir)
        accelerometer_file = pyedflib.EdfWriter("%s/%s_Accel.EDF" % (accel_dir, geneactivfile.file_name.replace("_GA_", "_GENEActiv_")[:-4]), 3)
        if not quiet: print(geneactivfile.file_info["date_of_birth"])
        accelerometer_file.setHeader({"technician": "",
                                      "recording_additional": "",
                                      "patientname": "",
                                      "patient_additional": "",
                                      "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                                      "equipment": "GENEActiv",
                                      "admincode": "",
                                      "gender": geneactivfile.file_info["sex"],
                                      "startdate": geneactivfile.file_info["start_time"],
                                      "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"],"%Y-%m-%d")})

        accelerometer_file.setSignalHeader(0, {"label": "x", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(geneactivfile.data['x']),
                                               "physical_min": min(geneactivfile.data['x']),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(1, {"label": "y", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(geneactivfile.data['y']),
                                               "physical_min": min(geneactivfile.data['y']),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(2, {"label": "z", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(geneactivfile.data['z']),
                                               "physical_min": min(geneactivfile.data['z']),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.writeSamples([geneactivfile.data['x'], geneactivfile.data['y'], geneactivfile.data['z']])
        accelerometer_file.close()

    if temperature_dir != "":
        if not quiet: print("Building Temperature EDF...")
        temperature_dir = os.path.abspath(temperature_dir)
        temperature_file = pyedflib.EdfWriter("%s/%s_Temp.EDF" % (temperature_dir, geneactivfile.file_name.replace("_GA_", "_GENEActiv_")[:-4]),1)
        temperature_file.setHeader({"technician": "",
                                    "recording_additional": "",
                                    "patientname": "",
                                    "patient_additional": "",
                                    "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                                    "equipment": "GENEActiv",
                                    "admincode": "",
                                    "gender": geneactivfile.file_info["sex"],
                                    "startdate": geneactivfile.file_info["start_time"],
                                    "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"],"%Y-%m-%d")})

        temperature_file.setSignalHeader(0, {"label": "temperature", "dimension": "deg. C", "sample_rate": 1,
                                             "physical_max": max(geneactivfile.data["temperature"]),
                                             "physical_min": min(geneactivfile.data["temperature"]),
                                             "digital_max": 32767, "digital_min": -32768,
                                             "prefilter": "pre1", "transducer": "trans1"})

        temperature_file.writeSamples([np.array(geneactivfile.data["temperature"])])
        temperature_file.close()

    if light_dir != "":
        if not quiet: print("Building Light EDF...")
        light_dir = os.path.abspath(light_dir)
        light_file = pyedflib.EdfWriter("%s/%s_Light.EDF" % (light_dir, geneactivfile.file_name.replace("_GA_", "_GENEActiv_")[:-4]), 1)
        light_file.setHeader({"technician": "",
                              "recording_additional": "",
                              "patientname": "",
                              "patient_additional": "",
                              "patientcode": "%r" % geneactivfile.file_info["subject_id"],
                              "equipment": "GENEActiv",
                              "admincode": "",
                              "gender": geneactivfile.file_info["sex"],
                              "startdate": geneactivfile.file_info["start_time"],
                              "birthdate": datetime.datetime.strptime(geneactivfile.file_info["date_of_birth"],"%Y-%m-%d")})

        light_file.setSignalHeader(0, {"label": "light", "dimension": "deg. C", "sample_rate": 75,
                                       "physical_max": max(geneactivfile.data["light"]),
                                       "physical_min": min(geneactivfile.data["light"]),
                                       "digital_max": 32767, "digital_min": -32768,
                                       "prefilter": "pre1", "transducer": "trans1"})

        light_file.writeSamples([np.array(geneactivfile.data["light"])])
        light_file.close()

    if button_dir != "":
        if not quiet: print("Building Button EDF...")
        button_dir = os.path.abspath(button_dir)
        button_file = pyedflib.EdfWriter("%s/%s_Button.EDF" % (button_dir, geneactivfile.file_name.replace("_GA_", "_GENEActiv_")[:-4]), 1)
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

        button_file.setSignalHeader(0, {"label": "button ", "dimension": "deg. C", "sample_rate": 75,
                                        "physical_max": max(geneactivfile.data['button']),
                                        "physical_min": min(geneactivfile.data["button"]),
                                        "digital_max": 32767, "digital_min": -32768,
                                        "prefilter": "pre1", "transducer": "trans1"})

        button_file.writeSamples([np.array(geneactivfile.data["button"])])
        button_file.close()
    if not quiet: print("EDF Conversion Complete.")


def edf_to_sensor(sensor, accel, ecg, temperature, light, button, metadata="accel"):
    """
    EDFToSensor function reads multiple EDF files and transforms them into a universal Sensor class in memory

    TODO: Implement ECG
    TODO: Implement metadata reading from different files
    Args:
        sensor: initialized owcurate.Sensor.Sensor object
            This is where the read information will be returned into
        path: String, location to path of files folder
            This goes to the directory of the files folder, where all the files are read in from
        accel: String
            File name of the accelerometer file to be read in
        ecg: String
            File name of the ECG file to be read in
        temperature: String
            File name of the Temperature file to be read in
        light: String
            File name of the Light sensor file to be read in
        button: String
            File name of the button sensor file to be read in
        metadata: One of "accel", "ecg", "temperature", "light", "button" that is not empty
            Chooses which file to return the metadata from (for the overall sensor)
            Not complete yet

    Returns:

    """
    if accel != "":
        sensor.init_accelerometer()
        with pyedflib.EdfReader(accel) as accelerometer_file:
            header = accelerometer_file.getHeader()
            accelerometer_header = accelerometer_file.getSignalHeader(0)

            sensor.accelerometer.frequency = accelerometer_header["sample_rate"]

            sensor.accelerometer.x = accelerometer_file.readSignal(0)
            sensor.accelerometer.y = accelerometer_file.readSignal(1)
            sensor.accelerometer.z = accelerometer_file.readSignal(2)

            sensor.accelerometer.n_samples = len(sensor.accelerometer.x)

            sensor.metadata.update({
                "subject_id": header["patientcode"],
                "sex": header["gender"],
                "start_time": header["startdate"],
                "date_of_birth": header["birthdate"],
            })
            sensor.accelerometer.start_time = sensor.metadata["start_time"]

    if temperature != "":
        sensor.init_thermometer()
        with pyedflib.EdfReader(temperature) as temperature_file:
            sensor.thermometer.frequency = temperature_file.getSignalHeader(0)["sample_rate"]
            sensor.thermometer.temperatures = temperature_file.readSignal(0)

    if light != "":
        sensor.init_light()
        with pyedflib.EdfReader(light) as light_file:
            sensor.light.frequency = light_file.getSignalHeader(0)["sample_rate"]
            sensor.light.light = light_file.readSignal(0)

    if button != "":
        sensor.init_button()
        with pyedflib.EdfReader(button) as button_file:
            sensor.light.frequency = button_file.getSignalHeader(0)["sample_rate"]
            sensor.button.button = button_file.readSignal(0)
