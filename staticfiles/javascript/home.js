
// main.js
// get Canvas element from home.html
const ctx = document.getElementById('studentChart');

// Chart variable declare for update/refresh
let studentChart = null;

// data fetch and  chart create from server
async function loadChartData() {
    try {
        //  JSON data fetch  from Django views
        const response = await fetch('/chart_data/');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json(); // department__departmentName and total students

        // create lebels and dataset by Chart.js 
        const labels = data.map(item => item.department__departmentName);
        const counts = data.map(item => item.total);
        

        // reset chart
        if (studentChart) {
            studentChart.destroy();
        }

        // creat new chart
        studentChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total of Students',
                    data: counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(240, 235, 234, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 } // integer ticks
                    }
                }
            }
        });

    } catch (err) {
        console.error('Error loading chart data:', err);
    }
}

// chart data load when Page load
document.addEventListener('DOMContentLoaded', () => {
    loadChartData();
});
