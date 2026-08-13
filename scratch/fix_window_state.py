filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

# 1. Attach window.state = state right after state object declaration
if 'window.state = state;' not in appCode:
    appCode = appCode.replace('const state = {', 'const state = window.state = {')
    print('Attached window.state = state!')

# 2. Update downloadMemberProfilePdf to check window.state.members safely
old_dl_start = "function downloadMemberProfilePdf(memberId, isSinglePage = false) {\n  const m = state.members.find(x => String(x.id) === String(memberId));"
new_dl_start = """function downloadMemberProfilePdf(memberId, isSinglePage = false) {
  const membersList = (window.state && window.state.members && window.state.members.length) ? window.state.members : state.members;
  const m = membersList.find(x => String(x.id) === String(memberId));"""

if old_dl_start in appCode:
    appCode = appCode.replace(old_dl_start, new_dl_start)
    print('Updated downloadMemberProfilePdf member lookup!')
else:
    # Alternate replacement
    appCode = appCode.replace("const m = state.members.find(x => String(x.id) === String(memberId));", "const membersList = (window.state && window.state.members && window.state.members.length) ? window.state.members : state.members;\n  const m = membersList.find(x => String(x.id) === String(memberId));")
    print('Updated member lookup fallback!')

# 3. Update badge lookup in downloadMemberProfilePdf
old_badge_lookup = "const badges = state.badges.filter(b => String(b.memberId || b.member_id) === String(memberId));"
new_badge_lookup = "const badgesList = (window.state && window.state.badges) ? window.state.badges : state.badges;\n  const badges = badgesList.filter(b => String(b.memberId || b.member_id) === String(memberId));"
appCode = appCode.replace(old_badge_lookup, new_badge_lookup)

with open(filePathApp, 'w', encoding='utf-8') as f:
    f.write(appCode)

print('Successfully fixed window.state synchronisation in app.js!')
