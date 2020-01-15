from Files.GENEActivFile import GENEActivFile
from Files.ga_to_edf import ga_to_edf


#geneactivfile = GENEActivFile(r"C:\Users\ahvert\PycharmProjects\owcurate\DataFiles_DoNotPush\OND05_SWP_1001_01_GA_LWrist.bin")
#geneactivfile.read(geneactivfile)
ga_to_edf("..\\DataFiles_DoNotPush\\KW4_LAnkle.bin","..\\DataFiles_DoNotPush\\Accelerometer","..\\DataFiles_DoNotPush\\Temperature","..\\DataFiles_DoNotPush\\Light","..\\DataFiles_DoNotPush\\Button")