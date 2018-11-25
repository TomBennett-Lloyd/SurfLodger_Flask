/* global google, map */
//global object to hold main html elements
var htmlElements = {};
var circles = [];
//color map for star ratings, to be used on markers
var starCols = ['#cc6699','#ff6666','#ffcc66','#ffff00','#99ff33','#33cc33'];
// global object to hold search settings incase we want these to be configurable in the future
var settings = {
    type : ['lodging'],
    keyword : ['surf'],
    radius : 1000,
    fields : ['opening_hours','website','place_id']
};
//set values for global variables once the document has loaded
$(document).ready(function(){
    $("#btnMapKey").click();
    htmlElements = {
        resultHolder : $(".templateResult > .resultItem > .card-body"),
        listCont : $(".results"),
        waitingDiv : $(".waitingDiv").html(),
        list : $(".results > ul"),
        newListHTML : ""
    };
    //initialise the settings menu with the default values
    $(".setting").each(function(){
        $(this).val(settings[$(this).attr("name")]);
    });
    //bind the change event to update the settings when the form is changed
    $(".setting").change(function (){
        var val = $(this).val();
        //the keyword is a free text option however there can be mutiple words so we need to split into array
        if ($(this).attr("name") === "keyword"){
            val= val.split(/[\s,]+/);
        }
        settings[$(this).attr("name")] = val;
    });
});
//This is the function used when a user clicks on the find accomodation popup on the map
function getPlaces(location){
    //set the waiting div in the list and show the list pane
    htmlElements.list.html(htmlElements.waitingDiv);
    htmlElements.listCont.removeClass("d-none");
    $("#map").addClass("col-sm-8");
    //get the data from the hidden form in the infowindow
    var dataIn = $(location).parent().children(".GMapVals").serializeArray();
    //build and proccess the request
    var location = { 
        lat: parseFloat(dataIn[0].value) , 
        lng: parseFloat(dataIn[1].value)
    };
    var request = {location: location,
            radius: settings.radius,
            type: settings.type,
            keyword:settings.keyword
     };
    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, nearbyCallback);
}
//handle the response from the nearby request
function nearbyCallback(results, status) {
   //if the call was successful
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    htmlElements.newListHTML = "";
    //remove old circles from map
    $(circles).each(function(){
        this.setMap(null);
    });
    circles = [];
    //go through the results
    for (var i = 0; i < results.length; i++) {
        var place = results[i];
        setPlaceMarker (place);//make the marker on the map
        htmlElements.resultHolder.children(".card-title").text(place.name);//Set the name for the list item
        
         //set the element's id to equal the place id to enable linking between elements and searching
        $(".templateResult > li").attr("id",place.place_id);
        
        setStars (place.rating);//set the star rating
        getDetails (place.place_id); //get the rest of the details
        htmlElements.newListHTML += $(".templateResult").html(); //add the new template to the list
    }
    //set the id of the template item back to nothing to avoid duplicate id's
    $(".templateResult > li").attr("id","");
    htmlElements.list.html(htmlElements.newListHTML);//render the new list
  }
  else 
  {
      //something went wrong, let the user know
      htmlElements.list.html("<h1 class='mt-4'>"+status+"</h1>");
  }
}
//handle the responce from the details request
function detailsCallback (place, status) {
    //if the request was successful then populate the remaining fields of the list
    if (status === google.maps.places.PlacesServiceStatus.OK) {
       //set the result item in the list using the place_id
      var resultHolder = $("#"+place.place_id+" > .card-body");
      //set the href for the link or disable it
       var btnLink = resultHolder.children("a");
      place.website ? btnLink.attr('href',place.website) : btnLink.addClass("disabled");
      //set the value of the opening hours if available
      var oHrs = place.opening_hours;
      if (oHrs && oHrs.weekday_text){
          resultHolder.children(".card-text").html(formatOpeningHours (oHrs.weekday_text));
      } else {
          resultHolder.children(".card-text").html("No opening hours available");
      }
    } else {
        //log the reason for the unsuccessful request
        console.log("request was unsuccessfull, reason:" + status);
    }
}
//process opening hours if available
function formatOpeningHours (weekdaytext) {
    //place the opening hours on separate lines
    var text = "Opening hours: </br>";
    $.each(weekdaytext, function(key,value){
        text+=value +"</br>";
    });
    return text;
}
//set marker for a place with the shading depending on open now, and color depending on rating.
function setPlaceMarker (place){
    var marker = new google.maps.Circle({
    strokeColor: starCols[Math.round(place.rating)],//set the outline color based on the rating
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: starCols[Math.round(place.rating)],//set the color based on the rating
    fillOpacity: place.opening_hours ? (place.opening_hours.open_now ? 0.7:0.3) : 0.5,//set the opacity based on open now
    map: map,
    center: place.geometry.location,
    radius: 50,//chosen as worked well with the small number of points that the search resulted in
    // would need to be smaller if there were more results
    customData:place.place_id//important, this is how the circle is related to list
  });
  //bring the marker forward to enable clicking
  marker.setOptions({zIndex:10});
  //bind the click event handler
  marker.addListener('click', function() {
      //un-highlight any currently selected items in list
      htmlElements.list.children(".active").removeClass("active");
      $("#"+this.customData).addClass("active");
      //make sure it's in view
      document.getElementById(this.customData).scrollIntoView();
  });
  //add reference to the global list
  circles.push(marker);
}
//set star rating
function setStars (rating){
    //set the star rating
    var stars = htmlElements.resultHolder.children(".card-subtitle").children("span");
    for (var c = 0; c < 6; c++){
        //fill the stars until the rating then empty (to overwrite the previous content of template)
        c < Math.round(rating) ? $(stars[c]).addClass("checked") : $(stars[c]).removeClass("checked");
    }
}
//details request
function getDetails (placeId) {
    //build request from place id and fields from the global settings
    var request = {
        placeId: placeId,
        fields: settings. fields
    };
    //process request
    service = new google.maps.places.PlacesService(map);
    service.getDetails(request, detailsCallback);
}

