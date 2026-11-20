"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const assert = require("node:assert/strict");
const puppeteer = require(process.env.PUPPETEER_PATH || "puppeteer");
const root = path.resolve(__dirname, "..");
const output = path.resolve(process.argv[2] || "browser-check");
fs.mkdirSync(output, {recursive:true});
const files = fs.readdirSync(root).filter(f => f.endsWith(".html")).sort();

async function main() {
  const browser = await puppeteer.launch({
    executablePath:process.env.BROWSER_EXECUTABLE || undefined,
    headless:true, pipe:true, args: process.env.AUDIT_CHROME_ARGS ? JSON.parse(process.env.AUDIT_CHROME_ARGS) : []
  });
  const report = {browser:await browser.version(), widths:[360,768,1440], pages:{}, controls:{}};
  try {
    const tab = await browser.newPage();
    const errors = [];
    const external = [];
    tab.on("pageerror", error => errors.push(error.message));
    await tab.setRequestInterception(true);
    tab.on("request", req => {
      if (/^https?:/.test(req.url())) { external.push(req.url()); req.abort(); }
      else req.continue();
    });
    const open = async name => tab.goto(pathToFileURL(path.join(root,name)).href, {waitUntil:"load"});
    for (const name of files) {
      await open(name);
      report.pages[name] = [];
      for (const width of report.widths) {
        await tab.setViewport({width,height:850,deviceScaleFactor:1});
        const row = await tab.evaluate(async () => {
          for (const i of document.images) i.loading = "eager";
          const loaded = await Promise.allSettled([...document.images].map(i=>i.decode()));
          await document.fonts.ready;
          const d = document.documentElement;
          return {
            width:innerWidth,overflow:d.scrollWidth>d.clientWidth+1,
            brokenImages:loaded.filter(r=>r.status==="rejected").length, figures:document.querySelectorAll("main figure").length,
            registeredMaps:document.querySelectorAll("[data-markmap] svg").length,
            h1:document.querySelectorAll("h1").length, main:document.querySelectorAll("main").length,
            black:getComputedStyle(document.body).backgroundColor==="rgb(0, 0, 0)",
            fonts:[...document.fonts].filter(f=>f.status==="loaded").map(f=>f.family),
            justified:getComputedStyle(document.querySelector("main p")).textAlign==="justify",
            imagesHaveAlt:[...document.images].every(i=>i.alt.length>0),
            mobileNav:getComputedStyle(document.querySelector("#navigation")).display!=="none",
            emDash:document.querySelector("main").textContent.includes("—"),
            copyComplete:document.querySelectorAll("pre code").length===document.querySelectorAll(".copy-button").length
          };
        });
        report.pages[name].push(row);
        if(width!==768) await tab.screenshot({path:path.join(output,name+"-"+width+".png")});
      }
    }
    await open("index.html");
    await tab.setViewport({width:360,height:800});
    await tab.focus("#navigation summary"); await tab.keyboard.press("Enter");
    report.controls.mobileKeyboard = await tab.$eval("#navigation",n=>n.open);
    await tab.select("#search-group","Practice"); await tab.type("#guide-search","invoice");
    const hits=await tab.$$eval("#search-results a",ns=>ns.map(n=>n.getAttribute("href")));
    assert(hits.length && hits.every(h=>/^(engineering|business|labs|research)\.html/.test(h)));
    await tab.focus("#guide-search"); await tab.keyboard.press("ArrowDown");
    assert(await tab.evaluate(()=>document.activeElement.matches("#search-results a")));
    await tab.keyboard.press("Escape");
    assert(await tab.$eval("#search-results",n=>n.hidden));
    await tab.select("#search-group",""); await tab.$eval("#guide-search",n=>{n.value="zzzznoexample";n.dispatchEvent(new Event("input"));});
    report.controls.search = hits.length+" filtered results; keyboard selection, Escape, and empty search passed";
    assert(await tab.$eval("#search-status",n=>n.textContent.includes("No results")));
    await tab.click('#timeout-demo input[value=after]');
    assert(await tab.$eval("#timeout-demo output",n=>n.textContent.includes("One draft already exists")));
    await tab.click('#timeout-demo input[value=before]');
    assert(await tab.$eval("#timeout-demo output",n=>n.textContent.includes("No draft exists")));
    report.controls.timeout = "Both recovery branches passed";
    await open("prompts.html");
    await tab.evaluate(()=>{Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async value=>{window.checkedClipboard=value;}}});});
    await tab.click(".copy-button");
    assert(await tab.evaluate(()=>window.checkedClipboard===document.querySelector("pre code").textContent));
    report.controls.copy = "Copied text matched the first full prompt with an isolated clipboard test double";
    await open("labs.html");
    await tab.select("#bench-comparison select","shift");
    assert.equal(await tab.$eval('[data-model=full] meter',n=>n.value),86);
    await tab.select("#bench-comparison select","test");
    assert.equal(await tab.$eval('[data-model=full] meter',n=>n.value),290);
    report.controls.benchmark = "Both populations matched the recorded full-rule totals";
    await open("usage.html");
    await tab.select("#lanes","4");
    assert.equal(await tab.$eval("#token-totals td:last-child",n=>n.textContent),"28,800");
    await tab.select("#lanes","1");
    assert.equal(await tab.$eval("#token-totals td:last-child",n=>n.textContent),"7,200");
    report.controls.tokenBudget = "One and four branches matched the illustrative token ledger";
    await open("graphs.html");
    const mapAudit = await tab.evaluate(()=>{
      return [...document.querySelectorAll('[data-markmap]')].map(host=>{
        host.closest("details").open=true;
        const root=host.querySelector('[data-map-key]');
        const before=host.querySelectorAll('[data-map-key]').length;
        root.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));
        const collapsed=host.querySelectorAll('[data-map-key]').length;
        host.querySelector('[data-map-key]').dispatchEvent(new MouseEvent("click",{bubbles:true}));
        return {map:host.dataset.markmap,before,collapsed,restored:host.querySelectorAll('[data-map-key]').length};
      });
    });
    assert.equal(mapAudit.length,3);assert(mapAudit.every(m=>m.collapsed<m.before&&m.restored===m.before));
    report.controls.maps=mapAudit;
    report.errors=errors; report.externalRequests=external;
    fs.writeFileSync(path.join(output,"results.json"),JSON.stringify(report,null,2)+"\n");
    const defects=Object.entries(report.pages).flatMap(([name,rows])=>rows.filter(r=>r.overflow||r.brokenImages||!r.black||!r.justified||r.h1!==1||r.main!==1||!r.imagesHaveAlt||r.emDash||!r.copyComplete||r.fonts.length!==2||r.mobileNav!==(r.width<701)).map(r=>({name,...r})));
    if(defects.length || errors.length || external.length) throw new Error(JSON.stringify({defects,errors,external}));
    console.log(files.length+" pages × "+report.widths.length+" widths passed. All interaction checks passed.");
  } finally { await browser.close(); }
}
main().catch(err=>{console.error(err.stack);process.exitCode=1;});

