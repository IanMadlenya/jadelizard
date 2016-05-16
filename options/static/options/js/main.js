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

$(document).ready(function(){
	render('#_nav', "#navbar_div")({});

	// Disable legs modal, strategy data modal, model settings modal until strategy is created
	$('#legs_btn').prop('disabled', true).css("color", "grey");
	$('#data_btn').prop('disabled', true).css("color", "grey");
	$('#model_btn').prop('disabled', true).css("color", "grey");
	var strategy=false

	$('#logo_btn').on('click', function(event){
		$('#project_info_modal').modal('toggle');
	});

	$("#graph_btn").on('click', function(event){
		graphData()
	});

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
					if('S0' in fields){
						$('#stgy-input-S0').css('border','0.05em solid #a72101');
					}
					else {
						$('#stgy-input-S0').removeAttr('style');
					}
					if('sigma' in fields){
						$('#stgy-input-sigma').css('border','0.05em solid #a72101');
					}
					else {
						$('#stgy-input-sigma').removeAttr('style');
					}
					if('q' in fields){
						$('#stgy-input-q').css('border','0.05em solid #a72101');
					}
					else {
						$('#stgy-input-q').removeAttr('style');
					}
					if('r' in fields){
						$('#stgy-input-r').css('border','0.05em solid #a72101');
					}
					else {
						$('#stgy-input-r').removeAttr('style');
					}
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

	$('#update_form_div'.on('submit', '#stgy_update_form', function(event){
		console.log("SUBMIT")
	});

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
					if('K' in fields){
						$('#add-input-k').css('border','0.05em solid #a72101');
					}
					else{
						$('#add-input-k').removeAttr('style');
					}
					if('T' in fields){
						$('#add-input-t').css('border','0.05em solid #a72101');
					}
					else{
						$('#add-input-t').removeAttr('style');
					}
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
					if('K' in fields){
						$('#edit-input-k').css('border','0.05em solid #a72101');
					}
					else{
						$('#edit-input-k').removeAttr('style');
					}
					if('T' in fields){
						$('#edit-input-t').css('border','0.05em solid #a72101');
					}
					else{
						$('#edit-input-t').removeAttr('style');
					}
				}
				else {
				getLegs();	
				$('.edit_btn').prop('disabled', false);
				}
			},
		});
	});

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
		$('#fields_template').remove()
	});

	$('#bt_input').on('click', function(event){
		render('#hidden_fields', '#fields_div')({});
	});

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
					if('ticker' in fields){
						$('#vol-input-ticker').css('border','0.05em solid #a72101');
					}
					else{
						$('#vol-input-ticker').removeAttr('style');
					}
					if('days' in fields){
						$('#vol-input-days').css('border','0.05em solid #a72101');
					}
					else{
						$('#vol-input-days').removeAttr('style');
					}
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



})

