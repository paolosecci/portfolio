// // Store our API endpoint inside queryUrl
var qUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
var pUrl = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_plates.json"


//Create a satellite view layer
var satelliteLayer = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGF1cmVsaWMiLCJhIjoiY2pteG9icGYyM3ZvaTNxbnk2a2F6MDZmciJ9.ZQhdib9of9UJDKThb3b1QA", {
    attribution: "Mapbox &copy | return to <a href=\"/#projects\">Demo</a>",
    maxZoom: 18,
    id: "mapbox.satellite",
});

//Create a greyscale view layer
var lightLayer = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGF1cmVsaWMiLCJhIjoiY2pteG9icGYyM3ZvaTNxbnk2a2F6MDZmciJ9.ZQhdib9of9UJDKThb3b1QA", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
});

//initialize the faultlines layer
var faultLines = new L.layerGroup();

//initialize the earthquakes layered by magnitude
var quakeLayers = {
    tier0: new L.LayerGroup(),
    tier1: new L.LayerGroup(),
    tier2: new L.LayerGroup(),
    tier3: new L.LayerGroup(),
    tier4: new L.LayerGroup(),
    tier5: new L.LayerGroup()
};


//initialize base maps
var baseMaps = {
    "Satellite View": satelliteLayer,
    "Outline View": lightLayer
};

//initialize the layer maps
var overlayMaps = {
    "Fault Lines": faultLines,
    "<1 Magnitude": quakeLayers.tier0,
    "1-2 Magnitude": quakeLayers.tier1,
    "2-3 Magnitude": quakeLayers.tier2,
    "3-4 Magnitude": quakeLayers.tier3,
    "4-5 Magnitude": quakeLayers.tier4,
    ">5 Magnitude": quakeLayers.tier5
};

//build the map
var map = L.map("map-id", {
    center: [0, 0],
    zoom: 2,
    worldCopyJump: true,
    layers: [
        satelliteLayer,
        faultLines,
        quakeLayers.tier0,
        quakeLayers.tier1,
        quakeLayers.tier2,
        quakeLayers.tier3,
        quakeLayers.tier4,
        quakeLayers.tier5
    ]
});

// build the legend
var info = L.control({
    position: "bottomright"
});

info.onAdd = function() {
    var div = L.DomUtil.create("div", "legend");
    var labels = ["<1", "1-2", "2-3", "3-4", "4-5", "5+"];
    var colors = ["#1a9850", "#91cf60", "#d9ef8b", "#fee08b", "#fc8d59", "#d73027"];
    div.innerHTML = "<div><b>Magnitudes</b></div>";
    for (var i=0; i < labels.length; i++) {
        div.innerHTML += '<i style="background:' + colors[i] + '">&nbsp;</i>&nbsp;&nbsp;' + labels[i] + '<br/>';
    }
    return div;
};

info.addTo(map);

//ensure the legend can flow with the zoom and position view
map.on('zoomed', onZoomend);
function onZoomend(){
    if(map.getZoom()>0){
        map.removeControl(info);
    }
};

//layer the ampes on each other
L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
}).addTo(map);

//draw the plate lines
d3.json(pUrl, function(data) {
    L.geoJSON(data, {
        onEachFeature: function(feature, layer) {
            layer.bindPopup(feature.properties.PlateName + " Plate");
        },
        style: {
            color: "#fdae61",
            weight: 2,
            fillOpacity: 0
        }
    }).addTo(faultLines);
});


//create a geoJson and filter by magnitude to add to each layer
d3.json(qUrl, function(data) {
    var allQuakes = L.geoJSON(data);

        var quake0 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag < 1;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#66bd63",
                    weight: 1,
                    fillColor: "#66bd63",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                    });
            }
        });

        var quake1 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag >= 1 && feature.properties.mag < 2;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#66bd63",
                    weight: 1,
                    fillColor: "#66bd63",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                    });
            }
        });

        var quake2 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag >= 2 && feature.properties.mag < 3;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#a6d96a",
                    weight: 1,
                    fillColor: "#a6d96a",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                })
            }
        });
        var quake3 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag >= 3 && feature.properties.mag < 4;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#fdae61",
                    weight: 1,
                    fillColor: "#fdae61",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                })
            }
        });
        var quake4 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag >= 4 && feature.properties.mag < 5;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#f46d43",
                    weight: 1,
                    fillColor: "#f46d43",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                })
            }
        });
        var quake5 = L.geoJSON(data, {
            filter: function(feature, layer) {
                return feature.properties.mag > 5;
            },
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: feature.properties.mag ** 1.7,
                    color: "#d73027",
                    weight: 1,
                    fillColor: "#d73027",
                    fillOpacity: 0.6,
                    }).on('click', function() {
                        this.bindPopup(feature.properties.title).openPopup();
                })
            }
        });


        quake0.addTo(quakeLayers.tier0)
        quake1.addTo(quakeLayers.tier1)
        quake2.addTo(quakeLayers.tier2)
        quake3.addTo(quakeLayers.tier3)
        quake4.addTo(quakeLayers.tier4)
        quake5.addTo(quakeLayers.tier5)
});
