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
            create_feature_popup: false,
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
            create_feature_popup: false,
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
     * Remove a layer from the layer group.
     * @param {L.Layer} layer L.Layer to remove.
     */
    removeLayer(layer) {
        this.#getGroupForEdit(layer).removeLayer(layer);
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

        var group = this.#getGroupForEdit(layer);

        if (group instanceof L.MarkerClusterGroup && group.hasLayer(layer)) {
            // Single Point
            group.zoomToShowLayer(layer, () => {
                // Zoom in further if we can
                window.setTimeout(() => {
                    if (this.#interactive_map.getMap().getZoom() < this.#interactive_map.getMaxZoom()) {
                        this.#interactive_map.zoomToBounds(this.#getLayerBounds(id));
                    }
                }, 300);
            });
            return;
        }

        // not visible
        this.#interactive_map.zoomToBounds(this.#getLayerBounds(id));
    }

    /**
     * Add a layer back to the group it belongs to. That should be the original L.geoJSON but has to be the the parent MarkerCluster if the geoJSON was added to a marker cluster.
     * @param {L.Layer} layer L.Layer
     */
    #addLayer(layer) {
        this.#getGroupForEdit(layer).addLayer(layer);
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

            // Checkbox requires a global counterpart
            if (this.#create_checkbox && document.getElementById(this.id + ':' + feature.properties.id)) {
                var label = document.createElement('label');
                label.className = 'popup-checkbox is-fullwidth';

                var label_text = document.createTextNode('Hide this marker');

                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';

                if (localStorage.getItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`)) {
                    checkbox.checked = true;
                }

                checkbox.addEventListener('change', element => {
                    if (element.target.checked) {
                        // check global checkbox
                        document.getElementById(this.id + ':' + feature.properties.id).checked = true;
                        // remove all with ID from map
                        this.#getLayers(feature.properties.id).forEach(l => {
                            this.#getGroupForEdit(l).removeLayer(l);
                        });
                        // save to localStorage
                        localStorage.setItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`, true);
                    } else {
                        // uncheck global checkbox
                        document.getElementById(this.id + ':' + feature.properties.id).checked = false;
                        // add all with ID to map
                        this.#getLayers(feature.properties.id).forEach(l => {
                            this.#addLayer(l);
                        });
                        // remove from localStorage
                        localStorage.removeItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`);
                    }
                });

                label.appendChild(checkbox);
                label.appendChild(label_text);
                html.appendChild(label);
            }

            return html;
        }.bind(this);

        layer.bindPopup(content, { maxWidth: "auto" });

        layer.on('popupopen', event => {
//            this.#interactive_map.getShareMarker().removeMarker();
            Utils.setHistoryState(this.id, feature.properties.id);

            // Listen for size changes and update when it does
            for (const entry of document.getElementById(`popup:${this.id}:${feature.properties.id}`).getElementsByClassName('popup-media')) {
                this.#resize_observer.observe(entry);
            }
        }, this);

        layer.on('popupclose', event => {
//            this.#interactive_map.getShareMarker().prevent();
            Utils.setHistoryState(undefined, undefined, this.#website_subdir);
            this.#resize_observer.disconnect();
        }, this);
    }

    /**
     * Create a sidebar checkbox for a feature if it doesn't already exist.
     * @param {object} feature Original feature object
     */
    #createSidebarCheckbox(feature, featureIndex) {
        if (!document.getElementById(this.id + ':' + feature.properties.id)) {
            var list_entry = document.createElement('li');
            list_entry.className = 'flex-grow-1';

            var leave_function = () => { this.removeFeatureHighlight(feature.properties.id); };
            list_entry.addEventListener('mouseenter', () => { this.highlightFeature(feature.properties.id); });
            list_entry.addEventListener('mouseleave', leave_function);

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = this.id + ':' + feature.properties.id;
            checkbox.className = 'flex-grow-0';

            var label = document.createElement('label');

            let completedIcon = feature.properties.completed ? '✅' : '❌';
            var leftSpan = document.createElement('span');
            leftSpan.appendChild(document.createTextNode((featureIndex + 1) + '. ' + feature.properties.id + ' ' + completedIcon));
            leftSpan.style.fontWeight = 'bold';

            var rightSpan = document.createElement('span');
            rightSpan.appendChild(document.createTextNode('(' + feature.properties.description + ')'));

            label.style.display = 'flex';
            label.style.justifyContent = 'space-between';
            label.style.width = '100%';

            label.appendChild(leftSpan);
            label.appendChild(rightSpan);
            label.htmlFor = checkbox.id;
            label.className = 'flex-grow-1';

            var icon = document.createElement('i');
            icon.className = 'fas fa-crosshairs fa-xs';

            list_entry.appendChild(checkbox);
            list_entry.appendChild(label);

            this.#sidebar_list_html.appendChild(list_entry);

            // hide if checked previously
            if (localStorage.getItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`)) {
                checkbox.checked = true;
            }

            // watch global checkbox
            if (document.getElementById(this.id + ':' + feature.properties.id) != null) {
                // if not a marker try to assign to the same checkbox as the corresponding marker
                document.getElementById(this.id + ':' + feature.properties.id).addEventListener('change', element => {
                    if (element.target.checked) {
                        // remove all layers with ID from map
                        this.#getLayers(feature.properties.id).forEach(l => {
                            this.#getGroupForEdit(l).removeLayer(l);
                        });
                        // save to localStorage
                        localStorage.setItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`, true);
                    } else {
                        // add all layers with ID to map
                        this.#getLayers(feature.properties.id).forEach(l => {
                            this.#addLayer(l);
                        });
                        // remove from localStorage
                        localStorage.removeItem(`${this.#website_subdir}:${this.id}:${feature.properties.id}`);
                    }
                });
            }
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
     * Get the layer group for adding and removing layers. This can differ from their original layer group.
     * @param {L.Layer} layer Layer
     * @returns L.LayerGroup
     */
    #getGroupForEdit(layer) {
        // The group is the GeoJSON FeatureGroup
        var group = this.#feature_group.getLayer(layer.feature._origin);
        var parent_group = this.#feature_group;

        // Subgroups can be nested, get top level
        while (parent_group instanceof L.FeatureGroup.SubGroup) {
            parent_group = this.#feature_group.getParentGroup();
        }

        // There's an issue with marker from a geojson with marker cluster so we have use parent cluster then
        if (parent_group instanceof L.MarkerClusterGroup) {
            group = parent_group;
        }

        return group;
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
    #user_layers;
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
            maxClusterRadius: 20,
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
        });;
        this.MAX_ZOOM = params.max_good_zoom;
        this.#website_subdir = params.website_subdir;

        this.#cluster_group = L.markerClusterGroup({
            spiderfyOnMaxZoom: true,
            maxClusterRadius: params.maxClusterRadius
        }).addTo(this.#map);

        this.#setUpToolbar();
        this.#setUpSidebar(params.attribution, params.website_source, this.#website_subdir);

        this.#user_layers = JSON.parse(localStorage.getItem(`${this.#website_subdir}:user_layers`));
        this.#map.on('overlayadd', event => {
            this.addUserLayer(event.name);
        });
        this.#map.on('overlayremove ', event => {
            this.removeUserLayer(event.name);

            if (this.hasLayer(this.#getLayerByName(event.name))) {
                this.#getLayerByName(event.name).removeAllHighlights();
            }
        });
    }

    /**
     * Add a new background tile layer.
     *
     * Use tiled maps if possible, allows better zooming
     * Make sure tiling scheme is growing downwards!
     * https://github.com/commenthol/gdal2tiles-leaflet
     * https://github.com/Leaflet/Leaflet/issues/4333#issuecomment-199753161
     *
     * `./gdal2tiles.py -l -p raster -w none -z 3-5 full_map.jpg map_tiles`
     * @param {string} name Display name of this layer, also the ID
     * @param {object} [args] Optional arguments. Most likely you want to adapt `minNativeZoom` and `maxNativeZoom` to the generated tiles
     * @param {int} [args.minNativeZoom=3] The minimal zoom that can be found in the path
     * @param {int} [args.maxNativeZoom=5] The maximal zoom that can be found in the path
     * @param {string} [args.attribution=''] Tile layer specific attribution
     * @param {string} [url=map_tiles/{z}/{x}/{y}.png] Path to tile images
     */
    addTileLayer(name, args, url = `tiles/{z}/{x}/{y}.png`) {
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

    /**
     * Add a new interactive layer to the interactive map from a geoJSON. Returns the layer to be able to e.g. add more geoJSONS.
     * @param {string} id Unique layer id
     * @param {string} geojson geoJSON with features to add
     * @param {object} [args] Optional arguments
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
     * @returns InteractiveLayer
     */
    addInteractiveLayer(id, geojson, args) {
        let layer = new InteractiveLayer(id, geojson, this, args);

        this.#interactive_layers.set(layer.id, layer);

        return layer;
    }

    /**
     * Add a layer to the remembered user preferences.
     * @param {string} name Layer ID
     */
    addUserLayer(name) {
        if (!this.#user_layers.includes(name)) {
            this.#user_layers.push(name);
        }
        localStorage.setItem(`${this.#website_subdir}:user_layers`, JSON.stringify(this.#user_layers));
    }


    /**
     * Finalize the interactive map. Call this after adding all layers to the map.
     */
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

        // Show remembered layers
        if (!this.#user_layers) {
            this.#user_layers = new Array();
            this.getLayers().forEach((layer, id) => {
                if (layer.isDefault()) {
                    this.#user_layers.push(layer.name);
                }
            });
        }
        this.getLayers().forEach((layer, id) => {
            if (this.#user_layers.includes(layer.name)) {
                layer.show();
            }
        });

        // Center view over map
        this.zoomToBounds(this.#getBounds());

        // hide all previously checked marker
        this.getLayers().forEach((layer, layer_id) => {
            layer.getAllLayers().forEach((array, feature_id) => {
                // Remove if checked
                if (localStorage.getItem(`${this.#website_subdir}:${layer_id}:${feature_id}`)) {
                    array.forEach(feature => {
                        layer.removeLayer(feature);
                    });
                }
            });
        });

        // Search in url for marker and locate them
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('share')) {
            const share = urlParams.get('share');

            let latlng = share.split(",");
        } else if (urlParams.has('list')) {
            const list = urlParams.get('list');

            if (this.hasLayer(list)) {
                var layer = this.getLayer(list);;

                // make group visible
                layer.show();

                if (!urlParams.has('id')) {
                    layer.zoomTo();

                    // if no id open sidebar
                    this.#sidebar._tabitems.every(element => {
                        if (element._id == list) {
                            this.#sidebar.open(list);
                            return false;
                        }
                        return true;
                    });
                } else {
                    const id = urlParams.get('id');

                    if (layer.hasFeature(id)) {
                        layer.highlightFeature(id);
                        layer.zoomToFeature(id);
                        this.#map.on('click', this.removeAllHighlights, this);
                    }

                    // TODO: unhide?
                }
            }
        }
    }

    /**
     * Get the parent marker cluster. Might not be used at all.
     * @returns L.MarkerClusterGroup
     */
    getClusterGroup() {
        return this.#cluster_group;
    }

    /**
     * Get the layer with a specific ID.
     * @param {string} id Layer ID
     * @returns InteractiveLayer
     */
    getLayer(id) {
        if (!this.#interactive_layers.has(id)) {
            return undefined;
        }

        return this.#interactive_layers.get(id);
    }

    /**
     * Get all layers this interactive map is aware of.
     * @returns Map<id, layer>
     */
    getLayers() {
        return this.#interactive_layers;
    }

    /**
     * Get the leaflet map.
     * @returns L.Map
     */
    getMap() {
        return this.#map;
    }

    /**
     * Get the maximum good looking zoom value.
     * @returns integer
     */
    getMaxZoom() {
        return this.MAX_ZOOM;
    }

    /**
     * Get the sidebar associated to this interactive map.
     * @returns L.Control.Sidebar
     */
    getSidebar() {
        return this.#sidebar;
    }

    /**
     * Get the subdirectory this interactive map is associated to.
     * @returns string
     */
    getWebsiteSubdir() {
        return this.#website_subdir;
    }

    /**
     * Check if this interactive map has a specific layer group.
     * @param {string} id Layer group ID
     * @returns boolean
     */
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

    /**
     * Remove a layer from the remembered user preferences.
     * @param {string} name ID of the layer
     */
    removeUserLayer(name) {
        this.#user_layers = this.#user_layers.filter((value, index, array) => {
            return value != name;
        });
        localStorage.setItem(`${this.#website_subdir}:user_layers`, JSON.stringify(this.#user_layers));
    }

    /**
     * Zoom to given bounds on this interactive map.
     * @param {L.LatLngBounds | L.LatLng[] | L.Point[] | Array[]} bounds Bounds to zoom to. Can be an array of points.
     */
    zoomToBounds(bounds) {
        this.#map.fitBounds(bounds, {
            maxZoom: this.MAX_ZOOM
        });
    }

    /**
     * Initialize the sidebar.
     * @param {string} attribution General attribution list about used stuff
     * @param {string} website Where to find the source of this interactive map
     * @param {string} website_subdir Subdir this interactive map will be hosted in
     */
    #setUpSidebar(attribution, website, website_subdir) {
        this.#sidebar = L.control.sidebar({
            autopan: true,
            closeButton: true,
            container: 'sidebar',
            position: 'left'
        }).addTo(this.#map);

        this.#sidebar.addPanel({
            id: 'visit-github',
            tab: '<i class="fab fa-github"></i>',
            position: 'bottom',
            button: website
        });

        // make group visible on pane opening
        this.#sidebar.on('content', event => {
            if (event.id == 'attributions') return;

            this.#map.addLayer(this.#interactive_layers.get(event.id).getGroup());
            Utils.setHistoryState(event.id);
        });

        this.#sidebar.on('closing', () => {
            Utils.setHistoryState(undefined, undefined, this.#website_subdir);
        })
    }

    /**
     * Initialize the editing toolbar.
     */
    #setUpToolbar() {
        // Disable general editing
        L.PM.setOptIn(true);
        this.#map.pm.addControls({
            position: 'bottomright',
            drawCircleMarker: false,
            oneBlock: false
        });
        this.#map.pm.toggleControls(); // hide by default
    }

    /**
     * Get the outer bounds of all layers on a map, including currently hidden layers.
     * @returns L.LatLngBounds
     */
    #getBounds() {
        var bounds = L.latLngBounds();

        this.getLayers().forEach((layer, k) => {
            bounds.extend(layer.getGroupBounds());
        });

        return bounds;
    }

    /**
     * Get a layer by its name.
     * @param {string} name Layer name
     * @returns L.Layer
     */
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
    /**
     * Get an icon with a background variation and a centered symbol/icon/short string/nothing on top.
     * @param {string} [icon_id=undefined] The ID for the icon that can be found in `images/icons/ID.png` (length > 2). Can also be a Font Awesome ID (fa-ID), a text (length <= 2) or undefined.
     * @param {string} [icon_mode=undefined] The ID for the background variation that can be found in `images/icons/marker_ID.svg`. Can be undefined for the default icon background.
     * @returns L.divIcon
     */
    static getCustomIcon(icon_id = undefined, completed = false) {
        var foregroundColor = completed ? '#FFAF00' : '#FF204E';
        return L.divIcon({
            className: 'map-marker',
            html: `
            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="15" viewBox="0 0 320 512"><path fill="${foregroundColor}" d="M16 144a144 144 0 1 1 288 0A144 144 0 1 1 16 144zM160 80c8.8 0 16-7.2 16-16s-7.2-16-16-16c-53 0-96 43-96 96c0 8.8 7.2 16 16 16s16-7.2 16-16c0-35.3 28.7-64 64-64zM128 480l0-162.9c10.4 1.9 21.1 2.9 32 2.9s21.6-1 32-2.9L192 480c0 17.7-14.3 32-32 32s-32-14.3-32-32z"/></svg>
        `,
            iconSize: [19, 14],
            popupAnchor: [1, -34],
            iconAnchor: [12, 41],
            tooltipAnchor: [0, 0]
        });
    }

    /**
     * Replace the current browser address bar.
     * If only `website_subdir` is given it will reset to that url
     * @param {string} [list_id=undefined] Group ID
     * @param {string} [feature_id=undefined] Feature ID
     * @param {string} [website_subdir=''] Resets to plain url
     */
    static setHistoryState(list_id = undefined, feature_id = undefined, website_subdir = '') {
        if (list_id && feature_id) {
            history.replaceState({}, "", `?list=${list_id}&id=${feature_id}`);
        } else if (list_id) {
            history.replaceState({}, "", `?list=${list_id}`);
        } else {
            // CORS is driving me crazy
            // https://stackoverflow.com/a/3920899
            switch (window.location.protocol) {
                case 'http:':
                case 'https:':
                    //remote file over http or https
                    history.replaceState({}, "", `/${website_subdir}/`);
                    break;
                case 'file:':
                    //local file
                    history.replaceState({}, "", `index.html`);
                    break;
                default:
                //some other protocol
            }
        }
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





