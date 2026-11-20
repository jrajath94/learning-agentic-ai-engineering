"use strict";

(() => {
  const outlines = {
    "task-dependencies": `# Task dependencies
## Identity
### Confirm person, product, and scope
## Research
### Collect sources and define acceptance
## Parallel work
### Experiments
#### Fix data, seeds, and metrics before runs
### Site
#### Draft claims from cited records
## Integration
### Combine outputs on one revision
## Audit
### Check claims, links, and behavior
## Retest
### Repeat checks after repairs`,
    "evidence-chain": `# Evidence chain
## Source records
### E01: repository and harness practice
### E03: evaluation design
### E07: release comparison
## Local observations
### Invoice service
#### Baseline returns 216 cents for a case that requires 217
### Sensor badge benchmark
#### Full rule scores 290 of 300 ordinary rows
#### Full rule scores 86 of 300 shifted rows
#### Sensor-only rule scores 249 of 300 shifted rows
### Support queue
#### R06 is old but closed
## Bounded recommendations
### Use exact integer rounding for invoice cents
### Test for input shift before relying on the badge
### Filter queue rows by status and age
### Stop at a human review boundary
## Limits
### Synthetic runs do not establish field performance
### A source claim does not prove local impact`,
    "learning-path": `# Learning path
## Foundations
### Tools, state, evidence, and stop rules
## Engineering
### Read the invoice contract
### Design boundary tests
### Inspect the patch and rerun checks
## Research
### Separate training and held-out rows
### Compare baseline and candidate
### Inspect errors by seed and split
## Business
### Trace claims to source rows
### Draft with citations
### Stop for human review
## Retrieval
### Recreate one rule without notes
## Transfer
### Apply the rule to new inputs
## Outcome
### Explain evidence and limits`
  };

  function makeTree(markdown) {
    const root = { label: "", children: [], depth: -1, key: "root" };
    const stack = [{ level: 0, node: root }];
    let index = 0;
    for (const line of markdown.split("\n")) {
      const match = /^(#{1,6})\s+(.+)$/.exec(line.trim());
      if (!match) continue;
      const level = match[1].length;
      const node = { label: match[2], children: [], depth: level - 1, key: `node-${index++}` };
      while (stack.length && stack[stack.length - 1].level >= level) stack.pop();
      stack[stack.length - 1].node.children.push(node);
      stack.push({ level, node });
    }
    return root;
  }

  function wrap(text, maxChars = 24) {
    const words = text.split(/\s+/);
    const lines = [];
    let line = "";
    for (const word of words) {
      const next = line ? `${line} ${word}` : word;
      if (next.length > maxChars && line) {
        lines.push(line);
        line = word;
      } else line = next;
    }
    if (line) lines.push(line);
    return lines;
  }

  function render(host, tree) {
    if (!document.getElementById("visual-outline-style")) {
      const style = document.createElement("style");
      style.id = "visual-outline-style";
      style.textContent = `
        [data-markmap] { max-width: 100%; overflow-x: auto; color: #ffffff; background: #000000; }
        [data-markmap] svg { display: block; width: 100%; min-width: 720px; height: auto; background: #000000; touch-action: pan-x pan-y; }
        [data-markmap] .map-link { fill: none; stroke: #b9e6ae; stroke-width: 2; }
        [data-markmap] .map-node rect { fill: #000000; stroke: #b9e6ae; stroke-width: 2; }
        [data-markmap] .map-node text { fill: #ffffff; font: 14px Arial, sans-serif; }
        [data-markmap] .map-node[aria-expanded="true"] rect { stroke-width: 3; }
        [data-markmap] .map-node:focus rect { stroke-width: 4; }
        [data-markmap] .map-node { cursor: pointer; outline: none; }
        [data-markmap] .map-node:focus-visible rect { stroke: #ffffff; }
      `;
      document.head.append(style);
    }
    const hostWidth = Math.max(host.clientWidth || 720, 720);
    const gapX = 230;
    const nodeW = 198;
    const top = tree.children[0];
    const collapsed = new Set();
    function closed(node) { return collapsed.has(node.key); }
    function shownChildren(node) { return closed(node) ? [] : node.children; }
    function visibleList(node) { return [node, ...shownChildren(node).flatMap(visibleList)]; }
    function setYs(node, start) {
      const children = shownChildren(node);
      if (!children.length) {
        node.y = start;
        return start + 76;
      }
      let cursor = start;
      for (const child of children) cursor = setYs(child, cursor);
      node.y = (children[0].y + children[children.length - 1].y) / 2;
      return cursor;
    }
    function redraw(focusKey) {
      const visible = visibleList(top);
      const yEnd = setYs(top, 46);
      const height = Math.max(140, yEnd + 12);
      const width = Math.max(hostWidth, (Math.max(...visible.map(n => n.depth)) + 1) * gapX + nodeW + 30);
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      svg.setAttribute("role", "tree");
      svg.setAttribute("aria-label", top.label);
      const title = document.createElementNS(svg.namespaceURI, "title");
      title.textContent = `${top.label}. Activate a branch to show or hide its child nodes.`;
      svg.append(title);
      const links = document.createElementNS(svg.namespaceURI, "g");
      links.setAttribute("aria-hidden", "true");
      for (const parent of visible) {
        for (const child of shownChildren(parent)) {
          const path = document.createElementNS(svg.namespaceURI, "path");
          const x1 = 18 + parent.depth * gapX + nodeW;
          const x2 = 18 + child.depth * gapX;
          path.setAttribute("d", `M ${x1} ${parent.y} C ${x1 + 28} ${parent.y}, ${x2 - 28} ${child.y}, ${x2} ${child.y}`);
          path.setAttribute("class", "map-link");
          links.append(path);
        }
      }
      svg.append(links);
      const nodes = document.createElementNS(svg.namespaceURI, "g");
      for (const node of visible) {
        const x = 18 + node.depth * gapX;
        const lines = wrap(node.label);
        const boxH = Math.max(42, lines.length * 18 + 16);
        const group = document.createElementNS(svg.namespaceURI, "g");
        group.setAttribute("class", "map-node");
        group.setAttribute("role", "treeitem");
        group.setAttribute("aria-level", String(node.depth + 1));
        group.setAttribute("aria-label", node.label);
        group.setAttribute("tabindex", node.key === (focusKey || top.key) ? "0" : "-1");
        if (node.children.length) group.setAttribute("aria-expanded", String(!closed(node)));
        group.setAttribute("transform", `translate(${x},${node.y - boxH / 2})`);
        const rect = document.createElementNS(svg.namespaceURI, "rect");
        rect.setAttribute("width", String(nodeW));
        rect.setAttribute("height", String(boxH));
        group.append(rect);
        const text = document.createElementNS(svg.namespaceURI, "text");
        const firstY = (boxH - (lines.length - 1) * 18) / 2 + 5;
        lines.forEach((line, i) => {
          const span = document.createElementNS(svg.namespaceURI, "tspan");
          span.setAttribute("x", String(nodeW / 2));
          span.setAttribute("y", String(firstY + i * 18));
          span.setAttribute("text-anchor", "middle");
          span.textContent = line;
          text.append(span);
        });
        group.append(text);
        const activate = () => {
          if (!node.children.length) return;
          if (closed(node)) collapsed.delete(node.key);
          else collapsed.add(node.key);
          redraw(node.key);
          host.querySelector(`[data-map-key="${node.key}"]`)?.focus();
        };
        group.setAttribute("data-map-key", node.key);
        group.addEventListener("click", activate);
        group.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            activate();
          } else if (event.key === "ArrowRight" && node.children.length && closed(node)) {
            event.preventDefault();
            activate();
          } else if (event.key === "ArrowLeft" && node.children.length && !closed(node)) {
            event.preventDefault();
            activate();
          } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            const current = visible.map(item => item.key).indexOf(node.key);
            const target = visible[Math.max(0, Math.min(visible.length - 1, current + (event.key === "ArrowDown" ? 1 : -1)))];
            host.querySelector(`[data-map-key="${target.key}"]`)?.focus();
          }
        });
        nodes.append(group);
      }
      svg.append(nodes);
      host.replaceChildren(svg);
    }
    if (top) {
      for (const child of top.children) if (child.children.length) collapsed.add(child.key);
      redraw(top.key);
    }
  }

  for (const host of document.querySelectorAll("[data-markmap]")) {
    const key = host.getAttribute("data-markmap");
    if (outlines[key]) render(host, makeTree(outlines[key]));
  }
})();
