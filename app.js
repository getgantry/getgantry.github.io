/* ===========================================================
   Gantry landing — interactions
   =========================================================== */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Nav scrolled state ---------- */
  var nav = document.getElementById("nav");
  function onScroll() {
    if (window.scrollY > 12) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Crane hero animation ---------- */
  var stage = document.getElementById("stage");
  var replay = document.getElementById("replay");
  function playCrane() {
    if (!stage) return;
    stage.classList.remove("playing");
    /* force reflow to restart animations */
    void stage.offsetWidth;
    stage.classList.add("playing");
  }
  if (replay) replay.addEventListener("click", playCrane);
  /* kick off shortly after load */
  window.addEventListener("load", function () {
    setTimeout(playCrane, 280);
  });

  /* ---------- Live GitHub star count ---------- */
  (function () {
    var el = document.getElementById("ghStars");
    if (!el) return;
    function fmt(n) {
      if (n >= 1000) {
        var s = (n / 1000).toFixed(n >= 10000 ? 0 : 1).replace(/\.0$/, "");
        return "★ " + s + "k";
      }
      return "★ " + n;
    }
    try {
      var c = JSON.parse(localStorage.getItem("gantry-stars") || "null");
      if (c && typeof c.n === "number" && Date.now() - c.t < 21600000) el.textContent = fmt(c.n);
    } catch (e) {}
    fetch("https://api.github.com/repos/getgantry/gantry", { headers: { "Accept": "application/vnd.github+json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.stargazers_count !== "number") return;
        el.textContent = fmt(d.stargazers_count);
        try { localStorage.setItem("gantry-stars", JSON.stringify({ n: d.stargazers_count, t: Date.now() })); } catch (e) {}
      })
      .catch(function () {});
  })();

  /* ---------- Copy buttons ---------- */
  document.querySelectorAll(".copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-copy") || "";
      navigator.clipboard.writeText(text).then(function () {
        var prev = b.textContent;
        b.textContent = "Copied";
        b.classList.add("done");
        setTimeout(function () { b.textContent = prev; b.classList.remove("done"); }, 1400);
      });
    });
  });

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Card hover spotlight ---------- */
  document.querySelectorAll(".cell").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty("--mx", (e.clientX - r.left) + "px");
      c.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- Parallax on screenshots ---------- */
  if (!reduce) {
    var pxEls = [].slice.call(document.querySelectorAll("[data-parallax]"));
    var ticking = false;
    function applyParallax() {
      var vh = window.innerHeight;
      pxEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var center = r.top + r.height / 2;
        var off = (center - vh / 2) / vh; /* -0.5..0.5 */
        var amt = parseFloat(el.getAttribute("data-parallax")) || 0;
        el.style.transform = "translateY(" + (off * amt * -140).toFixed(1) + "px)";
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(applyParallax); }
    }, { passive: true });
    applyParallax();
  }

  /* ---------- Sparkline builder ---------- */
  function buildSpark(values, lineId, areaId) {
    var line = document.getElementById(lineId);
    var area = areaId ? document.getElementById(areaId) : null;
    if (!line) return;
    var W = 120, H = 38, pad = 3;
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    var span = (max - min) || 1;
    var step = W / (values.length - 1);
    var pts = values.map(function (v, i) {
      var x = i * step;
      var y = pad + (H - pad * 2) * (1 - (v - min) / span);
      return [x, y];
    });
    var d = pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join(" ");
    line.setAttribute("d", d);
    if (area) {
      var stroke = getComputedStyle(line).stroke;
      area.setAttribute("d", d + " L" + W + " " + H + " L0 " + H + " Z");
      area.setAttribute("fill", stroke);
      area.setAttribute("opacity", "0.12");
    }
  }
  function noisy(base, amp, n, jitter) {
    var out = [], v = base;
    for (var i = 0; i < n; i++) {
      v += (Math.random() - 0.5) * jitter;
      out.push(Math.max(0, base + Math.sin(i / 2.2) * amp * 0.4 + (v - base)));
    }
    return out;
  }
  buildSpark(noisy(40, 30, 26, 14), "cpuLine", "cpuArea");
  buildSpark(noisy(55, 14, 26, 6), "memLine", "memArea");

  /* ---------- Fleet host list (mini live UI) ---------- */
  var HOSTS = [
    { name: "Local",   sub: "Docker 29.4 · OrbStack", cpu: "10%", run: 4,  unh: 0, color: "var(--steel)" },
    { name: "Nettop",  sub: "Ubuntu 24.04 LTS",       cpu: "4%",  run: 23, unh: 2, color: "var(--green)" },
    { name: "dedic",   sub: "Ubuntu 24.04 LTS",       cpu: "48%", run: 31, unh: 0, color: "var(--crane-2)" },
    { name: "SuperSet",sub: "CentOS Stream 9",        cpu: "3%",  run: 8,  unh: 3, color: "var(--steel)" }
  ];
  var hostList = document.getElementById("hostList");
  if (hostList) {
    function sparkPath(seed) {
      var W = 64, H = 16, n = 16, d = "", v = H / 2;
      for (var i = 0; i < n; i++) {
        v += (Math.sin(i * 1.3 + seed) + (Math.random() - 0.5)) * 2.2;
        v = Math.max(2, Math.min(H - 2, v));
        d += (i ? "L" : "M") + (i * (W / (n - 1))).toFixed(1) + " " + v.toFixed(1) + " ";
      }
      return d;
    }
    HOSTS.forEach(function (h, idx) {
      var row = document.createElement("div");
      row.style.cssText = "display:flex;align-items:center;gap:10px;padding:9px 12px;border-bottom:1px solid var(--border);";
      row.innerHTML =
        '<span style="width:7px;height:7px;border-radius:50%;background:' + (h.unh ? "var(--red)" : "var(--green)") + ';flex:none"></span>' +
        '<div style="min-width:74px"><div style="font-size:0.8rem;font-weight:650;color:var(--text)">' + h.name + '</div>' +
        '<div style="font-size:0.66rem;color:var(--text-mut)">' + h.sub + '</div></div>' +
        '<svg viewBox="0 0 64 16" preserveAspectRatio="none" style="width:64px;height:16px;flex:none"><path d="' + sparkPath(idx) + '" fill="none" stroke="' + h.color + '" stroke-width="1.4"/></svg>' +
        '<div style="margin-left:auto;text-align:right">' +
        '<div style="font-size:0.8rem;font-weight:650;color:var(--text)">' + h.cpu + '</div>' +
        '<div style="font-size:0.66rem;color:' + (h.unh ? "var(--red)" : "var(--text-mut)") + '">' + h.run + ' running' + (h.unh ? " · " + h.unh + " unhealthy" : "") + '</div></div>';
      hostList.appendChild(row);
    });
    hostList.lastChild.style.borderBottom = "none";
  }

  /* ---------- Live log stream ---------- */
  var LOG_LINES = [
    ['10:06:14', 'info', 'starting worker · concurrency=8'],
    ['10:06:14', 'ok',   'connected redis://cache:6379'],
    ['10:06:15', 'info', 'task superset.sql_lab received'],
    ['10:06:15', 'ok',   'task succeeded in 0.42s'],
    ['10:06:16', 'warn', 'health check latency 1.8s'],
    ['10:06:17', 'info', 'beat: scheduling 12 periodic tasks'],
    ['10:06:18', 'err',  'connection reset by peer'],
    ['10:06:18', 'info', 'retry in 2s (backoff)'],
    ['10:06:20', 'ok',   'reconnected · stream resumed'],
    ['10:06:21', 'info', 'task superset.cache_warmup received'],
  ];
  var logStream = document.getElementById("logStream");
  if (logStream && !reduce) {
    var li = 0;
    function pushLog() {
      var L = LOG_LINES[li % LOG_LINES.length];
      var el = document.createElement("div");
      el.className = "ln";
      el.innerHTML = '<span class="t">' + L[0] + '</span> <span class="' + L[1] + '">' + L[1].toUpperCase() + '</span> ' + L[2];
      logStream.appendChild(el);
      requestAnimationFrame(function () { el.classList.add("show"); });
      while (logStream.children.length > 6) logStream.removeChild(logStream.firstChild);
      li++;
    }
    for (var k = 0; k < 5; k++) pushLog();
    setInterval(pushLog, 1600);
  } else if (logStream) {
    LOG_LINES.slice(0, 6).forEach(function (L) {
      var el = document.createElement("div");
      el.className = "ln show";
      el.innerHTML = '<span class="t">' + L[0] + '</span> <span class="' + L[1] + '">' + L[1].toUpperCase() + '</span> ' + L[2];
      logStream.appendChild(el);
    });
  }
})();
