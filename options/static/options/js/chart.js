var d3_chart = c3.generate({

	data: {
		x: 'price_range',
		columns: [
			["price_range"],
			],

		type:'area',

		empty: {
			label: {
				text: "Create a Strategy to begin."
			}
		},

		colors: {
			strategy_profit: '#0073e5'
		},

		selection: {
			enabled: true,
			multiple: true,
		},
	},

	axis: {
		x: {
			label: {
				text: "Value of Underlying Instrument at First Expiration",
				position: "inner-middle"
			},
			tick: {
				culling: {
					max:10
				},
				count: 40,
				format: function(value) {return "$" + value.toFixed(2)},
			},
		},
		y: {
			label: {
				text: "Strategy Profit", 
				position: "outer-middle",
			},
			tick: {
				format: d3.format("$"), 
			}, 
		},
	},

	grid: {
		y: {
			lines: [
				{value: 0}
			]
		}
	},

	point: {
		show: false,
		select: {
			r: 4
		},
	},

	tooltip: {
		format: {
			title: function(x) {return "Underlying Value $" + x},
			value: function (value, id) {return "$" + value.toFixed(2)},
			name: function(id) {
				if(id==='strategy_profit'){
					return "Strategy Profit"
				}
			}
		}
	},

	legend: {
		show: false,
	},

	subchart: {
		show: true,
		size: {
			height:50
		}
	},

	area: {
		zerobased: false
	},

	size: {
		height:640
	},

	bindto: "#d3_chart", 

});








