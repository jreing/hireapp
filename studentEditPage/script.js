var newNum = $('.cloneme').length -1;
var elems = $('.cloneme').length;


var courses = $("#courses option").map(function () {
    return this.value;
}).get();

if (elems == 1){
	var inputs = document.getElementsByClassName("buttondel");
	inputs[0].disabled = true;
}

function b(id) {
  
  num = id.substring(9);
  elems--;

  $('#cloneme' + num).remove(); // remove the correct element

  //if only one element remains, disable the "remove" button
  if (elems == 1) {
	    var inputs = document.getElementsByClassName("buttondel");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = true;
	}
  }
}




$('#buttonadd').click(function ab() {
  elems++;
  newNum = new Number(newNum + 1); // the numeric ID of the new input field being added
  // create the new element via clone(), and manipulate it's ID using newNum value
  //var newElem = $('#cloneme' + (newNum - 1)).clone().attr('id', 'cloneme' + newNum);
  var newElem = $('.cloneme:first').clone().attr('id', 'cloneme' + newNum).attr('class', 'cloneme')
  // manipulate the name/id values of the input inside the new element
  newElem.children().eq(0).val('');
  newElem.children().eq(1).val('');
  newElem.children().eq(2).attr('id', 'buttondel' + newNum).attr('class', 'buttondel');
 
 
  // insert the new element after the last "duplicatable" input field
  //$('#cloneme' + (newNum-1)).after(newElem);
  $(newElem).insertBefore('#avgEntry');
  // enable the "remove" button
  //$('.buttondel').attr('disabled', '');
  var inputs = document.getElementsByClassName("buttondel");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = false;
	}


});

//$('.buttondel').click(function b() {
//	alert("calle buttondel");
  //var num = this.id.substring(9);
  //elems--;

 // $('#cloneme' + num).remove(); // remove the last element

  //if only one element remains, disable the "remove" button
  //if (elems == 1)
   // $('.buttondel').attr('disabled', 'disabled');
//});
function validateForm() {
	
	var allCourseNamesValid = $(".feedback-input").filter(function (key, element) {
        var value = $(element).val();   
        return value === "" || courses.indexOf(value) < 0;
    }).length === 0;

	var git=document.getElementById("git").value;
	
 	var allGradesValid = $(".feedback-input2").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 
	
	var avgValid = $(".average").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 
	
	var file = document.getElementById('cv');
	var iscvvalid=true;

	if (file.value!==""){
		if (file.value.match(/\.([^.]+)$/)==null) {
			iscvvalid=false;
		}
		else{
			var ext =  file.value.match(/\.([^.]+)$/)[1];
			switch(ext){
				case 'pdf':
					break;
				default:
					iscvvalid=false;
			}
		}
	}
	
    if ( !allCourseNamesValid) {
		alert("please enter a valid course name");
		return false }
		
    if (!allGradesValid) {
		alert("please enter a grade between 60 and 100");
		return false }
		
	if (!avgValid) {
		alert("please enter a grade average between 60 and 100");
		return false }
	
	if (git!="" && git.substring(0,"www.github.com/".length) !== "www.github.com/"){
		alert("please enter github.com/(YOUR ACCOUNT)");
		return false;
	}
	
	if (!iscvvalid){
		alert('Error: Chosen file type is not allowed, please insert a pdf file');
		return false
	}	
	
	return true;
}

function setSelect(elem){

	var residence = document.getElementById(elem).value;
	
	var select = document.getElementById(elem)
	//alert(elem + " len " + select.length)
	for (var i=1; i<select.length;i++){
		if (select[i].value === residence){
			select.selectedIndex = i;
			}
		}		
}
	
setSelect("residence")
setSelect("availability")
setSelect("year")

function delClick(){
	if (confirm("האם אתה בטוח שברצונך למחוק את הפרופיל שלך?")== true){
		location.href = 'deleteStudent'
	}
	else{
		return
	}
		
}





	