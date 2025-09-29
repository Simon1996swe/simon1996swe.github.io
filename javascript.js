console.log("✅ javascript.js loaded");

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

// Start charts with defaults
createChart("chart1", "OMXSTO:NOVO_B");
createChart("chart2", "NASDAQ:INTC");
createChart("chart3", "OMXSTO:OMXS30");

// Search update
function updateCharts() {
    const symbol = document.getElementById("stockInput").value.toUpperCase();
    if (symbol) {
        console.log("🔄 Updating charts with:", symbol);
        createChart("chart1", symbol);
        createChart("chart2", symbol);
        createChart("chart3", symbol);
    }
}
