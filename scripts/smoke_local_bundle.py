"""Run the actual frozen engine without a system Python or provider credentials."""
import json
import os
import subprocess
import urllib.request
from pathlib import Path

root=Path(__file__).resolve().parent.parent
exe=root/'src-tauri/runtime/local-engine'/('local-engine.exe' if os.name=='nt' else 'local-engine')
proc=subprocess.Popen([str(exe)],cwd=exe.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
    line=proc.stdout.readline()
    assert line.startswith('LOCAL_ENGINE_READY='),line
    ready=json.loads(line.split('=',1)[1])
    def read(path):
        request=urllib.request.Request('http://127.0.0.1:'+str(ready['port'])+path,
            headers={'Authorization':'Bearer '+ready['token']})
        with urllib.request.urlopen(request,timeout=10) as response:return json.load(response)
    assert read('/health')['ok'] is True
    ids={a['id'] for a in read('/agents')['agents']}
    assert 'coordenador-marketing-ia' in ids and 'mentor-trafego-pago' in ids
    assert len(ids)>=9
    print('Frozen engine: real HTTP health and packaged agent configurations OK')
finally:
    proc.terminate()
    proc.wait(timeout=10)
