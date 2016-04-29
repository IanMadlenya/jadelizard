var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};

var strategyData = function(options){
        $.ajax({
            url: "/graphdata/",
            method: "GET"
        }).done(options.callback);
    }

// render navbar and strategy data 
$(document).ready(function(){
	render('#_nav', "#navbar_div")({});
	// same as: 
	// var template = $('#_nav').html();
	// var rendered = Mustache.render(template, {});
	// $("#navbar_div").html(rendered);
	render("#_strategy_data", "#data_div")({});
	// make ajax request for demo view here


});









