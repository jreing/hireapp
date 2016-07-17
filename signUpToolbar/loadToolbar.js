document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
//add toolbar html to the page that included this script
$(function loadtoolbar(){
	$("#includedContent").load("/signUpToolbar/index.html");
});
//window.onunload = function(){}

