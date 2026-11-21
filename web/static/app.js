"use strict";
const $ = (s) => document.querySelector(s);
const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v;
    else if (k === "text") n.textContent = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v);
  }
  for (const c of kids.flat()) if (c != null) n.append(c);
  return n;
};
const CLASS_PL = { odwolanie: "Odwołanie", pelnomocnictwo: "Pełnomocnictwo", przelew: "Potwierdzenie przelewu" };
const fmtNum = (x) => (Math.round(x * 100) / 100).toString().replace(".", ",");
const pretty = (o) => JSON.stringify(o, null, 2);

let files = [];
let last = null;

function showError(msg) { const e = $("#error"); e.textContent = msg; e.hidden = !msg; }

function renderQueue() {
  $("#queue").replaceChildren(...files.map((f, i) =>
    el("li", {}, el("span", { text: f.name, title: f.name }),
      el("button", { type: "button", "aria-label": "Usuń " + f.name, text: "×", onclick: () => { files.splice(i, 1); renderQueue(); } }))));
  $("#go").disabled = files.length === 0;
  $("#clear").hidden = files.length === 0;
}
function addFiles(list) {
  for (const f of list) {
    if (!/\.pdf$/i.test(f.name)) { showError("Pominięto „" + f.name + "”: to nie jest plik PDF."); continue; }
    if (!files.some((x) => x.name === f.name && x.size === f.size)) files.push(f);
  }
  renderQueue();
}

const drop = $("#drop");
["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add("over"); }));
["dragleave", "drop"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
drop.addEventListener("drop", (e) => { showError(""); addFiles(e.dataTransfer.files); });
$("#file").addEventListener("change", (e) => { showError(""); addFiles(e.target.files); e.target.value = ""; });
$("#clear").addEventListener("click", () => { files = []; renderQueue(); $("#results").hidden = true; showError(""); });

$("#go").addEventListener("click", async () => {
  showError(""); $("#results").hidden = true;
  const fd = new FormData();
  files.forEach((f) => fd.append("files", f, f.name));
  fd.append("case", $("#case").value.trim() || "sprawa");
  $("#go").disabled = true; $("#progress").hidden = false;
  try {
    const r = await fetch("/api/process", { method: "POST", body: fd });
    if (!r.ok) {
      let m = "Serwer odrzucił zapytanie (" + r.status + ").";
      try { const j = await r.json(); if (typeof j.detail === "string") m = j.detail; } catch (_) {}
      throw new Error(m);
    }
    last = await r.json();
    render(last);
  } catch (e) {
    showError(e.message || "Nie udało się przetworzyć plików. Sprawdź połączenie i spróbuj ponownie.");
  } finally {
    $("#progress").hidden = true; $("#go").disabled = files.length === 0;
  }
});

function saveBlob(name, blob) {
  const a = el("a", { href: URL.createObjectURL(blob), download: name });
  document.body.append(a); a.click(); a.remove();
}

$("#zip").addEventListener("click", async () => {
  if (!last) return;
  const filesObj = {};
  last.documents.forEach((d) => { if (d.output_name && d.data) filesObj[d.output_name] = d.data; });
  const r = await fetch("/api/zip", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ case: last.case, files: filesObj }) });
  if (!r.ok) { showError("Nie udało się zbudować archiwum ZIP."); return; }
  saveBlob(last.case + ".zip", await r.blob());
});

function render(res) {
  $("#case-title").textContent = "Sprawa: " + res.case;
  const acc = res.documents.filter((d) => d.output_name).length;
  const rej = res.documents.length - acc;
  $("#summary").textContent = "Liczba plików: " + res.documents.length + ". Rozpoznane: " + acc + ". Odrzucone: " + rej + " (dla odrzuconych nie powstaje plik JSON).";
  $("#zip").disabled = acc === 0;
  const ch = $("#checks"); ch.replaceChildren();
  if (res.checks.length) {
    ch.append(el("div", { class: "checks" }, el("h3", { text: "Spójność sprawy" }),
      el("ul", {}, res.checks.map((c) => el("li", {},
        el("span", { class: "dot " + (c.ok === true ? "t" : c.ok === false ? "f" : "n"), "aria-label": c.ok === true ? "zgodne" : c.ok === false ? "niezgodne" : "nie dotyczy", text: c.ok === true ? "✓" : c.ok === false ? "✗" : "–" }),
        el("span", {}, c.name, c.detail ? el("small", { text: "  " + c.detail }) : null))))));
  }
  $("#docs").replaceChildren(...res.documents.map(docCard));
  $("#results").hidden = false;
  $("#results").scrollIntoView({ behavior: "smooth", block: "start" });
}

function docCard(d, idx) {
  const c = d.classification;
  const rejected = !d.output_name;
  const label = rejected ? "Odrzucony" : (CLASS_PL[c.doc_class] || c.doc_class);
  const stamp = el("div", { class: "stamp" }, label,
    rejected ? null : el("b", { text: fmtNum(c.score) }),
    el("small", { text: rejected ? "brak pliku JSON" : "wynik klasyfikacji" }));

  const entries = Object.entries(c.scores || {}).sort((a, b) => b[1] - a[1]);
  const max = Math.max(1, ...entries.map((e) => e[1]));
  const scores = entries.length ? el("div", { class: "scores", role: "group", "aria-label": "Wyniki dla poszczególnych klas" },
    entries.map(([k, v], i) => [
      el("span", { text: CLASS_PL[k] || k }),
      el("span", { class: "t" + (i === 0 && !rejected ? " top1" : "") }, el("i", { style: "width:" + Math.round(100 * v / max) + "%" })),
      el("span", { text: fmtNum(v) })]).flat()) : null;

  const head = el("div", { class: "doc-head" }, stamp,
    el("div", {},
      el("p", { class: "fname" }, d.input_name, d.output_name ? el("small", { text: "  → " + d.output_name }) : null),
      el("p", { class: "reason" }, el("strong", { text: rejected ? "Powód odrzucenia: " : "Dlaczego ta klasa: " }), c.reason || (rejected ? "dokument nie pasuje do żadnej znanej klasy" : "brak opisu")),
      scores,
      d.warnings.length ? el("div", { class: "warns" }, d.warnings.map((w) => el("div", { text: w }))) : null));

  const card = el("article", { class: "doc" + (rejected ? " rejected" : "") }, head);
  if (rejected) return card;

  const id = "d" + idx;
  const jsonText = pretty(d.data);
  const jsonPane = el("div", { class: "pane", id: id + "-json", role: "tabpanel", hidden: "" },
    el("div", { class: "tools" },
      el("button", { type: "button", class: "ghost", text: "Kopiuj JSON", onclick: async (e) => {
        const b = e.target;
        try { await navigator.clipboard.writeText(jsonText); b.textContent = "Skopiowano"; } catch (_) { b.textContent = "Nie udało się skopiować"; }
        setTimeout(() => (b.textContent = "Kopiuj JSON"), 1600); } }),
      el("button", { type: "button", text: "Pobierz " + d.output_name, onclick: () => saveBlob(d.output_name, new Blob([jsonText + "\n"], { type: "application/json" })) })),
    el("pre", { class: "json", tabindex: "0", text: jsonText }));
  const evPane = el("div", { class: "pane", id: id + "-ev", role: "tabpanel" }, evidenceTable(d.evidence));
  const mk = (t, pane, sel) => el("button", { type: "button", role: "tab", "aria-selected": sel, "aria-controls": pane.id, text: t });
  const t1 = mk("Dowody dla pól (" + d.evidence.length + ")", evPane, "true");
  const t2 = mk("JSON", jsonPane, "false");
  [[t1, evPane, jsonPane], [t2, jsonPane, evPane]].forEach(([t, on, off]) => t.addEventListener("click", () => {
    t1.setAttribute("aria-selected", "false"); t2.setAttribute("aria-selected", "false");
    t.setAttribute("aria-selected", "true"); on.hidden = false; off.hidden = true;
  }));
  card.append(el("div", { class: "tabs", role: "tablist" }, t1, t2), evPane, jsonPane);
  return card;
}

function show(v) {
  if (v === null || v === undefined) return el("span", { class: "null", text: "null" });
  return typeof v === "string" ? v : JSON.stringify(v);
}
function snippetCell(snippet, value) {
  if (!snippet) return el("span", { class: "null", text: "brak" });
  const v = value == null ? "" : String(value);
  const i = v ? snippet.indexOf(v) : -1;
  if (i < 0) return snippet;
  return [snippet.slice(0, i), el("mark", { text: v }), snippet.slice(i + v.length)];
}
function evidenceTable(ev) {
  if (!ev.length) return el("p", { class: "empty", text: "Silnik nie zwrócił jeszcze dowodów dla pól tego dokumentu." });
  const filter = el("input", { type: "search", placeholder: "Filtruj po polu, wartości lub regule", "aria-label": "Filtruj dowody" });
  const rows = ev.map((e) => {
    const cf = e.confidence == null ? 1 : e.confidence;
    const cls = cf >= 0.85 ? "" : cf >= 0.6 ? "mid" : "low";
    const tr = el("tr", {},
      el("td", { class: "path", "data-l": "Pole" }, e.path),
      el("td", { class: "val", "data-l": "Wartość" }, show(e.value)),
      el("td", { class: "pg", "data-l": "Strona", text: e.page == null ? "–" : String(e.page) }),
      el("td", { class: "snip", "data-l": "Fragment źródła" }, snippetCell(e.snippet, e.value)),
      el("td", { class: "rule", "data-l": "Reguła", text: e.rule || "–" }),
      el("td", { class: "cf", "data-l": "Pewność" }, el("span", { class: "conf " + cls }, el("i", { style: "width:" + Math.round(cf * 100) + "%" })), fmtNum(cf)));
    tr.dataset.q = (e.path + " " + (e.value == null ? "" : e.value) + " " + (e.rule || "")).toLowerCase();
    return tr;
  });
  filter.addEventListener("input", () => { const q = filter.value.toLowerCase(); rows.forEach((r) => { r.hidden = !!q && !r.dataset.q.includes(q); }); });
  const head = el("tr", {}, ["Pole", "Wartość", "Strona", "Fragment źródła", "Reguła", "Pewność"].map((h) => el("th", { scope: "col", text: h })));
  return el("div", {}, el("div", { class: "ev-filter" }, filter),
    el("div", { class: "ev-wrap" }, el("table", { class: "ev" }, el("thead", {}, head), el("tbody", {}, rows))));
}
