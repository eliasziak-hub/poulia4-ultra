#!/usr/bin/env python3
"""Build data/poulia4-feed.json from a Blogger Atom export."""
import sys, json, re, html
import xml.etree.ElementTree as ET
from pathlib import Path
atom=ET.parse(sys.argv[1]).getroot()
A="{http://www.w3.org/2005/Atom}"; B="{http://schemas.google.com/blogger/2018}"
out=[]
for e in atom.findall(A+"entry"):
    title=(e.findtext(A+"title") or "").strip()
    content=e.find(A+"content")
    raw=html.unescape(content.text or "") if content is not None else ""
    plain=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",raw))).strip()
    filename=e.findtext(B+"filename") or ""
    labels=[c.get("term","") for c in e.findall(A+"category") if c.get("term")]
    imgs=re.findall(r"<img[^>]+src=[\\"']([^\\"']+)",raw,re.I)
    scientific=list(dict.fromkeys(re.findall(r"\(([A-Z][a-z]+(?:\s+[a-z][a-z-]+){1,2})\)",plain)))
    out.append({"title":title,"url":"https://poulia4.blogspot.com"+filename if filename.startswith("/") else "https://poulia4.blogspot.com","labels":labels,"summary":plain[:560],"image":imgs[0] if imgs else "","scientific":scientific[:3],"published":e.findtext(A+"published") or ""})
Path("data").mkdir(exist_ok=True)
Path("data/poulia4-feed.json").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print(f"Wrote {len(out)} posts")
