# 1. Update app.js null-safeties and toast container fallback
filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

# Fix showToast to fallback to #toast
old_showToast = "const container = $('#toastContainer');"
new_showToast = "const container = $('#toastContainer') || $('#toast') || document.getElementById('toast');"
appCode = appCode.replace(old_showToast, new_showToast)

# Fix bindAuth null check
old_bindAuth = "const form = $('#loginForm');"
new_bindAuth = "const form = $('#loginForm');\n  if (!form) return;"
appCode = appCode.replace(old_bindAuth, new_bindAuth)

# Fix buildMemberMilestonesHtml string comparison
old_member_find = "const member = state.members.find(m => m.id === memberId) || state.leaders.find(l => l.id === memberId);"
new_member_find = "const member = state.members.find(m => String(m.id) === String(memberId)) || state.leaders.find(l => String(l.id) === String(memberId));"
appCode = appCode.replace(old_member_find, new_member_find)

with open(filePathApp, 'w', encoding='utf-8') as f:
    f.write(appCode)

print('Updated app.js with toast fallback and null-safeties!')

# 2. Add PDF libraries (html2canvas, jspdf, html2pdf) to head of mobile/register/index.html
filePathRegister = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePathRegister, 'r', encoding='utf-8') as f:
    regHtml = f.read()

pdf_libs = '''  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>'''

if 'html2canvas.min.js' not in regHtml:
    head_end = regHtml.find('</head>')
    if head_end >= 0:
        regHtml = regHtml[:head_end] + pdf_libs + '\n' + regHtml[head_end:]
        with open(filePathRegister, 'w', encoding='utf-8') as f:
            f.write(regHtml)
        print('Successfully added html2canvas, jspdf, and html2pdf CDN libraries to mobile/register/index.html head!')
    else:
        print('Could not find </head> in mobile/register/index.html!')
else:
    print('PDF libraries already in mobile/register/index.html head.')
