/* global google, settings */
//set Global variables
var map;
var markers;
var bounds;
var latRegex = new RegExp("^(\\+|-)?(?:90(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,6})?))$" , "gi");
var lonRegex = new RegExp("^(\\+|-)?(?:180(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,6})?))$" , "gi");
// function to process when google initialises the map
function initMap() {
    if (document.getElementById('map')) {
        //init the map
       map = new google.maps.Map(document.getElementById('map'), {
         center: {lat:50.28, lng: -3.87},
         zoom: 12
       });
       // Initialise the Google maps autocomplete API for the input
       var autocomplete = document.getElementById('txtLocation');
       autocomplete=new google.maps.places.Autocomplete(autocomplete);
       // Bind the map's bounds (viewport) property to the autocomplete object,
       autocomplete.bindTo('bounds', map);
       //set the event handler for when a user selects a place from the searchbar
       var  form = $("#searchForm");
       place_changer(form,autocomplete,map);
       //set the map to drop a pin when double clicked
       google.maps.event.addListener(map, 'dblclick', function(event) {
            var place = {};
            place.geometry = {location: event.latLng};
            setMarker("Dropped Pin", place);
       });
    }
}
//Bind an event handler to the place change event
function place_changer(form, autocomplete) {
    //bind the marker creation to the search bar
    form.submit(function (event) {
    event.preventDefault();
    //get the place from the autocomplete input or
    //if theres no place then the user hasn't selected an option from the dropdown
    //it might be a lat lng so we'll test for that before raising the error alert
    var place = autocomplete.getPlace() || {name : $("#txtLocation").val()};
    //if there's no geometry see whether it's a lat long or whether the place just dosen't have geometry
    place.geometry ? place : place = checkLatLon(place);
    //if there's still not geometry the extraction of lat long failed
    if (!place) {return;}
    //build the address string if there is one
    var address = buildAddress(place.address_components);
    //put the marker on the map
    setMarker(address,place);
  });
}
//Set the marker
function setMarker(address,place) {
    var infowindow = setInfoWindow(place,address);
    //init the marker
    var marker = new google.maps.Marker({
      map: map,
      anchorPoint: new google.maps.Point(0, -29)
    });
    //set the marker position
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
    //bind the infowindow to the marker
    infowindow.open(map, marker);
    //toggle the info window to open when marker is clicked
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
    //add a circle to denote the seach radius
    var circle = new google.maps.Circle({
            strokeColor: '#d0d0e1',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#d0d0e1',
            fillOpacity: 0.3,
            map: map,
            center: place.geometry.location,
            //if the settings object isn't present then the places script isn't registered 
            //and the map is not being used for searching
            radius: settings.radius || 0 
          });
     circle.setOptions({zIndex:0});
    //set the map view to center on the new point
    map.setCenter(place.geometry.location);
    map.setZoom(15);
}
//Build the infowindow content
function setInfoWindow(place,address){
    //get the template for the marker content
    var infowindowContent = document.getElementById('infowindow-content');
    var hiddenForm = $(infowindowContent).children('#GMapVals');
    //assign the values to the hidden form in the marker so that they can be used for searching
    hiddenForm.children('#lat').val(place.geometry.location.lat());
    hiddenForm.children('#lng').val(place.geometry.location.lng());
    hiddenForm.children('#name').val(place.name);
    // put together the content of the marker
    infowindowContent.children['place-icon'].src = place.icon;
    infowindowContent.children['place-name'].textContent = place.name;
    infowindowContent.children['place-address'].textContent = address;
    //init the infowindow
    var infowindow = new google.maps.InfoWindow(); 
    infowindow.setContent(infowindowContent.innerHTML);
    return infowindow;
}
//this is the function attached to the 'use my location' button
function userLocation (){
    //check if geolocation is possible in this browser
    if (navigator.geolocation) {
        //try to get the location
        navigator.geolocation.getCurrentPosition(function(position) {
            var place = {};
            place.geometry = {location: {}};
            place.geometry.location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            //set the marker
            setMarker("Your Location",place);
        }, function() {
            // location is unavailable (possibly due to the user not giving permissoins)
            handleLocationError(true, new google.maps.InfoWindow, map.getCenter());
          });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, new google.maps.InfoWindow, map.getCenter());
    }
}
//handle errors in the HTML5 geolocation
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}   
//Check to see if the number is a lat lon and add it to the place object
function checkLatLon (place){
    var latlon = place.name.split(/[\s,]+/);
    if (latlon.length === 2){
        if (latlon[0].match(latRegex) && latlon[1].match(lonRegex)){
            place.geometry ={};
            //set a new google maps latlng object for consistency with the place object from the searchbar
            place.geometry.location =  new google.maps.LatLng(latlon[0],latlon[1]);
            return place;
        }
    }
    // User entered the name of a Place that was not suggested and
    // pressed the Enter key, or the Place Details request failed.
    window.alert("Please make sure you either enter a valid lat lng or select an option from the list.");
    return false;
}
//build the address string
function buildAddress (addrComps){
    var address = '';
    if (addrComps) {
      address = [
        (addrComps[0] && addrComps[0].short_name || ''),
        (addrComps[1] && addrComps[1].short_name || ''),
        (addrComps[2] && addrComps[2].short_name || '')
      ].join(' ');
    }
    return address;
}