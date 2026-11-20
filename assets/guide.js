"use strict";

(() => {
  const input = document.querySelector("#guide-search");
  const group = document.querySelector("#search-group");
  const region = document.querySelector("#search-results");
  const status = document.querySelector("#search-status");
  const limit = 12;

  function words(value) {
    return value.toLowerCase().match(/[\p{L}\p{N}]+/gu) || [];
  }

  function localLink(value) {
    return /^[\w-]+\.html(?:#[\w-]+)?$/.test(value);
  }

  if (input && group && region && status) {
    const index = (window.GUIDE_INDEX || []).filter(record => localLink(record.href)).map(record => ({
      ...record,
      heading: new Set(words(record.title + " " + record.section)),
      body: new Set(words(record.text)),
    }));

    function score(record, terms) {
      let total = 0;
      for (const term of terms) {
        if (record.heading.has(term)) total += 5;
        else if (record.body.has(term)) total += 3;
        else if ([...record.heading].some(word => word.startsWith(term))) total += 2;
        else if ([...record.body].some(word => word.startsWith(term))) total += 1;
        else return -1;
      }
      return total;
    }

    function hideResults() {
      region.hidden = true;
      input.setAttribute("aria-expanded", "false");
      status.textContent = "";
    }

    function renderResults() {
      const terms = [...new Set(words(input.value.slice(0, 240)))];
      region.replaceChildren();
      if (!terms.length && !group.value) {
        hideResults();
        return;
      }
      const matches = index
        .filter(record => !group.value || record.group === group.value)
        .map(record => ({ record, score: score(record, terms) }))
        .filter(match => match.score >= 0)
        .sort((a, b) => b.score - a.score);
      const list = document.createElement("ul");
      for (const { record } of matches.slice(0, limit)) {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = record.href;
        link.textContent = record.section ? record.title + " · " + record.section : record.title;
        item.append(link);
        list.append(item);
      }
      if (list.childElementCount) region.append(list);
      region.hidden = !matches.length;
      input.setAttribute("aria-expanded", String(!region.hidden));
      if (!matches.length) status.textContent = "No results.";
      else if (matches.length > limit) status.textContent = "First " + limit + " of " + matches.length + " results.";
      else status.textContent = matches.length + (matches.length === 1 ? " result." : " results.");
    }

    input.setAttribute("aria-controls", region.id);
    input.addEventListener("input", renderResults);
    group.addEventListener("change", renderResults);
    input.addEventListener("keydown", event => {
      if (event.key === "ArrowDown" || event.key === "Enter") {
        if (region.hidden) renderResults();
        const first = region.querySelector("a");
        if (!region.hidden && first) {
          event.preventDefault();
          if (event.key === "Enter") first.click();
          else first.focus();
        }
      }
    });
    region.addEventListener("keydown", event => {
      const links = [...region.querySelectorAll("a")];
      const position = links.indexOf(document.activeElement);
      if (event.key === "ArrowDown" && position < links.length - 1) {
        event.preventDefault();
        links[position + 1].focus();
      }
      if (event.key === "ArrowUp" && position >= 0) {
        event.preventDefault();
        (links[position - 1] || input).focus();
      }
    });
    document.addEventListener("keydown", event => {
      if (event.key !== "Escape" || region.hidden) return;
      if (region.contains(document.activeElement)) input.focus();
      hideResults();
    });
    renderResults();
  }

  function legacyCopy(value) {
    const field = document.createElement("textarea");
    field.value = value;
    field.readOnly = true;
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.append(field);
    field.select();
    try {
      return document.execCommand("copy");
    } finally {
      field.remove();
    }
  }

  for (const code of document.querySelectorAll("pre code")) {
    const pre = code.closest("pre");
    if (pre.dataset.copyControl) continue;
    pre.dataset.copyControl = "true";
    const controls = document.createElement("div");
    controls.className = "copy-controls";
    const button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", "Copy code block");
    const message = document.createElement("span");
    message.className = "copy-status";
    message.setAttribute("role", "status");
    controls.append(button, message);
    pre.before(controls);

    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-busy") === "true") return;
      button.setAttribute("aria-busy", "true");
      message.textContent = "";
      let copied = false;
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          try {
            await navigator.clipboard.writeText(code.textContent);
            copied = true;
          } catch {
            copied = legacyCopy(code.textContent);
          }
        } else {
          copied = legacyCopy(code.textContent);
        }
      } catch {
        copied = false;
      }
      button.removeAttribute("aria-busy");
      if (copied) {
        message.textContent = "Copied.";
        if (document.activeElement === document.body) button.focus({ preventScroll: true });
      } else {
        message.textContent = "Copy unavailable. The code is selected for manual copy.";
        pre.tabIndex = -1;
        pre.focus({ preventScroll: true });
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    });
  }
})();
