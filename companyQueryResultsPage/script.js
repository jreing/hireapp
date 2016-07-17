
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

	var NoStudentsSelected = $(".checkbox").filter(function (key, element) {
        var value = $(element)[0].checked;
		return value
    }).length === 0;

	
    if ( NoStudentsSelected) {
		alert("please select at least one recipient");
		return false; }
		

	return true;
}

