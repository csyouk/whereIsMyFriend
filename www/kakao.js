    var userPosition;
    function sendLog(){
      var data = {"user_agent":navigator.userAgent, "path":window.location.pathname};
      console.log(data);
      $.ajax({
        url: "/log",
        type:'POST',
        dataType:'JSON',
        data: JSON.stringify(data),
        success:function(data, status, jqXHR){
          console.log("done");
        },
        error:function(jqXHR, status, error){
          console.log(jqXHR);
          console.log(status);
          console.log(error);
        }}
      );
    }
    function getLocation()
    {
      if (navigator.geolocation) {
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
    sendLog();
    getLocation();

    Kakao.init('69001b60516dc2437c4272a1b8fa2f89');
    Kakao.Auth.createLoginButton({
      container: '#kakao-login-btn',
      success: function(authObj) {
        Kakao.API.request({
          url: '/v1/user/me',
          success: function(res) {
            res.userAgent = navigator.userAgent
            try{
              res.latitude = userPosition.coords.latitude;
              res.longitude = userPosition.coords.longitude;
            } catch(err){
              console.log("error : ", err);
              var userInfo = JSON.stringify(res);
              $.ajax({
                url: "/error",
                type:'POST',
                dataType:'JSON',
                data:userInfo,
                success:function(data, status, jqXHR){
                  console.log("done");
                  window.location.href = "http://" + location.host +"/friends.html"
                },
                error:function(jqXHR, status, error){
                  console.log(jqXHR);
                  console.log(status);
                  console.log(error);
                }}
              );
            }

            var userInfo = JSON.stringify(res);
            // alert("data", res);
            $.ajax({
              url: "/users/"+res.id,
              type:'POST',
              dataType:'JSON',
              data:userInfo,
              success:function(data, status, jqXHR){
                console.log("done");
                window.location.href = "http://" + location.host +"/friends.html"
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
