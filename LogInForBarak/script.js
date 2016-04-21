//document.getElementById("login").style.width = document.getElementById("employ_button").style.width;
var isStudent=undefined;

function ForceLogin() {
	console.log('forced');
	 if (isStudent==true){
		window.location="/studenthandler";
	}
	else{
		window.location="/companyQueryFormPage";
	}
} 

function onLogin(googleUser){
	console.log('start');
	//alert("Started onLogin")
	console.log('Logging In');
	//var id_token = googleUser.getAuthResponse().id_token;
	var profile = googleUser.getBasicProfile();
	console.log(profile);
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
	console.log('mark');
	xhr.open('POST', '/tokenSignIn');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	xhr.send('user_id=' + profile.Ka + "&email=" + email + "&isStudent=" + isStudent);
	
	document.getElementById("employ_button").disabled=false;
	
	console.log(xhr.readyState);
	//alert("Ending onLogin");
	setTimeout(function() {ForceLogin()}, 1000);
	//ForceLogin();
}

function onFailure(error) {
  console.log(error);
  location.reload();
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
