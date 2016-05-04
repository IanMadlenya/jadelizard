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

$(document).ready(function(){
	render('#_nav', "#navbar_div")({});
	render("#_strategy_data", "#data_div")({});

	$("#graph_btn").on('click', function(event){
		strategyData()
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
				console.log(data)
			}
		});

	$('#stgy_modal').on('hidden.bs.modal', function () {
    $(this).find(".field-input").val('').end();
	});

	$('#stgy_modal').modal('hide')
	});

	$('#legs_btn').on('click', function(event){
		render('#legs_form_script', '#add_leg_div')({});
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
					var rendered = Mustache.render(template, {data:data})
					$('#manage_legs_div').html(rendered);
				}
			}
		})
	});

	$('#add_leg_div').on('submit', '#legs_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/legsform",
			method: "POST",
			'data':data,
			success: function(data){
				console.log(data)
			}
		});

		$('#legs_modal').on('hidden.bs.modal', function () {
    		$(this).find(".field-input").val('').end();
		});

		// $('#legs_modal').modal('hide')

	});

	$('#manage_legs_div').on('submit', '.delete_leg_form', function(event){
		event.preventDefault();
		var id_ = $(this).data('id');
		console.log($(this).serialize()),
		$.ajax({
			url: "/options/deleteleg",
			method: "POST",
			data: $(this).serialize(),
			success: function(data){
				var template = $("#legs_manage_script").html()
				var rendered = Mustache.render(template, {data:data})
				$('#manage_legs_div').html(rendered);
				console.log(data)
			}
		});
	});


})






















