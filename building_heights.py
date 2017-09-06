import arcpy

# Setup Workspace
gdb = r'C:\Users\brownr\Desktop\building_heights\building_heights_data\building_heights.gdb'
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

last_return_raster = r'C:\Users\brownr\Desktop\building_heights\building_heights_data\lastreturn'
ground_return_raster = r'C:\Users\brownr\Desktop\building_heights\building_heights_data\groundreturn'
building_footprints = r'C:\Users\brownr\Desktop\building_heights\building_heights_data\building_heights.gdb\buildings'
output_dir = r'C:\Users\brownr\Desktop\building_heights\building_heights_data'
prj = r'\\metanoia\geodata\PW\sw_tech\Coordinate_Systems\NAD 1983 StatePlane Virginia South FIPS 4502 (US Feet).prj'    
def proj_rast():
    ground_return_raster_filled = arcpy.sa.Fill(ground_return_raster)
    last_return_raster_filled = arcpy.sa.Fill(last_return_raster)
    ground_return_raster_projected = output_dir + '\\gr_proj'
    last_return_raster_projected = output_dir + '\\lr_proj'
    arcpy.ProjectRaster_management(ground_return_raster_filled, ground_return_raster_projected, prj)
    arcpy.ProjectRaster_management(last_return_raster_filled, last_return_raster_projected, prj)

def struc():
    # Create copy of footprint layer. Bypasses editing rights for adding and 
    # Calculating num_points field
    footprint_source = building_footprints
    footprint = output_dir + '\\building_footprints.shp'
    arcpy.CopyFeatures_management(footprint_source, footprint)
    # Adds Num_Points field to copy
    arcpy.AddField_management(footprint, 'Num_Points', 'LONG')
    # Calculates Num_Points to be 10% of structure area
    arcpy.CalculateField_management(footprint, 'Num_Points',
    '[Shape_Area]*0.1', 'VB')
    # Creates Ran_Points layer based on Num_Points field in Structures
    arcpy.CreateRandomPoints_management(output_dir,'Ran_Points.shp', footprint,
    number_of_points_or_field='Num_Points')
    # Creates features to hold BIN info from Structures and location Ran_Points
    int_list = [footprint, output_dir+'\\Ran_Points.shp']
    arcpy.Intersect_analysis(int_list, output_dir+'\\Points_G_Int.shp')
    arcpy.Intersect_analysis(int_list, output_dir+'\\Points_LR_Int')
    # Adds elevation data to each point, one set for ground points, one set for
    # last return points. Last return points are used to cut out the noise of
    # trees, birds, and other anomolies in LIDAR data
    arcpy.AddSurfaceInformation_3d(output_dir+'\\Points_G_Int.shp', output_dir + '\\gr_proj', 'Z')
    arcpy.AddSurfaceInformation_3d(output_dir+'\\Points_LR_Int.shp', output_dir + '\\lr_proj', 'Z')

struc()

# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')    