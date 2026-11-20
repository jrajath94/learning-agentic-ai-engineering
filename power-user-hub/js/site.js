(function () {
  var path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav a").forEach(function (a) {
    if (a.getAttribute("href") === path) a.setAttribute("aria-current", "page");
  });

  var q = document.getElementById("q");
  if (q && location.pathname.endsWith("search.html")) {
    var params = new URLSearchParams(location.search);
    if (params.get("q")) q.value = params.get("q");
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
      var box = document.getElementById("q");
      if (box) { e.preventDefault(); box.focus(); }
    }
  });

  var pageFilter = document.getElementById("pagefilter");
  if (pageFilter) {
    pageFilter.addEventListener("input", function () {
      var needle = pageFilter.value.trim().toLowerCase();
      document.querySelectorAll("main .section, main .card, main .prompt, main .person, main .wf, main tbody tr").forEach(function (el) {
        var hay = (el.innerText || "").toLowerCase();
        el.classList.toggle("hidden", needle.length > 1 && hay.indexOf(needle) === -1);
      });
    });
  }

  function runSearch() {
    var root = document.getElementById("results");
    if (!root || !window.HUB_INDEX) return;
    var needle = (q && q.value || "").trim().toLowerCase();
    var cluster = (document.getElementById("cluster") || {}).value || "";
    var rows = window.HUB_INDEX.filter(function (item) {
      var blob = (item.title + " " + item.text + " " + item.cluster).toLowerCase();
      if (needle && blob.indexOf(needle) === -1) return false;
      if (cluster && item.cluster !== cluster) return false;
      return true;
    });
    root.innerHTML = rows.map(function (item) {
      return '<article class="card"><p class="kicker">' + item.cluster + '</p><h3><a href="' + item.href + '">' + item.title + '</a></h3><p>' + item.text + '</p></article>';
    }).join("") || '<p class="muted">No matches. Try a product name, a person, or a claim id such as C12.</p>';
    var count = document.getElementById("count");
    if (count) count.textContent = rows.length + " entries";
  }

  if (document.getElementById("results")) {
    if (q) q.addEventListener("input", runSearch);
    var cluster = document.getElementById("cluster");
    if (cluster) cluster.addEventListener("change", runSearch);
    runSearch();
  }

  document.querySelectorAll("[data-ledger]").forEach(function (node) {
    var claims = window.HUB_CLAIMS || [];
    var cluster = node.getAttribute("data-ledger") || "";
    var kind = node.getAttribute("data-kind") || "";
    var rows = claims.filter(function (c) {
      if (cluster && c.cluster !== cluster) return false;
      if (kind && c.independence !== kind) return false;
      return true;
    });
    var html = '<table><thead><tr><th>Id</th><th>Claim</th><th>Source</th><th>Conf.</th></tr></thead><tbody>';
    rows.forEach(function (c) {
      html += '<tr id="' + c.id + '"><td><a href="sources.html#' + c.id + '">' + c.id + '</a></td><td>' + c.claim + '</td><td><a href="' + c.url + '">' + c.source_title + '</a><br><span class="muted">' + c.author + ' · ' + c.date + ' · ' + c.independence + '</span></td><td>' + c.confidence + '</td></tr>';
    });
    html += '</tbody></table>';
    node.innerHTML = html;
  });
})();
