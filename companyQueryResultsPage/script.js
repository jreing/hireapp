
// Listen for click on toggle checkbox
$('#select-all').click(function(event) {
  if (this.checked) {
    // Iterate each checkbox
    $(':checkbox').each(function() {
      this.checked = true;
    });
  }
  if (!this.checked) {
    // Iterate each checkbox
    $(':checkbox').each(function() {
      this.checked = false;
    });
  }
});
//validate form before submission, alert message if input is bad
function validateForm() {

  var companyName=document.getElementById("companyName").value;

  var companyMail=document.getElementById("companyMail").value;

  var jobName=document.getElementById("jobName").value;

  var jobDescription=document.getElementById("jobDescription").value;

	var NoStudentsSelected = $(".checkbox").filter(function (key, element) {
        var value = $(element)[0].checked;
		return value
  }).length === 0;

  if ( NoStudentsSelected) {
		alert("please select at least one recipient");
		return false; }

  if (companyName.length==0){
      alert("please enter a company name");
      return false;
    }

  if ((companyMail.length==0)||companyMail.length>70 || !companyMail.includes("@") || companyMail.includes(" ") || companyMail.indexOf("@")!= companyMail.lastIndexOf("@")||companyMail.includes("..")){
      alert("please enter a valid company email");
      return false;
    }

  if (jobName.length==0){
      alert("please enter a job name");
      return false;
    }

  if (jobDescription.length==0){
      alert("please enter a job description");
      return false;
    }

  return true;
}

$(document).ready(function() {
// Tooltip only Text
var msg=" .הסטודנטים בתוצאות החיפוש מופיעים בצבעים <br> .כחול עבור סטודנטים שעדיין לא שלחת להם הודעה וירוק עבור סטודנטים שכן"
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
        var mousex = e.pageX - 560; //Get X coordinates
        var mousey = e.pageY - 10; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
	});
});
