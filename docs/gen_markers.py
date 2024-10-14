import katas
import json

with open('markers_master.json') as f:
    markers_master = json.load(f)

markers = {
    "version": "4",
    "type": "FeatureCollection",
    "features": []
}

for f in markers_master['features']:
    if f['properties']['type'] == 'destination':
        f['properties']['katas'] = katas.katas[f['properties']['_id']]

    markers['features'].append(f)


with open('markers.json', 'w') as f:
    json.dump(markers, f, indent=2)
