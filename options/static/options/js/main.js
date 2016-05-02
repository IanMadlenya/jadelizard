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
	// render navbar
	render('#_nav', "#navbar_div")({});
	render("#_strategy_data", "#data_div")({});
	// run function to send strategy data to C3
	strategyData()

	$('#stgy_btn').on('click','a', function(event){
		$('#stgy_modal').modal(options)
		$('#stgy_modal').modal('show')

	});

	$('#stgy_form').on('submit', function(event){
		var data = $(this).serialize();
		$.ajax({
			url: "/options/stgyform",
			method: "POST",
			'data':data,
			'success':function(data){
				console.log(data)
			}
		});
	})
});



















