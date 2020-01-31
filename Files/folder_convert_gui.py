# Author:  Adam Vert
# Date:  January, 2020


# ======================================== IMPORTS ========================================

import PySimpleGUI as sg
import os
from folder_convert_script import folder_convert


# ======================================== FUNCTION =========================================
def folder_convert_gui(input='', output='', device_edf = False, correct_drift=True, overwrite=False, quiet=False):
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
    layout = [[sg.Text('Input Folder', size=(10, 1)), sg.Input(input), sg.FolderBrowse()],
              [sg.Text('Output Folder', size=(10, 1)), sg.Input(output), sg.FolderBrowse()],
              [sg.Checkbox('Device Edf', default = device_edf), sg.Checkbox('Correct Drift:', default=correct_drift), sg.Checkbox('Overwrite:', default=overwrite), sg.Checkbox('Quiet', default=quiet)],
              [sg.OK(), sg.Cancel()]]

    # Name GUI and read file
    window = sg.Window('GA to EDF Folder Conversion', layout)
    event, values = window.Read()

    # Set up Cancel button
    if event == 'Cancel' or event is None:
        window.close()
        exit("Program Cancelled")

    # Set up OK button
    if event == "OK":
        # Verify that the paths given exist
        while not (os.path.exists(values[0]) and os.path.exists(values[1])):
            window.refresh
            a = os.path.exists(values[0])
            b = os.path.exists(values[1])
            if a + b == 0:
                sg.popup_error('ERROR: INPUT FOLDER PATH AND OUTPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Names.')
            elif a == 0:
                sg.Popup('ERROR: INPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Name.')
            elif b == 0:
                sg.Popup('ERROR: OUTPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Name.')
            event, values = window.Read()

            # Check for cancel button again

            if event == 'Cancel' or event is None:
                window.close()
                exit("Program Cancelled")
            continue

    # Close GUI
    window.close()

    # Run script using values obtained from GUI input
    folder_convert(values[0], values[1], values[2], values[3], values[4], values[5])


# Call function to make file work like an executable
folder_convert_gui()
