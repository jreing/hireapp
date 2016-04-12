//document.getElementById("login").style.width = document.getElementById("employ_button").style.width;
var isStudent;

function ForceLogin() {
			 if (isStudent){
						window.location="studentInputPage/index.html";
					}
					else{
						window.location="companyQueryFormPage/index.html";
					}
			} 


          function onSignIn(googleUser) {
            var profile = googleUser.getBasicProfile();
            console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
            console.log('Name: ' + profile.getName());
            console.log('Image URL: ' + profile.getImageUrl());
			var email = profile.getEmail();
            console.log('Email: ' + email);
            //window.location="chooseEmployOrStudentPage/index.html";
			document.getElementById("employ_button").disabled=false;
					 if (email.endsWith('tau.ac.il')){
						isStudent=true;
					}
					else{
						isStudent=false;
					}
			} 
			
