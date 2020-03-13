# DAVID DING OCTOBER 30TH 2019


# ======================================== IMPORTS ========================================

import pyedflib



# ======================================== DEFINITIONS ========================================

def EDFToSensor(sensor, accel, ecg, temperature, light, button, metadata="accelerometer"):
    '''
    EDFToSensor function reads multiple EDF files and transforms them into a universal Sensors class in memory

    TODO: Implement ECG
    TODO: Implement metadata reading from different files
    Args:
        sensor: initialized owcurate.Sensors.Sensors object
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
        metadata: One of "accelerometer", "ecg", "temperature", "light", "button" that is not empty
            Chooses which file to return the metadata from (for the overall sensor)
            Not complete yet

    Returns:

    '''
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
