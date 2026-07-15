# ==========================================
# Antigravity IDE Patcher
# Created by Neps
# ==========================================

import os

files_to_patch = [
    {
        "path": r"E:\D\Antigravity IDE\resources\app\out\vs\workbench\workbench.desktop.main.js",
        "target": 'd=a.osName==="linux"&&a.isGoogleInternal,h=a.isGoogleInternal',
        "replacement": 'd=true,h=true'
    },
    {
        "path": r"E:\D\Antigravity IDE\resources\app\out\vs\workbench\workbench.desktop.main.js",
        "target": 'this.setSelectedModel(or(Bnc,{choice:{case:"model",value:r}}),void 0,!1)',
        "replacement": 'this.setSelectedModel(or(Bnc,{choice:{case:"model",value:r}}),((_n_)=>{const t=XJt(_n_);return t?Object.values(t)[0]:void 0})(n),!1)'
    },
    {
        "path": r"E:\D\Antigravity IDE\resources\app\out\main.js",
        "target": 'f=o.osName==="linux"&&o.isGoogleInternal,p=o.isGoogleInternal',
        "replacement": 'f=true,p=true'
    },
    {
        "path": r"E:\D\Antigravity IDE\resources\app\out\jetskiAgent\main.js",
        "target": 'f=o.osName==="linux"&&o.isGoogleInternal,g=o.isGoogleInternal',
        "replacement": 'f=true,g=true'
    }
]

for item in files_to_patch:
    path = item["path"]
    target = item["target"]
    replacement = item["replacement"]
    print(f"Patching {path}...")
    if not os.path.exists(path):
        print(f"ERROR: File {path} not found!")
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    count = content.count(target)
    if count == 0:
        print(f"WARNING: Target string not found in {path}!")
        continue
    
    content = content.replace(target, replacement)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"SUCCESS: Patched {count} occurrence(s) in {path}.")
