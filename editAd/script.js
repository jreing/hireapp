var newNum = $('.cloneme').length -1;
var elems = $('.cloneme').length;


var newNumtwo = $('.clonemetwo').length -1;
var elemstwo = $('.clonemetwo').length;


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

if (elemstwo == 1){
	var inputs = document.getElementsByClassName("buttondeltwo");
	inputs[0].disabled = true;
}

function btwo(id) {
  numtwo = id.substring(12);
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
 
  //newElem.children().eq(2)[ 0 ].onclick= b;
 
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
  //newElemtwo.children().eq(0).val('');
  newElemtwo.children().eq(1).val('');
  newElemtwo.children().eq(2).attr('id', 'buttondeltwo' + newNumtwo).attr('class', 'buttondeltwo');

  //newElemtwo.children().eq(2)[ 0 ].onclick= btwo;
 
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

/*
$('.buttondel')[ 0 ].onclick= b;
$('.buttondel').attr('disabled', 'disabled');
$('.buttondeltwo')[ 0 ].onclick= btwo;
$('.buttondeltwo').attr('disabled', 'disabled');
*/
function setSelect(elem){
	var chValue = document.getElementById(elem).value;
	var select = document.getElementById(elem)
	//alert(elem + " len " + select.length)
	for (var i=1; i<select.length;i++){
		if (select[i].value === chValue){
			select.selectedIndex = i;
			}
		}
	select[0].value = 0
}

setSelect("year")
setSelect("availability")
setSelect("residence")


k=0
ct = "ctype" + k
while(document.getElementById(ct)!=null){
	setSelect(ct)
	k+=1
	ct = "ctype" +k
}



function validateForm() {
 	var gradeWithoutCourse = $(".cloneme").filter(function (key, element) {
        var course = $(element).children().eq(0).val();
		var grade = $(element).children().eq(1).val(); 		
        return grade !== "" && (course === ""|| courses.indexOf(course) < 0);
    }).length !== 0;
	
 	var CourseWithoutGrade = $(".cloneme").filter(function (key, element) {
        var course = $(element).children().eq(0).val();
		var grade = $(element).children().eq(1).val(); 		
        return grade === "" && !(course === ""|| courses.indexOf(course) < 0);
    }).length !== 0;
	
	
 	var gradeWithoutCategory = $(".clonemetwo").filter(function (key, element) {
        var category = $(element).children().eq(0).val();
		var grade = $(element).children().eq(1).val();
		//alert("category, grade are"+(category!=0)+" , "+(grade === ""));
        return category==0 && grade !== "";
    }).length !== 0; 	
	
 	var categoryWithoutGrade = $(".clonemetwo").filter(function (key, element) {
        var category = $(element).children().eq(0).val();
		var grade = $(element).children().eq(1).val();
		//alert("category, grade are"+(category!=0)+" , "+(grade === ""));
        return category!=0 && grade === "";
    }).length !== 0;
	
	var noAverage = $("#avgentry #avg").filter(function (key, element) {
		var avgchk = $(element).val();
        return avgchk === "";
    }).length !== 0;
	
	
	var noJobDescription = $("#note").filter(function (key, element) {
        var desc = $(element).val();
        return desc === "";
    }).length !== 0;
	
	
	var noNameForJob = $("#jobId").filter(function (key, element) {
		var name = $(element).val();
		//alert("AS");
        return name === "";
    }).length !== 0; 

	
    if (gradeWithoutCourse) {
		alert("Exists a grade with a missing course name.\nPlease enter a valid course name");
		return false }
		
    if (CourseWithoutGrade) {
		alert("Exists a course with a missing grade.\nPlease enter a course grade between 60 and 100");
		return false }
	
	if (gradeWithoutCategory) {
		alert("Exists a grade filter without a proper category.\nPlease enter a category for the grade");
		return false } 
		
	if (categoryWithoutGrade) {
		alert("Exists a category filter without a proper grade.\nPlease enter a grade average between 60 and 100 for the category");
		return false } 
		
	if (noAverage) {
		alert("Please enter an average between 60 and 100");
		return false }
		
	if (noNameForJob) {
		alert("Please enter a name for the job");
		return false }
		
	if (noJobDescription) {
		alert("Please enter a description for the job");
		return false }
	
	return true;
}

$(document).ready(function() {
// Tooltip only Text
var msg=".הוספה של אשכול מאפשרת לבצע חיפוש עבור סטודנטים שלמדו קבוצה של קורסים בעלי נושא משותף<br>כך לדוגמה, חיפוש אחר אשכול של אבטחת מידע יחזיר סטודנטים שלמדו לפחות קורס אחד באבטחת מידע<br> ושהממוצע שלהם בקורסים שלקחו בנושא גדול מהממוצע שהוזן בחיפוש"
$('#toolTipThree').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="tooltip"></p>')
        .html(msg)
        .appendTo('body')
        .fadeIn('slow');
}, function() {
        // Hover out code
        $(this).attr('title', $(this).data('tipText'));
        $('.tooltip').remove();
}).mousemove(function(e) {
        var mousex = e.pageX - 730; //Get X coordinates
        var mousey = e.pageY - 10; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
	});
});

$(document).ready(function() {
// Tooltip only Text
var msg=".חלק זה מאפשר לך להוסיף לחיפוש רשימת קורסים עם ציון מינימלי עבור כל קורס <br> .תוצאות החיפוש יכילו רק סטודנטים שלמדו את הקורסים הללו וקיבלו בהם ציון גבוה מהציון שהוזן<br>"
$('#toolTipTwo').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="tooltip"></p>')
        .html(msg)
        .appendTo('body')
        .fadeIn('slow');
}, function() {
        // Hover out code
        $(this).attr('title', $(this).data('tipText'));
        $('.tooltip').remove();
}).mousemove(function(e) {
        var mousex = e.pageX - 680; //Get X coordinates
        var mousey = e.pageY - 10; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
	});
});


$(document).ready(function() {
// Tooltip only Text
var msg="חלק זה מאפשר לחפש ביטויים בקורות חיים שהועלו לאתר <br> .כך למשל הכנסת הביטוי לינוקס תחזיר סטודנטים שהמילה מופיעה בקורות החיים שלהם  <br> .באפשרותך לחפש יותר מביטוי אחד באמצעות הכנסת הביטויים השונים עם רווחים ביניהם"
$('#toolTipOne').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="tooltip"></p>')
        .html(msg)
        .appendTo('body')
        .fadeIn('slow');
}, function() {
        // Hover out code
        $(this).attr('title', $(this).data('tipText'));
        $('.tooltip').remove();
}).mousemove(function(e) {
        var mousex = e.pageX - 630; //Get X coordinates
        var mousey = e.pageY - 10; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
	});
});





