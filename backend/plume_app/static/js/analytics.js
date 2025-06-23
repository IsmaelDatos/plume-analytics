document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('historicalChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: JSON.parse(document.getElementById('historicalChart').dataset.labels),
            datasets: [{
                label: 'Total XP',
                data: JSON.parse(document.getElementById('historicalChart').dataset.data),
                borderColor: '#FF3200',
                backgroundColor: 'rgba(255, 50, 0, 0.1)',
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function (value) {
                            return value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
});
