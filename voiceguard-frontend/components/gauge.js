/**
 * VoiceGuard · Gauge Component
 * Animates the semicircular confidence meter.
 */

function animateGauge(pct, isReal) {
  const arcLength = 251;
  const offset = arcLength - (arcLength * pct) / 100;
  const fill    = document.getElementById("gaugeFill");
  const pctEl   = document.getElementById("gaugePct");
  const stop1   = document.getElementById("gaugeStop1");
  const stop2   = document.getElementById("gaugeStop2");
  const needle  = document.getElementById("gaugeNeedle");

  // Color theme: true = green (real), "challenge" = amber, false = red (fake)
  if (isReal === "challenge") {
    stop1.style.stopColor = "#fbbf24";
    stop2.style.stopColor = "#f59e0b";
    needle.setAttribute("fill", "#f59e0b");
  } else if (isReal) {
    stop1.style.stopColor = "#4ade80";
    stop2.style.stopColor = "#22c55e";
    needle.setAttribute("fill", "#22c55e");
  } else {
    stop1.style.stopColor = "#f87171";
    stop2.style.stopColor = "#ef4444";
    needle.setAttribute("fill", "#ef4444");
  }

  // Needle position along semicircle arc
  const angle = (pct / 100) * 180 - 180;
  const rad   = (angle * Math.PI) / 180;
  const cx    = 100 + 80 * Math.cos(rad);
  const cy    = 100 + 80 * Math.sin(rad);

  setTimeout(() => {
    fill.style.strokeDashoffset = offset;
    needle.setAttribute("cx", cx.toFixed(1));
    needle.setAttribute("cy", cy.toFixed(1));
  }, 100);

  // Animated counter
  let current = 0;
  const duration = 1200;
  const stepSize = pct / (duration / 16);
  const counter = setInterval(() => {
    current = Math.min(current + stepSize, pct);
    pctEl.textContent = Math.round(current) + "%";
    if (current >= pct) clearInterval(counter);
  }, 16);
}

function resetGauge() {
  const fill   = document.getElementById("gaugeFill");
  const pctEl  = document.getElementById("gaugePct");
  const needle = document.getElementById("gaugeNeedle");
  fill.style.strokeDashoffset = "251";
  pctEl.textContent = "0%";
  needle.setAttribute("cx", "20");
  needle.setAttribute("cy", "100");
}
