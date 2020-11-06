/*Key Functions
 ========================================================*/
(function($){ //create closure so we can safely use $ as alias for jQuery
$(document).ready(function(){
// initialise plugin
	var example = $('#example, #example1, #example2').superfish({
	//add options here if required
	});
	// buttons to demonstrate Superfish's public methods
	$('.destroy').on('click', function(){
	example.superfish('destroy');
	});
	$('.init').on('click', function(){
	example.superfish();
	});
	$('.open').on('click', function(){
	example.children('li:first').superfish('show');
	});
	$('.close').on('click', function(){
	example.children('li:first').superfish('hide');
	});
});
})(jQuery);




/*  myCarousel1
========================================================*/
jQuery(document).ready(function($) {

$('#myCarousel1').carousel({
//interval: 5000;
interval:false
});

$('#carousel-text').html($('#slide-content-0').html());

//Handles the carousel thumbnails
$('[id^=carousel-selector-]').click( function(){
var id = this.id.substr(this.id.lastIndexOf("-") + 1);
var id = parseInt(id);
$('#myCarousel1').carousel(id);
});


// When the carousel slides, auto update the text
$('#myCarousel1').on('slid.bs.carousel', function (e) {
var id = $('.item.active').data('slide-number');
$('#carousel-text').html($('#slide-content-'+id).html());
});
});



/* imagelightbox.min.JS
 ========================================================*/



/* Focus .JS
 ========================================================*/

/* Advance Search */

function load_as_lightbox() {
        var DocumentHeight = $(document).height();
        $('.as_lightbox_wrapper').css('height', DocumentHeight); // Set document height for As_Lightbox wrapper
    }
    function ShowLightBox(DivId) {
        $('.as_lightbox_wrapper').show(); // Show the wrapper
        $('#' + DivId + '').show('slow'); // Show the Lightbox div, you can use another jQuery view functions such as fadeIn, fadeToggle for animations
    }
    function HideLightBox(DivId) {
        $('.as_lightbox_wrapper').hide('slow'); // Hide the As_Lightbox wrapper
        $('#' + DivId + '').hide(); // Hide the div
    }
    $(document).ready(function () {
        load_as_lightbox(); // call this function after document loads
        $('#Show_Lightbox').click(function () {
            ShowLightBox('Simple_Lightbox'); // call the As_Lightbox show function
            return false;
        });
        $('#as_lightbox_close').click(function () {
            HideLightBox('Simple_Lightbox'); // call the As_Lightbox close function
            return false;
        });
    });

/* Flex Slider Bottom .JS
 ========================================================*/

	$(document).ready(function() {
    
    $("#flexiselDemo3").flexisel({
        visibleItems: 5,
        itemsToScroll: 1,         
        autoPlay: {
            enable: true,
            interval: 3000,
            pauseOnHover: true
        }        
    });
	
	/* $('#playButton').click(function () {
    $('#flexiselDemo3').flexisel('play');
	});
	$('#pauseButton').click(function () {
		$('#flexiselDemo3').flexisel('pause');
	}); */
        
    
});


/* Alert Logo */
function confirm_alert(node) {
    return confirm("This is an external link.Do you want to continue.");
}




