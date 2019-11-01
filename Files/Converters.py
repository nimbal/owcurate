# DAVID DING OCTOBER 30TH 2019


# ======================================== IMPORTS ========================================
from Device.GENEActiv import *
from Device.Bittium import *
import pyedflib


# ======================================== DEFINITIONS ========================================
def GENEActivToEDF(GENEActiv, path, accel=True, temperature=True, light=True, button=True):
    """ This method outputs the GENEActiv data from the GENEActiv class into various EDF Files
    Supposedly Universal

    TODO: Fix all formatting issues and type matching
    TODO: Combining signals into the same files

    Args:
        GENEActiv: GENEActiv File
        outputfiles:

    Returns:

    """

    # Outputting Accelerometer Information
    if accel:
        accelerometer_file = pyedflib.EdfWriter(path + GENEActiv.file_name[:-4] + "Accelerometer.EDF", 3)
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

    if temperature:
        temperature_file = pyedflib.EdfWriter(path + GENEActiv.file_name[:-4] + "Temperature.EDF", 1)

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

    if light:
        light_file = pyedflib.EdfWriter(path + GENEActiv.file_name[:-4] + "Light.EDF", 1)

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

    if button:
        button_file = pyedflib.EdfWriter(path + GENEActiv.file_name[:-4] + "Button.EDF", 1)
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


# TODO: FINISH THIS
def EDFToSensor(sensor, path, accel, ecg, temperature, light, button):

    if accel is not "":
        with pyedflib.EdfReader(join(path, accel)) as accelerometer_file:

            header = accelerometer_file.getHeader()
            accelerometer_header = accelerometer_file.getSignalHeader(0)

            sensor.metadata.update({
                "subject_id": header["patientcode"],
                "sex": header["gender"],
                "start_time": header["startdate"],
                "date_of_birth": header["birthdate"],
                "measurement_frequency": accelerometer_header["sample_rate"]
            })

            GENEActiv.x = accelerometer_file.readSignal(0)
            GENEActiv.y = accelerometer_file.readSignal(1)
            GENEActiv.z = accelerometer_file.readSignal(2)

    if temperature is not "":
        with pyedflib.EdfReader(join(path, temperature)) as temperature_file:
            GENEActiv.temperature = temperature_file.readSignal(0)

    if light is not "":
        with pyedflib.EdfReader(join(path, light)) as light_file:
            GENEActiv.light = light_file.readSignal(0)

    if button is not "":
        with pyedflib.EdfReader(join(path, button)) as button_file:
            GENEActiv.button = button_file.readSignal(0)
