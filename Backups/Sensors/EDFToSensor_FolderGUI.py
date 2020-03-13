# Author:  Adam Vert
# Date:  January, 2020


# ======================================== IMPORTS ========================================

import PySimpleGUI as sg
import os
from EDFToSensor import *
from Sensor import *


# ======================================== FUNCTION =========================================
def EDFtoSensor_GUI(accelerometer='', temperature='',light = '',button = ''):
    """
        The folder_convert_gui function takes a creates a graphical interface for the folder_conver() function

        Args:
            input: string
                Path to directory with all the binary GENEActive files
            output: string
                Path to head directory where you want all the EDF files to go ([ONDO5]_[GENEActiv] in Folder structure example)
            device_edf: Bool
                Do you want the function to create a device wide EDF file that stores all 5 sensors in one EDF file
            correct_drift: Bool
                Should the function correct the clock drift on the incoming data?
            overwrite: Bool
                Do you want to redo the conversion on data that has previously been converted?
            quiet: Bool
                Silence the print function?

        Examples: (change input and output paths)
            #folder_convert_gui("C:\\PATH\\TO\\INPUT\\FOLDER", "C:\\PATH\\TO\\OUTPUT\\FOLDER\\OND05_GENEActiv", correct_drift=True, overwrite=False, quiet=False)

        Returns:
            - EDF Files for all
            - A csv file list for each of the 4 parameters (Accelerometer, Temperature, Light, Button)
        """

    # Set colour scheme of GUI
    sg.theme('Default 1')

    # Define the layout of the GUI
    layout = [[sg.Checkbox('Accelerometer Edf?', default = True),sg.Text('Accelerometer EDF:'), sg.Input(accelerometer), sg.FileBrowse()],
              [sg.Checkbox('Temperature Edf?', default = True),sg.Text('Temperature EDF:'), sg.Input(temperature), sg.FileBrowse()],
              [sg.Checkbox('Light Edf?', default = True),sg.Text('Light EDF:'), sg.Input(light), sg.FileBrowse()],
              [sg.Checkbox('Button Edf?', default = True,),sg.Text('Button EDF:'), sg.Input(button), sg.FileBrowse()],
              [sg.OK(), sg.Cancel()]]

    # Name GUI and read file
    window = sg.Window('EDFToSensor_GUI', layout)
    event, values = window.Read()
    print(values)

    # Set up Cancel button
    if event == 'Cancel' or event is None:
        window.close()
        return "Program Cancelled"

    # Set up OK button
    if event == "OK":
        accelerometer, temperature, light, button = ("","","","")
        if values[0] is True:
            accelerometer = values[1]
            while os.path.exists(accelerometer) is False:
                window.refresh
                sg.popup_error("ERROR: ACCELEROMETER PATH NOT RECOGNIZED")
                event, values = window.Read()
                accelerometer = values[1]
                # Check for cancel button again

                if event == 'Cancel' or event is None:
                    window.close()
                    return "Program Cancelled"

                # Check if they deactivate EDF
                if values[0] == False:
                    break

                continue

        if values[2] is True:
            temperature = values[3]
            while os.path.exists(temperature) is False:
                window.refresh
                sg.popup_error("ERROR: TEMPERATURE PATH NOT RECOGNIZED")
                event, values = window.Read()
                temperature = values[3]

                # Check for cancel button again
                if event == 'Cancel' or event is None:
                    window.close()
                    return "Program Cancelled"

                # Check if they deactivate EDF
                if values[2] == False:
                    break

                continue

        if values[4] is True:
            light = values[5]
            while os.path.exists(light) is False:
                window.refresh
                sg.popup_error("ERROR: LIGHT PATH NOT RECOGNIZED")
                event, values = window.Read()
                light = values[5]

                # Check for cancel button again
                if event == 'Cancel' or event is None:
                    window.close()
                    return "Program Cancelled"

                #Check if they deactivate EDF
                if values[4] == False:
                    break

                continue

        if values[6] is True:
            button = values[7]
            while os.path.exists(button) is False:
                window.refresh
                sg.popup_error("ERROR: BUTTON PATH NOT RECOGNIZED")
                event, values = window.Read()
                button = values[7]

                # Check for cancel button again
                if event == 'Cancel' or event is None:
                    window.close()
                    return "Program Cancelled"

                # Check if they deactivate EDF
                if values[6] == False:
                    break

                continue

    # Close GUI
    window.close()

    # Run script using values obtained from GUI input
    return EDFToSensor(Sensor(), accelerometer,"", temperature, light, button)


# Call function to make file work like an executable

#EDFtoSensor_GUI()
