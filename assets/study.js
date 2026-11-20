"use strict";

const timeoutDemo = document.querySelector("#timeout-demo");
if (timeoutDemo) {
  const outcomes = {
    before: ["No draft exists", "Read the source again, then create one draft. Keep the same request ID."],
    after: ["One draft already exists", "Verify its contents and advance to review. A second write would duplicate work."]
  };
  const observation = timeoutDemo.querySelector("output");
  timeoutDemo.addEventListener("change", event => {
    const result = outcomes[event.target.value];
    if (result) observation.textContent = result[0] + ". " + result[1];
  });
}

const bench = document.querySelector("#bench-comparison");
if (bench) {
  const measured = JSON.parse(bench.dataset.scores);
  const group = bench.querySelector("select");
  const rows = Array.from(bench.querySelectorAll("[data-model]"));
  const outcome = bench.querySelector("output");
  function update() {
    const values = measured[group.value];
    rows.forEach(row => {
      const value = values[row.dataset.model];
      row.querySelector("meter").value = value;
      row.querySelector("b").textContent = value + " / 300";
    });
    outcome.textContent = group.value === "test"
      ? "The badge helps on ordinary rows. Removing it costs 39 correct predictions."
      : "Under the deliberate shift, removing the badge gains 163 correct predictions.";
  }
  group.addEventListener("change", update);
  update();
}


const lanes = document.querySelector("#lanes");
if (lanes) {
  lanes.addEventListener("change", () => {
    const calls = Number(lanes.value) * 3;
    const values = [calls, calls * 2000, calls * 1200, calls * 400, calls * 2400];
    document.querySelectorAll("#token-totals td").forEach((cell, index) => {
      cell.textContent = values[index].toLocaleString("en-US");
    });
    document.querySelector("#token-reading").textContent =
      calls + " calls account for " + values[4].toLocaleString("en-US") +
      " tokens. Cached input is already included.";
  });
}
