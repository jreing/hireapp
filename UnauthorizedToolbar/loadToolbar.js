document.body.innerHTML = '<div id="includedContent"></div>'+document.body.innerHTML;

$("#includedContent").load("/UnauthorizedToolbar/index.html");

window.onunload = function(){}

