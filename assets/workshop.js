"use strict";

(() => {
  // Scope saved state to the local chapter path, including its parent folders.
  const chapter = document.querySelector("main[data-workshop-progress]");
  if (!chapter) return;
  const storageKey = "guide.workshop.v1:" + location.pathname;
  let state = { completed: {}, bookmark: "" };
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "null");
    if (saved && typeof saved === "object") {
      if (saved.completed && typeof saved.completed === "object") state.completed = saved.completed;
      if (typeof saved.bookmark === "string") state.bookmark = saved.bookmark;
    }
  } catch { /* The chapter remains usable when storage is unavailable. */ }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); return true; }
    catch { return false; }
  }

  const headings = [...chapter.querySelectorAll("h2[id]")].filter(h => !h.closest("#find"));
  if (headings.length) {
    const existingContents = chapter.querySelector(".contents");
    const nav = existingContents || document.createElement("nav");
    if (!existingContents) {
      nav.className = "workshop-contents";
      nav.setAttribute("aria-label", "In this chapter");
    }
    const title = document.createElement("p");
    title.className = "workshop-label";
    title.textContent = "In this chapter";
    const list = document.createElement("ol");
    headings.forEach(heading => {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = "#" + encodeURIComponent(heading.id);
      link.textContent = heading.textContent;
      item.append(link);
      list.append(item);
    });
    const resume = document.createElement("a");
    resume.className = "workshop-resume";
    function updateResume() {
      const heading = headings.find(h => h.id === state.bookmark);
      resume.hidden = !heading;
      if (heading) {
        resume.href = "#" + encodeURIComponent(heading.id);
        resume.textContent = "Resume: " + heading.textContent;
      }
    }
    updateResume();
    if (existingContents) {
      nav.after(resume);
    } else {
      nav.append(title, list, resume);
      (chapter.querySelector(".title") || headings[0]).after(nav);
    }
    headings.forEach(heading => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "workshop-bookmark";
      button.textContent = "Save section";
      button.setAttribute("aria-label", "Save section: " + heading.textContent);
      const status = document.createElement("span");
      status.className = "workshop-status";
      status.setAttribute("role", "status");
      button.addEventListener("click", () => {
        state.bookmark = heading.id;
        status.textContent = save() ? "Section saved." : "Local storage is unavailable.";
        updateResume();
      });
      heading.after(button, status);
    });
  }

  const checkboxes = [...chapter.querySelectorAll('input[type="checkbox"][data-progress-key]')];
  if (chapter.hasAttribute("data-workshop-progress") && checkboxes.length) {
    checkboxes.forEach(box => {
      const key = box.dataset.progressKey;
      if (!key) return;
      box.checked = state.completed[key] === true;
      box.addEventListener("change", () => {
        state.completed[key] = box.checked;
        if (!save()) progressStatus.textContent = "Local storage is unavailable.";
        else progressStatus.textContent = "Progress saved.";
      });
    });
    const controls = document.createElement("div");
    controls.className = "workshop-progress";
    const clear = document.createElement("button");
    clear.type = "button";
    clear.textContent = "Clear chapter progress";
    const progressStatus = document.createElement("span");
    progressStatus.className = "workshop-status";
    progressStatus.setAttribute("role", "status");
    clear.addEventListener("click", () => {
      state.completed = {};
      checkboxes.forEach(box => { box.checked = false; });
      progressStatus.textContent = save() ? "Chapter progress cleared." : "Local storage is unavailable.";
    });
    controls.append(clear, progressStatus);
    const nav = chapter.querySelector(".workshop-contents, .contents");
    if (nav) nav.after(controls);
    else chapter.prepend(controls);
  }

  chapter.querySelectorAll("table").forEach(table => {
    if (table.closest(".table-scroll, .table-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "table-scroll";
    wrap.setAttribute("role", "region");
    const caption = table.querySelector("caption");
    wrap.setAttribute("aria-label", caption ? "Scrollable table: " + caption.textContent.trim() : "Scrollable data table");
    wrap.tabIndex = 0;
    table.before(wrap);
    wrap.append(table);
  });
})();
