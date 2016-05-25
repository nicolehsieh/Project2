var map = L.map('mapid');

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
		attribution: 'Map data &copy; <a href="http://www.osm.org">OpenStreetMap</a>',
		maxZoom: 18
	}).addTo(map);
map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

// longitudes and latitudes points
var points = {{ g["points"]}};	

// some polyline options
var polylineOptions = {
	color: 'blue',
	weight: 6,
	opacity: 0.9
};

var polyline = new L.Polyline(points, polylineOptions);
map.addLayer(polyline);

// zoom the map to the polyline
map.fitBounds(polyline.getBounds());