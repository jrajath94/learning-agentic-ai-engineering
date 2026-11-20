"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { fileURLToPath, pathToFileURL } = require("node:url");
const puppeteer = require(process.env.PUPPETEER_PATH || "puppeteer");
const root = path.resolve(__dirname, "..");
const chapters = ["workshop-engineering.html", "workshop-research.html", "workshop-automation.html", "community.html", "resource-study.html", "workflow-kit.html", "social-practice.html", "run-viewer.html"];

async function main() {
  for (const name of chapters) assert(fs.existsSync(path.join(root, name)), "Missing chapter: " + name);
  const browser = await puppeteer.launch({
    executablePath: process.env.BROWSER_EXECUTABLE || undefined,
    headless: true,
    pipe: true,
    args: process.env.AUDIT_CHROME_ARGS ? JSON.parse(process.env.AUDIT_CHROME_ARGS) : []
  });
  const errors = [];
  const blocked = [];
  try {
    const page = await browser.newPage();
    page.on("pageerror", error => errors.push(error.message));
    await page.setRequestInterception(true);
    page.on("request", request => {
      if (!/^(file|data|blob):/.test(request.url())) {
        blocked.push(request.url());
        request.abort();
      } else request.continue();
    });
    const anchors = new Map();
    for (const name of chapters) {
      console.log("Checking " + name);
      await page.goto(pathToFileURL(path.join(root, name)).href, { waitUntil: "load" });
      const audit = await page.evaluate(async () => {
        for (const image of document.images) image.loading = "eager";
        await Promise.all([...document.images].map(image => image.decode()));
        return {
          links: [...document.querySelectorAll('a[href]')].map(a => ({href: a.href, download: a.hasAttribute("download")})),
          diagrams: [...document.querySelectorAll('a[href$=".mmd"]')].map(a => ({
            source: a.href,
            image: a.closest("figure")?.querySelector('img[src$=".svg"]')?.src || [...document.images].find(i => i.src === a.href.replace(/\.mmd$/, ".svg"))?.src || "",
            alt: a.closest("figure")?.querySelector('img[src$=".svg"]')?.alt || [...document.images].find(i => i.src === a.href.replace(/\.mmd$/, ".svg"))?.alt || ""
          })),
          blocks: [...document.querySelectorAll("pre code")].map(code => code.textContent),
          buttons: document.querySelectorAll(".copy-button").length
        };
      });
      assert.equal(audit.buttons, audit.blocks.length, name + ": code copy controls");
      for (const [i, block] of audit.blocks.entries()) {
        assert(block.trim().length, name + ": empty code block");
        await page.evaluate(() => Object.defineProperty(navigator, "clipboard", {configurable:true, value:{writeText:async value => {window.testCopied = value;}}}));
        await page.evaluate(index => document.querySelectorAll(".copy-button")[index].click(), i);
        await page.waitForFunction(() => typeof window.testCopied === "string");
        assert.equal(await page.evaluate(() => window.testCopied), block, name + ": copied code differs");
        await page.evaluate(() => { delete window.testCopied; });
      }
      for (const diagram of audit.diagrams) {
        assert(diagram.image && diagram.alt, name + ": diagram needs a visible SVG and alt text");
        assert.equal(diagram.image.replace(/\.svg$/, ".mmd"), diagram.source, name + ": diagram source mismatch");
        const svg = fs.readFileSync(fileURLToPath(diagram.image), "utf8");
        assert(/<svg\b/.test(svg) && /(?:<text\b|<foreignObject\b|<path\b)/.test(svg), name + ": empty SVG");
        assert(!/Syntax error|mermaid version/i.test(svg), name + ": diagram render error");
      }
      for (const link of audit.links) {
        const url = new URL(link.href);
        if (url.protocol !== "file:") continue;
        url.hash = "";
        const target = fileURLToPath(url);
        assert(fs.existsSync(target), name + ": missing local link " + target);
        if (link.download) assert(fs.statSync(target).isFile() && fs.statSync(target).size > 0, name + ": empty download");
        const fragment = new URL(link.href).hash;
        if (fragment && target.endsWith(".html")) {
          if (!anchors.has(target)) {
            const html = fs.readFileSync(target, "utf8");
            anchors.set(target, await page.evaluate(source => [...new DOMParser().parseFromString(source, "text/html").querySelectorAll("[id]")].map(n => n.id), html));
          }
          assert(anchors.get(target).includes(decodeURIComponent(fragment.slice(1))), name + ": missing link target " + link.href);
        }
      }
      await page.setViewport({width:360, height:850});
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1), name + ": page overflow");
    }
    await page.goto(pathToFileURL(path.join(root, "run-viewer.html")).href, {waitUntil:"load"});
    for (const [value, expected] of [["engineering", "Combined revision suite"], ["research", "retain baseline"], ["automation", "draft_staged"]]) {
      await page.select("#run-select", value);
      assert((await page.$eval("#run-panel", node => node.textContent)).includes(expected), "Recorded run view did not change");
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1), "Recorded run view overflow");
      const disclosure = await page.$("#run-panel details");
      await disclosure.evaluate(node => {node.open = true;});
      assert(await disclosure.evaluate(node => node.open), "Prediction answer did not open");
    }
    const workshop = chapters[0];
    await page.goto(pathToFileURL(path.join(root, workshop)).href, {waitUntil:"load"});
    assert(await page.$('main[data-workshop-progress] input[data-progress-key]'), "Missing opt-in progress checkbox");
    await page.focus('main[data-workshop-progress] input[data-progress-key]');
    const before = await page.$eval('main[data-workshop-progress] input[data-progress-key]', n => n.checked);
    await page.keyboard.press("Space");
    assert.notEqual(await page.$eval('main[data-workshop-progress] input[data-progress-key]', n => n.checked), before);
    const saved = !before;
    await page.reload({waitUntil:"load"});
    assert.equal(await page.$eval('main[data-workshop-progress] input[data-progress-key]', n => n.checked), saved, "Progress did not persist");
    await page.focus(".workshop-bookmark");
    await page.keyboard.press("Enter");
    await page.reload({waitUntil:"load"});
    assert(await page.$eval(".workshop-resume", n => !n.hidden && n.hash.length > 1), "Section bookmark did not persist");
    await page.evaluate(() => [...document.querySelectorAll(".workshop-progress button")].find(b => b.textContent === "Clear chapter progress").click());
    assert(await page.$$eval('main[data-workshop-progress] input[data-progress-key]', boxes => boxes.every(b => !b.checked)), "Progress did not clear");
    await page.reload({waitUntil:"load"});
    assert(await page.$$eval('main[data-workshop-progress] input[data-progress-key]', boxes => boxes.every(b => !b.checked)), "Cleared progress did not persist");
    assert(await page.$eval(".workshop-resume", n => !n.hidden), "Clear removed the section bookmark");
    assert.deepEqual(errors, [], "Browser errors");
    assert.deepEqual(blocked, [], "Network requests");
    console.log(chapters.length + " chapters passed offline asset, link, copy, and progress checks.");
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error.stack); process.exitCode = 1; });
