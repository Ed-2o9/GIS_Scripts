# This tool is to copy the lined date into the install date if a lined date exist.
# The reason is that we need all the install dates for every main.
# This is only for sewer.

import arcpy

# Feature layer to work on.
inputft = arcpy.GetParameter(0)

# Select features with lined dates and no install date.
arcpy.management.SelectLayerByAttribute(inputft, "NEW_SELECTION", "InstallDate IS NULL And LinedYear IS NOT NULL")

