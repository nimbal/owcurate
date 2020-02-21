# Author:  Adam Vert
# Date:  January, 2020

# ======================================== FUNCTION =========================================
def file_naming(geneactivfile):
    """
    Creates and returns the properly formatted file names for the 4 outputted edf files
    """
    file_name_split = geneactivfile.file_name.split("_")
    if file_name_split[3] == "01":
        file_name_split[3] = "A"
    elif file_name_split[3] == "02":
        file_name_split[3] = "B"
    else:
        print("WARNING VISIT CODE WAS NOT 01 or 02. PUTTING VISIT CODE AS 00 IN FILE NAME")
        file_name_split[3] = "00"

    base_name = '_'.join(file_name_split)
    accelerometer_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Accelerometer_")[:-4])
    temperature_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Temperature_")[:-4])
    light_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Light_")[:-4])
    button_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Button_")[:-4])
    device_file_name = "%s.edf" % (base_name.replace("_GA_", "_GENEActiv_Device_")[:-4])
    return accelerometer_file_name, temperature_file_name, light_file_name, button_file_name, device_file_name
