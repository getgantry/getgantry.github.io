/* Language menu and the "available in your language" hint. Never redirects. */
(function () {
  "use strict";
  var HINTS = {"en":{"hint_text":"This page is also available in English.","hint_link":"Read in English","hint_close":"Close"},"de":{"hint_text":"Diese Seite gibt es auch auf Deutsch.","hint_link":"Auf Deutsch lesen","hint_close":"Schließen"},"fr":{"hint_text":"Cette page existe aussi en français.","hint_link":"Lire en français","hint_close":"Fermer"},"es":{"hint_text":"Esta página también está disponible en español.","hint_link":"Leer en español","hint_close":"Cerrar"},"it":{"hint_text":"Questa pagina è disponibile anche in italiano.","hint_link":"Leggi in italiano","hint_close":"Chiudi"},"pt-PT":{"hint_text":"Esta página também está disponível em português.","hint_link":"Ler em português","hint_close":"Fechar"},"nl":{"hint_text":"Deze pagina is ook beschikbaar in het Nederlands.","hint_link":"Lees in het Nederlands","hint_close":"Sluit"},"sv":{"hint_text":"Den här sidan finns även på svenska.","hint_link":"Läs på svenska","hint_close":"Stäng"},"da":{"hint_text":"Denne side findes også på dansk.","hint_link":"Læs på dansk","hint_close":"Luk"},"nb":{"hint_text":"Denne siden finnes også på norsk.","hint_link":"Les på norsk","hint_close":"Lukk"},"fi":{"hint_text":"Tämä sivu on saatavilla myös suomeksi.","hint_link":"Lue suomeksi","hint_close":"Sulje"},"pl":{"hint_text":"Ta strona jest dostępna także po polsku.","hint_link":"Czytaj po polsku","hint_close":"Zamknij"},"cs":{"hint_text":"Tato stránka je k dispozici také v češtině.","hint_link":"Číst česky","hint_close":"Zavřít"},"sk":{"hint_text":"Táto stránka je k dispozícii aj v slovenčine.","hint_link":"Čítať po slovensky","hint_close":"Zavrieť"},"hu":{"hint_text":"Ez az oldal magyarul is elérhető.","hint_link":"Olvasás magyarul","hint_close":"Bezárás"},"ro":{"hint_text":"Această pagină este disponibilă și în limba română.","hint_link":"Citiți în română","hint_close":"Închide"},"bg":{"hint_text":"Тази страница е достъпна и на български.","hint_link":"Прочетете на български","hint_close":"Затвори"},"el":{"hint_text":"Αυτή η σελίδα είναι διαθέσιμη και στα ελληνικά.","hint_link":"Διαβάστε στα ελληνικά","hint_close":"Κλείσιμο"},"hr":{"hint_text":"Ova je stranica dostupna i na hrvatskom.","hint_link":"Čitaj na hrvatskom","hint_close":"Zatvori"},"sl":{"hint_text":"Ta stran je na voljo tudi v slovenščini.","hint_link":"Beri v slovenščini","hint_close":"Zapri"},"sr":{"hint_text":"Ова страница постоји и на српском.","hint_link":"Читај на српском","hint_close":"Затвори"},"sr-Latn":{"hint_text":"Ova stranica postoji i na srpskom.","hint_link":"Čitaj na srpskom","hint_close":"Zatvori"},"lt":{"hint_text":"Šį puslapį galima skaityti ir lietuvių kalba.","hint_link":"Skaityti lietuviškai","hint_close":"Uždaryti"},"lv":{"hint_text":"Šī lapa ir pieejama arī latviešu valodā.","hint_link":"Lasīt latviski","hint_close":"Aizvērt"},"et":{"hint_text":"See leht on saadaval ka eesti keeles.","hint_link":"Loe eesti keeles","hint_close":"Sulge"},"uk":{"hint_text":"Ця сторінка доступна й українською мовою.","hint_link":"Читати українською","hint_close":"Закрити"},"ru":{"hint_text":"Эта страница есть и на русском языке.","hint_link":"Читать на русском","hint_close":"Закрыть"}};
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
