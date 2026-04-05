const visitors = fetch("mycounturl")
.then(response => response.json())
.then(count => { document.getElementById("counter").textContent = count.count; });