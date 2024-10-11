import katas
import json

with open('docs/markers_master.json') as f:
    markers_master = json.load(f)

markers = {
    "version": "4",
    "type": "FeatureCollection",
    "features": []
}

for f in markers_master['features']:
    section = katas.katas[f['properties']['_id']]
    if f['geometry']['type'] == 'Point':
        f['properties']['katas'] = section['katas']
        markers['features'].append(f)

    elif f['geometry']['type'] == 'LineString':
        steps = min(section['steps'], len(section['katas']))
        step = len(f['geometry']['coordinates']) / steps
        coords_idx = [round(i * step) for i in range(steps)][:-1] + [-1]  # is any case, take the last element

        for i in coords_idx:
            markers['features'].append({
                "type": "Feature",
                "properties": {
                    "id": f['properties']['_id'] + '_' + str(i),
                    "step": i,
                    "icon_class": section['icon_class']
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": f['geometry']['coordinates'][i]
                }
            })


with open('docs/markers.json', 'w') as f:
    json.dump(markers, f, indent=2)
