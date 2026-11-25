"""Read-only Git proof that the redesign updates the existing product."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='f73713f3f89b17bf8b42a8fef741708a83302a23'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def exists_in_history(commit):return subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT).returncode==0
def content(ref,path):return git('show',ref+':'+path)
phases={'A':'73b0252','B':'d9ced12','C':'1b59f35','D':'fe1a584','E':'c41e590','F':'7b32303','G_H':'1ef07cc'}
base_files=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
head_files=set(git('ls-tree','-r','--name-only','HEAD').decode().splitlines())
protected=[f for f in base_files if f.endswith('.py') or f.startswith(('supabase/','mcp/','mcp_content/','skills/','commands/')) or f in ('config.py','vercel.json','requirements.txt','.github/workflows/ci.yml','.github/workflows/desktop.yml')]
changed_protected=set(git('diff','--name-only',BASE,'HEAD','--',*protected).decode().splitlines())
unchanged=[f for f in protected if f not in changed_protected]
old_html=content(BASE,'static/index.html').decode()
new_html=content('HEAD','static/index.html').decode()
ids=lambda s:set(re.findall(r'\bid="([^"\s]+)"',s))
functions=lambda s:set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',s))
config_checks={}
for f in base_files:
    if not re.match(r'configs/meta-ads(?:-[a-z]{2})?\.json$',f):continue
    old=json.loads(content(BASE,f));new=json.loads(content('HEAD',f))
    for d in (old,new):
        d.pop('branding',None);d.pop('colors',None)
    config_checks[f]=old==new
old_tauri=json.loads(content(BASE,'src-tauri/tauri.conf.json'))
new_tauri=json.loads(content('HEAD','src-tauri/tauri.conf.json'))
for d in (old_tauri,new_tauri):
    d.pop('productName',None)
    for window in d['app']['windows']:window.pop('title',None)
report={
    'base':BASE,'head':git('rev-parse','HEAD').decode().strip(),
    'remote_main':git('rev-parse','origin/main').decode().strip(),
    'base_is_ancestor':exists_in_history(BASE),
    'remote_main_is_ancestor':exists_in_history('origin/main'),
    'claude_phases_in_history':{p:exists_in_history(c) for p,c in phases.items()},
    'removed_base_files':sorted(set(base_files)-head_files),
    'protected_files_checked':len(protected),
    'modified_protected_files':sorted(set(protected)-set(unchanged)),
    'removed_literal_interface_ids':sorted(ids(old_html)-ids(new_html)),
    'removed_named_frontend_functions':sorted(functions(old_html)-functions(new_html)),
    'config_behavior_preserved':config_checks,
    'desktop_config_except_branding_unchanged':old_tauri==new_tauri,
    'vercel_config_sha256':hashlib.sha256(content('HEAD','vercel.json')).hexdigest(),
    'merge_tree':git('merge-tree','--write-tree','origin/main','HEAD').decode().strip(),
    'head_tree':git('rev-parse','HEAD^{tree}').decode().strip(),
}
assert report['base_is_ancestor'] and report['remote_main_is_ancestor']
assert all(report['claude_phases_in_history'].values())
assert not report['removed_base_files'] and not report['modified_protected_files']
assert not report['removed_literal_interface_ids'] and not report['removed_named_frontend_functions']
assert all(config_checks.values()) and report['desktop_config_except_branding_unchanged']
assert report['merge_tree']==report['head_tree'],'Main advanced; inspect the simulated merge'
print(json.dumps(report,ensure_ascii=False,indent=2))
