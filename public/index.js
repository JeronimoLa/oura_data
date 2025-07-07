async function createChart() {
    try {
        const response = await fetch("http://localhost:8000/api/sleep-chart");
        const metric_data = await response.json();
        // console.log(metric_data["series"])
        var options = {
            stroke: {
                curve: 'smooth'
            },
            
            chart: { 
                type: "area",
                height: 280,
                toolbar: {
                    show: false,
          
                },
            },
            colors: [
                '#3B82F6', // Primary Blue
                '#6366F1', // Indigo
                '#14B8A6', // Teal
                '#10B981', // Emerald Green
                '#0EA5E9', // Sky Blue
                '#F59E0B', // Amber
                '#F43F5E', // Rose
                '#64748B'  // Slate Gray
            ],  
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
    const response = await fetch("http://localhost:8000/api/sleep-radials");
    const sleep_radials = await response.json();
    document.getElementById("date").innerText = sleep_radials["day"]
    const unzipObject = obj => [
        Object.keys(obj),
        Object.values(obj)];
    a = unzipObject(sleep_radials["data"]); 

    const chartIds = ['radial', 'radial-1', 'radial-2', 'radial-3', 'radial-4'];      
    const configuration = []
    for (i=0; i<chartIds.length; i++){

        const options = {
            chart: {
              type: "radialBar",
              height: 180,
              sparkline: { enabled: true },
              animations: { enabled: true, easing: "easeout", speed: 800 },
            },
            // series: [value],
            series: [a[1][i]],

            // labels: ["Sleep %"],
            labels: [a[0][i]],

            plotOptions: {
              radialBar: {
                hollow: { size: "69%" },
                track: { background: "#dbeafe" },
                dataLabels: {
                  value: {
                    fontSize: "20px",
                    fontWeight: "700",
                    color: "#1e3a8a",
                  },
                  name: {
                    fontSize: "13px",
                    color: "#3b82f6",
                    fontWeight: "600",
                  },
                },
              },
            },
            colors: ["#3b82f6"],
            stroke: { lineCap: "round" },
          };
        configuration.push(options)
    }
    chartIds.forEach((id, index) => {
        const chart = new ApexCharts(document.querySelector(`#${id}`), configuration[index]);
        chart.render();
    });
}
window.addEventListener('DOMContentLoaded', createRadials);


async function createWeeklyChart() {
  try {
    const response = await fetch("http://localhost:8000/api/weekly-sleep-data");
    const metric_data = await response.json();
    document.getElementById("timeframe").innerText = metric_data["date_range"]
    document.getElementById("averages").innerHTML = metric_data["averages"]
    document.getElementById("weekly-data").innerHTML = metric_data["weekly_data"]

    console.log(metric_data)
  } 
  catch (error) {
      console.error("Error loading weekly data:", error);
    }
}
window.addEventListener('DOMContentLoaded', createWeeklyChart);
