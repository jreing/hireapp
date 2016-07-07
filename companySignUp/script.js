
function validateForm() {



	var mailAdd=document.getElementById("mailAdd").value;

	var role=document.getElementById("role").value;

	var compName=document.getElementById("compName").value;


	if ((role.length==0) || (compName.length==0) || (mailAdd.length==0)){
		alert("please fill the entire 3 fields");
		return false;
	}



	if (mailAdd.length>70 || !mailAdd.includes("@") || mailAdd.includes(" ") || mailAdd.indexOf("@")!= mailAdd.lastIndexOf("@")|| mailAdd.includes("..")){

		alert("please enter a valid email address");
		return false;
	}

	return true;


}

