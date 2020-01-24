from Files.GENEActivFile import *


def file_naming(geneactivfile):
    """
    Creates and returns the properly formatted file names for the 4 outputted edf files
    """
    accelerometer_file_name = "%s.edf" % (geneactivfile.file_name.replace("_GA_", "_GENEActiv_Accelerometer_")[:-4])
    temperature_file_name = "%s.edf" % (geneactivfile.file_name.replace("_GA_", "_GENEActiv_Temperature_")[:-4])
    light_file_name = "%s.edf" % (geneactivfile.file_name.replace("_GA_", "_GENEActiv_Light_")[:-4])
    button_file_name = "%s.edf" % (geneactivfile.file_name.replace("_GA_", "_GENEActiv_Button_")[:-4])
    device_file_name = "%s.edf" % (geneactivfile.file_name.replace("_GA_", "_GENEActiv_Device_")[:-4])
    return accelerometer_file_name, temperature_file_name, light_file_name, button_file_name, device_file_name


def folder_naming(): x = 1
