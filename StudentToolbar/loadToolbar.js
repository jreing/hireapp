document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;

//check if student is valid and load toolbar if she's valid
//otherwise display error page (=data sent from server)
$(function loadtoolbar(){
	$.post("/validateStudent", function(data){
		
		if (data.split("#")[1]=="accepted"){
			$("#includedContent").load("/StudentToolbar/index.html");
		}
		else {
			document.write(data);
		}
	});
});
	
	
window.onunload = function(){}
