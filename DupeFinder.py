##This tool searches for duplicates in a field and adds a number to the end.
## Started 12/10/21


import arcpy

# Get the first parameter. The feature layer you need to search for duplicates.
inputFt = arcpy.GetParameter(0)

# Get the second parameter. The attribute in the feature layer to search for dupes.
inputFtAtt = arcpy.GetParameter(1)

# Output dataset name
outData = str(inputFt) + "_Dupes"


# Use FindIdentical to find duplicates.
arcpy.management.FindIdentical(inputFt,outData,inputFtAtt,out_record_option= "ONLY_DUPLICATES")


