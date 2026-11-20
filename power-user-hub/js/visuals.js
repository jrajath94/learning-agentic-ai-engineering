const MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
const LIB_URL = "https://cdn.jsdelivr.net/npm/markmap-lib@0.18.12/+esm";
const VIEW_URL = "https://cdn.jsdelivr.net/npm/markmap-view@0.18.12/+esm";

function fail(node, err) {
  const p = document.createElement("p");
  p.className = "note";
  p.textContent = "Diagram failed to load from the CDN. The source is still in the page. " + (err && err.message ? err.message: "");
  node.insertAdjacentElement("afterend", p);
}

async function renderMermaid() {
  const blocks = document.querySelectorAll(".mermaid");
  if (!blocks.length) return;
  try {
    const mermaid = (await import(MERMAID_URL)).default;
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      fontFamily: "Plus Jakarta Sans, sans-serif",
      themeVariables: {
        darkMode: true,
        background: "#000000",
        primaryColor: "#141414",
        primaryTextColor: "#f4f1ea",
        primaryBorderColor: "#e0b15b",
        secondaryColor: "#101010",
        secondaryTextColor: "#f4f1ea",
        tertiaryColor: "#0c0c0c",
        tertiaryTextColor: "#f4f1ea",
        lineColor: "#e0b15b",
        textColor: "#f4f1ea",
        mainBkg: "#141414",
        nodeBorder: "#e0b15b",
        clusterBkg: "#0c0c0c",
        clusterBorder: "#2a2a2a",
        titleColor: "#f4f1ea",
        actorBkg: "#141414",
        actorBorder: "#e0b15b",
        actorTextColor: "#f4f1ea",
        signalColor: "#e0b15b",
        signalTextColor: "#f4f1ea",
        labelBoxBkgColor: "#141414",
        labelBoxBorderColor: "#e0b15b",
        labelTextColor: "#f4f1ea",
        loopTextColor: "#f4f1ea",
        noteBkgColor: "#1a1a1a",
        noteTextColor: "#f4f1ea",
        noteBorderColor: "#e0b15b",
        activationBkgColor: "#2a2418",
        activationBorderColor: "#e0b15b",
        sequenceNumberColor: "#000000"
      }
    });
    await mermaid.run({ nodes: blocks });
  } catch (err) {
    blocks.forEach((node) => fail(node, err));
  }
}

async function renderMarkmap() {
  const scripts = document.querySelectorAll('script[type="text/markmap"]');
  if (!scripts.length) return;
  try {
    const { Transformer } = await import(LIB_URL);
    const { Markmap } = await import(VIEW_URL);
    const transformer = new Transformer();
    scripts.forEach((script) => {
      const svg = script.previousElementSibling;
      if (!svg || svg.tagName.toLowerCase() !== "svg") return;
      const { root } = transformer.transform(script.textContent);
      Markmap.create(svg, {
        color: () => "#e0b15b",
        duration: 0,
        paddingX: 16,
        maxWidth: 280
      }, root);
      svg.style.setProperty("--markmap-text-color", "#f4f1ea");
      svg.style.setProperty("--markmap-code-color", "#f4f1ea");
      svg.style.setProperty("--markmap-code-bg", "#141414");
      svg.style.setProperty("--markmap-circle-open-bg", "#000");
    });
  } catch (err) {
    scripts.forEach((node) => fail(node, err));
  }
}

renderMermaid();
renderMarkmap();
