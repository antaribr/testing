filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update STEP_LABELS in JS
old_labels = "var STEP_LABELS = {\n      unit:'Select Your Unit', name:'Select Your Name', pin:'Security PIN',\n      badges:'Your Badges', milestones:'Your Journey', done:'Done!'\n    };"
new_labels = "var STEP_LABELS = {\n      unit:'اختر وحدتك / Select Unit', name:'اختر الاسم / Select Name', pin:'رمز الأمان / Security PIN',\n      badges:'شاراتك / Your Badges', milestones:'مسيرتك الكشفية / Your Journey', done:'Done!'\n    };"
html = html.replace(old_labels, new_labels)

# 2. Update UNITS array in JS
old_units = """var UNITS = [
      {key:'Beavers',   ar:'Beavers',   color:'#ec4899', ink:'#fff'}, // زهري
      {key:'Cubs',      ar:'Cubs',    color:'#facc15', ink:'#5b3a00'}, // اصفر
      {key:'Girlscouts',ar:'Girlscouts',  color:'#86efac', ink:'#14532d'}, // اخضر فاتح
      {key:'Boyscouts', ar:'Boyscouts',   color:'#166534', ink:'#fff'},   // اخضر غامق
      {key:'Pioneers',  ar:'Pioneers',  color:'#fca5a5', ink:'#7f1d1d'}, // احمر فاتح
      {key:'Rovers',    ar:'Rovers',   color:'#991b1b', ink:'#fff'},    // احمر غامق
      {key:'Leaders',   ar:'Leaders', color:'#4f46e5', ink:'#fff'}
    ];"""

new_units = """var UNITS = [
      {key:'Beavers',   ar:'البرامعم / Beavers',   color:'#ec4899', ink:'#fff'}, // زهري
      {key:'Cubs',      ar:'الأشبال والزهرات / Cubs', color:'#facc15', ink:'#5b3a00'}, // اصفر
      {key:'Girlscouts',ar:'المرشدات / Girl Scouts',  color:'#86efac', ink:'#14532d'}, // اخضر فاتح
      {key:'Boyscouts', ar:'الكشافة / Boy Scouts',   color:'#166534', ink:'#fff'},   // اخضر غامق
      {key:'Pioneers',  ar:'المتقدم / Pioneers',  color:'#fca5a5', ink:'#7f1d1d'}, // احمر فاتح
      {key:'Rovers',    ar:'الجوالة والدليلات / Rovers', color:'#991b1b', ink:'#fff'},  // احمر غامق
      {key:'Leaders',   ar:'القادة / Leaders', color:'#4f46e5', ink:'#fff'}
    ];"""
html = html.replace(old_units, new_units)

# 3. Update HTML step headings & subtitles for Steps 1-5
replacements = [
    # Topbar & Step 1
    ('<div class="eyebrow" id="stepEyebrow">Registration</div>', '<div class="eyebrow" id="stepEyebrow">التسجيل / Registration</div>'),
    ('<div class="heading" id="stepHeading">Select Your Unit</div>', '<div class="heading" id="stepHeading">اختر وحدتك / Select Your Unit</div>'),
    ('<h1 class="step-title">Select Your Unit</h1>', '<h1 class="step-title">اختر وحدتك / Select Your Unit</h1>'),
    ('<p class="step-sub">Tap the unit you belong to</p>', '<p class="step-sub">اضغط على الوحدة التي تنتمي إليها / Tap the unit you belong to</p>'),
    
    # Step 2
    ('<h1 class="step-title">Select Your Name</h1>', '<h1 class="step-title">اختر اسمك / Select Your Name</h1>'),
    ('placeholder="🔍 Search by name..."', 'placeholder="🔍 ابحث عن اسمك / Search by name..."'),
    
    # Step 3
    ('<h1 class="step-title" id="pinTitle">Create Security PIN</h1>', '<h1 class="step-title" id="pinTitle">إنشاء رمز الأمان / Create Security PIN</h1>'),
    ('<p class="step-sub" id="pinSub">A 4-digit PIN to secure your profile from unauthorized changes.</p>', '<p class="step-sub" id="pinSub">رمز مكون من 4 أرقام لحماية ملفك الشخصي من التغييرات / A 4-digit PIN to secure your profile.</p>'),
    ('<button type="button" class="pin-key action" data-k="clear">Clear</button>', '<button type="button" class="pin-key action" data-k="clear">مسح / Clear</button>'),
    
    # Step 4
    ('<h1 class="step-title">Your Badges</h1>', '<h1 class="step-title">شاراتك الكشفية / Your Badges</h1>'),
    ('<p class="step-sub">Tap on each badge you have earned. They will be saved automatically.</p>', '<p class="step-sub">اضغط على الشارات التي حصلت عليها / Tap on each badge you have earned.</p>'),
    
    # Step 5
    ('<h1 class="step-title" id="milestonesTitle">Your Scouting Journey</h1>', '<h1 class="step-title" id="milestonesTitle">مسيرتك الكشفية / Your Scouting Journey</h1>'),
    ('<p class="step-sub" id="milestonesSub">Answer the following questions. Your responses are saved automatically.</p>', '<p class="step-sub" id="milestonesSub">أجب عن الأسئلة التالية لتحديث ملفك الكشفي / Answer the following questions.</p>'),
    ('<label class="ms-field-label" for="msJoinYear">Year Joined the Lebanese Scout Association</label>', '<label class="ms-field-label" for="msJoinYear">سنة الانضمام إلى الكشاف المسلم / Year Joined</label>'),
    
    # Yellow branch labels
    ('<h3>Yellow Branch</h3>', '<h3>الفرع الأصفر / Yellow Branch</h3>'),
    ('<label class="ms-field-label">هل مررت بYellow Branch؟</label>', '<label class="ms-field-label">هل مررت بالفرع الأصفر؟ / Did you pass Yellow Branch?</label>'),
    ('<label class="ms-field-label">Select your achievements Select your achievements</label>', '<label class="ms-field-label">اختر الأوسمة والرتب المحققة / Select your achievements</label>'),
    
    # Green branch labels
    ('<h3>Green Branch</h3>', '<h3>الفرع الأخضر / Green Branch</h3>'),
    ('<label class="ms-field-label">هل مررت بGreen Branch؟</label>', '<label class="ms-field-label">هل مررت بالفرع الأخضر؟ / Did you pass Green Branch?</label>'),
    ('<label class="ms-field-label">هل شغلت أحد Leadership Roles التالية؟</label>', '<label class="ms-field-label">هل شغلت أحد المراكز القيادية التالية؟ / Did you hold any leadership roles?</label>'),
    ('<label class="ms-field-label">هل أتممت التكريس الكشفي في Green Branch؟</label>', '<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأخضر؟ / Did you complete consecration?</label>'),
    ('<label class="ms-field-label">Consecration Year</label>', '<label class="ms-field-label">سنة التكريس / Consecration Year</label>'),
    
    # Red branch labels
    ('<h3>Red Branch</h3>', '<h3>الفرع الأحمر / Red Branch</h3>'),
    ('<label class="ms-field-label">هل مررت بRed Branch؟</label>', '<label class="ms-field-label">هل مررت بالفرع الأحمر؟ / Did you pass Red Branch?</label>'),
    ('<label class="ms-field-label">Did you hold any of the following roles? Leadership Roles التالية؟</label>', '<label class="ms-field-label">هل شغلت أحد المراكز القيادية التالية؟ / Did you hold any leadership roles?</label>'),
    ('<label class="ms-field-label">هل أتممت التكريس الكشفي في Red Branch؟</label>', '<label class="ms-field-label">هل أتممت التكريس الكشفي في الفرع الأحمر؟ / Did you complete consecration?</label>'),
    ('<label class="ms-field-label">هل أتممت الرحيل الكشفي في Red Branch؟</label>', '<label class="ms-field-label">هل أتممت الرحيل الكشفي في الفرع الأحمر؟ / Did you complete departure?</label>'),
    ('<label class="ms-field-label">Departure Year</label>', '<label class="ms-field-label">سنة الرحيل / Departure Year</label>'),

    # Leader labels
    ('<h3 style="margin-top: 0; margin-bottom: 16px; color: var(--primary); font-size: 16px; font-weight: 700; border-bottom: 1px solid var(--line); padding-bottom: 8px;">Leader\'s Journey</h3>', '<h3 style="margin-top: 0; margin-bottom: 16px; color: var(--primary); font-size: 16px; font-weight: 700; border-bottom: 1px solid var(--line); padding-bottom: 8px;">مسيرة القائد / Leader\'s Journey</h3>'),
    ('<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">Current Rank</label>', '<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">الرتبة الحالية / Current Rank</label>'),
    ('<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">تاريخ Rank (Date of Rank)</label>', '<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">تاريخ الرتبة / Date of Rank</label>'),
    ('<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 8px;">Previous Ranks</label>', '<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 8px;">الرتب السابقة / Previous Ranks</label>'),
    ('<button type="button" class="primary-btn" id="addLeaderRankBtn" style="background: var(--primary-tint); color: var(--primary); border: 1px dashed var(--primary); padding: 8px 12px; border-radius: 8px; font-weight: 600; width: 100%; margin-top: 8px; font-size: 13px;">+ Add Previous Rank</button>', '<button type="button" class="primary-btn" id="addLeaderRankBtn" style="background: var(--primary-tint); color: var(--primary); border: 1px dashed var(--primary); padding: 8px 12px; border-radius: 8px; font-weight: 600; width: 100%; margin-top: 8px; font-size: 13px;">+ إضافة رتبة سابقة / Add Previous Rank</button>'),
    ('<label class="ms-field-label" style="font-weight: 700; font-size: 14px; color: var(--primary); display: block; margin-bottom: 8px;">Scout Title</label>', '<label class="ms-field-label" style="font-weight: 700; font-size: 14px; color: var(--primary); display: block; margin-bottom: 8px;">اللقب الكشفي / Scout Title</label>'),
    ('<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">Consecration Date</label>', '<label class="ms-field-label" style="font-weight: 700; font-size: 13px; color: var(--text-secondary); display: block; margin-bottom: 4px;">تاريخ التكريس / Consecration Date</label>'),

    # PIN JS Messages
    ("document.getElementById('pinTitle').textContent = isReturningUser ? 'Enter Security PIN' : 'Create Security PIN';", "document.getElementById('pinTitle').textContent = isReturningUser ? 'إدخال رمز الأمان / Enter Security PIN' : 'إنشاء رمز الأمان / Create Security PIN';"),
    ("document.getElementById('pinSub').textContent   = isReturningUser\n        ? 'Enter your previously chosen PIN to edit your profile.'\n        : 'A 4-digit PIN to secure your profile from unauthorized changes.';", "document.getElementById('pinSub').textContent   = isReturningUser\n        ? 'أدخل رمز الأمان الخاص بك للتعديل / Enter your previously chosen PIN to edit profile.'\n        : 'رمز مكون من 4 أرقام لحماية ملفك الشخصي / A 4-digit PIN to secure your profile.';"),
    ("document.getElementById('pinError').textContent = 'Incorrect PIN, please try again';", "document.getElementById('pinError').textContent = 'رمز غير صحيح، يرجى المحاولة مجدداً / Incorrect PIN, please try again';")
]

for old, new in replacements:
    html = html.replace(old, new)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully restored Arabic/bilingual text in Steps 1-5 while keeping Step 6 100% English!')
