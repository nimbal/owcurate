import PySimpleGUI as sg
import os
import sys
from folder_convert_script import folder_convert


def folder_convert_gui(input='',output='', correct_drift=True, overwrite=False, quiet=False):
    """
        The folder_convert_gui function takes a creates a graphical interface for the folder_conver() function

        Args:
            input: string
                Path to directory with all the binary GENEActive files
            output: string
                Path to head directory where you want all the EDF files to go ([ONDO5]_[GENEActiv] in Folder structure example)
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
            - A csv file list for each of the 4 parameters (Accel, Tenmp, Light, Button)

        """

    # Set colour scheme of GUI
    sg.theme('Default 1')

    # Define the layout of the GUI
    layout = [[sg.Text('Input Folder',size=(10,1)), sg.Input(input), sg.FolderBrowse()],
              [sg.Text('Output Folder',size=(10,1)), sg.Input(output), sg.FolderBrowse()],
              [sg.Checkbox('Correct Drift:', default=correct_drift), sg.Checkbox('Overwrite:', default=overwrite), sg.Checkbox('Quiet', default=quiet)],
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
        while not (os.path.exists(values[0]) and os.path.exists(values[1])):
            window.refresh
            a = os.path.exists(values[0])
            b = os.path.exists(values[1])
            if a+b == 0:
                sg.popup_error('ERROR: INPUT FOLDER PATH AND OUTPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Names.')
            elif a == 0:
                sg.Popup('ERROR: INPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Name.')
            elif b == 0:
                sg.Popup('ERROR: OUTPUT FOLDER PATH NOT RECOGNIZED. Please Enter Valid Path Name.')
            event, values = window.Read()
            continue
    
    # Close GUI
    window.close()

    # Run script using values obtained from GUI input
    folder_convert(values[0],values[1],values[2],values[3],values[4])
       
# Call function to make file work like an executable
folder_convert_gui()
