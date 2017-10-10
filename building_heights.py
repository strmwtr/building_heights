import arcpy

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

def delta_raster(in_raster_1, in_raster_2, output_dir):
    ''' Equivalent to Raster Calculator expression "in_raster_1 - in_raster_2

        Subtracts in_raster_1 from in_raster_2 and stores output at 
        output_dir\delta_raster
    '''
    delta_raster = arcpy.sa.Minus(in_raster_1, in_raster_2)
    delta_raster.save(output_dir + r'\delta')
    return delta_raster

def fill(in_raster, output_dir):
    ''' Fills raster '''
    filled_raster = arcpy.sa.Fill(in_raster)
    filled_raster.save(output_dir + r'\delta_raster')

def proj_rast(in_raster, output_dir, in_feat):
    ''' Projects raster '''
    temp = output_dir + r'\temp.shp'
    prj = output_dir + r'\temp.prj'
    arcpy.CopyFeatures_management(in_feat, temp)
    arcpy.ProjectRaster_management(in_raster, in_raster + '_p', prj)
    
def random_points(feature, out_location):
    arcpy.AddField_management(feature, 'Num_Points', 'LONG')
    arcpy.CalculateField_management(feature, 'Num_Points', 
    '[Shape_Area]*0.1', 'VB')
    arcpy.CreateRandomPoints_management(out_location, 'random_points', feature,
    number_of_points_or_field='Num_Points')

def elevation_data(in_feature, in_raster):
    arcpy.AddSurfaceInformation_3d(in_feature, in_raster, 'Z')

def footprint_elevation(footprint, elevation_points, out_location, unique_id):
    arcpy.Intersect_analysis([footprint, elevation_points], 'elevation_points')
    arcpy.Statistics_analysis('elevation_points', 'stats', [['Z','MEAN']],
    unique_id)

def create_building_heights_feature(in_feat_1, in_feat_2, unique_id, out_location):
    arcpy.JoinField_management(in_feat_1, unique_id, in_feat_2, unique_id)

    arcpy.FeatureClassToFeatureClass_conversion (in_feat_1, out_location,
    'Building_Heights')

    arcpy.AddField_management('Building_Heights', 'Height', 'SHORT')
    arcpy.CalculateField_management('Building_Heights', 'Height', 
    '[MEAN_Z]', 'VB')

# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')    
