"use strict";
(() => {
  const select = document.querySelector("#run-select");
  const panel = document.querySelector("#run-panel");
  const data = window.RUN_VIEWER_DATA;
  if (!select || !panel || !data) return;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const row = cells => "<tr>" + cells.map((cell, i) => `<${i ? "td" : "th scope=\"row\""}>${escape(cell)}</${i ? "td" : "th"}>`).join("") + "</tr>";
  function render() {
    const type = select.value;
    let html;
    if (type === "engineering") {
      const e = data.engineering;
      html = `<h3>Engineering: the first patch misses a conflict</h3><p>Compare the original, the candidate, and the combined revision. Each test count applies to the suite named in the record.</p><div class="table-scroll" role="region" aria-label="Engineering results" tabindex="0"><table><thead><tr><th>Recorded stage</th><th>Tests</th><th>Result</th></tr></thead><tbody>${row(["Original smoke suite",e.base.count,e.base.result])}${row(["Candidate implementation suite",e.candidate.count,e.candidate.result])}${row(["Candidate with review suite",e.review.count,e.review.result])}${row(["Combined revision suite",e.fixed.count,e.fixed.result])}</tbody></table></div><p>On the conflict fixture, the candidate exits ${escape(e.conflictExit)} and prints a pass result. The combined revision exits ${escape(e.fixedExit)} and reports the conflict.</p><details><summary>Predict: what if an input token value conflicts on a repeated pair?</summary><p>The contract requires exit 2 and empty stdout. The review suite tests each token field.</p></details><p class="run-source"><a href="workshops/engineering/evidence/run.txt">Open the recorded engineering run</a></p>`;
    } else if (type === "research") {
      const r = data.research;
      html = `<h3>Research: held-out query H03</h3><p>Query: ${escape(r.query)}. Required card: ${escape(r.expected.join(", "))}. The query is critical.</p><div class="table-scroll" role="region" aria-label="Held-out retrieval results" tabindex="0"><table><thead><tr><th>System</th><th>Returned cards</th><th>H03 recall</th><th>Mean recall</th><th>Mean precision</th></tr></thead><tbody>${row(["Baseline",r.baseline.ids.join(", "),r.baseline.recall,r.baseline.meanRecall,r.baseline.precision])}${row(["Combined",r.candidate.ids.join(", "),r.candidate.recall,r.candidate.meanRecall,r.candidate.precision])}</tbody></table></div><p>The combined candidate misses ${escape(r.expected.join(", "))}. The recorded decision is <strong>${escape(r.decision)}</strong>.</p><details><summary>Predict: would a new output directory make this held-out test independent again?</summary><p>No. The team already knows the result. A new held-out set is needed for a fresh test.</p></details><p class="run-source"><a href="workshops/research/records/holdout-report.json">Open the recorded held-out report</a></p>`;
    } else {
      const a = data.automation;
      html = `<h3>Automation: retry at two commit boundaries</h3><p>Both first attempts stop without a receipt. The database state determines the next action.</p><div class="table-scroll" role="region" aria-label="Retry results" tabindex="0"><table><thead><tr><th>Stop point</th><th>Exit</th><th>State after stop</th><th>Evidence rows</th><th>Retry outcome</th></tr></thead><tbody>${row(["Before draft commit",a.before.exit,a.before.state,a.before.evidence,a.before.retry])}${row(["After draft commit",a.after.exit,a.after.state,a.after.evidence,a.after.retry])}</tbody></table></div><p>Both retries reach <code>draft_staged</code>. The replay records the same final draft and state as the clean run.</p><details><summary>Predict: what happens if you run the same export once more after a successful retry?</summary><p>The workflow reuses the existing draft for the same run key.</p></details><p class="run-source"><a href="workshops/automation/results/replay.json">Open the recorded retry histories</a></p>`;
    }
    panel.className = "run-panel";
    panel.innerHTML = html;
  }
  select.addEventListener("change", render);
  render();
})();
