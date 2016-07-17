document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
//script to load toolbar to the html page that includes this script
$(function loadtoolbar(){
      $("#includedContent").load("/toolbar/index.html");
	  
    });
