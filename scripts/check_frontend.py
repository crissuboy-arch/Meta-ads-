"""Validate the source-served frontend; this project has no npm compilation step."""
import json
import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.ids=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k=='id':self.ids.append(v)

count=0
with tempfile.TemporaryDirectory(prefix='ofensiva-frontend-') as tmp:
    for page in (ROOT/'static').glob('*.html'):
        source=page.read_text(encoding='utf-8');parser=Parser();parser.feed(source)
        assert len(parser.ids)==len(set(parser.ids)),f'Duplicate HTML IDs: {page.name}'
        for i,script in enumerate(re.findall(r'<script\b[^>]*>(.*?)</script>',source,re.S|re.I)):
            target=Path(tmp)/f'{page.stem}-{i}.js';target.write_text(script,encoding='utf-8')
            subprocess.run(['node','--check',str(target)],check=True,capture_output=True)
            count+=1
    for script in (ROOT/'static').glob('*.js'):
        subprocess.run(['node','--check',str(script)],check=True,capture_output=True)
        count+=1
manifest=json.loads((ROOT/'static/manifest.json').read_text(encoding='utf-8'))
for icon in manifest['icons']:
    assert (ROOT/'static'/icon['src'].lstrip('/')).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
print(f'Frontend validated: {count} JavaScript units, unique HTML IDs, manifest and official PNG icons.')
tracking_test=ROOT/'scripts/test_tracking_insights.cjs'
if tracking_test.exists():
    subprocess.run(['node','--test',str(tracking_test)],check=True)
