import os, re, json, html, markdown
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = {}  # slug -> dict(title, md, group, cat)
def read(p): return open(p, encoding="utf-8").read()
def strip_fm(t):
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":"); meta[k.strip()] = v.strip()
        t = t[m.end():]
    return meta, t
def add(slug, path, group):
    meta, body = strip_fm(read(path))
    title = meta.get("title") or re.search(r"^# (.+)$", body, re.M).group(1)
    pages[slug] = dict(title=title, md=body, group=group, updated=meta.get("updated",""), path=os.path.relpath(path, ROOT))
add("index", f"{ROOT}/index.md", "home")
for sub, group in [("categories","分類類別"),("items","物品"),("concepts","概念"),("law","法規與地方差異"),("sources","來源摘要"),("maintenance","維護")]:
    files=sorted(os.listdir(f"{ROOT}/wiki/{sub}"))
    if sub=="categories":
        pref=["cat-bulky.md","cat-hazardous.md","cat-food.md","cat-recyclable.md","cat-general.md"]
        files=[f for f in pref if f in files]+[f for f in files if f not in pref]
    if sub=="items":
        pref=[x+".md" for x in "item-paper item-iron item-aluminum item-glass item-plastic item-disc item-phone item-cooking-oil item-mandatory item-food-raw-cooked item-receipt item-pressurized-can item-gas-cylinder item-plastic-bag item-styrofoam item-lithium-battery".split()]
        files=[f for f in pref if f in files]+[f for f in files if f not in pref]
    for f in files:
        add(f[:-3], f"{ROOT}/wiki/{sub}/{f}", group)
for f in sorted(os.listdir(f"{ROOT}/raw")):
    sid = f.split("-")[0]
    add(f"raw-{sid}", f"{ROOT}/raw/{f}", "原始資料")
add("log", f"{ROOT}/log.md", "維護")
add("schema", f"{ROOT}/SCHEMA.md", "維護")
add("agents", f"{ROOT}/AGENTS.md", "維護")

CAT = {"cat-bulky":"bulky","cat-hazardous":"hazard","cat-food":"food","cat-recyclable":"recycle","cat-general":"general"}

def render(md):
    def link(m):
        s = m.group(1)
        if s not in pages: return f'<span class="broken">{html.escape(s)}</span>'
        c = CAT.get(s, "")
        return f'<a href="#{s}" class="wl {c}">{html.escape(pages[s]["title"]).replace("〔","&#x3014;").replace("〕","&#x3015;")}</a>'
    md = re.sub(r"\[\[([^\]]+)\]\]", link, md)
    md = re.sub(r"raw/(S\d+)-[^\s（）)]+\.md", lambda m: f'<a href="#raw-{m.group(1)}">raw/{m.group(1)} 原始資料</a>', md)
    out = markdown.markdown(md, extensions=["tables"])
    out = re.sub(r"〔(S\d+)〕", r'<a class="cite" href="#\1">\1</a>', out)
    out = out.replace("⚠", '<span class="warn" aria-label="待釐清">⚠</span>').replace("✔", '<span class="ok" aria-label="已釐清">✔</span>').replace("◇", '<span class="unoff" aria-label="非官方來源">◇</span>')
    out = re.sub(r'(https?://[^\s<"]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', out) if False else out
    return out

sections, nav = [], {}
for slug, p in pages.items():
    cls = CAT.get(slug, "")
    meta = f'<p class="meta">最後更新 {p["updated"]}　檔案 {html.escape(p["path"])}</p>' if p["updated"] else f'<p class="meta">檔案 {html.escape(p["path"])}</p>'
    sections.append(f'<article class="page {cls}" id="p-{slug}" data-slug="{slug}" hidden>{meta}{render(p["md"])}</article>')
    nav.setdefault(p["group"], []).append(slug)

order = ["分類類別","物品","概念","法規與地方差異","來源摘要","原始資料","維護"]
navhtml = '<a href="#index" class="nav-home" data-slug="index">首頁</a>'
for g in order:
    if g not in nav: continue
    navhtml += f'<p class="nav-g">{g}</p><ul>' + "".join(
        f'<li><a href="#{s}" data-slug="{s}" class="{CAT.get(s,"")}">{html.escape(pages[s]["title"])}</a></li>' for s in nav[g]) + "</ul>"

src = {p["path"]: read(os.path.join(ROOT, p["path"])) for p in pages.values()}
tpl = read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"template.html"))
outhtml = tpl.replace("%%NAV%%", navhtml).replace("%%PAGES%%", "\n".join(sections)).replace("%%SRC%%", json.dumps(src, ensure_ascii=False).replace("</", "<\\/")).replace("%%COUNT%%", str(sum(1 for s in pages if re.fullmatch(r"S\d+", s))))
open(f"{ROOT}/../garbage-wiki.html","w",encoding="utf-8").write(outhtml)
print("pages:", len(pages))
