import arcpy

#Input feature to fix, this should be a sewer line.
inputftf = arcpy.GetParameter(0)

#Inpute grid system.
inputgrid = arcpy.GetParameter(1)



minfoquery = "FromMH IS NOT NULL And ToMH IS NOT NULL And FacilityID = '1'"

#Select sewer lines with manhole info
arcpy.SelectLayerByAttribute_management(inputftf, "NEW_SELECTION", minfoquery)

#Make a temporary feature layer of items to name.
arcpy.MakeFeatureLayer_management(inputftf, "FtFlayer")

FtFLayer = "FtFlayer"

FtFcount = arcpy.GetCount_management(FtFLayer)

arcpy.AddMessage(FtFcount)

#Select grids that intersect sewer main features.
arcpy.SelectLayerByLocation_management(inputgrid, "INTERSECT", FtFLayer )

#Make a temporary feature layer of grids that were selected.
arcpy.MakeFeatureLayer_management(inputgrid, "GridLayer")


arcpy.SelectLayerByAttribute_management(inputgrid, 'CLEAR_SELECTION')
arcpy.SelectLayerByAttribute_management(inputftf, 'CLEAR_SELECTION')

GridLayer = "GridLayer"

gridcount = arcpy.GetCount_management(GridLayer)

arcpy.AddMessage(gridcount)

GridNumList = []

#Creates a list of the intersecting grid numbers.
with arcpy.da.SearchCursor(GridLayer, "NewGridNo") as cursor:
    for row in cursor:
        rowStr = str(row)
        rowStr = rowStr[2:7]
        GridNumList.append(rowStr)

for grid in GridNumList:
    rowquery = """{} LIKE '%{}%'""".format("NewGridNo", str(grid))
#Select a grid from the GridNumList.
    arcpy.SelectLayerByAttribute_management(GridLayer, "NEW_SELECTION", rowquery)
#Select a sewer line that intersects the previously selected grid.
    arcpy.SelectLayerByLocation_management(FtFLayer, "INTERSECT", GridLayer)
    fields = ['FacilityID','FromMH','ToMH']
    with arcpy.da.UpdateCursor(FtFLayer,fields) as cursor:
        for row in cursor:
            frommh = str(row[1])
            ToMH = str(row[2])
            if len(frommh) > 1 and len(ToMH) > 1 :
                sewerN = grid +"_"+ "MH" + frommh + "MH" + ToMH
                row[0] = sewerN
                arcpy.AddMessage(sewerN)
                cursor.updateRow(row)


