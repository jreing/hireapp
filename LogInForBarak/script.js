//document.getElementById("login").style.width = document.getElementById("employ_button").style.width;
var isStudent=undefined;

function ForceLogin() {
	//alert("Started ForceLogin")
	 if (isStudent==true){
		window.location="/studenthandler";
	}
	else{
		window.location="/companyQueryFormPage/index.html";
	}
} 

function onLogin(googleUser){
	//alert("Started onLogin")
	console.log('Logging In');
	var id_token = googleUser.getAuthResponse().id_token;
	var profile = googleUser.getBasicProfile();
	console.log('idToken: ' + id_token);
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail()); 
	var email = profile.getEmail();
	if (email.endsWith('tau.ac.il')){
		isStudent=true;
		}
	else{
		isStudent=false;
	}
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/tokenSignIn');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onload = function() {
		console.log('Signed in as: ' + xhr.responseText);

	};
	xhr.send('idtoken=' + id_token ) ;
	//document.getElementById("employ_button").disabled=false;
	ForceLogin();
	}
