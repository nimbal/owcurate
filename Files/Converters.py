# DAVID DING OCTOBER 30TH 2019


# ======================================== IMPORTS ========================================
from Device.GENEActiv import *
from Device.Bittium import *
import pyedflib


# ======================================== DEFINITIONS ========================================
def GENEActivToEDF(GENEActiv, path, accel="Accelerometer.EDF", temperature="Thermometer.EDF", light="Light.EDF", button="Button.EDF"):
    '''
    GENEActivToEDF is a universal class that takes GENEActiv device output and transforms it into EDF Files
    Args:
        GENEActiv: initialized owcurate.Device.GENEActiv.GENEActiv class
            This is where the information (to be outputted into EDF) is read from
        path: String
            directory to be outputted to
        accel: String
            File name of the accelerometer path, if empty, will not output accelerometer
        temperature: String
                File name of the temperature path, if empty, will not output temperature
        light: String
            File name of the light path, if empty, will not output light
        button: String
            File name of the button path, if empty, will not output button

    Examples:
        geneactiv = GENEActiv()

        geneactiv.read_from_raw(path)

        geneactiv.calculate_time_shift()

        GENEActivToEDF(geneactiv, output_path)


    Returns:
        EDF Files corresponding to above specifications
    '''

    # Outputting Accelerometer Information
    if accel is not "":
        accelerometer_file = pyedflib.EdfWriter("%s/%s" % (path, accel), 3)
        accelerometer_file.setHeader({"technician": "",
                                      "recording_additional": "",
                                      "patientname": "",
                                      "patient_additional": "",
                                      "patientcode": "%i" % GENEActiv.metadata["subject_id"],
                                      "equipment": "GENEActiv",
                                      "admincode": "",
                                      "gender": GENEActiv.metadata["sex"],
                                      "startdate": GENEActiv.metadata["start_time"],
                                      "birthdate": datetime.datetime.strptime(GENEActiv.metadata["date_of_birth"], "%Y-%m-%d")})

        accelerometer_file.setSignalHeader(0, {"label": "x", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(GENEActiv.x), "physical_min": min(GENEActiv.x),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(1, {"label": "y", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(GENEActiv.y), "physical_min": min(GENEActiv.y),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.setSignalHeader(2, {"label": "z", "dimension": "G", "sample_rate": 75,
                                               "physical_max": max(GENEActiv.z), "physical_min": min(GENEActiv.z),
                                               "digital_max": 32767, "digital_min": -32768,
                                               "prefilter": "pre1", "transducer": "trans1"})

        accelerometer_file.writeSamples([GENEActiv.x, GENEActiv.y, GENEActiv.z])
        accelerometer_file.close()

    if temperature is not "":
        temperature_file = pyedflib.EdfWriter("%s/%s" % (path, temperature), 1)

        temperature_file.setHeader({"technician": "",
                                    "recording_additional": "",
                                    "patientname": "",
                                    "patient_additional": "",
                                    "patientcode": "%i" % GENEActiv.metadata["subject_id"],
                                    "equipment": "GENEActiv",
                                    "admincode": "",
                                    "gender": GENEActiv.metadata["sex"],
                                    "startdate": GENEActiv.metadata["start_time"],
                                    "birthdate": datetime.datetime.strptime(GENEActiv.metadata["date_of_birth"], "%Y-%m-%d")})

        temperature_file.setSignalHeader(0, {"label": "temperature", "dimension": "deg. C", "sample_rate": 1,
                                             "physical_max": max(GENEActiv.temperature), "physical_min": min(GENEActiv.temperature),
                                             "digital_max": 32767, "digital_min": -32768,
                                             "prefilter": "pre1", "transducer": "trans1"})

        temperature_file.writeSamples([GENEActiv.temperature])
        temperature_file.close()

    if light is not "":
        light_file = pyedflib.EdfWriter("%s/%s" % (path, light), 1)

        light_file.setHeader({"technician": "",
                              "recording_additional": "",
                              "patientname": "",
                              "patient_additional": "",
                              "patientcode": "%i" % GENEActiv.metadata["subject_id"],
                              "equipment": "GENEActiv",
                              "admincode": "",
                              "gender": GENEActiv.metadata["sex"],
                              "startdate": GENEActiv.metadata["start_time"],
                              "birthdate": datetime.datetime.strptime(GENEActiv.metadata["date_of_birth"], "%Y-%m-%d")})

        light_file.setSignalHeader(0, {"label": "light", "dimension": "deg. C", "sample_rate": 75,
                                       "physical_max": max(GENEActiv.temperature),
                                       "physical_min": min(GENEActiv.temperature),
                                       "digital_max": 32767, "digital_min": -32768,
                                       "prefilter": "pre1", "transducer": "trans1"})

        light_file.writeSamples([GENEActiv.light])
        light_file.close()

    if button is not "":
        button_file = pyedflib.EdfWriter("%s/%s" % (path, button), 1)
        button_file.setHeader({"technician": "",
                               "recording_additional": "",
                               "patientname": "",
                               "patient_additional": "",
                               "patientcode": "%i" % GENEActiv.metadata["subject_id"],
                               "equipment": "GENEActiv",
                               "admincode": "",
                               "gender": GENEActiv.metadata["sex"],
                               "startdate": GENEActiv.metadata["start_time"],
                               "birthdate": datetime.datetime.strptime(GENEActiv.metadata["date_of_birth"], "%Y-%m-%d")})

        button_file.setSignalHeader(0, {"label": "button ", "dimension": "deg. C", "sample_rate": 75,
                                        "physical_max": max(GENEActiv.temperature),
                                        "physical_min": min(GENEActiv.temperature),
                                        "digital_max": 32767, "digital_min": -32768,
                                        "prefilter": "pre1", "transducer": "trans1"})

        button_file.writeSamples([GENEActiv.button])
        button_file.close()


def EDFToSensor(sensor, path, accel, ecg, temperature, light, button, metadata="accel"):
    '''
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

    '''
    if accel is not "":
        sensor.init_accelerometer()
        with pyedflib.EdfReader(join(path, accel)) as accelerometer_file:
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

    if temperature is not "":
        sensor.init_thermometer()
        with pyedflib.EdfReader(join(path, temperature)) as temperature_file:
            sensor.thermometer.frequency = temperature_file.getSignalHeader(0)["sample_rate"]
            sensor.thermometer.temperatures = temperature_file.readSignal(0)

    if light is not "":
        sensor.init_light()
        with pyedflib.EdfReader(join(path, light)) as light_file:
            sensor.thermometer.frequency = light_file.getSignalHeader(0)["sample_rate"]
            sensor.thermometer.temperatures = light_file.readSignal(0)

    if button is not "":
        with pyedflib.EdfReader(join(path, button)) as button_file:
            sensor.thermometer.frequency = button_file.getSignalHeader(0)["sample_rate"]
            sensor.thermometer.temperatures = button_file.readSignal(0)
