const visitors = fetch("https://ej6k6nb4fe.execute-api.us-east-1.amazonaws.com/count")
.then(response => response.json())
.then(count => { document.getElementById("counter").textContent = count; });