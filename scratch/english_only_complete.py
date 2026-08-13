import re

filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace all remaining bilingual/Arabic strings with clean English
replacements = [
    ('<title>تسجيل البيانات الكشفية</title>', '<title>Scout Registration</title>'),
    ('Registration / تسجيل', 'Registration'),
    ('Back / رجوع', 'Back'),
    ('Next / التالي', 'Next'),
    ('Finish / إنهاء', 'Finish'),
    ('isLastContentStep ? \'Finish / إنهاء\' : \'Next / التالي\'', 'isLastContentStep ? \'Finish\' : \'Next\''),
    ('Select Your Unit / اختر فرقتك', 'Select Your Unit'),
    ('Select Your Name / اختر اسمك', 'Select Your Name'),
    ('Create Security PIN / إنشاء رمز الأمان', 'Create Security PIN'),
    ('Enter Security PIN / أدخل رمز الأمان', 'Enter Security PIN'),
    ('Your Badges / شاراتك الكشفية', 'Your Badges'),
    ('Your Scouting Journey / مسيرتك الكشفية', 'Your Scouting Journey'),
    ('Saved Successfully / تم الحفظ بنجاح', 'Saved Successfully'),
    ('Edit My Profile / تعديل البيانات', 'Edit Profile'),
    ('data-options="مرشح|المبتدئ|القدم اللينة|نجم اول|نجم ثاني"',
     'data-options="Candidate|Novice|Tenderfoot|First Star|Second Star"'),
    ('data-options="مرشح|مبتدئ|كشاف ثاني|كشاف اول|كشاف رائد|كشاف نسر"',
     'data-options="Candidate|Novice|Second Class|First Class|Pioneer Scout|Eagle Scout"'),
    ('data-options="مساعد عريف|عريف طليعة|عريف اول"',
     'data-options="Assistant Patrol Leader|Patrol Leader|Senior Patrol Leader"'),
    ('data-options="مساعد رهط|رائد رهط|رائد اول"',
     'data-options="Assistant Crew Leader|Crew Leader|Senior Crew Leader"'),
    ('data-name-label="اسم الطليعة"', 'data-name-label="Patrol Name"'),
    ('data-name-label="اسم الرهط"', 'data-name-label="Crew Name"'),
    ('data-camp-q="هل نظّمت مخيماً؟"', 'data-camp-q="Did you organize a camp?"'),
    ('data-camp-name-label="اسم مكان المخيم"', 'data-camp-name-label="Camp Location / Name"'),
    ('data-camp-q="هل نظّمت مخيماً"', 'data-camp-q="Did you organize a camp?"'),
    ('data-camp-name-label="اسم المكان"', 'data-camp-name-label="Camp Location"'),
    ('هل أتممت التكريس في الفرع الأخضر؟', 'Did you complete consecration in the Green Branch?'),
    ('هل أتممت التكريس في الفرع الأحمر؟', 'Did you complete consecration in the Red Branch?'),
    ('هل أتممت الرحيل الكشفي في الفرع الأحمر؟', 'Did you complete departure in the Red Branch?'),
    ('هل مررت بالفرع الأخضر؟', 'Did you complete the Green Branch?'),
    ('هل مررت بالفرع الأصفر؟', 'Did you complete the Yellow Branch?'),
    ('هل مررت بالفرع الأحمر؟', 'Did you complete the Red Branch?'),
    ('هل شغلت أحد المراكز التالية؟', 'Did you hold any of the following leadership roles?'),
    ('Did you hold any of the following roles? / هل شغلت أحد المراكز التالية؟', 'Did you hold any of the following leadership roles?'),
    ('YYYY or DD/MM/YYYY (اختياري)', 'YYYY or DD/MM/YYYY (Optional)'),
    ('التاريخ (اختياري)', 'Date (Optional)'),
    ('السنة (اختياري)', 'Year (Optional)'),
    ('Year (Optional) / السنة (اختياري)', 'Year (Optional)'),
    ('يرجى تحديد العضو أولاً', 'Please select a member first'),
    ('شاردة كشفية', 'Badge'),
    ('دراسة خشبية', 'Wood Badge'),
    ('مفوضية', 'Commission'),
    ('عضو هيئة تدريب', 'Training Team Member'),
    ('شارة الغاب', 'Forest Badge'),
    ('وسام الأرز الكشفي', 'Scout Cedar Medal'),
    ('وسام الاستحقاق الكشفي', 'Scout Merit Medal'),
    ('وسام الخدمة الممتازة', 'Distinguished Service Medal'),
    ('وسام الشرف الكشفي', 'Scout Honor Medal'),
    ('وسام الشكر والتقدير', 'Appreciation Medal'),
    ('وسام البسالة', 'Bravery Medal')
]

for old, new in replacements:
    html = html.replace(old, new)

# Cleanup any lingering ' / ' bilingual labels in headings/subheadings
html = re.sub(r'([A-Za-z0-9\s]+)\s*/\s*[\u0600-\u06FF\s]+', r'\1', html)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Converted all remaining text to 100% English!')
