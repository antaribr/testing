import re

filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the orphaned brace between Done header and PDF generator
bad_pattern = r'// ─── Done ─────────────────────────────────────────────────────────\s*}\s*// ─── Single-Page Scout Pass PDF Generator'
good_replacement = '// ─── Done ─────────────────────────────────────────────────────────\n    // ─── Single-Page Scout Pass PDF Generator'

if re.search(bad_pattern, html):
    html = re.sub(bad_pattern, good_replacement, html)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Cleaned orphaned closing brace from mobile/register/index.html!')
else:
    print('Pattern not found, checking manual string replace...')
    old_snippet = '''    // ─── Done ─────────────────────────────────────────────────────────
    
    
    }'''
    if old_snippet in html:
        html = html.replace(old_snippet, '    // ─── Done ─────────────────────────────────────────────────────────')
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(html)
        print('Cleaned old snippet successfully!')
