function createChart(container, symbol) {
    document.getElementById(container).innerHTML = ""; // Rensa innan render
    new TradingView.widget({
        "container_id": container,
        "width": "100%",
        "height": "300",
        "symbol": symbol,
        "interval": "D",
        "timezone": "Europe/Stockholm",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "withdateranges": true,
        "hide_side_toolbar": true,
        "allow_symbol_change": false
    });
}

function updateCharts() {
    const symbol = document.getElementById("stockInput").value.toUpperCase();
    if (symbol) {
        createChart("chart1", symbol);
        createChart("chart2", symbol);
        createChart("chart3", symbol);
    }
}
