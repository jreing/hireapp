document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
//function to load toolbar to html page that includes the script
$(function loadtoolbar(){
	$("#includedContent").load("/HelpToolbar/index.html");
});
//window.onunload = function(){}

