#!/usr/bin/env python

import geojson

class toolbox(object):
  def __init__(self, db):
    self.db = db

  def findStop(self, stop_id):
    data = self.db.select('stops',stop_id=stop_id)
    if data:
      stop = data[0]
      l = self.db.select('stop_seq',stop_id=stop_id)
      lineas = [t['trip_id'] for t in l]
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'], stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':lineas,
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      response = geojson.geoJsonFeatCollection([f])
    else:
      response = {'success': False}
    return response

  def routes(self):
    routes = []
    for row in self.db.select('routes'):
      data = {}
      for k in ['route_id', 'agency_id', 'route_short_name', 
        'route_long_name', 'route_desc', 'route_type', 
        'route_color']:
        data.update({k:row[k]})
      routes.append(data)
    return {'routes': routes}

  def trips(self, route_id):
    trips = []
    for row in self.db.select('trips',route_id=route_id):
      trips.append({
        'service_id':row['service_id'],
        'trip_id':row['trip_id'],
        'trip_headsign':row['trip_headsign'],
        'trip_short_name':row['trip_short_name'],
        'direction_id':row['direction_id'],
        'shape_id':row['shape_id']
        })
    return {'trips':trips}

  def shape(self, shape_id):
    result = self.db.select('shapes',shape_id=shape_id)
    coordList = [[p['shape_pt_lon'],p['shape_pt_lat']] for p in result]
    feature = geojson.geoJsonLineString(shape_id,coordList,{'type':'Line'})
    return geojson.geoJsonFeatCollection([feature])

  def tripStops(self, trip_id):
    features = []
    stopCodes = []
    q = """SELECT stop_id,is_timepoint 
      FROM stop_seq WHERE trip_id="{0}"
      ORDER BY stop_sequence""".format(trip_id)
    self.db.query(q)
    for i,row in enumerate(self.db.cursor.fetchall()):
      stopCodes.append([i,row['stop_id'],row['is_timepoint']])

    for i,stop_id,is_timepoint in stopCodes:
      d = self.db.select('stops',stop_id=stop_id)[0]
      l = self.db.select('stop_seq',stop_id=stop_id)
      lineas = [t['trip_id'] for t in l]
      f = geojson.geoJsonFeature(stop_id,
        d['stop_lon'],
        d['stop_lat'],
        {'stop_id':d['stop_id'],
        'stop_seq':i+1,
        'is_timepoint':bool(is_timepoint),
        'stop_lineas':lineas,
        'stop_calle':d['stop_calle'],
        'stop_numero':d['stop_numero'],
        'stop_esquina':d['stop_esquina'],
        'stop_entre':d['stop_entre']})
      features.append(f)
    return geojson.geoJsonFeatCollection(features)

  def bbox(self, bbox):
    w,s,e,n = map(float,bbox.split(','))
    q = """SELECT * 
      FROM stops s INNER JOIN stop_seq sq ON s.stop_id=sq.stop_id
      WHERE
        (stop_lat BETWEEN {s} AND {n})
        AND 
        (stop_lon BETWEEN {w} AND {e})
      LIMIT 300
      """.format(s=s,n=n,w=w,e=e)
    self.db.query(q)
    features = []
    d = {}
    for r in self.db.cursor.fetchall():
      stop = dict(r)
      linea = stop.pop('trip_id')
      stop_id = stop.pop('stop_id')
      if stop_id in d:
        d[stop_id]['lineas'].append(linea)
      else:
        d[stop_id] = stop
        d[stop_id]['lineas'] = [linea]
    for stop_id,stop in d.items():
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'],
        stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':stop['lineas'],
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      features.append(f)
    return geojson.geoJsonFeatCollection(features)

  def set_timepoint(self, trip_id, stop_id, is_timepoint):
    q = """UPDATE stop_seq 
        SET is_timepoint={is_timepoint}
        WHERE stop_id='{stop_id}' 
          AND trip_id='{trip_id}'
      """.format(trip_id=trip_id, stop_id=stop_id, 
        is_timepoint=is_timepoint)
    self.db.query(q)
    return {'is_timepoint': is_timepoint}

if __name__ == '__main__':
  import ormgeneric as o
  db = o.dbInterface('dbRecorridos.sqlite')
  tb = toolbox(db)
  print tb.findStop('C0004')