var form = $("#APIKeyForm");
//bind submittion event to the API checks and save procedure
form.submit(function(event){
  $(".waiting").removeClass("d-none");
  $("#error").addClass("d-none");
  event.preventDefault();
  getPlacesService();
});

function getPlacesService() {
   //load in the places library with the API key submitted, this won't error till we try to use it if the key is wrong
  var key = $("#txtPlacesKey").val();
  loadScript('https://maps.googleapis.com/maps/api/js?key=' +
          key + '&libraries=places', testService);
}

function loadScript(url, callback)
{
    // build the script tag
    var head = document.head;
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    // bind the event to the callback function.
    // two events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;
    // append the script to the head
    head.appendChild(script);
}

function testService() {
    //test the new service once it's loaded in
    //create an instance of the service
    var service = new google.maps.places.PlacesService(document.getElementById("attributions"));
    //set a timeout incase the request fails. as this is async we can't capture a failiure so we have to give it a 
    //reasonable time to complete the task and if that elapses without success conclude that it has failed. There 
    //will be a log in the console however this is handled within the service and as far as i'm aware we dont have
    //access.
    setTimeout(timoutHandler,20000);
    //try the request
    service.findPlaceFromQuery({
        query:"bantham",
        fields: ['name']
    },processResult);
}
  
function processResult(result, serviceStatus){
    // check to see whether our api key has be declined, it will only get this far if it's valid in terms of formatting
    // however it might not  have permissions for the url it's being requested from.
    if (serviceStatus !== "REQUEST_DENIED"){
        //show the attributions as per places legal requirements
        $("#attribution").removeClass("d-none");
        //add the verifyed config to the file and save for future use
        $(".waiting").addClass("d-none");
        $("#success").removeClass("d-none");
        setTimeout(form.submit, 8000);
    } else {
        //if this isn't a valid API key then log the results and display error messages
        console.log(result);
        console.log(serviceStatus);
        $(".waiting").addClass("d-none");
        $("#error").removeClass("d-none");
        setTimeout(reloader,8000);
    }
}

function timoutHandler() {
    //process to handle the response timeout as though it was a denied request
    if($("#success").hasClass("d-none")){
        processResult("null","REQUEST_DENIED");
    }
}

function reloader() {
    //just a way to simplify it's use in the callbacks
    location.reload();
}