mermaid.initialize({
  startOnLoad: false,
  theme: "dark",
  securityLevel: "strict",
});

function repairRemoteIncludeUrl(url) {
  if (!url) {
    return url;
  }

  const localOrigin = window.location.origin;

  const malformedPrefixes = [
    `${localOrigin}http://`,
    `${localOrigin}https://`,
    `${localOrigin}/http://`,
    `${localOrigin}/https://`,
  ];

  for (const prefix of malformedPrefixes) {
    if (url.startsWith(prefix)) {
      const externalUrl = url.slice(
        prefix.startsWith(`${localOrigin}/`)
          ? localOrigin.length + 1
          : localOrigin.length
      );

      return new URL(externalUrl).href;
    }
  }

  return url;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function renderMermaidDiagrams(hook) {
  hook.doneEach(function () {
    const diagrams = document.querySelectorAll(".mermaid");
    if (diagrams.length) {
      mermaid.run({ nodes: diagrams }).catch((error) => {
        console.error("Unable to render Mermaid diagrams", error);
      });
    }
  });
}

window.$docsify = {
  name: "FINT",
  logo: "/_media/fint-novari.svg",
  homepage: "home.md",

  auto2top: true,
  nativeEmoji: true,
  executeScript: false,

  loadSidebar: true,
  subMaxLevel: 2,

  loadNavbar: true,
  coverpage: true,

  alias: {
    "/.*/_navbar.md": "/_navbar.md",
  },

  markdown: {
    renderer: {
      image(token) {
        const href = repairRemoteIncludeUrl(token.href);
        // Docsify otherwise prefixes root-relative Markdown images with the current route.
        const source = href.startsWith("/") && !href.startsWith("//")
          ? new URL(href, window.location.origin).href
          : href;
        const markup = this.origin.image.call(this, {
          ...token,
          href: source,
        });
        const template = document.createElement("template");
        template.innerHTML = markup;
        const image = template.content.querySelector("img");
        if (image && new URL(image.src, window.location.href).origin !== window.location.origin) {
          image.crossOrigin = "anonymous";
        }
        return template.innerHTML;
      },

      link(token) {
        return this.origin.link.call(this, {
          ...token,
          href: repairRemoteIncludeUrl(token.href),
        });
      },

      code({ text, lang }) {
        if (lang === "mermaid") {
          return `<div class="mermaid">${escapeHtml(text)}</div>`;
        }

        return this.origin.code.apply(this, arguments);
      },
    },
  },

  plugins: [
    renderMermaidDiagrams,
  ],

  search: {
    paths: "auto",
    placeholder: "Søk",
    noData: "Sorry, men vi fant ingenting 😔",
    depth: 2,
  },

  plantuml: {
    skin: "default",
    serverPath: "https://www.plantuml.com/plantuml/svg/",
  },
};
