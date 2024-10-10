import katas
import json
import math

with open('docs/markers.json') as f:
    coords = [m['geometry']['coordinates'] for m in json.load(f)['features'] if m['geometry']['type'] == 'Point']

markers = {
    "version": "4",
    "type": "FeatureCollection",
    "features": []
}

# s = math.ceil(len(katas.katas) / len(coords))
# c_i = 0

for i, (f, d) in enumerate(katas.katas):
    if len(coords) == i:
        break
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
    # if (i + 1) % s == 0:
    #     c_i += 1


with open('docs/markers.json', 'w') as f:
    json.dump(markers, f, indent=2)
