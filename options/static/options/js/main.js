var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};

var demoCallback = function demoCallback(data){
	var prices = data.data.map(function(item){
		return item[0];
	});
	var strategyData = data.data.map(function(item){
		return item[1];
	});
	
};

$(document).ready(function(){
	render('#_nav', "#navbar_div")({});
	// same as: 
	// var template = $('#_nav').html();
	// var rendered = Mustache.render(template, {});
	// $("#navbar_div").html(rendered);
	render("#_strategy_data", "#data_div")({});
	// make ajax request for demo view here


});









