document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
$(function loadtoolbar(){
	$("#includedContent").load("/signUpToolbar/index.html");
});
//window.onunload = function(){}

