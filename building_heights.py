import arcpy

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

last_return_raster = r'C:\Users\brownr\Desktop\building_heights_data\source_raster\last_return'
ground_return_raster = r'C:\Users\brownr\Desktop\building_heights_data\source_raster\ground_return'
building_footprints = r'C:\Users\brownr\Desktop\building_heights_data\building_heights.gdb\buildings'
output_dir = r'C:\Users\brownr\Desktop\building_heights_data\outputs3'
prj = r'\\metanoia\geodata\PW\sw_tech\Coordinate_Systems\NAD 1983 StatePlane Virginia South FIPS 4502 (US Feet).prj'    

def delta_raster(in_raster_1, in_raster_2):
    ''' Equivalent to Raster Calculator expression "in_raster_1 - in_raster_2

        Subtracts in_raster_1 from in_raster_2 and stores output at 
        output_dir\delta_raster
    '''
    delta_raster = arcpy.sa.Minus(in_raster_1, in_raster_2)
    delta_raster.save(output_dir + '\\delta_raster')
    return delta_raster

def fill(in_raster):
    ''' Fills raster '''
    filled_raster = arcpy.sa.Fill(in_raster)
    return filled_raster

def proj_rast(in_raster, out_raster, prj):
    ''' Projects raster '''
    arcpy.ProjectRaster_management(in_raster, out_raster, prj)

def random_points(feature, out_location):
    temp = out_location + '\\temp.shp'
    arcpy.CopyFeatures_management(feature, temp)
    arcpy.AddField_management(temp, 'Num_Points', 'LONG')
    arcpy.CalculateField_management(temp, 'Num_Points', 
    '[Shape_Area]*0.1', 'VB')
    arcpy.CreateRandomPoints_management(output_dir,'Ran_Points.shp', temp,
    number_of_points_or_field='Num_Points')

def elevation_data(in_feature, in_raster):
    arcpy.AddSurfaceInformation_3d(in_feature, in_raster, 'Z')

def footprint_elevation(footprint, elevation_points, out_location, unique_id):
    arcpy.Intersect_analysis([footprint, elevation_points], out_location+'\\footprint_points.shp')
    arcpy.Statistics_analysis(out_location+'\\footprint_points.shp', out_location+'\\Ground_Stats', [['Z','MEAN']],
    unique_id)

def create_building_heights_feature(in_feature_1, in_feature_2, unique_id, out_location):
    arcpy.JoinField_management(in_feature_1, unique_id, in_feature_2, unique_id)

    arcpy.FeatureClassToFeatureClass_conversion (in_feature_1, out_location,
    'Building_Heights.shp')


delta_raster(last_return_raster,ground_return_raster)
random_points(building_footprints, output_dir)
elevation_data(output_dir+'\\Ran_Points.shp', output_dir+'\\delta_raster')
footprint_elevation(building_footprints, output_dir+'\\Ran_Points.shp', output_dir, 'BIN')
create_building_heights_feature(output_dir+'\\temp.shp', output_dir+'\\ground_stats', 'BIN', output_dir)

# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')    