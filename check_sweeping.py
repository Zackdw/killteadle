import json, re
with open('data.json') as f:
    data = json.load(f)

print('=== Operatives with sweeping in name ===')
for op in data:
    if re.search(r'sweep', op['name'], re.I):
        print(f'{op["name"]}: {op["weapon_rules"]}')

print('\n=== Operatives with Torrent but not Blast ===')
for op in data:
    if 'Torrent' in op.get('weapon_rules', []) and 'Blast' not in op.get('weapon_rules', []):
        print(f'{op["name"]}: {op["weapon_rules"]}')

print('\n=== Operatives with Blast but not Torrent ===')
for op in data:
    if 'Blast' in op.get('weapon_rules', []) and 'Torrent' not in op.get('weapon_rules', []):
        print(f'{op["name"]}: {op["weapon_rules"]}')
