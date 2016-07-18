var isStudent=undefined;

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

//loads the appropriate page depending on type of user
function ForceLogin() {
	while (getCookie("id")==""){
	}
	if (isStudent==true){
		window.location="/studenthandler";
	}
	else{
		window.location="/createAd";
	}
} 



function onLogin(googleUser){

	console.log('Logging In');

	//make sure cookie (and love) don't last long
	var date = new Date();
    date.setTime(date.getTime()+(2*60*60*1000));
	var expires = "; expires="+date.toGMTString();
	document.cookie="expires=" +expires ;

	//get user profile
	var profile = googleUser.getBasicProfile();
	var user_id=profile.Ka;
	
	//console.log('idToken: ' + id_token);
	//console.log('Name: ' + profile.getName());
	//console.log('Image URL: ' + profile.getImageUrl());
	//console.log('Email: ' + profile.getEmail()); 

	//client side check if user is student or company (server side)
	var email = profile.getEmail();
	if (email.endsWith('tau.ac.il')){
		isStudent=true;
		}
	else{
		isStudent=false;
	}

	//send HTTP request to server for logging in to app
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/tokenSignIn');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.send('user_id=' + profile.Ka + "&email=" + email + "&isStudent=" + isStudent);
	
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			if (xhr.responseText!=""){ //bad response
				window.location="/unauthorized"
			}	
			else {		//good response
				setTimeout(ForceLogin, 1000);
			}
		}
	}
}

function onFailure(error) {
  console.log(error);
  location.reload();
}

//create google button- works only when adblock is not on

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
