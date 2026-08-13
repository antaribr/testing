filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix unitStr definition
html = html.replace('var unitName = m.unit || chosenUnit || "Rovers";',
                    'var unitName = m.unit || chosenUnit || "Rovers";\n        var unitStr = unitName;')

# Also add mobile-web-app-capable meta tag if missing or replace deprecated tag
html = html.replace('<meta name="apple-mobile-web-app-capable" content="yes">',
                    '<meta name="mobile-web-app-capable" content="yes">\n  <meta name="apple-mobile-web-app-capable" content="yes">')

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed ReferenceError: unitStr is not defined!')
