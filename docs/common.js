/**
 * A general interactive map layer which includes marker and polygons created from geoJSON features.
 */
class InteractiveLayer {
    #create_checkbox;
    #ignore_next_resize = new Set(); // set of entries to skip initial resize call
    #feature_group;
    #geojsons = new Array();
    #highlighted_layers = new Array();
    #interactive_map;
    #is_default;
    #layers = new Map();
    #polygon_style_highlights = new Map();
    #resize_observer = new ResizeObserver(entries => {
        for (const entry of entries) {
            let feature_id = entry.target.closest('.popup-id').id.split(':')[2];

            // The observer also fires when it gets added so ignore that resize 'event'
            // or else we'll get a infinite loop
            if (this.#ignore_next_resize.has(feature_id)) {
                this.#ignore_next_resize.delete(feature_id);
                continue;
            }

            this.#getLayers(feature_id).forEach(layer => {
                if (layer.isPopupOpen()) {
                    this.#resize_observer.unobserve(entry.target);

                    // This changes the content of the element and the observer looses track of it because of that
                    // That's why we're re-adding the observer
                    layer.getPopup().update();

                    // The observer also fires when it gets added so ignore that resize 'event'
                    // or else we'll get a infinite loop
                    this.#ignore_next_resize.add(feature_id);
                    for (const element of document.getElementById(`popup:${this.id}:${feature_id}`).getElementsByClassName('popup-media')) {
                        this.#resize_observer.observe(element);
                    }
                }
            });
        }
    });
    #sidebar;
    #sidebar_list_html = undefined;
    #website_subdir;

    #default_onEachFeature = function (feature, layer) { };
    #default_pointToLayer = function (feature, latlng) {
        return L.marker(latlng, {
            icon: Utils.getCustomIcon(this.id),
            riseOnHover: true
        });
    };
    #default_polygon_style = function (feature) { return {}; };
    #default_polygon_style_highlight = function () {
        return {
            opacity: 1.0,
            fillOpacity: 0.7
        }
    };
    #default_sidebar_icon_html = function () {
        return `<img class="sidebar-image" src="images/icons/${this.id}.png" />`;
    };

    /**
     * A layer containing marker and polygons created from geoJSON features.
     * Multiple features can form a logical combined feature by having the same feature ID.
     * @param {string} id Unique layer id
     * @param {string} geojson geoJSON including features to add to the layer
     * @param {InteractiveMap} interactive_map Interactive map
     * @param {object} [args] Object containing various optional arguments
     * @param {string} [args.name=this.id] Human readable display name of the layer. Default: `this.id`
     * @param {boolean} [args.create_checkbox=false] Create a sidebar with a trackable list. Default: false
     * @param {boolean} [args.create_feature_popup=false] Create a popup for the first batch of geoJSON features. Default: false
     * @param {boolean} [args.is_default=false] Show this layer by default if a user visits the map for the first time. Default: false
     * @param {string | function} [args.sidebar_icon_html=function () { return `<img class="sidebar-image" src="images/icons/${this.id}.png" />`; }] A html string for the sidebar icon. Can be a function which returns a html string. The function has access to values of this layer e.g. the `this.id`.
     * @param {function} [args.onEachFeature=function (feature, layer) { }] A function with stuff to do on each feature. Has access to values of this layer e.g. `this.id`. Default: `function (feature, layer) { }`
     * @param {function} [args.pointToLayer=function (feature, latlng) { return L.marker(latlng, { icon: Utils.getCustomIcon(this.id), riseOnHover: true }); }] A function describing what to do when putting a geoJSON point to a layer.
     * @param {object | function} [args.polygon_style=function (feature) { return {}; }] An object or function returning an object with L.Path options. https://leafletjs.com/reference.html#path
     * @param {object | function} [args.polygon_style_highlight=function () { return { opacity: 1.0, fillOpacity: 0.7 }}] An object or function returning an object with L.Path options. https://leafletjs.com/reference.html#path
     * @param {L.LayerGroup} [args.feature_group=L.featureGroup.subGroup(this.#interactive_map.getClusterGroup())] The group all geoJson features get added to. Defaults to the default marker cluster.
     */
    constructor(id, geojson, interactive_map, args) {
        let defaults = {
            name: id,
            create_checkbox: false,
            create_feature_popup: true,
            is_default: false,
            sidebar_icon_html: this.#default_sidebar_icon_html,
            pointToLayer: this.#default_pointToLayer,
            onEachFeature: this.#default_onEachFeature,
            polygon_style: this.#default_polygon_style,
            polygon_style_highlight: this.#default_polygon_style_highlight
        };

        let params = { ...defaults, ...args };

        this.id = id;
        this.name = params.name;
        this.#interactive_map = interactive_map;

        this.#create_checkbox = params.create_checkbox;
        this.#is_default = params.is_default;
        this.#feature_group = params.feature_group ? params.feature_group : L.featureGroup.subGroup(this.#interactive_map.getClusterGroup());
        this.#sidebar = this.#interactive_map.getSidebar();
        this.#website_subdir = this.#interactive_map.getWebsiteSubdir();

        if (this.#create_checkbox) {
            this.#sidebar_list_html = this.#createSidebarTab(params.sidebar_icon_html);
        }

        this.addGeoJson(geojson, {
            create_feature_popup: params.create_feature_popup,
            pointToLayer: params.pointToLayer,
            onEachFeature: params.onEachFeature,
            polygon_style: params.polygon_style,
            polygon_style_highlight: params.polygon_style_highlight
        });
    }

    /**
     * Add another geoJSON to this layer group.
     * @param {string} geojson geoJSON containing the features to add
     * @param {object} [args] Optional arguments
     * @param {boolean} [args.create_feature_popup=false] Create a popup for each feature
     * @param {function} [args.onEachFeature=function (feature, layer) { }] A function with stuff to do on each feature. Has access to values of this layer e.g. `this.id`. Default: `function (feature, layer) { }`
     * @param {function} [args.pointToLayer=function (feature, latlng) { return L.marker(latlng, { icon: Utils.getCustomIcon(this.id), riseOnHover: true }); }] A function describing what to do when putting a geoJSON point to a layer.
     * @param {object | function} [args.polygon_style=function (feature) { return {}; }] An object or function returning an object with L.Path options. https://leafletjs.com/reference.html#path
     * @param {object | function} [args.polygon_style_highlight=function () { return { opacity: 1.0, fillOpacity: 0.7 }}] An object or function returning an object with L.Path options. https://leafletjs.com/reference.html#path
     */
    addGeoJson(geojson, args) {
        let defaults = {
            create_feature_popup: true,
            pointToLayer: this.#default_pointToLayer,
            onEachFeature: this.#default_onEachFeature,
            polygon_style: this.#default_polygon_style,
            polygon_style_highlight: this.#default_polygon_style_highlight
        };

        let params = { ...defaults, ...args };
        var onEachFeature = params.onEachFeature.bind(this);

        var geojson_layer = L.geoJSON(geojson, {
            pointToLayer: params.pointToLayer.bind(this),
            onEachFeature: (feature, layer) => {
                const featureIndex = geojson.features.indexOf(feature);
                if (this.#create_checkbox) {
                    this.#createSidebarCheckbox(feature, featureIndex);
                }

                if (params.create_feature_popup) {
                    this.#createFeaturePopup(feature, layer);
                }

                onEachFeature(feature, layer);

                this.#setFeature(feature.properties.id, layer);
            },
            style: params.polygon_style
        });

        this.#geojsons.push(geojson_layer);

        if (params.polygon_style_highlight instanceof Function) {
            this.#polygon_style_highlights.set(geojson_layer, params.polygon_style_highlight.bind(this));
        } else {
            this.#polygon_style_highlights.set(geojson_layer, params.polygon_style_highlight);
        }

        this.#feature_group.addLayer(geojson_layer);
        geojson_layer.eachLayer(layer => {
            layer.feature._origin = this.#feature_group.getLayerId(geojson_layer);
        });
    }

    /**
     * Get a map of all layers.
     * @returns Map<id, layers[]>
     */
    getAllLayers() {
        return this.#layers;
    }

    /**
     * Get the group layer which contains all markers and polygons.
     * @returns L.LayerGroup
     */
    getGroup() {
        return this.#feature_group;
    }

    /**
     * Get the outer bounds of this entire layer group.
     * @returns L.LatLngBounds
     */
    getGroupBounds() {
        var bounds = L.latLngBounds();

        this.#layers.forEach((layers, key) => {
            bounds.extend(this.#getLayerBounds(key));
        });

        return bounds;
    }

    /**
     * Check if this layer group has a feature.
     * @param {string} id Feature ID
     * @returns boolean
     */
    hasFeature(id) {
        return this.#layers.has(id);
    }

    /**
     * Highlight a feature.
     * @param {string} id Feature ID
     */
    highlightFeature(id) {
        this.#getLayers(id).forEach(layer => {
            if (layer instanceof L.Path) {
                this.#highlightPolygon(layer);
            } else {
                // Marker
                this.#highlightPoint(layer);
            }
        });

        this.#interactive_map.getMap().on('click', () => { this.removeFeatureHighlight(id); });
    }

    /**
     * Check if this is a lay which should be visible by default.
     * @returns boolean
     */
    isDefault() {
        return this.#is_default;
    }

    /**
     * Remove all currently active highlights for this layer group.
     */
    removeAllHighlights() {
        this.#highlighted_layers.forEach(layer => {
            if (layer instanceof L.Path) {
                this.#removePolygonHighlight(layer);
            } else {
                this.#removePointHighlight(layer);
            }
        });

        this.#highlighted_layers = [];
        this.#interactive_map.getMap().off('click', this.removeAllHighlights, this);
    }

    /**
     * Remove a active highlight for a feature.
     * @param {string} id Feature ID
     */
    removeFeatureHighlight(id) {
        // Remove from the same array that gets iterated
        // https://stackoverflow.com/a/24813338
        var layers = this.#getLayers(id);

        for (const index of this.#reverseKeys(this.#highlighted_layers)) {
            var layer = this.#highlighted_layers[index];

            if (!layers.includes(layer)) {
                continue;
            }

            if (layer instanceof L.Path) {
                this.#removePolygonHighlight(layer);
                this.#highlighted_layers.splice(index, 1);
            } else {
                this.#removePointHighlight(layer);
                this.#highlighted_layers.splice(index, 1);
            }
        }

        this.#interactive_map.getMap().off('click', () => { this.removeFeatureHighlight(id); });
    }

    /**
     * Set the amount of columns of the sidebar grid.
     * @returns Nothing
     */
    setSidebarColumnCount() {
        if (!this.#sidebar_list_html) {
            return;
        }

        var length = 4;
        var columns = 1;

        this.#layers.forEach((layer, id) => {
            if (id.length > length) {
                length = id.length;
            }
        });

        if (length < 5) {
            columns = 3;
        } else if (length < 15) {
            columns = 2;
        }

        this.#sidebar_list_html.setAttribute('style', `grid-template-columns: repeat(${columns}, auto)`);
    }

    /**
     * Show this layer group on the map.
     */
    show() {
        this.getGroup().addTo(this.#interactive_map.getMap());
    }

    /**
     * Zoom to this layer group.
     */
    zoomTo() {
        this.#interactive_map.zoomToBounds(this.getGroupBounds());
    }

    /**
     * Zoom to a specific feature.
     * @param {string} id Feature ID
     * @returns Nothing
     */
    zoomToFeature(id) {
        var layers = this.#getLayers(id);

        if (layers.length > 1) {
            // Multiple features
            this.#interactive_map.zoomToBounds(this.#getLayerBounds(id));
            return;
        }

        var layer = layers[0];

        if (layer instanceof L.Path) {
            // Polygon
            this.#interactive_map.zoomToBounds(this.#getLayerBounds(id));
            return;
        }

        // not visible
        this.#interactive_map.zoomToBounds(this.#getLayerBounds(id));
    }

    /**
     * Create a popup for a feature.
     * @param {object} feature Original feature object
     * @param {L.Layer} layer Resulting layer
     */
    #createFeaturePopup(feature, layer) {
        let content = function (layer) {
            var html = document.createElement('div');
            html.className = 'popup-id';
            html.id = `popup:${this.id}:${feature.properties.id}`;

            if (feature.properties.iframe_url) {
                var iframe = document.createElement('iframe');
                iframe.src = feature.properties.iframe_url;
                iframe.width = "600px";
                iframe.height = "600px";
                iframe.setAttribute('frameborder', '0');
                iframe.setAttribute('allowfullscreen', 'true');

                html.appendChild(iframe);
            } else {
                var title = document.createElement('h2');
                title.className = 'popup-title';
                title.innerHTML = feature.properties.name ? feature.properties.name : feature.properties.id;

                html.appendChild(title);

                if (feature.properties.description) {
                    var description = document.createElement('p');
                    description.className = 'popup-description';
                    var span = document.createElement('span');
                    span.setAttribute('style', 'white-space: pre-wrap');
                    span.appendChild(document.createTextNode(feature.properties.description));
                    description.appendChild(span);

                    html.appendChild(description);
                }
            }

            return html;
        }.bind(this);

        layer.bindPopup(content, { maxWidth: "auto", closeOnClick: true });

        layer.on('popupopen', event => {
            // Listen for size changes and update when it does
            for (const entry of document.getElementById(`popup:${this.id}:${feature.properties.id}`).getElementsByClassName('popup-media')) {
                this.#resize_observer.observe(entry);
            }
        }, this);

        layer.on('popupclose', event => {
            this.#resize_observer.disconnect();
        }, this);
    }

    /**
     * Create a sidebar checkbox for a feature if it doesn't already exist.
     * @param {object} feature Original feature object
     */
    #createSidebarCheckbox(feature, featureIndex) {
        if (!document.getElementById(this.id + ':' + feature.properties.id)) {
            if (feature.properties.type != 'destination') {
                return;
            }

            var list_entry = document.createElement('li');
            list_entry.className = 'flex-grow-1';

            var leave_function = () => { this.removeFeatureHighlight(feature.properties.id); };
            list_entry.addEventListener('mouseenter', () => { this.highlightFeature(feature.properties.id); });
            list_entry.addEventListener('mouseleave', leave_function);

            var label = document.createElement('label');
            var leftSpan = document.createElement('span');
            leftSpan.appendChild(document.createTextNode(feature.properties.id));
            leftSpan.style.fontWeight = 'bold';
            leftSpan.style.fontSize = '25px';

            var rightSpan = document.createElement('span');
            rightSpan.appendChild(document.createTextNode(feature.properties.completed + ' completed / ' + feature.properties.required_steps + ' required'));
            rightSpan.style.fontSize = '15px';

            label.style.display = 'flex';
            label.style.justifyContent = 'space-between';
            label.style.width = '100%';
            label.style.alignItems = 'center';

            label.appendChild(leftSpan);
            label.appendChild(rightSpan);
            label.className = 'flex-grow-1';

            list_entry.appendChild(label);
            this.#sidebar_list_html.appendChild(list_entry);

            feature.properties.katas.forEach((kata, kataIndex) => {
                var list_entry = document.createElement('li');
                list_entry.className = 'flex-grow-1';

                var label = document.createElement('label');

                let completedIcon = kata[2] === '1' ? '✅' : '❌';
                var leftSpan = document.createElement('span');
                leftSpan.appendChild(document.createTextNode(completedIcon + ' ' + kata[0]));
                leftSpan.style.fontWeight = 'bold';

                var rightSpan = document.createElement('span');
                rightSpan.appendChild(document.createTextNode(kata[1]));

                label.style.display = 'flex';
                label.style.justifyContent = 'space-between';
                label.style.width = '100%';

                label.appendChild(leftSpan);
                label.appendChild(rightSpan);
                label.className = 'flex-grow-1';

                list_entry.appendChild(label);
                this.#sidebar_list_html.appendChild(list_entry);
            });

        }
    }

    /**
     * Create a sidebar tab for this layer group.
     * @param {string} icon_html Icon html
     * @returns HTMLUListElement
     */
    #createSidebarTab(icon_html) {
        var list = document.createElement('ul');
        list.className = 'collectibles_list';

        var icon = icon_html;

        if (icon_html instanceof Function) {
            icon = icon_html.bind(this);
            icon = icon();
        }

        // Add list to sidebar
        this.#sidebar.addPanel({
            id: this.id,
            tab: icon,
            title: this.name,
            pane: '<p></p>' // placeholder to get a proper pane
        });
        document.getElementById(this.id).appendChild(list);

        return list;
    }

    /**
     * Get all layers with a specific feature ID.
     * @param {string} id ID of features to retrieve.
     * @returns Array of layers with that feature ID.
     */
    #getLayers(id) {
        return this.#layers.get(id);
    }

    /**
     * Get the bounds of all layers with a feature ID
     * @param {string} id Feature ID
     * @returns L.LatLngBounds
     */
    #getLayerBounds(id) {
        var bounds = L.latLngBounds();

        this.#getLayers(id).forEach(layer => {
            if (layer instanceof L.Polyline) {
                // Polygons
                bounds.extend(layer.getBounds());
            } else if (layer instanceof L.Circle) {
                // FIXME: This somehow fails:
                // bounds.extend(layer.getBounds());
                // Do this in the meantime:
                var position = layer._latlng;
                var radius = layer._mRadius;
                bounds.extend([[position.lat - radius, position.lng - radius], [position.lat + radius, position.lng + radius]]);
            } else {
                // Point
                bounds.extend([layer.getLatLng()]);
            }
        });

        return bounds;
    }

    /**
     * Highlight a point (marker)
     * @param {L.Layer} layer Marker
     * @returns Nothing
     */
    #highlightPoint(layer) {
        if (this.#highlighted_layers.includes(layer)) {
            return;
        }

        var icon = layer.getIcon();
        icon.options.html = `<div class="map-marker-ping"></div>${icon.options.html}`;
        layer.setIcon(icon);

        this.#highlighted_layers.push(layer);
    }

    /**
     * Highlight a polygon
     * @param {L.Layer} layer Polygon
     * @returns Nothing
     */
    #highlightPolygon(layer) {
        if (this.#highlighted_layers.includes(layer)) {
            return;
        }

        this.#polygon_style_highlights.forEach((style, geojson) => {
            if (geojson.hasLayer(layer)) {
                if (style instanceof Function) {
                    layer.setStyle(style(layer.feature));
                } else {
                    layer.setStyle(style);
                }
            }
        });


        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }

        this.#highlighted_layers.push(layer);
    }

    /**
     * Remove a highlight from a point (marker)
     * @param {L.Layer} layer Marker
     * @returns Nothing
     */
    #removePointHighlight(layer) {
        if (!this.#highlighted_layers.includes(layer)) {
            return;
        }

        var icon = layer.getIcon();
        icon.options.html = icon.options.html.replace('<div class="map-marker-ping"></div>', '');
        layer.setIcon(icon);
    }

    /**
     * Remove a highlight from a polygon. If no layer is specified the whole geoJson will remove the highlight.
     * @param {L.Layer} [layer=undefined] Polygon
     * @returns Nothing
     */
    #removePolygonHighlight(layer = undefined) {
        if (layer) {
            if (!this.#highlighted_layers.includes(layer)) {
                return;
            }

            this.#geojsons.forEach(geojson => {
                if (geojson.hasLayer(layer)) {
                    geojson.resetStyle(layer);
                    return;
                }
            });
            return;
        }

        this.#geojsons.forEach(geojson => {
            geojson.resetStyle(layer);
        });
    }

    // For removeFeatureHighlight()
    // https://stackoverflow.com/a/24813338
    * #reverseKeys(arr) {
        var key = arr.length - 1;

        while (key >= 0) {
            yield key;
            key -= 1;
        }
    }

    /**
     * Map a layer to a feature ID.
     * @param {string} id Feature ID
     * @param {L.Layer} layer Feature layer
     */
    #setFeature(id, layer) {
        if (!this.#layers.has(id)) {
            this.#layers.set(id, new Array());
        }

        this.#layers.get(id).push(layer);
    }
}


/*
Interactive map
*/


class InteractiveMap {
    #cluster_group;
    #interactive_layers = new Map();
    #map;
    #overlay_maps = new Object();
    #sidebar;
    #tile_layers = new Object();
    #website_subdir = '';

    /**
     *
     * @param {string} id ID of the html div this map gets added to
     * @param {object} [args] Optional arguments
     * @param {string} [args.attribution=''] General attribution html list about used stuff. Wrap every attribution in its own `<li></li>`
     * @param {int} [args.max_good_zoom=5] Specify the maximum good looking zoom which will be used for location events
     * @param {int} [args.max_map_zoom=8] Maximum zoom the user can zoom to even if it looks ugly. Use a reasonable value here
     * @param {string} [args.website_source] Where to find the source of this interactive map
     * @param {string} [args.website_subdir] Subdir this interactive map will be hosted in
     */
    constructor(id, args) {
        let defaults = {
            maxClusterRadius: 0,
            attribution: '',
            max_good_zoom: 5,
            website_source: '',
            website_subdir: '',
            max_map_zoom: 8
        }
        let params = { ...defaults, ...args };

        this.#map = L.map(id, {
            crs: L.CRS.Simple,
            maxZoom: params.max_map_zoom,
        });
        this.MAX_ZOOM = params.max_good_zoom;
        this.#website_subdir = params.website_subdir;

        this.#setUpSidebar(params.attribution, params.website_source, this.#website_subdir);
    }

    removeMap() {
        this.#map.removeLayer(this.#cluster_group);
        this.#map.removeControl(this.#sidebar);
        this.#map.remove();
    }

    addTileLayer(name, args, url = `https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/python_katas_map/tiles/{z}/{x}/{y}.png`) {
        let defaults = {
            minNativeZoom: 3,
            maxNativeZoom: 5,
            noWrap: true,
            detectRetina: true
        }
        let params = { ...defaults, ...args };
        params.maxNativeZoom = L.Browser.retina ? params.maxNativeZoom - 1 : params.maxNativeZoom; // 1 level LOWER for high pixel ratio device.

        var tile_layer = new L.tileLayer(url, params);

        // Make first base layer visible by default
        if (Object.keys(this.#tile_layers).length < 1) {
            tile_layer.addTo(this.#map);
        }

        this.#tile_layers[name] = tile_layer;
    }

    addInteractiveLayer(id, geojson, args) {
        let layer = new InteractiveLayer(id, geojson, this, args);
        this.#interactive_layers.set(layer.id, layer);
        return layer;
    }

    finalize() {
        // Set the column size for each interactive layer sidebar
        this.getLayers().forEach((layer, id) => {
            layer.setSidebarColumnCount();
        });

        // Defining overlay maps - markers
        this.getLayers().forEach((layer, id) => {
            this.#overlay_maps[layer.name] = layer.getGroup();
        });

        // Add layer selection to map
        L.control.layers(this.#tile_layers, this.#overlay_maps, {
            hideSingleBase: true
        }).addTo(this.#map);

        this.getLayers().forEach((layer, id) => {
            layer.show();
        });

        // Center view over map
        this.zoomToBounds(this.#getBounds());
    }

    getClusterGroup() {
        return this.#cluster_group;
    }

    getLayer(id) {
        if (!this.#interactive_layers.has(id)) {
            return undefined;
        }

        return this.#interactive_layers.get(id);
    }

    getLayers() {
        return this.#interactive_layers;
    }

    getMap() {
        return this.#map;
    }

    getMaxZoom() {
        return this.MAX_ZOOM;
    }

    getSidebar() {
        return this.#sidebar;
    }

    getWebsiteSubdir() {
        return this.#website_subdir;
    }

    hasLayer(id) {
        return this.#interactive_layers.has(id);
    }

    /**
     * Remove all currently active highlights.
     */
    removeAllHighlights() {
        this.getLayers().forEach((layer, id) => {
            layer.removeAllHighlights();
        });
        this.#map.off('click', this.removeAllHighlights, this);
    }

    zoomToBounds(bounds) {
        this.#map.fitBounds(bounds, {
            maxZoom: this.MAX_ZOOM
        });
    }

    #setUpSidebar(attribution, website, website_subdir) {
        this.#sidebar = L.control.sidebar({
            autopan: true,
            closeButton: true,
            container: 'sidebar',
            position: 'left'
        }).addTo(this.#map);

        this.#sidebar.addPanel({
            id: 'reload',
            tab: '<i class="fas fa-sync-alt"></i>',
            title: 'Reload map',
            position: 'bottom',
            button: () => {
                init(true);
            }
        });

        this.#sidebar.addPanel({
            id: 'github',
            tab: '<i class="fab fa-github"></i>',
            title: 'Change tracking repo',
            position: 'bottom',
            button: () => {
                document.getElementById('repoModal').style.display = 'block';
                document.getElementById('modalTooltip').style.visibility = 'hidden';
            }
        });


        // make group visible on pane opening
        this.#sidebar.on('content', event => {
            this.#map.addLayer(this.#interactive_layers.get(event.id).getGroup());
        });


    }

    #getBounds() {
        var bounds = L.latLngBounds();

        this.getLayers().forEach((layer, k) => {
            bounds.extend(layer.getGroupBounds());
        });

        return bounds;
    }

    #getLayerByName(name) {
        var interactive_layer = undefined;
        this.#interactive_layers.forEach((layer, id) => {
            if (layer.name == name) {
                interactive_layer = layer;
            }
        });

        return interactive_layer;
    }
}


/*
Utils
*/

class Utils {
    static getCustomIcon(feature) {
        var colorClass = feature.properties.current ? 'current' : (feature.properties.achieved ? 'achieved' : 'noncurrent');
        var remaining = feature.properties.required_steps - feature.properties.completed;
        var marker_html = feature.properties.type != 'destination' ? feature.properties.icon_element
         : `<i class="leaflet-marker-icon marker-cluster marker-cluster-${colorClass}-background marker-cluster-${colorClass} ${colorClass === 'current' ? 'pulse-effect' : ''}" style="pointer-events: auto !important; margin-left: -20px; margin-top: -20px; width: 40px; height: 40px; opacity: 1"><div><span>${remaining > 0 ? remaining : '<i class="fa-solid fa-crown"></i>'}</span></div></i>`;
        var iconSize = feature.properties.type != 'destination' ? 23 : 8;
        var popupLocationSize = feature.properties.type != 'destination' ? [5, -10] : [-5, -40];

        return L.divIcon({
            className: 'map-marker',
            html: marker_html,
            iconSize: [iconSize, 0],
            popupAnchor: popupLocationSize,   // the popup with name and description
            iconAnchor: [4, 13],
            tooltipAnchor: [0, 0]
        });
    }
}

/*
Generate Markers
*/


function setCookie(name, value) {
    var date = new Date();
    date.setTime(date.getTime() + (30 * 24 * 60 * 60 * 1000));
    var expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value) + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}


async function fetchTestResultsId(katas_repo) {
    const url = `https://raw.githubusercontent.com/${katas_repo}/refs/heads/internal/test/.test_results_id?cb=${Math.random()}`;

    try {
        const response = await fetch(url);
        if (response.ok) {
            const runId = await response.text();
            return runId.trim();
        } else {
            console.error("Failed to fetch .test_results_id");
        }
    } catch (error) {
        console.error("Error fetching .test_results_id:", error);
    }
    return null;
}

async function fetchWorkflowJobs(katas_repo, runId) {
    const baseUrl = `https://api.github.com/repos/${katas_repo}/actions/runs/${runId}/jobs`;
    let allResults = [];
    let page = 1;

    try {
        while (true) {
            const url = `${baseUrl}?per_page=100&page=${page}`;
            const response = await fetch(url);

            if (!response.ok) {
                console.error("Failed to fetch workflow jobs");
                break;
            }

            const data = await response.json();
            const results = data.jobs
                .filter(job => job.name.startsWith("test_") && job.conclusion === "success")
                .map(job => job.name.replace(/^test_/, ''));
            allResults = allResults.concat(results);

            if (page * 100 >= data.total_count) {
                break;
            }

            page++;
        }
        return allResults;
    } catch (error) {
        console.error("Error fetching workflow jobs:", error);
    }

    return [];
}



function triggerFireworks() {
    var duration = 7 * 1000;
    var end = Date.now() + duration;

    (function frame() {
        confetti({
            particleCount: 15,
            startVelocity: 20,
            spread: 360,
            origin: { x: 0.5, y: 0 }, // center of the screen
            zIndex: 9999
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
}


document.getElementById('submitRepo').onclick = function() {
    const accountInput = document.getElementById('accountInput').value;
    const repoInput = document.getElementById('repoInput').value;
    const fullName = accountInput + '/' + repoInput;
    const regex = /^[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+$/;

    if (regex.test(fullName.trim())) {
        setCookie('python_katas', fullName.trim() + '#null#null#');
        location.reload();
    }
};


let interactive_map;
async function init(reload = false) {

    const response = await fetch('markers.json');
    const data = await response.json();

    let katas_repo, test_results_id, markers_ver, test_results;
    let results_str = '';

    const cached_katas = getCookie('python_katas');
    if (cached_katas) {
        [katas_repo, test_results_id, markers_ver, test_results] = cached_katas.split('#');
        document.getElementById('accountInput').value = katas_repo.split('/')[0];
        document.getElementById('repoInput').value = katas_repo.split('/')[1];

        const current_test_results_id = await fetchTestResultsId(katas_repo);
        if (current_test_results_id) {
          if (test_results_id === current_test_results_id && markers_ver === data.version) {
            results_str = test_results;

          } else {
            const current_test_results = await fetchWorkflowJobs(katas_repo, current_test_results_id);
            results_str = data.features
              .filter(f => f.properties.type === 'destination')
              .map(f => f.properties.katas.map(kata => kata[0]))
              .map(katas => katas.map(kata => current_test_results.includes(kata) ? '1' : '0').join('')).join('_');

            setCookie('python_katas', katas_repo + '#' + current_test_results_id + '#' + data.version + '#' + results_str);
          }
        }
    }

    let player, current_feature;

    for (let i = data.features.length - 1; i >= 0; i--) {
        const f = data.features[i];
        if (f.properties.type != 'destination') {
            continue;
        }

        const res = results_str.split('_')[i];

        f.properties.completed = 0;
        f.properties.required_steps = Math.min(f.properties.required_steps, f.properties.katas.length);
        f.properties.katas = f.properties.katas.map((k, j) => {
          if (res[j] === '1') f.properties.completed++;
          return [...k, res[j]];
        });

        if (f.properties.completed < f.properties.required_steps) {
            const step_idx = Math.floor((f.properties.completed / f.properties.required_steps) * f.properties.steps.length)
            current_feature = f;
            player = {
              "type": "Feature",
              "properties": {
                "type": "player",
                "id": f.properties.id,
                "name": "You Are Here",
                "description": f.properties.destination_description,
                "icon_element": f.properties.icon_element
              },
              "geometry": {
                "type": "Point",
                "coordinates": f.properties.steps[step_idx]
              }
            };
        } else {
            f.properties.achieved = true;
        }
    }

    if (player) {
        data.features.push(player);
        current_feature.properties.current = true;
    }

    if (interactive_map) {
        interactive_map.removeMap();
    }

    interactive_map = new InteractiveMap('map', {
        max_good_zoom: 5,
        max_map_zoom: 7,
        website_subdir: 'PythonKatas'
    });

    interactive_map.addTileLayer('Ingame map', {
        minNativeZoom: 2,
        maxNativeZoom: 5,
    });

    interactive_map.addInteractiveLayer('markers', data, {
        name: "Python Katas",
        create_checkbox: true,
        create_feature_popup: true,
        sidebar_icon_html: '<i class="fab fa-python"></i>',
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {
                icon: Utils.getCustomIcon(feature),
                riseOnHover: true
            });
        }
    });

    interactive_map.finalize();

    if (data.features.filter(feature => feature.properties.type === 'destination').every(feature => feature.properties.achieved === true)) {
        triggerFireworks();
    }
}
