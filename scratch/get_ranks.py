import re

for fname in [r'c:\Users\PC\Documents\GitHub\testing\mobile\index.html', r'c:\Users\PC\Documents\GitHub\testing\index.html']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        print('=== File:', fname)
        for m in re.finditer(r'data-options="([^"]+)"', text):
            print('  ', m.group(1))
    except Exception as e:
        print(e)
