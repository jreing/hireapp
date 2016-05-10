
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

function validateForm() {
	alert("hi");
	var NoStudentsSelected = $(".checkbox").filter(function (key, element) {
        var value = $(element).checked();   
		alert("var");
		return value
    }).length === 0;

	
    if ( NoStudentsSelected) {
		alert("please select at least one recipient");
		return false }
		

	return true;
}