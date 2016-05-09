//document.getElementById("login").style.width = document.getElementById("employ_button").style.width;
var isStudent=undefined;

function ForceLogin() {
	 if (isStudent==true){
		window.location="/studenthandler";
	}
	else{
		window.location="/companyQueryFormPage";
	}
} 

function onLogin(googleUser){
	//alert("Started onLogin")
	console.log('Logging In');
	//var id_token = googleUser.getAuthResponse().id_token;
	
	//make sure cookie (and love) don't last long
	var date = new Date();
    date.setTime(date.getTime()+(2*60*60*1000));
	var expires = "; expires="+date.toGMTString();
	document.cookie="expires=" +expires ;
	
	var profile = googleUser.getBasicProfile();
	//console.log(profile);
	var user_id=profile.Ka;
	
	//console.log('idToken: ' + id_token);
	//console.log('Name: ' + profile.getName());
	//console.log('Image URL: ' + profile.getImageUrl());
	//console.log('Email: ' + profile.getEmail()); 
	var email = profile.getEmail();
	if (email.endsWith('tau.ac.il')){
		isStudent=true;
		}
	else{
		isStudent=false;
	}

	var xhr = new XMLHttpRequest();
	//alert("Started on Login")
	//console.log('mark');
	xhr.open('POST', '/tokenSignIn');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	xhr.send('user_id=' + profile.Ka + "&email=" + email + "&isStudent=" + isStudent);
	
	document.getElementById("employ_button").disabled=false;
	
	//console.log(xhr.readyState);
	//alert("Ending onLogin");
	setTimeout(function() {ForceLogin()}, 1000);
	//ForceLogin();
}

function onFailure(error) {
  console.log(error);
  location.reload();
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
} 

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
	// var token = gapi.auth.getToken();
	// alert(token)
	// if (token) {
	// var accessToken = gapi.auth.getToken().access_token;
	// if (accessToken) {
    // // make http get request towards: 'https://accounts.google.com/o/oauth2/revoke?token=' + accessToken
    // // In angular you can do it like this:
    // // $http({
    // //   method: 'GET',
    // //   url: 'https://accounts.google.com/o/oauth2/revoke?token=' + accessToken
    // // });
	  // }
	// }
	//gapi.auth.setToken(null);
	//gapi.auth.signOut();
	auth2.signOut();
	document.cookie = "expires=Thu, 01 Jan 1970 00:00:00 UTC";
	
	document.location="/StudentLogout"
	
	
  }
  

function renderButton() {
  gapi.signin2.render('my-signin2', {
	'scope': 'profile email',
	'width': 240,
	'height': 50,
	'longtitle': true,
	'theme': 'dark',
	'onsuccess': onLogin,
	'onfailure': onFailure
  });
}
