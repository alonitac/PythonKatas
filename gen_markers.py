import katas
import json

with open('docs/markers.json') as f:
    coords = [m['geometry']['coordinates'] for m in json.load(f)['features']]

markers = {
    "version": "4",
    "type": "FeatureCollection",
    "features": []
}

for i, (f, d) in enumerate(katas.katas):
    markers['features'].append({
            "type": "Feature",
            "properties": {
                "id": f,
                "name": f,
                "description": d
            },
            "geometry": {
                "type": "Point",
                "coordinates": coords[i]
            }
    })


with open('docs/markers.json', 'w') as f:
    json.dump(markers, f, indent=2)
