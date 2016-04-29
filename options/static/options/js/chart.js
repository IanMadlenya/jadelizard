


var d3_chart = c3.generate({
    data: {
        x: 'Price',
        columns: [
            ['Price', 30, 50, 100, 230, 300, 310],
            ['Profit', 30, 200, 100, 400, 150, 250],
        ]
    },
    bindto: "#d3_chart", 

});