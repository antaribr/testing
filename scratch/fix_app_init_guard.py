filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

# 1. Update showToast container lookup
old_showToast = "function showToast(message, type = 'info', duration = 4000) {\n  const container = document.getElementById('toastContainer');"
new_showToast = "function showToast(message, type = 'info', duration = 4000) {\n  const container = document.getElementById('toastContainer') || document.getElementById('toast');"

if old_showToast in appCode:
    appCode = appCode.replace(old_showToast, new_showToast)
    print('Updated showToast in app.js!')
else:
    # Try alternate match if formatting differs
    appCode = appCode.replace("const container = document.getElementById('toastContainer');", "const container = document.getElementById('toastContainer') || document.getElementById('toast');")
    print('Updated toastContainer fallback in app.js!')

# 2. Add guard at top of init() in app.js so standalone pages don't throw dashboard errors
old_init = "function init() {"
new_init = "function init() {\n  if (!document.getElementById('membersTableBody') && !document.getElementById('navMenu') && !document.getElementById('statsPageContainer')) {\n    return; // Skip dashboard DOM initialization on mobile/standalone pages\n  }"

appCode = appCode.replace(old_init, new_init, 1)

with open(filePathApp, 'w', encoding='utf-8') as f:
    f.write(appCode)

print('Added page guard to init() in app.js!')
