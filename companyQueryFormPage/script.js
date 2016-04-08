var newNum = 0;
var elems = 1;
var newNumtwo = 0;
var elemstwo = 1;
alert("Hello! I am an alert box!!");
$('#buttonadd').click(function() {
  elems++;
  newNum = new Number(newNum + 1); // the numeric ID of the new input field being added
  // create the new element via clone(), and manipulate it's ID using newNum value
  //var newElem = $('#cloneme' + (newNum - 1)).clone().attr('id', 'cloneme' + newNum);
  var newElem = $('.cloneme:first').clone().attr('id', 'cloneme' + newNum).attr('class', 'cloneme');
  // manipulate the name/id values of the input inside the new element
  newElem.children().eq(0).val('');
  newElem.children().eq(1).val('');
  newElem.children().eq(2).attr('id', 'buttondel' + newNum).attr('class', 'buttondel');

  // insert the new element after the last "duplicatable" input field
  //$('#cloneme' + (newNum-1)).after(newElem);
  $(newElem).insertBefore('#bysubject');
  // enable the "remove" button
  $('.buttondel').attr('disabled', '');


});

$('.buttondel').click(function() {
  var num = this.id.substring(9);
  elems--;

  $('#cloneme' + num).remove(); // remove the last element

  //if only one element remains, disable the "remove" button
  if (elems == 1)
    $('.buttondel').attr('disabled', 'disabled');
});

$('#buttonaddtwo').click(function() {
  elemstwo++;
  newNumtwo = new Number(newNumtwo + 1); // the numeric ID of the new input field being added
  // create the new element via clone(), and manipulate it's ID using newNum value
  //var newElem = $('#cloneme' + (newNum - 1)).clone().attr('id', 'cloneme' + newNum);
  var newElem = $('.clonemetwo:first').clone().attr('id', 'clonemetwo' + newNumtwo).attr('class', 'clonemetwo');
  // manipulate the name/id values of the input inside the new element
  newElem.children().eq(0).val('');
  newElem.children().eq(1).val('');
  newElem.children().eq(2).attr('id', 'buttondeltwo' + newNumtwo).attr('class', 'buttondeltwo');

  // insert the new element after the last "duplicatable" input field
  //$('#cloneme' + (newNum-1)).after(newElem);
  $(newElem).insertBefore('#avgentry');
  // enable the "remove" button
  $('.buttondeltwo').attr('disabled', '');

});

$('.buttondeltwo').click(function() {
  var num = this.id.substring(12);
  elemstwo--;

  $('#clonemetwo' + num).remove(); // remove the last element

  //if only one element remains, disable the "remove" button
  if (elemstwo == 1)
    $('.buttondeltwo').attr('disabled', 'disabled');
});

$('.buttondeltwo').attr('disabled', 'disabled');
$('.buttondel').attr('disabled', 'disabled');