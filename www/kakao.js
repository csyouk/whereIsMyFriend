    var userPosition;
    function getLocation()
    {
      if (navigator.geolocation)
      {
        navigator.geolocation.getCurrentPosition(showPosition,showError);

      }
      else{alert("Geolocation is not supported by this browser.");}
    }
    function showPosition(position)
    {
      userPosition = position;
      console.log(userPosition);
      // x2.innerHTML="Latitude: " + position.coords.latitude +
      // "<br />Longitude: " + position.coords.longitude;
    }
    function showError(error)
    {
        alert(error);
    }
    getLocation();

    Kakao.init('69001b60516dc2437c4272a1b8fa2f89');
    Kakao.Auth.createLoginButton({
      container: '#kakao-login-btn',
      success: function(authObj) {
        Kakao.API.request({
          url: '/v1/user/me',
          success: function(res) {
            res.latitude = userPosition.coords.latitude;
            res.longitude = userPosition.coords.longitude;
            var userInfo = JSON.stringify(res);
            $.ajax({
              url: "/users/"+res.id,
              type:'POST',
              dataType:'JSON',
              data:userInfo,
              success:function(data, status, jqXHR){
                console.log("done");
                window.location.href = "http://" + location.host +"/friends.html"
                // window.location.href = 'whereIsMyFriend.com'
              },
              error:function(jqXHR, status, error){
                console.log(jqXHR);
                console.log(status);
                console.log(error);
              }}
            );
          },
          fail: function(error) {
            alert(JSON.stringify(error))
          }
        });
      },
      fail: function(err) {
        alert(JSON.stringify(err))
      }
    });
