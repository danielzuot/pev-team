/**
 * Called on the intiial page load.
 */
function init() {
  var map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 12,
    center: new google.maps.LatLng(42.3601, -71.0589),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var path = [
    new google.maps.LatLng(42.351248, -71.082297),
    new google.maps.LatLng(42.3744, -71.1169)
  ];

  var line = new google.maps.Polyline({
    path: path,
    strokeColor: '#ff0000',
    strokeOpacity: 1.0,
    strokeWeight: 3
  });
  line.setMap(map);
}

// Register an event listener to fire once when the page finishes loading.
google.maps.event.addDomListener(window, 'load', init);

$(document).ready(function() {

  $( '#taxi-data' ).submit(function(event) {
      event.preventDefault();
      var pickupFile = $('#pickup-csv-file').val();
      var dropoffFile = $('#dropoff-csv-file').val();
      
      console.log(pickupFile);
      console.log(dropoffFile);

  });
});