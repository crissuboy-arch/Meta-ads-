"""Embed the tested tracking module into the existing source-served app shell."""
from pathlib import Path

root=Path(__file__).resolve().parents[1]
page=root/'static/index.html'
source=page.read_text(encoding='utf-8')
start='// TRACKING INSIGHTS START'
end='// TRACKING INSIGHTS END'
block=start+'\n'+(root/'static/tracking-insights.js').read_text(encoding='utf-8')+'\n'+end+'\n'
if start in source:
    a=source.index(start);b=source.index(end,a)+len(end)
    source=source[:a]+block+source[b:]
else:
    source=source.replace('boot();input.focus();',block+'boot();input.focus();',1)
page.write_text(source,encoding='utf-8')
