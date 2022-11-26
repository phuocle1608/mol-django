function generateColorSet(listoflabel, xtype) {
    const colorSet = ["rgba(0, 135, 136, 1)", "rgba(0, 166, 198, 1)", "rgba(0, 143, 172, 1)", "rgba(3, 73, 92, 1)", "rgba(167, 121, 79, 1)"];
    if (xtype == "background"){
        let new_arr = []
        for (let item of colorSet.slice(0, listoflabel.length)) {
            new_arr.push(item.replace("1)", "0.8)"))
        }
        return new_arr
    } else {
        return colorSet.slice(0, listoflabel.length)
    }

}

// console.log(generate([1, 2, 3, 4], "background"))

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart revenue_by_source
var ctx = document.getElementById("revenue_by_source");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: revenue_by_source['label'], //["Direct", "Referral", "Social", "TEST"],
        datasets: [{
            data: revenue_by_source['value'],
            backgroundColor: generateColorSet(revenue_by_source['label'], "background"),
            hoverBackgroundColor: generateColorSet(revenue_by_source['label'], "backgroundhover"),
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 10,
            yPadding: 5,
            displayColors: false,
            caretPadding: 5,
        },
        legend: {
            display: true

        },
        cutoutPercentage: 70,
    },
});

//https://www.youtube.com/watch?v=0OIZnoZ8GUU

// Pie Chart Example
var ctx = document.getElementById("revenue_by_product");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: revenue_by_product['label'],
        datasets: [{
            data: revenue_by_product['value'],
            backgroundColor: generateColorSet(revenue_by_product['label'], "background"),
            hoverBackgroundColor: generateColorSet(revenue_by_product['label'], "backgroundhover"),
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 10,
            yPadding: 5,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: true
        },
        cutoutPercentage: 70,
    },
});
