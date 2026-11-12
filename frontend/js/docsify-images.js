// Load after the CDN plugins, before Docsify starts on DOMContentLoaded.
(() => {
  function anonymousImages(html) {
    const template = document.createElement("template");
    template.innerHTML = html;
    template.content.querySelectorAll("img[src]").forEach((image) => {
      if (new URL(image.src, window.location.href).origin !== window.location.origin) {
        image.crossOrigin = "anonymous";
      }
    });
    return template.innerHTML;
  }

  // PlantUML uses this public helper to build detached elements. Add CORS while
  // the markup is still inert, before those image elements can start requests.
  const create = Docsify.dom.create;
  Docsify.dom.create = function (tag, html) {
    return create(tag, typeof html === "string" ? anonymousImages(html) : html);
  };

  // Register last so raw HTML and images produced by other plugins are covered.
  window.$docsify.plugins.push(function (hook) {
    hook.afterEach(anonymousImages);
  });
})();
