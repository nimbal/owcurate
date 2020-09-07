import sys
sys.path.append('/Users/kbeyer/repos')

import owcurate.Files.OND06_metadata as bi

# NIMBAL FILES
datapkg_dir = (
    '/Volumes/nimbal$/Data/ReMiNDD/Processed Data/Bittium/OND06_ALL_01_SNSR_BITF_2020MAY31_DATAPKG')

# LOCAL FILES
#datapkg_dir = ('/Users/kbeyer/repos/test_data/DATAPKG')



# CREATE FILELIST CSV
#bi.create_filelist_csv(datapkg_dir)

# CREATE DATA CSV
bi.create_data_csv(datapkg_dir)





