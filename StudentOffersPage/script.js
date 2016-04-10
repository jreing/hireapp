$(".button").click(function() { 
	var num = this.id.substring(6);
    $(('#extra'+num)).toggle('display');
	
	str=$(('#button'+num)).text();
	if (str == "הצג פרטים")
		str="הסתר פרטים";
	else
		str="הצג פרטים";
	$(('#button'+num)).text(str);
});

$('.form-extra').hide();
$('#empty').hide();
var count = $("#scroll").children().length;
if (count == 0) {
	$('#scroll').hide();
	$('#empty').show();

}


