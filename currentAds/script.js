
$(document).ready(function() {
// Tooltip only Text
var msg=".מודעות שמהן עדיין לא שולחת הודעה לסטודנטים מופיעות בצבע כחול <br> .מודעות שמהן כבר שלחת הודעה מופיעות בירוק"
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
        var mousex = e.pageX - 505; //Get X coordinates
        var mousey = e.pageY - 10; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
	});
});




