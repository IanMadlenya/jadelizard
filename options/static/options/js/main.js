var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};

// Sends JSON data to C3 to be graphed
var strategyData = function(options){
		$.ajax({
			url: "/options/graphdata",
			method: "GET",
			dataType: "json",
			success: function(data){
				data = JSON.parse(data);
				d3_chart.load({
					json: data,
					keys: {
						value: ['price_range', 'strategy_profit']
					},
				});
			}
	});
};

$(document).ready(function(){
	// display navbar
	render('#_nav', "#navbar_div")({});
	render("#_strategy_data", "#data_div")({});
	// run function to send strategy data to C3
	strategyData()

	// display strategy modal on click 
	$('#stgy_btn').on('click','a', function(event){
		$('#stgy_modal').modal('toggle')
	});

	// send strategy form data to views on submit
	$('#stgy_form').on('submit', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/stgyform",
			method: "POST",
			'data':data,
			'success':function(data){
				console.log(data)
			}
		});

	$('#stgy_modal').on('hidden.bs.modal', function () {
    $(this).find("input,textarea,select").val('').end();
	});

	$('#stgy_modal').modal('hide')

	});

	// display strategy legs modal on click
	$('#legs_btn').on('click','a', function(event){
		$('#legs_modal').modal('toggle')
	});

	// send legs form data to views on submit
	$('#legs_form').on('submit', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/legsform",
			method: "POST",
			'data':data,
			'success':function(data){
				console.log(data)
			}
		});

		$('#legs_modal').on('hidden.bs.modal', function () {
    		$(this).find("input,textarea,select").val('').end();
		});

		$('#legs_modal').modal('hide')

	});

})






















