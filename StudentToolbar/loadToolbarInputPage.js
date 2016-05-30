document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
	
$(function loadtoolbar(){
	$.post("/validateStudent", function(data){
		
		if (data.split("#")[1]=="accepted"){
			$("#includedContent").load("/StudentToolbar/indexInputPage.html");
		}
		else {
			document.write("Session timeout");
		}
	});
});
	
	
window.onunload = function(){}
