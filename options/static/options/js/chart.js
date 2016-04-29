


var d3_chart = c3.generate({
	
	data: {
		x: 'Price',
		columns: [
			['Price', 30, 50, 100, 230, 300, 310],
			['Profit', 30, 200, 100, 400, 150, 250],
		],

		type:'area',
		empty: {
			label: {
				text: "Create a Strategy or Load a Template to begin."
			}
		},
		colors: {
			Profit: '#15e596',
		},
		selection: {
			enabled: true,
			multiple: false,
		},
	},

	axis: {
		x: {
			label: {
				text: "Price of Underlying Security at First Expiration",
				position: "outer-middle"
			}
		},
		y: {
			label: {
				text: "Strategy Profit", 
				position: "outer-middle",
			}
		}
	},

	grid: {
		x: {
			show: true
		},
		y: {
			show: true
		}
	},

	legend: {
		show: false,
	},

	zoom: {
		enabled: true,
		rescaled: true,
		extent: [1,50]
	},

	area: {
		zerobased: false
	},

	bindto: "#d3_chart", 

});

// var d3_chart = c3.generate({

// 	data: {

// 		json: [

// 		],
		
// 		keys: {
// 			x: ''
// 		}



// 	}







// 	bindto: "#d3_chart", 

// });