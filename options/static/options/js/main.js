var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};

// Sends JSON data to C3 for graphing
var graphData = function(options){
		$.ajax({
			url: "/options/graphdata",
			method: "GET",
			dataType: "json",
			success: function(data){
				var S0 = data.S0;
				var data = JSON.parse(data.data);
				d3_chart.load({
					json: data,
					keys: {
						value: ['price_range', 'strategy_profit']
					},
				});
				d3_chart.xgrids([{value: S0, text: 'S0'},])
			},	
			statusCode: {
				412: function() {
					$('#no_strategy_modal').modal('toggle')
				},
				422: function() {
					$('#empty_modal').modal('toggle')
				},
			},
	});
};

var unloadData = function(){
	d3_chart.unload({
		ids: ['price_range','strategy_profit']
	});
	d3_chart.xgrids.remove()
	d3_chart.ygrids.remove()
};

var getLegs = function(){
	$.ajax({
		url: "/options/displaylegs",
		method: "GET",
		dataType: "json",
		success: function(data){
			if(data.length===0){
				render('#legs_empty_message', '#manage_legs_div')({});
			}
			else{
				var template = $("#legs_manage_script").html()
				var rendered = Mustache.render(template, data)
				$('#manage_legs_div').html(rendered);
			}
		}
	});
};

var getStrategy = function(){
	$.ajax({
		url: "/options/strategyinfo",
		method: "GET",
		dataType: "json",
		success: function(data){
			if(data.length===0){
				render('#no_strategy_message', '#strategy_info_div')({});
			}
			else{
				var template = $("#strategy_info_script").html()
				var rendered = Mustache.render(template, data)
				$('#strategy_info_div').html(rendered);
			}
		}
	});
}

$(document).ready(function(){
	render('#_nav', "#navbar_div")({});
	render("#_strategy_data", "#data_div")({});

	// Global strategy variable blocks access to Legs modal until a strategy is created
	$('#legs_btn').prop('disabled', true).css("color", "grey");
	strategy=false

	$("#graph_btn").on('click', function(event){
		graphData()
	});

	$('#stgy_btn').on('click','a', function(event){
		$('#stgy_modal').modal('toggle')
	});

	$('#stgy_form').on('submit', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/stgyform",
			method: "POST",
			'data':data,
			success:function(data){
				$('#legs_btn').prop('disabled', false).css("color", "black");
				strategy=true
			}
		});

	$('#stgy_modal').on('hidden.bs.modal', function () {
    $(this).find(".field-input").val('').end();
	});

	$('#stgy_modal').modal('hide')
	});

	$('#legs_btn').on('click', function(event){
		if(strategy===true){
			getStrategy();
			render('#legs_form_script', '#add_leg_div')({});
			getLegs();
		}
	});

	$('#add_leg_div').on('submit', '#legs_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/legsform",
			method: "POST",
			'data':data,
			success: function(data){
				$(this).find(".field-input").val('').end();
				render('#legs_form_script', '#add_leg_div')({});
				getLegs();
			},
			statusCode: {
				422: function() {
					$('#max_legs_modal').modal('toggle')
					$(this).find(".field-input").val('').end();
					render('#legs_form_script', '#add_leg_div')({});
				},
			}
		});
	});

	$('#manage_legs_div').on('submit', '.delete_leg_form', function(event){
		event.preventDefault();
		var id_ = $(this).data('id');
		$.ajax({
			url: "/options/deleteleg",
			method: "POST",
			data: $(this).serialize(),
			success: function(data){
				getLegs();
			}
		});
	});

	$('#clear_btn').on('click', function(event){
		$.ajax({
			url: "/options/clear",
			method: "POST",
			success: function(data){
				console.log("Session strategy deleted")
				unloadData()
				$('#legs_btn').prop('disabled', true).css("color", "grey");
				strategy=false
			}
		});
	});

})






















