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
  $(newElem).insertBefore('#cventry');
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


 	var allGradesValid = $(".feedback-input2").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 
	
	var avgValid = $(".average").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 

    if ( !allCourseNamesValid) {
		alert("please enter a valid course name");
		return false }
		
    if (!allGradesValid) {
		alert("please enter a grade between 60 and 100");
		return false }
		
	if (!avgValid) {
		alert("please enter a grade average between 60 and 100");
		return false }
		
	return true;
}

var residence = document.getElementById("element2").value;
var select = document.getElementById("element2")

for (var i=1; i<select.length;i++){
	if (select[i].value === residence){
		select.selectedIndex = i;
		}
	}

//make sure that file chosen has a valid extension
var file = document.getElementById('cv');

file.onchange = function(e){
	var bad=false;
	if (this.value.match(/\.([^.]+)$/)==null) {
		bad=true;
	}
	else{
		var ext =  this.value.match(/\.([^.]+)$/)[1];
	    switch(ext){
			case 'pdf':
			case 'doc':
			case 'docx':
			case 'txt':
				break;
			default:
				bad=true;
		}
	}
	if (bad==true){
		alert('Error: Chosen file type is not allowed, allowed types are: *.doc, *.docx, *.pdf, *.txt');
		this.value='';
	}
};
