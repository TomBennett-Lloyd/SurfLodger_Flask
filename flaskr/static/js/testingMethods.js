/* global starCols, google, map */

//method used to test the location circles and create legend
function createLegend () {
    place={};
    //pick somewhere out to sea for consistent background
    var lat = 55;
    var lng = -20;
    //array of open_now options
    var openNow = [{open_now:false},null,{open_now:true}];
    for (var open in openNow) {
        //migrate circle location each iteration to create grid of circles
        lat+=0.001;
        var lng = -20;
        for (var stars in starCols) {
            lng+=0.002;
            //build dummy place object
            place.rating = stars;
            place.opening_hours = openNow[open];
            place.geometry = {location : new google.maps.LatLng(lat,lng)};
            place.place_id = "";
            //plot circle on map
            setPlaceMarker (place);
        }
    }
    //find the circles!
    map.setCenter(place.geometry.location);
    map.setZoom(15);
}
