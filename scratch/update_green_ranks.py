filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Green Branch options with exact list from screenshot:
# المرشح | المبتدئ | الوعد | كشاف ثاني | كشاف أول
old_green = 'data-options="مرشح|مبتدئ|ثانية|أولى|متقدم|عقيد"'
new_green = 'data-options="المرشح|المبتدئ|الوعد|كشاف ثاني|كشاف أول"'

if old_green in html:
    html = html.replace(old_green, new_green)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Successfully updated Green Branch ranks!')
else:
    print('Target string not found in mobile/register/index.html')
