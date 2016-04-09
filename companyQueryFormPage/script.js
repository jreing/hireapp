var newNum = 0;
var elems = 1;
var newNumtwo = 0;
var elemstwo = 1;

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

function btwo() {
  var numtwo = this.id.substring(12);
  elemstwo--;

  $('#clonemetwo' + numtwo).remove(); // remove the correct element

  //if only one element remains, disable the "remove" button
  if (elemstwo == 1) {
	    var inputs = document.getElementsByClassName("buttondeltwo");
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
  $(newElem).insertBefore('#bysubject');
  // enable the "remove" button
  //$('.buttondel').attr('disabled', '');
  var inputs = document.getElementsByClassName("buttondel");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = false;
	}


});

$('#buttonaddtwo').click(function abtwo() {
  elemstwo++;
  newNumtwo = new Number(newNumtwo + 1); // the numeric ID of the new input field being added
  // create the new element via clone(), and manipulate it's ID using newNum value
  //var newElem = $('#cloneme' + (newNum - 1)).clone().attr('id', 'cloneme' + newNum);
  var newElemtwo = $('.clonemetwo:first').clone().attr('id', 'clonemetwo' + newNumtwo).attr('class', 'clonemetwo');
  // manipulate the name/id values of the input inside the new element
  newElemtwo.children().eq(0).val('');
  newElemtwo.children().eq(1).val('');
  newElemtwo.children().eq(2).attr('id', 'buttondeltwo' + newNumtwo).attr('class', 'buttondeltwo');
 
  newElemtwo.children().eq(2)[ 0 ].onclick= btwo;
 
  // insert the new element after the last "duplicatable" input field
  //$('#cloneme' + (newNum-1)).after(newElem);
  $(newElemtwo).insertBefore('#avgentry');
  // enable the "remove" button
  //$('.buttondel').attr('disabled', '');
  var inputs = document.getElementsByClassName("buttondeltwo");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = false;
	}


});



$('.buttondel')[ 0 ].onclick= b;
$('.buttondel').attr('disabled', 'disabled');
$('.buttondeltwo')[ 0 ].onclick= btwo;
$('.buttondeltwo').attr('disabled', 'disabled');
