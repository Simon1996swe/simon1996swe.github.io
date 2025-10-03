const canvas = document.getElementById("candles-bg");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let candles = [];
const candleWidth = 10;
const candleGap = 6;
const candleCount = Math.floor(canvas.width / (candleWidth + candleGap));

function randomCandle(x) {
  const high = Math.random() * canvas.height * 0.4 + 50;
  const low = high + Math.random() * 100 + 20;
  const open = high + Math.random() * (low - high);
  const close = high + Math.random() * (low - high);
  return { x, high, low, open, close };
}

for (let i = 0; i < candleCount; i++) {
  candles.push(randomCandle(i * (candleWidth + candleGap)));
}

function drawCandles() {
  ctx.fillStyle = "rgba(13, 17, 23, 0.25)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let c of candles) {
    // wick
    ctx.strokeStyle = "#aaa";
    ctx.beginPath();
    ctx.moveTo(c.x + candleWidth / 2, c.high);
    ctx.lineTo(c.x + candleWidth / 2, c.low);
    ctx.stroke();

    // body
    const isBull = c.close < c.open;
    ctx.fillStyle = isBull ? "rgba(74, 222, 128, 0.8)" : "rgba(239, 68, 68, 0.8)";
    ctx.fillRect(c.x, Math.min(c.open, c.close), candleWidth, Math.abs(c.close - c.open));
  }

  // move candles
  for (let c of candles) {
    c.x -= 1;
  }

  if (candles[0].x < -candleWidth) {
    candles.shift();
    candles.push(randomCandle(canvas.width));
  }
}

setInterval(drawCandles, 40);

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});
