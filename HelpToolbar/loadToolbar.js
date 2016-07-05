document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
$(function loadtoolbar(){
	$("#includedContent").load("/HelpToolbar/index.html");
});
//window.onunload = function(){}

