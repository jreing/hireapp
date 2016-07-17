document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
// js code to load toolbar to page that includes  this script
$(function loadtoolbar(){
	$("#includedContent").load("/ToFirstPageToolbar/index.html");
});
//window.onunload = function(){}

