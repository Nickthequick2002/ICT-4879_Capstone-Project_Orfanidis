
let myChart = null;

function fetchAndRenderChart() {
    var ctxElement = document.getElementById('progressChart');
    if (!ctxElement) return;

    fetch('/accounts/progress-data/')
        .then(response => response.json())
        .then(data => {
            // Update Text Stats
            if (data.streak !== undefined) {
                const streakEl = document.getElementById('stat-streak');
                if (streakEl) streakEl.innerText = data.streak;
            }
            if (data.total_workouts !== undefined) {
                const workoutEl = document.getElementById('stat-workouts');
                if (workoutEl) workoutEl.innerText = data.total_workouts;
            }

            var ctx = ctxElement.getContext('2d');
            
            // Destroy existing chart if present to avoid overlap
            if (myChart) {
                myChart.destroy();
            }

            // Create Gradient
            var gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(255, 140, 66, 0.5)'); // Brand Orange Opacity
            gradient.addColorStop(1, 'rgba(255, 140, 66, 0.0)');

            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Body Weight (kg)',
                        data: data.weights,
                        backgroundColor: gradient,
                        borderColor: '#ff8c42',
                        borderWidth: 3,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#ff8c42',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#333',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            cornerRadius: 10,
                            displayColors: false
                        }
                    },
                    scales: {
                        y: {
                            grid: { borderDash: [5, 5], color: 'rgba(0,0,0,0.05)' },
                            ticks: { font: { family: "'Inter', sans-serif" } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { font: { family: "'Inter', sans-serif" } }
                        }
                    }
                }
            });
        })
        .catch(console.error);
}

document.addEventListener('DOMContentLoaded', fetchAndRenderChart);

// Expose logging function globally
window.submitProgressLog = function() {
    const weight = document.getElementById('log-weight').value;
    const workouts = document.getElementById('log-workouts').value;
    
    // Simple validation
    if (!weight) {
        alert("Please enter a weight.");
        return;
    }

    const formData = new FormData();
    formData.append('weight', weight);
    formData.append('workouts', workouts);
    // CSRF Token - grab from cookie or hidden input if available. 
    // Django AJAX usually needs 'X-CSRFToken'. We can use a helper or valid form submission if we had {% csrf_token %} in HTML.
    // The modal HTML DOES NOT have csrf_token tag? Oops.
    // I need to fetch CSRF token from document cookie.
    
    const csrfToken = getCookie('csrftoken'); 

    fetch('/accounts/log-progress/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close Modal
            $('#logProgressModal').modal('hide');
            // Refresh Chart
            fetchAndRenderChart();
            // Optional: Show success message/toast
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
};

// CSRF Helper function (standard Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
