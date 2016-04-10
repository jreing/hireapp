
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

$(function() {
    //----- OPEN
    $('[data-popup-open]').on('click', function(e)  {
		//alert(this.id);
        var targeted_popup_class = $( ".btn" ).attr('data-popup-open');
        $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
		
 });
 $('[data-popup-open]').click();
 
 $(".popup").fadeOut(2000);
    //----- CLOSE
    $('[data-popup-close]').on('click', function(e)  {
        var targeted_popup_class = jQuery(this).attr('data-popup-close');
        $('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
 
        e.preventDefault();
    });
});


