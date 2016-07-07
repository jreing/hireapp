
function validateForm() {



	var mailAdd=document.getElementById("mailAdd").value;

	if (mailAdd.length>70 || !mailAdd.includes("@") || mailAdd.includes(" ")){

		alert("please enter a valid email address");
		return false;
	}

	return true;


}

