import os,re,glob
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files=glob.glob(R+"/wiki/**/*.md",recursive=True)+[R+"/index.md"]
slugs={os.path.basename(f)[:-3] for f in files}|{"index","log","schema","agents"}
inbound={s:set() for s in slugs}; res={"broken":[],"warn":[],"unofficial":[],"stale":[],"nocite":[],"fm":[]}
for f in files:
    s=os.path.basename(f)[:-3]; t=open(f,encoding='utf-8').read()
    for l in re.findall(r"\[\[([^\]]+)\]\]",t):
        if l not in slugs: res["broken"].append((s,l))
        elif l!=s: inbound[l].add(s)
    for c in set(re.findall(r"〔(S\d)",t)):
        if c!=s and c in inbound: inbound[c].add(s)
    for line in t.splitlines():
        if "⚠" in line: res["warn"].append((s,line.strip()[:70]))
        if "◇" in line and "maintenance" not in f: res["unofficial"].append((s,line.strip()[:70]))
        if "maintenance" not in f and re.search(r"將由第|待第 ?\d|後續來源補充|第 \d 篇來源確認",line): res["stale"].append((s,line.strip()[:70]))
    if s not in("index",) and "maintenance" not in f and not re.search(r"〔S\d",t): res["nocite"].append(s)
    m=re.search(r"sources: \[(.*?)\]",t)
    used=set(re.findall(r"〔(S\d)",t))
    if m:
        decl={x.strip() for x in m.group(1).split(",")}
        if used-decl: res["fm"].append((s,"未宣告",sorted(used-decl)))
orph=[s for s,v in inbound.items() if not (v-{"index"}) and s not in("index","log","schema","agents") and not s.startswith("lint")]
for k,v in res.items(): print(k,len(v)); [print("  ",x) for x in v]
print("orphans(only index links):",orph)
idx=open(R+"/index.md",encoding='utf-8').read()
print("not in index:",[x for x in slugs if f"[[{x}]]" not in idx and x not in("index",)])
print("pages",len(files))
