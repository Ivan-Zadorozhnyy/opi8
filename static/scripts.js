document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('load-report-btn').addEventListener('click', loadEndpoints);
});

function loadEndpoints() {
  fetch('/api/reports')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      const list = document.getElementById('endpoint-list');
      list.innerHTML = '';

      data.forEach(endpoint => {
        let div = document.createElement('div');
        div.innerHTML = `<strong>Name:</strong> ${endpoint.name} <br>
                         <strong>Metrics:</strong> ${endpoint.metrics.join(', ')} <br>
                         <strong>Users:</strong> ${endpoint.users.join(', ')}`;
        list.appendChild(div);
      });
    })
    .catch(error => {
      console.error('Error fetching the endpoints:', error);
    });
}
