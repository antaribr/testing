import os
import re

filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Direct string replacements for step done & toast/PDF messages
replacements = [
    ('Leaders / القادة', 'Leaders'),
    ('Select Your Unit', 'Select Your Unit'),
    ('Tap the unit you belong to', 'Tap the unit you belong to'),
    ('Saved Successfully', 'Registration Saved Successfully!'),
    ('تم حفظ بياناتك بنجاح!', 'Registration Saved Successfully!'),
    ('شكراً لتسجيل وتحديث معلوماتك الكشفية. يمكنك الآن تحميل وثيقة القيد الرسمية الخاصة بك مباشرة بصيغة PDF.',
     'Thank you for updating your scouting profile. You can now download your official Scout Pass PDF directly.'),
    ('تحميل وثيقة القيد الكشفية (PDF) / Download Scout Pass PDF', 'Download Scout Pass (PDF)'),
    ('تعديل البيانات مرة أخرى / Edit Profile', 'Edit Profile'),
    ('تعديل البيانات مرة أخرى', 'Edit Profile'),
    ('جاري تجهيز وثيقة القيد الكشفية (PDF)...', 'Preparing Scout Pass PDF...'),
    ('تم تحميل وثيقة القيد الكشفية بنجاح! / Single-page PDF downloaded!', 'Scout Pass PDF downloaded successfully!'),
    ('تعذر العثور على مكتبة PDF', 'PDF library not available'),
    ('خطأ في تحميل PDF:', 'PDF Download Error:'),
    ('سنة الانضمام إلى الجمعية', 'Year Joined the Association'),
    ('الفرع الأصفر', 'Yellow Branch'),
    ('هل مررت بالفرع الأصفر؟', 'Did you complete the Yellow Branch?'),
    ('الرتب:', 'Ranks:'),
    ('اختر ما أنجزت', 'Select your achievements'),
    ('Select your achievements / اختر ما أنجزت', 'Select your achievements'),
    ('الفرع الأخضر', 'Green Branch'),
    ('هل مررت بالفرع الأخضر؟', 'Did you complete the Green Branch?'),
    ('التكريس:', 'Consecration:'),
    ('الفرع الأحمر', 'Red Branch'),
    ('هل مررت بالفرع الأحمر؟', 'Did you complete the Red Branch?'),
    ('الرحيل:', 'Departure:'),
    ('المسيرة', 'Journey'),
    ('مسيرة القائد (Leader\'s Journey)', 'Leader\'s Journey'),
    ('الرتبة الحالية (Current Rank)', 'Current Rank'),
    ('الرتبة الحالية', 'Current Rank'),
    ('الرتبة', 'Rank'),
    ('تاريخ الرتبة (Date of Rank)', 'Date of Rank'),
    ('تاريخ الرتبة', 'Date of Rank'),
    ('الرتب السابقة (Previous Ranks)', 'Previous Ranks'),
    ('الرتب القيادية السابقة (Previous Ranks)', 'Previous Ranks'),
    ('+ إضافة رتبة سابقة', '+ Add Previous Rank'),
    ('التلقيب الكشفي (Scout Title)', 'Scout Title'),
    ('التلقيب الكشفي', 'Scout Title'),
    ('اللقب الكشفي', 'Scout Title'),
    ('اللقب', 'Title'),
    ('مكان التلقيب', 'Title Location'),
    ('المكان', 'Location'),
    ('العراب (Godfather)', 'Godfather'),
    ('العراب', 'Godfather'),
    ('تاريخ التلقيب', 'Title Date'),
    ('تاريخ التكريس القيادي (Consecration Date)', 'Consecration Date'),
    ('تاريخ التكريس القيادي', 'Consecration Date'),
    ('هل أتممت التكريس في الفرع الأخضر؟', 'Did you complete consecration in Green Branch?'),
    ('هل أتممت التكريس في الفرع الأحمر؟', 'Did you complete consecration in Red Branch?'),
    ('هل أتممت الرحيل الكشفي في الفرع الأحمر؟', 'Did you complete departure in Red Branch?'),
    ('سنة الرحيل', 'Departure Year'),
    ('سنة التكريس', 'Consecration Year'),
    ('اسم المخيم', 'Camp Name'),
    ('مكان المخيم', 'Camp Location'),
    ('تاريخ المخيم', 'Camp Date'),
    ('نظّم مخيماً', 'Organized a Camp'),
    ('نعم (بدون تفاصيل)', 'Yes (no details)'),
    ('المراكز', 'Leadership Roles'),
    ('هل شغلت أحد المراكز التالية؟', 'Did you hold any of the following leadership roles?'),
    ('اسم الطليعة', 'Patrol Name'),
    ('نعم', 'Yes'),
    ('لا', 'No'),
    ('يرجى تحديد العضو أولاً', 'Please select a member first'),
    ('لم يتم تحديد شارات بعد', 'No badges earned yet'),
    ('لا يوجد سجل مسيرة مسجل حالياً', 'No journey recorded yet'),
    ('خطأ: ', 'Error: ')
]

for old, new in replacements:
    html = html.replace(old, new)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Replaced all Arabic strings with 100% English!')
