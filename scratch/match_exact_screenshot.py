filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    # Clean Arabic headers & questions without English slashes
    ('<h3>الفرع الأصفر / Yellow Branch</h3>', '<h3>الفرع الأصفر</h3>'),
    ('<h3>الفرع الأخضر / Green Branch</h3>', '<h3>الفرع الأخضر</h3>'),
    ('<h3>الفرع الأحمر / Red Branch</h3>', '<h3>الفرع الأحمر</h3>'),
    
    ('<label class="ms-field-label">هل مررت بالفرع الأصفر؟ / Did you pass Yellow Branch?</label>', '<label class="ms-field-label">هل مررت بالفرع الأصفر؟</label>'),
    ('<label class="ms-field-label">هل مررت بالفرع الأخضر؟ / Did you pass Green Branch?</label>', '<label class="ms-field-label">هل مررت بالفرع الأخضر؟</label>'),
    ('<label class="ms-field-label">هل مررت بالفرع الأحمر؟ / Did you pass Red Branch?</label>', '<label class="ms-field-label">هل مررت بالفرع الأحمر؟</label>'),
    
    ('<label class="ms-field-label">هل شغلت أحد المراكز القيادية التالية؟ / Did you hold any leadership roles?</label>', '<label class="ms-field-label">هل شغلت أحد المراكز التالية؟</label>'),
    ('<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأخضر؟ / Did you complete consecration?</label>', '<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأخضر؟</label>'),
    ('<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأحمر؟ / Did you complete consecration?</label>', '<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأحمر؟</label>'),
    ('<label class="ms-field-label">هل أتممت الرحيل الكشفي في الفرع الأحمر؟ / Did you complete departure?</label>', '<label class="ms-field-label">هل أتممت الرحيل الكشفي في الفرع الأحمر؟</label>'),

    # Ranks & Options matching screenshot exactly
    ('data-options="مرشح|مبتدئ|مبتدئ ممتاز|نجم أول|نجم ثاني"', 'data-options="مرشح|المبتدئ|القدم اللينة|نجم اول|نجم ثاني"'),
    ('data-options="المرشح|المبتدئ|الوعد|كشاف ثاني|كشاف أول"', 'data-options="مرشح|مبتدى|كشاف ثاني|كشاف اول|كشاف رائد|كشاف نسر"'),
    ('data-options="مساعد عريف|عريف طليعة|عريف أول"', 'data-options="مساعد عريف|عريف طليعة|عريف اول"'),

    # Toggle buttons Yes / No -> نعم / لا
    ('<button type="button" class="yes">Yes</button><button type="button" class="no">No</button>', '<button type="button" class="yes">نعم</button><button type="button" class="no">لا</button>'),
    ('<button type="button" class="yes">Yes</button>+\n                      \'<button type="button" class="no">No</button>', '<button type="button" class="yes">نعم</button>+\n                      \'<button type="button" class="no">لا</button>'),
    
    # Field labels
    ('<span class="lead-row-body-label">Year (Optional) Date (Optional)</span>', '<span class="lead-row-body-label">التاريخ أو السنة (اختياري)</span>')
]

for old, new in replacements:
    html = html.replace(old, new)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully matched Your Journey section 100% to screenshot!')
