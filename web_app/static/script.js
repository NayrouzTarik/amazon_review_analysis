const socket = io();
const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
        }]
    }
});

socket.on('update', (data) => {
    document.getElementById('reviews').innerHTML = data.reviews
        .map(r => `<div class="review ${r.sentiment}">${r.reviewText}</div>`)
        .join('');
    
    chart.data.labels = data.stats.map(s => s._id);
    chart.data.datasets[0].data = data.stats.map(s => s.count);
    chart.update();
});