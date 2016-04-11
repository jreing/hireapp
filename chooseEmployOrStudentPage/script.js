//$.getScript("https://apis.google.com/js/platform.js")
function onSignIn(googleUser){
	var id_token = googleUser.getAuthResponse().id_token;
	var profile = googleUser.getBasicProfile();
	console.log('idToken: ' + id_token);
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail()); 
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/tokenSignIn');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onload = function() {
		console.log('Signed in as: ' + xhr.responseText);
		window.location="chooseEmployOrStudentPage/index.html";
	};
	xhr.send('idtoken=' + id_token) ;}
 	//function signOut() 
	//var auth2 = gapi.auth2.getAuthInstance();
	//auth2.signOut().then(function () {
	//	console.log('User signed out.');
	//		});

