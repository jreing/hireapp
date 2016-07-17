document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
notStudent=false
//function to load the correct toobar according to user type
$(function loadtoolbar(){
	//check if user is a logged in student
	$.post("/validateStudent", function(data){
		
		if (data.split("#")[1]=="accepted"){
			$("#includedContent").load("/StudentToolbar/index.html");
		}
		else { //user isn't a student
			//so check if user is a company
			$.post("/validateCompany", function(data2){
				if (data2.split("#")[1]=="accepted"){
					$("#includedContent").load("/CompanyToolbar/index.html");
				}
				else { //user isn't a student and isn't a company
					$("#includedContent").load("/ToFirstPageToolbar/index.html");
				}
			});
		};
	});
});
	
window.onunload = function(){}
