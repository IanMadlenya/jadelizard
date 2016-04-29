var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};

$(document).ready(function(){
	render('#_nav', "#navbar_div")({});
	// same as: 
	// var template = $('#_nav').html();
	// var rendered = Mustache.render(template, {});
	// $("#navbar_div").html(rendered);
});









