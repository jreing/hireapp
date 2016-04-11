var newNum = 0;
var elems = 1;
var courses = $("#courses option").map(function () {
    return this.value;
}).get();

function b() {
  var num = this.id.substring(9);
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
  var newElem = $('.cloneme:first').clone().attr('id', 'cloneme' + newNum).attr('class', 'cloneme');
  // manipulate the name/id values of the input inside the new element
  newElem.children().eq(0).val('');
  newElem.children().eq(1).val('');
  newElem.children().eq(2).attr('id', 'buttondel' + newNum).attr('class', 'buttondel');
 
  newElem.children().eq(2)[ 0 ].onclick= b;
 
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
var allValid = $(".feedback-input").filter(function (key, element) {
        var value = $(element).val();
        
        return value !== "" && courses.indexOf(value) < 0;
    }).length === 0;

    if ( !allValid ) {
		alert("invalid course name");
		return false }

	return true;


}

$('.buttondel')[ 0 ].onclick= b;
$('.buttondel').attr('disabled', 'disabled');

