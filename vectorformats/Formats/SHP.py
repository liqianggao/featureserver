'''
Created on May 18, 2011

@author: michel
'''

from vectorformats.Formats.Format import Format
import vectorformats.lib.shapefile as shapefile 
import StringIO

class SHP(Format):

    def encode(self, features, props = None, fixed_props = False, **kwargs):
        ''' '''
        writer = shapefile.Writer()
        
        columns = self.datasource.attribute_cols.split(',')
        for col in columns:
            col = self.getFormatedAttributName(col)
            writer.field(col)
        
        for feature in features:
            self.encode_feature(feature, writer)
        
        shpBuffer = StringIO.StringIO()
        shxBuffer = StringIO.StringIO()
        dbfBuffer = StringIO.StringIO()
        
        writer.saveShp(shpBuffer)
        writer.saveShx(shxBuffer)
        writer.saveDbf(dbfBuffer)
        
        return (shpBuffer, shxBuffer, dbfBuffer)
    
    def encode_feature(self, feature, writer):
        
        if feature['geometry']['type'] == 'Point':
            writer.shapeType = shapefile.POINT
            writer.point(feature['geometry']['coordinates'][0], feature['geometry']['coordinates'][1])
        elif feature['geometry']['type'] == 'LineString':
            writer.shapeType = shapefile.POLYLINE
            parts = []
            parts.append(feature['geometry']['coordinates'])
            writer.line(parts=parts)
        elif feature['geometry']['type'] == 'Polygon':
            writer.shapeType = shapefile.POLYGON
            writer.poly(parts=feature['geometry']['coordinates'])
        else:
            raise Exception("Could not convert geometry of type %s." % feature['geometry']['type'])
        
        records = {}
        for key, property in feature.properties.iteritems():
            if property == None:
                records[key] = ''
            else:
                records[key] = property.encode('utf-8')
        writer.record(**records)
        