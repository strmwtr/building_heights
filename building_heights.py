import arcpy

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

# Setup Workspace
gdb = r'\\metanoia\geodata\PW\sw_tech\Building_Heights\Building_Heights.gdb'
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

# Cleans up workspace during code development
def fresh():
    rasts = arcpy.ListRasters()
    feats = arcpy.ListFeatureClasses()
    for feat in feats:
        arcpy.Delete_management(feat)
    for rast in rasts:
        if rast not in ('Last_Returns', 'Ground_All_Returns'):
            arcpy.Delete_management(rast)

# Fills sinkholes in rasters created from LIDAR
# Last_Returns is made of All Classes and Last Returns
# Ground is made of Ground Class and All Returns     
def fill_rast():
    G_F = arcpy.sa.Fill('Ground_All_Returns')
    G_F.save(gdb + '\\G_F')
    L_F = arcpy.sa.Fill('Last_Returns')
    L_F.save(gdb + '\\L_F')

# Projects rasters to match structures projection
def proj_rast():
    prj = r'\\metanoia\geodata\PW\sw_tech\Coordinate_Systems\NAD 1983 ' \
    'StatePlane Virginia South FIPS 4502 (US Feet).prj'
    arcpy.ProjectRaster_management('G_F', 'Ground', prj)
    arcpy.ProjectRaster_management('L_F', 'LastReturns', prj)

# Preps Structures and Rasters for calculations
def struc():
    # Copies Structure layer from SDE
    bldg = 'Database Connections\\Connection to GISPRDDB direct connect.sde' \
    '\\cvgis.CITY.Buildings\\cvgis.CITY.structure_existing_area'
    arcpy.CopyFeatures_management(bldg, 'Structures')
    # Adds Num_Points field to copy  
    arcpy.AddField_management('Structures', 'Num_Points', 'LONG')
    # Calculates Num_Points to be 10% of structure area
    arcpy.CalculateField_management('Structures', 'Num_Points', 
    '[Shape_Area]*0.1', 'VB')
    # Creates Ran_Points layer based on Num_Points field in Structures
    arcpy.CreateRandomPoints_management(gdb,'Ran_Points', 'Structures', 
    number_of_points_or_field='Num_Points')
    # Creates features to hold BIN info from Structures and location Ran_Points
    int_list = ['Structures', 'Ran_Points']
    arcpy.Intersect_analysis(int_list, 'Points_G_Int')
    arcpy.Intersect_analysis(int_list, 'Points_LR_Int')
    # Adds elevation data to each point, one set for ground points, one set for
    # last return points. Last return points are used to cut out the noise of 
    # trees, birds, and other anomolies in LIDAR data
    arcpy.AddSurfaceInformation_3d('Points_G_Int', 'G_F', 'Z')
    arcpy.AddSurfaceInformation_3d('Points_LR_Int', 'L_F', 'Z')

# Calculates statitics for elevation
def stats():
    # Calculates the mean elevation of each unique BIN for both Ground and Last
    # Returns, stores it in field Ground_Mean_Z or LR_Mean_Z
    arcpy.Statistics_analysis('Points_G_Int', 'Ground_Stats', [['Z','MEAN']], 
    'BIN')
    arcpy.Statistics_analysis('Points_LR_Int', 'Last_Return_Stats', 
    [['Z','MEAN']], 'BIN')
    arcpy.AddField_management('Ground_Stats', 'Ground_Mean_Z', 'FLOAT')
    arcpy.AddField_management('Last_Return_Stats', 'LR_Mean_Z', 'FLOAT')
    arcpy.CalculateField_management('Ground_Stats', 'Ground_Mean_Z', 
    '[MEAN_Z]', 'VB')
    arcpy.CalculateField_management('Last_Return_Stats', 'LR_Mean_Z', 
    '[MEAN_Z]', 'VB')
    # Joins Structures with summary statistics and exports to new feature
    arcpy.JoinField_management('Structures', 'BIN', 'Ground_Stats', 'BIN')
    arcpy.JoinField_management('Structures', 'BIN', 'Last_Return_Stats', 'BIN')
    arcpy.FeatureClassToFeatureClass_conversion ('Structures', gdb, 
    'Building_Heights')
    # Calculates Building_Height as LR_Mean_Z - Ground_Mean_Z
    arcpy.AddField_management('Building_Heights', 'Building_Height', 'SHORT')
    arcpy.CalculateField_management('Building_Heights', 'Building_Height', 
    '[LR_Mean_Z] - [Ground_Mean_Z]', 'VB')

# Cleans up all intermediate steps 
def clean():
    rasts = arcpy.ListRasters()
    feats = arcpy.ListFeatureClasses()
    tables = arcpy.ListTables()
    for feat in feats:
        if feat != 'Building_Heights':
            arcpy.Delete_management(feat)
    for rast in rasts:
        if rast not in ('Last_Returns', 'Ground_All_Returns'):
            arcpy.Delete_management(rast)
    for table in tables:
        arcpy.Delete_management(table)
  
#fresh()
#fill_rast()     
#proj_rast()
#struc()
stats()
#clean()

# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')