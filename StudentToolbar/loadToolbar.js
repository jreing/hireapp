document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;
$(function loadtoolbar(){
      $("#includedContent").load("/StudentToolbar/index.html");
	  
    });