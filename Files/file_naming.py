# Author:  Adam Vert
# Date:  January, 2020

# ======================================== FUNCTION =========================================
def file_naming(geneactivfile):
    """
    Creates and returns the properly formatted file names for the 4 outputted edf files
    """
    file_name_split = geneactivfile.file_name.split("_")
    #file_name_split[4] = "00"
    base_name = '_'.join(file_name_split)
    accelerometer_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Accelerometer_")[:-4])
    temperature_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Temperature_")[:-4])
    light_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Light_")[:-4])
    button_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Button_")[:-4])
    device_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Device_")[:-4])
    return accelerometer_file_name, temperature_file_name, light_file_name, button_file_name, device_file_name

from GENEActivFile import *
geneactivfile = GENEActivFile(r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\Chris Data\OND01_WTL_Chris_1_GA_LAnkle.bin")
geneactivfile.read()
print(file_naming(geneactivfile))