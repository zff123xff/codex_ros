#!/usr/bin/env python3
"""Install global ROS instructions and transport helper without replacing user settings."""
import argparse
import datetime
import os
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
args = parser.parse_args()
target = args.codex_home.expanduser().resolve()
payload = Path(__file__).resolve().parent
target.mkdir(parents=True, exist_ok=True)
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')

def write(path, content):
    if path.exists() and path.read_text() == content:
        return
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + '.bak.' + stamp))
    path.write_text(content)

# Modify only these two settings. Preserve tables and all unrelated settings.
config = target / 'config.toml'
text = config.read_text() if config.exists() else ''
first_table = re.search(r'^\s*\[', text, re.M)
boundary = first_table.start() if first_table else len(text)
root, tables = text[:boundary], text[boundary:]
root, count = re.subn(r'^sandbox_mode\s*=.*$', 'sandbox_mode = "workspace-write"', root, flags=re.M)
if not count:
    root = 'sandbox_mode = "workspace-write"\n' + root
section = re.search(r'^\[sandbox_workspace_write\]\s*\n(.*?)(?=^\s*\[|\Z)', tables, re.M | re.S)
if section:
    body, count = re.subn(r'^network_access\s*=.*$', 'network_access = true', section.group(1), flags=re.M)
    if not count:
        body = 'network_access = true\n' + body
    tables = tables[:section.start(1)] + body + tables[section.end(1):]
else:
    tables = tables.rstrip() + '\n\n[sandbox_workspace_write]\nnetwork_access = true\n'
write(config, root + tables)

override = target / 'AGENTS.override.md'
agents = override if override.exists() and override.read_text().strip() else target / 'AGENTS.md'
old = agents.read_text() if agents.exists() else ''
block = (payload / 'agents.md').read_text().strip()
pattern = r'<!-- codex-ros:begin -->.*?<!-- codex-ros:end -->'
if re.search(pattern, old, re.S):
    new = re.sub(pattern, lambda _: block, old, flags=re.S)
else:
    new = old.rstrip() + ('\n\n' if old.strip() else '') + block + '\n'
write(agents, new)
ros = target / 'ros'
ros.mkdir(exist_ok=True)
for name in ('setup.bash', 'fastdds_udp.xml'):
    write(ros / name, (payload / name).read_text())
print(f'Installed global ROS support in {target}. Existing changed files have timestamped backups.')
print('Restart Codex to load global instructions and sandbox settings. Inherited or managed policies may override these settings.')
