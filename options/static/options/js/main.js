
var render = function(templateSelector, dropZone){
	var template = $(templateSelector).html();
	return function(data){
		var rendered = Mustache.render(template, data);
		$(dropZone).html(rendered);
	};
};



// not supporting Safari due to issues with Bootstrap
var disableSafari = false
var safari =  ((navigator.vendor==="Apple Computer, Inc." && navigator.platform.includes('Mac')) ? true : false)

// renders full screen error message
var browserMessage = function(template){
	$('#navbar_div').remove();
	$('#d3_chart').remove();
	$('html').css('height','100%');
	$('body').css({'background-color':'#efefef', 'height':'100%', 'width':'100%'});
	render(template, 'body')({});
}

// Sends JSON data to C3 for graphing
var graphData = function(options){
		$.ajax({
			url: "/home/graphdata",
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
				$('.c3-axis-x-label').css('visibility', 'visible')
				$('.c3-axis-y-label').css('visibility', 'visible')
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


// Clears graph and removes grid lines
var unloadData = function(){
	d3_chart.unload({
		ids: ['price_range','strategy_profit']
	});
	d3_chart.xgrids.remove()
	d3_chart.ygrids.remove()
	$('.c3-axis-x-label').css('visibility', 'hidden')
	$('.c3-axis-y-label').css('visibility', 'hidden')
};

// Global variable for strategy stock shares 
var stock = {"longqty":0, "shortqty":0}

// All Legs and Stock
var getLegs = function(){
	$.ajax({
		url: "/home/displaylegs",
		method: "GET",
		dataType: "json",
		success: function(data){
			if(data['legs'].length===0){
				render('#legs_empty_message', '#manage_legs_div')({});
			}
			else{
				data['longqty'] = stock['longqty']
				data['shortqty'] = stock['shortqty']
				var template = $("#legs_manage_script").html()
				var rendered = Mustache.render(template, data)
				$('#manage_legs_div').html(rendered);
			}
		}
	});

};

var getStock = function(){
	var template = $('#shares_script').html()
	var rendered = Mustache.render(template, stock)
	$('#stock_div').html(rendered);
}

// UpdateStrategy context - show strategy data in stgy update form
// LegsModal context - show strategy data in legs modal
var getStrategy = function(context){
	$.ajax({
		url: "/home/strategyinfo",
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
		url: "/home/deleteleg",
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
// html input names must match django form names
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

// on successful completion for non-closing forms
var showInputSuccess = function(selector){
	$(selector).css('border', '0.05em solid #00a86b')
	setTimeout(function(){($(selector).removeAttr('style'))}, 800);
}

// Enable (bool=false) and Disable (bool=true) buttons
var disableButtons = function(bool){
	color = ((bool===true) ? "grey" : "black")
	$('#legs_btn').prop('disabled', bool).css("color", color);
	$('#data_btn').prop('disabled', bool).css("color", color);
	$('#model_btn').prop('disabled', bool).css("color", color);
	$('#range_btn').prop('disabled', bool).css("color", color);
}

$(document).ready(function(){

	// Currently not supporting Safari
	if(safari===true && disableSafari===true){
		browserMessage('#browser_message')
		return
	}

	// Render navbar
	render('#_nav', "#navbar_div")({});

	// Disable legs modal, strategy data modal, model settings modal until strategy is created
	// no strategy present
	// default range setting
	disableButtons(true)
	var strategy=false
	var range="auto"


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

	// clear inputs on form hide
	$('#stgy_modal').on('hidden.bs.modal', function () {
		$('.stgy-input').removeAttr('style');
    	$(this).find(".field-input").val('').end();
	});

	$('#stgy_form').on('submit', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/home/stgyform",
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
					disableButtons(false)
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
			url: "/home/updatestgy", 
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
			// getStock();
		}
	});

	$('#add_leg_div').on('submit', '#legs_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: "/home/legsform",
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
			url: "/home/getleg",
			method: "GET", 
			dataType: "json",
			data: {id:id_},
			success: function(data){
				var template = $('#update_leg_script').html()
				var rendered = Mustache.render(template, data)
				$(id_selector).html(rendered);
				$('.edit_btn').prop('disabled', true);

				(data['position']==='long') ? $('#position_long').prop("selected", true) : $('#position_short').prop("selected", true);
				(data['kind']==='call') ? $('#kind_call').prop("selected", true) : $('#kind_put').prop("selected", true);
			}
		});
	});

	$('#manage_legs_div').on('submit', '.update_leg_form', function(event){
		event.preventDefault();
		var data = $(this).serialize();
		$.ajax({
			url: '/home/updateleg',
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

	$('#manage_legs_div').on('click', '.stock_save_btn', function(event){
		var data = $('#stock_form').serialize()
		$.ajax({
			url: '/home/setstock', 
			method: 'POST', 
			'data': data,
			success: function(data){
				if('fields' in data){
					ids = ['#stock-input-long', '#stock-input-short']
					fields = JSON.parse(data['fields'])
					showInputErrors(ids, fields)
				}
				else {
					showInputSuccess('.stock-input')
					stock['longqty'] = data['longqty']
					stock['shortqty'] = data['shortqty']	
				}

			}

		});

	});




	// Clear current strategy and window
	$('#clear_btn').on('click', function(event){
		$.ajax({
			url: "/home/clear",
			method: "POST",
			success: function(data){
				unloadData()
				disableButtons(true)
				strategy=false
				$('#stgy_btn').text('New Strategy');
				$('#range_form')[0].reset();
				stock = {'longqty':0, 'shortqty':0}
			}
		});
	});



	// Strategy Greek Values and Setup Cost
	$('#data_btn').on('click', function(event){
		if(strategy===true){
			$.ajax({
				url: "/home/strategydata",
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
			url: "/home/choosemodel",
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
		if(strategy===true){
			$('#range_modal').modal('toggle')			
		}
	});

	$('#enter_input').on('click', function(event){
		range="manual"
		render('#range_hidden_fields', '#range_fields_div')({});
		$('#range_fields_div').css('border-left', '1px solid black');
	});

	$('#auto_input').on('click', function(event){
		range="auto"
		$('#range_fields_template').remove();
		$('#range_fields_div').css('border-left', '0px');
	})

	$('#range_submit_btn').on('click', function(event){
		if(range==="auto"){
			$.ajax({
				url: "/home/resetrange",
				method: "POST",
				success:function(){
					$('#range_modal').modal('toggle');
					$('#range_form')[0].reset();
				}
			})
		}
		else if(range==="manual"){
			data = $('#range_form').serialize()
			$.ajax({
				url: "/home/graphrange",
				method: "POST",
				'data':data,
				success:function(data){
					if('fields' in data){
						fields=JSON.parse(data['fields'])
						ids = ['#range-input-start', '#range-input-end']	
						showInputErrors(ids, fields)
					}
					else{
						$('#range_modal').modal('toggle');
						$('.range-input').removeAttr('style')
					}
				}
			})
		}
	});



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
			url:"/home/volcalc",
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
			url: "/home/getr",
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
			url: "/home/loadtemplate",
			method: "POST",
			data: {id:id_},
			success: function(data){
				stock = data["stock"]
				strategy=true
				disableButtons(false)
				$('#stgy_btn').text('Edit Strategy');
			}
		});
	});



})






