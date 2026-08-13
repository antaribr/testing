filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    # Yellow ranks
    ('data-options="Candidate|Novice|Tenderfoot|First Star|Second Star"', 'data-options="مرشح|مبتدئ|مبتدئ ممتاز|نجم أول|نجم ثاني"'),
    
    # Green ranks & leadership
    ('data-options="Candidate|Novice|Second Class|First Class|Pioneer Scout|Eagle Scout"', 'data-options="مرشح|مبتدئ|ثانية|أولى|متقدم|عقيد"'),
    ('data-options="Assistant Patrol Leader|Patrol Leader|Senior Patrol Leader"', 'data-options="مساعد عريف|عريف طليعة|عريف أول"'),
    ('data-name-label="Patrol Name"', 'data-name-label="اسم الطليعة"'),
    ('data-camp-place-label="Camp Location"', 'data-camp-place-label="مكان المخيم"'),
    ('data-camp-date-label="Camp Date"', 'data-camp-date-label="تاريخ المخيم"'),
    
    # Red ranks & leadership
    ('data-name-label="Crew Name"', 'data-name-label="اسم الرهط"')
]

for old, new in replacements:
    html = html.replace(old, new)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully restored Arabic-only rank chip names and leadership options in Your Journey!')
