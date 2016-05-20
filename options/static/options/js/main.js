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
				d3_chart.ygrids([{value: 0},])
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

// All Legs
var getLegs = function(){
	$.ajax({
		url: "/options/displaylegs",
		method: "GET",
		dataType: "json",
		success: function(data){
			if(data['legs'].length===0){
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

// UpdateStrategy context - show strategy data in stgy update form
// LegsModal context - show strategy data in legs modal
var getStrategy = function(context){
	$.ajax({
		url: "/options/strategyinfo",
		method: "GET",
		dataType: "json",
		success: function(data){
			if(context==="LegsModal"){
				var template = $("#strategy_info_script").html()
				var rendered = Mustache.render(template, data)
				$('#strategy_info_div').html(rendered);
				}
			else if(context==="UpdateStrategy"){
				data['sigma']=data['sigma']*100
				data['q']=data['q']*100
				data['r']=data['r']*100
				var template = $('#stgy_update_form_script').html()
				var rendered = Mustache.render(template, data)
				$('#update_form_div').html(rendered);
			}
		}
	});
}

var deleteLeg = function(form) {
		$.ajax({
		url: "/options/deleteleg",
		method: "POST",
		data: form.serialize(),
		success: function(data){
			getLegs();
		}
	});
}

// Shows Form Errors for input fields
// first argument - array of IDs for checked input fields
// second argument - dictionary of errors returned by form
var showInputErrors = function(arr, loc){
	for(var i=0; i<arr.length; i++){
		id = arr[i]
		name = $(id).attr('name');
		if(name in loc){
			$(id).css('border','0.05em solid #a72101');
		}
		else{
			$(id).removeAttr('style');
		}
	}
}

$(document).ready(function(){
	
	// Render navbar
	render('#_nav', "#navbar_div")({});

	// Disable legs modal, strategy data modal, model settings modal until strategy is created
	$('#legs_btn').prop('disabled', true).css("color", "grey");
	$('#data_btn').prop('disabled', true).css("color", "grey");
	$('#model_btn').prop('disabled', true).css("color", "grey");
	var strategy=false


	// Logo Modal
	$('#logo_btn').on('click', function(event){
		$('#project_info_modal').modal('toggle');
	});


	// Graph 
	$("#graph_btn").on('click', function(event){
		graphData()
	});


	// Creating and updating custom Options Strategies
	$('#stgy_btn').on('click', function(event){
		if(strategy===false){	
			$('#stgy_modal').modal('toggle');
		}
		else if(strategy===true){
			$('#stgy_update_modal').modal('toggle');
			getStrategy("UpdateStrategy");
		}
	});

	$('#stgy_modal').on('hidden.bs.modal', function () {
		$('.stgy-input').removeAttr('style');
    	$(this).find(".field-input").val('').end();
	});

	$('#stgy_form').on('submit', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/stgyform",
			method: "POST",
			'data':data,
			success:function(data){
				if('fields' in data){
					fields=JSON.parse(data['fields'])	
					ids = ['#stgy-input-S0', '#stgy-input-sigma', '#stgy-input-q', '#stgy-input-r']
					showInputErrors(ids, fields)
				}
				else{
					$('.stgy-input').removeAttr('style');
					$('#legs_btn').prop('disabled', false).css("color", "black");
					$('#data_btn').prop('disabled', false).css("color", "black");
					$('#model_btn').prop('disabled', false).css("color", "black");
					strategy=true
					$('#stgy_modal').modal('hide')
					$('#stgy_btn').text('Edit Strategy');
				}
			}, 
		});
	});

	$('#update_form_div').on('submit', '#stgy_update_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/options/updatestgy", 
			method: "POST", 
			'data': data,
			success:function(data){
				if('fields' in data){
					fields=JSON.parse(data['fields'])	
					ids = ['#stgy-update-input-S0', '#stgy-update-input-sigma', '#stgy-update-input-q', '#stgy-update-input-r' ]
					showInputErrors(ids, fields)
				}
				else{
					$('#stgy_update_modal').modal('toggle');
				}
			}
		})
	});




	// Adding, Viewing, Editing, Deleting Legs Modal
	$('#legs_btn').on('click', function(event){
		if(strategy===true){
			getStrategy("LegsModal");
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
				if('fields' in data){
					fields=JSON.parse(data['fields'])
					ids = ['#add-input-k', '#add-input-t']	
					showInputErrors(ids, fields)
				}
				else {
					$(this).find(".field-input").val('').end();
					render('#legs_form_script', '#add_leg_div')({});
					getLegs();
				}
			},
			// Strategy max # legs reached
			statusCode: {
				422: function() {
					render('#strategy-full', '#add_leg_desc')({});
					$(this).find(".field-input").val('').end();
					render('#legs_form_script', '#add_leg_div')({});
				},
			}
		});
	});

	$('#manage_legs_div').on('submit', '.delete_leg_form', function(event){
		event.preventDefault();
		deleteLeg($(this));
	});

	$('#manage_legs_div').on('click', '.edit_btn', function(event){
		event.preventDefault();
		var id_ = $(this).data('id');
		var id_selector = "#".concat(id_);
		$.ajax({
			url: "/options/getleg",
			method: "GET", 
			dataType: "json",
			data: {id:id_},
			success: function(data){
				var template = $('#update_leg_script').html()
				var rendered = Mustache.render(template, data)
				$(id_selector).html(rendered);
				$('.edit_btn').prop('disabled', true);
				if(data['position']==='long'){
					$('#position_long').prop("selected", true)
				}
				else if(data['position']==='short'){
					$('#position_short').prop("selected", true)
				}
				if(data['kind']==='call'){
					$('#kind_call').prop("selected", true)
				}
				else if(data['kind']==='put'){
					$('#kind_put').prop("selected", true)
				}
			}
		});
	});

	$('#manage_legs_div').on('submit', '.update_leg_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: '/options/updateleg',
			method: 'POST',
			'data': data,
			success: function(data){
				if('fields' in data){
					fields=JSON.parse(data['fields'])
					ids = ['#edit-input-k', '#edit-input-t']	
					showInputErrors(ids, fields)
				}
				else {
				getLegs();	
				$('.edit_btn').prop('disabled', false);
				}
			},
		});
	});




	// Clear current strategy and window
	$('#clear_btn').on('click', function(event){
		$.ajax({
			url: "/options/clear",
			method: "POST",
			success: function(data){
				unloadData()
				$('#legs_btn').prop('disabled', true).css("color", "grey");
				$('#data_btn').prop('disabled', true).css("color", "grey");
				$('#model_btn').prop('disabled', true).css("color", "grey");
				strategy=false
				$('#stgy_btn').text('New Strategy');
			}
		});
	});



	// Strategy Greek Values and Setup Cost
	$('#data_btn').on('click', function(event){
		if(strategy===true){
			$.ajax({
				url: "/options/strategydata",
				method: "GET", 
				dataType: "json",
				success: function(data){
					if("status" in data){
						render('#legs_empty_message', '#data_div')({});
					}
					else{
					var template = $("#strategy_data_script").html()
					var rendered = Mustache.render(template, data)
					$('#data_div').html(rendered);
					}
				}
			});
		}
	});


	// Pricing Model Settings
	$('#model_btn').on('click', function(event){
		if(strategy===true){
			$('#model_modal').modal('toggle')			
		}
	});

	$('#model_form').on('submit', function(event){
		var data = $(this).serialize();
		event.preventDefault();
		$.ajax({
			url: "/options/choosemodel",
			method: "POST",
			'data':data,
			success:function(data){
				$('#model_modal').modal('hide')
			}
		});
	});

	$('#bs_input').on('click', function(event){
		$('#fields_template').remove();
	});

	$('#bt_input').on('click', function(event){
		render('#hidden_fields', '#fields_div')({});
	});



	// Window Settings
	$('#range_btn').on('click', function(event){
		$('#range_modal').modal('toggle')
	});

	$('#enter_input').on('click', function(event){
		render('#range_hidden_fields', '#range_fields_div')({});
	});

	$('#auto_input').on('click', function(event){
		$('#range_fields_template').remove();
	})



	// Volatility by Ticker Tool
	$('#vol_form_hide').on('click', function(event){
		$('#vol_result_div').remove()
		$('#conn_error_div').remove()
		$('#vol_form')[0].reset();
		$('.vol-input').removeAttr('style');
		$('#vol_modal').modal('hide')
	});

	$('#vol_form').on('submit', function(event){
		event.preventDefault();
		$('.vol-input').removeAttr('style');
		$.ajax({
			url:"/options/volcalc",
			method: "GET", 
			'data':$(this).serialize(), 
			success: function(data){
				if('fields' in data){
					fields=JSON.parse(data['fields'])
					ids = ['#vol-input-ticker', '#vol-input-days']	
					showInputErrors(ids, fields)
				}
				else{
				var template = $("#vol_result_script").html()
				var rendered = Mustache.render(template, data)
				$('#vol_result_container').html(rendered);
				}
			},
			statusCode: {
				503: function() {
					render('#conn_error_script', '#vol_result_container')({});
				}
			}
		});
	});



	// Fetch risk-free rate tool
	$('#r_btn').on('click', function(event){
		$('#r_loading').show()
		$.ajax({
			url: "/options/getr",
			method: "GET", 
			'data':$(this).serialize(),
			success: function(data){
				$('#r_loading').hide()
				var template = $("#r_result_script").html()
				var rendered = Mustache.render(template, data)
				$('#r_result').html(rendered);
			},
			statusCode: {
				503: function(){
					$('#r_loading').hide()
					render('#conn_error_script', '#r_result')({});
				}
			}
		});
	});

	$('#r_hide').on('click', function(event){
		$('#r_result_div').remove()
		$('#r_modal').modal('hide')
	});



	// Load pre-configured strategy template 
	$('.template_btn').on('click', function(event){
		id_ = $(this).attr('id')
		$.ajax({
			url: "/options/loadtemplate",
			method: "POST",
			data: {id:id_},
			success: function(data){
				strategy=true
				$('#legs_btn').prop('disabled', false).css("color", "black");
				$('#data_btn').prop('disabled', false).css("color", "black");
				$('#model_btn').prop('disabled', false).css("color", "black");
				$('#stgy_btn').text('Edit Strategy');
			}
		});
	});



})






