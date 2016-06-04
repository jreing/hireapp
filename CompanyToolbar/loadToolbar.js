document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;

$(function loadtoolbar(){
	$.post("/validateCompany", function(data){	
		if (data.split("#")[1]=="accepted"){
			$("#includedContent").load("/CompanyToolbar/index.html");
		}
		else {
			document.write("Session timeout");
		}
	});
});
	
window.onunload = function(){}
