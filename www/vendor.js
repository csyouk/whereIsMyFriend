function sendLog(){
  $.ajax({
    url: "/log",
    type:'POST',
    dataType:'JSON',
    data:JSON.stringify({"user_agent":navigator.userAgent, "path":window.location.pathname}),
    success:function(data, status, jqXHR){
      console.log("done");
      // window.location.href = 'whereIsMyFriend.com'
    },
    error:function(jqXHR, status, error){
      console.log(jqXHR);
      console.log(status);
      console.log(error);
    }}
  );
}


String.prototype.interpolate = function (o) {
  return this.replace(/{([^{}]*)}/g,
  function (a, b) {
    var r = o[b];
    return typeof r === 'string' || typeof r === 'number' ? r : a;
  }
);
};

function initialize() {

  var initLocation = new google.maps.LatLng(37.6669031,127.1187065);
  var mapOptions = {
    zoom: 8,
    center: initLocation,
    mapTypeControl:false
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  $.ajax({
    url: "http://" + location.host +'/users',
    type:'GET',
    dataType:'JSON',
    success:function(data, status, jqXHR){
      console.log("done");
      console.log(data);
      console.log(status);
      console.log(jqXHR);

      var users = data.result;
      for (var i = 0; i < users.length; i++) {
        users[i];
        setInfoWindows(map, users[i]);
      };

    },
    error:function(jqXHR, status, error){
      console.log(jqXHR);
      console.log(status);
      console.log(error);
    }
  });
}

function setInfoWindows(map, user){
  console.log("user ", user);
  var userLocation = new google.maps.LatLng(user.latitude, user.longitude);

  var contentString =
  '<div id="iw-container">' +
  '<div class="iw-title">{name}</div>'.interpolate({name:user.nickname}) +
  '<div class="iw-content">' +
  "<img class='round' src='{imgSrc}' />".interpolate({imgSrc:user.thumbnail_image}) +
  '</div>' +
  '<div class="iw-bottom-gradient"></div>' +
  '</div>';


  var infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 300
  });

  marker = new CustomMarker(
    userLocation,
    map,
    {
      marker_id: user.kakao_id
    }
  );

  google.maps.event.addListener(marker, 'click', function(){ infoWindow.open(map, marker) });

  infoWindow.open(map, marker);

  google.maps.event.addListener(infoWindow, 'domready', function() {

    // Reference to the DIV that wraps the bottom of infowindow
    var iwOuter = $('.gm-style-iw');

    /* Since this div is in a position prior to .gm-div style-iw.
    * We use jQuery and create a iwBackground variable,
    * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
    */
    var iwBackground = iwOuter.prev();

    // Removes background shadow DIV
    iwBackground.children(':nth-child(2)').css({'display' : 'none'});

    // Removes white background DIV
    iwBackground.children(':nth-child(4)').css({'display' : 'none'});

    // Moves the infowindow 115px to the right.
    iwOuter.parent().parent().css({left: '0px'});

    // Moves the shadow of the arrow 76px to the left margin.
    iwBackground.children(':nth-child(1)').attr('style', function(i,s){ return s + 'left: 0px !important;'});

    // Moves the arrow 76px to the left margin.
    iwBackground.children(':nth-child(3)').attr('style', function(i,s){ return s + 'left: 0px !important;'});

    // Changes the desired tail shadow color.
    iwBackground.children(':nth-child(3)').find('div').children().css({'box-shadow': 'rgba(72, 181, 233, 0.6) 0px 1px 6px', 'z-index' : '1'});

    // Reference to the div that groups the close button elements.
    var iwCloseBtn = iwOuter.next();

    // Apply the desired effect to the close button
    iwCloseBtn.css({opacity: '1', right: '40px', top: '3px', border: '7px solid #48b5e9', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9'});

    // If the content of infowindow not exceed the set maximum height, then the gradient is removed.
    if($('.iw-content').height() < 140){
      $('.iw-bottom-gradient').css({display: 'none'});
    }

    // The API automatically applies 0.7 opacity to the button after the mouseout event. This function reverses this event to the desired value.
    iwCloseBtn.mouseout(function(){
      $(this).css({opacity: '1'});
    });
  });
}
sendLog()
google.maps.event.addDomListener(window, 'load', initialize);
