"use strict";
const fs = require("node:fs");
const path = require("node:path");
const {pathToFileURL} = require("node:url");
const assert = require("node:assert/strict");
const puppeteer = require(process.env.PUPPETEER_PATH || "puppeteer");
const root = path.resolve(__dirname, "..");
const read = file => fs.readFileSync(path.join(root, file), "utf8");
const record = read("workshops/engineering/evidence/run.txt");
function section(name) {
  const match = record.match(new RegExp("^## " + name + "\\n([\\s\\S]*?)(?=\\n## |(?![\\s\\S]))", "m"));
  assert(match, "Missing record section: " + name);
  return match[1];
}
function suite(name) {
  const text = section(name);
  const count = text.match(/Ran (\d+) tests/);
  const result = text.match(/^(OK|FAILED \(failures=\d+\))$/m);
  assert(count && result, "Incomplete suite: " + name);
  return {count:count[1], result:result[1]};
}
const conflict = section("candidate-probe / conflict");
const fixed = section("repo / conflict");
const holdout = JSON.parse(read("workshops/research/records/holdout-report.json"));
const base = holdout.baseline.rows.find(row => row.id === "H03");
const candidate = holdout.candidate.rows.find(row => row.id === "H03");
const replay = JSON.parse(read("workshops/automation/results/replay.json"));
function crash(name) {
  const c = replay.crashes.find(row => row.injection === name);
  assert(c);
  return {exit:c.exit, state:c.state_after_exit.state, evidence:c.state_after_exit.evidence.length, retry:c.retry.outcome};
}
const data = {
  engineering:{base:suite("Base smoke tests"),candidate:suite("Candidate with implementation tests"),review:suite("Candidate with independent review tests"),fixed:suite("Combined revision tests"),conflictExit:conflict.match(/^exit (\d+)/m)[1],fixedExit:fixed.match(/^exit (\d+)/m)[1]},
  research:{query:base.query,expected:base.expected,baseline:{ids:base.ranked.map(x=>x.id),recall:base.recall,meanRecall:holdout.baseline.metrics.macro_recall,precision:holdout.baseline.metrics.macro_precision},candidate:{ids:candidate.ranked.map(x=>x.id),recall:candidate.recall,meanRecall:holdout.candidate.metrics.macro_recall,precision:holdout.candidate.metrics.macro_precision},decision:holdout.decision},
  automation:{before:crash("before-draft-commit"),after:crash("after-draft-commit")}
};
fs.writeFileSync(path.join(root, "assets/run-viewer-data.js"), "window.RUN_VIEWER_DATA = " + JSON.stringify(data, null, 2) + ";\n");
async function main() {
  const browser = await puppeteer.launch({executablePath:process.env.BROWSER_EXECUTABLE || undefined, headless:true, pipe:true,args:process.env.AUDIT_CHROME_ARGS ? JSON.parse(process.env.AUDIT_CHROME_ARGS) : []});
  try {
    const page = await browser.newPage();
    const errors = [], requests = [];
    page.on("pageerror", error => errors.push(error.message));
    await page.setRequestInterception(true);
    page.on("request", request => {
      if (!/^(file|data|blob):/.test(request.url())) {requests.push(request.url()); request.abort();}
      else request.continue();
    });
    await page.setViewport({width:1100,height:900,deviceScaleFactor:2});
    await page.goto(pathToFileURL(path.join(root,"run-viewer.html")).href,{waitUntil:"load"});
    await page.evaluate(() => document.fonts.ready);
    const directory = path.join(root,"assets/screenshots");
    fs.mkdirSync(directory,{recursive:true});
    const manifest = [];
    for (const type of ["engineering","research","automation"]) {
      await page.select("#run-select",type);
      await page.waitForSelector(".run-panel h3");
      const target = await page.$("#run-panel");
      assert(target, "Missing run viewer");
      const file = "assets/screenshots/" + type + "-run.png";
      await target.screenshot({path:path.join(root,file)});
      manifest.push({id:type,file,caption:"Local run viewer. Recorded " + type + " output.",source:{engineering:"workshops/engineering/evidence/run.txt",research:"workshops/research/records/holdout-report.json",automation:"workshops/automation/results/replay.json"}[type]});
      console.log("Captured " + file);
    }
    assert.deepEqual(errors,[]); assert.deepEqual(requests,[]);
    fs.writeFileSync(path.join(root,"data/screenshots.json"),JSON.stringify(manifest,null,2)+"\n");
  } finally {await browser.close();}
}
main().catch(error=>{console.error(error.stack);process.exitCode=1;});
