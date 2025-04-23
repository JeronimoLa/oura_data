async function createChart() {
    try {
        const response = await fetch("http://localhost:8000/metrics");
        const metric_data = await response.json();

        var options = {
            stroke: {
                curve: 'smooth'
            },
            chart: { height: 280, type: "area" },
            dataLabels: { enabled: false },
            series: metric_data["series"],
            fill: {
                type: "gradient",
                gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.3,
                opacityTo: 0.5,
                stops: [0, 100],
                },
            },
            xaxis: { categories: metric_data["categories"] },
        };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();

    } catch (error) {
      console.error("Error loading chart data:", error);
    }
  }
// Call the function when the page loads
window.addEventListener('DOMContentLoaded', createChart);

async function createRadials(){
    const chartIds = ['radial', 'radial-1', 'radial-2', 'radial-3', 'radial-4', 'radial-5'];      
    var options = {
        series: [20],
        chart: {
            height: '100%',
            type: 'radialBar',
        },
        plotOptions: {
            radialBar: {
            hollow: {
                size: '70%',
            }
            },
        },
    labels: ['Cricket'],
    };


    chartIds.forEach(id => {
        const chart = new ApexCharts(document.querySelector(`#${id}`), options);
        chart.render();
    });
}
window.addEventListener('DOMContentLoaded', createRadials);