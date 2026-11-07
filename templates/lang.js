/* Language menu and the "available in your language" hint. Never redirects. */
(function () {
  "use strict";
  var HINTS = /*HINTS*/{};
  var KEY = "gantry-lang-hint";

  document.querySelectorAll("details.lang-menu").forEach(function (menu) {
    document.addEventListener("click", function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    menu.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
  });

  var current = document.documentElement.lang;
  var links = {};
  document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function (l) {
    var code = l.getAttribute("hreflang");
    if (HINTS[code]) links[code] = l.getAttribute("href");
  });

  function match(tag) {
    var t = String(tag || "").toLowerCase();
    var codes = Object.keys(links);
    for (var i = 0; i < codes.length; i++) if (codes[i].toLowerCase() === t) return codes[i];
    var base = t.split("-")[0];
    if (base === "sr") return /latn/.test(t) ? "sr-Latn" : "sr";
    if (base === "no" || base === "nn") base = "nb";
    for (var j = 0; j < codes.length; j++) if (codes[j].toLowerCase().split("-")[0] === base) return codes[j];
    return null;
  }

  var wanted = null;
  var prefs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
  for (var k = 0; k < prefs.length && !wanted; k++) wanted = match(prefs[k]);
  if (!wanted || wanted === current || !links[wanted]) return;
  try { if (localStorage.getItem(KEY) === wanted) return; } catch (e) {}

  var h = HINTS[wanted];
  var bar = document.createElement("div");
  bar.className = "lang-hint";
  bar.setAttribute("role", "region");
  bar.setAttribute("lang", wanted);
  bar.setAttribute("aria-label", h.hint_text);
  var p = document.createElement("p");
  p.textContent = h.hint_text + " ";
  var a = document.createElement("a");
  a.href = new URL(links[wanted]).pathname;
  a.hreflang = wanted;
  a.textContent = h.hint_link;
  p.appendChild(a);
  var close = document.createElement("button");
  close.type = "button";
  close.className = "lang-hint-close";
  close.setAttribute("aria-label", h.hint_close);
  close.textContent = "×";
  close.addEventListener("click", function () {
    try { localStorage.setItem(KEY, wanted); } catch (e) {}
    bar.remove();
  });
  bar.appendChild(p);
  bar.appendChild(close);
  document.body.appendChild(bar);
})();
