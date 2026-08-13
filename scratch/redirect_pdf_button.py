# 1. Expose downloadMemberProfilePdf on window in app.js
filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

if 'window.downloadMemberProfilePdf = downloadMemberProfilePdf;' not in appCode:
    appCode += '\n\nwindow.downloadMemberProfilePdf = downloadMemberProfilePdf;\nwindow.buildMemberMilestonesHtml = buildMemberMilestonesHtml;\nwindow.cleanHtmlForPdf = cleanHtmlForPdf;\nwindow.exportElementToPdf = exportElementToPdf;\n'
    with open(filePathApp, 'w', encoding='utf-8') as f:
        f.write(appCode)
    print('Exposed downloadMemberProfilePdf on window in app.js!')

# 2. Update mobile/register/index.html to call window.downloadMemberProfilePdf
filePathRegister = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePathRegister, 'r', encoding='utf-8') as f:
    regHtml = f.read()

s1 = regHtml.find('function ageDecimal(dob)')
if s1 < 0:
    s1 = regHtml.find('// ─── Done ─────────────────────────────────────────────────────────')

s2 = regHtml.find('document.getElementById(\'editAgainBtn\')')

redirect_js = r'''
    // ─── Redirect to main app.js Single Page PDF download (DRY, Zero Duplication) ───
    function redirectAndDownloadProfilePdf() {
      if (!chosenMember) {
        toast("Please select a member first", "error");
        return;
      }

      toast("Preparing Scout Record PDF...", "info");

      window.state = window.state || { members: [], badges: [], memberMilestones: [], badgeDefs: [], ranks: [] };
      if (!Array.isArray(window.state.members)) window.state.members = [];
      if (!Array.isArray(window.state.badges)) window.state.badges = [];
      if (!Array.isArray(window.state.memberMilestones)) window.state.memberMilestones = [];
      if (!Array.isArray(window.state.badgeDefs)) window.state.badgeDefs = [];
      if (!Array.isArray(window.state.ranks)) window.state.ranks = [];

      var mId = String(chosenMember.id);
      var formattedMember = {
        id: mId,
        fullName: chosenMember.full_name || chosenMember.fullName || [chosenMember.first_name, chosenMember.middle_name, chosenMember.last_name].filter(Boolean).join(" ") || "Member Profile",
        unit: chosenMember.unit || chosenUnit || "Rovers",
        gender: chosenMember.gender || "—",
        dob: chosenMember.dob || "—",
        bloodType: chosenMember.blood_type || chosenMember.bloodType || "—",
        phone: chosenMember.phone || "—",
        nationality: chosenMember.nationality || "Lebanese",
        parentType: chosenMember.parent_type || chosenMember.parentType || "Mother",
        parentPhone: chosenMember.parent_phone || chosenMember.parentPhone || "—",
        email: chosenMember.email || "—"
      };

      var existingIdx = window.state.members.findIndex(function(x) { return String(x.id) === mId; });
      if (existingIdx >= 0) {
        window.state.members[existingIdx] = formattedMember;
      } else {
        window.state.members.push(formattedMember);
      }

      var msIdx = window.state.memberMilestones.findIndex(function(x) { return String(x.member_id || x.memberId) === mId; });
      var msData = Object.assign({}, milestones, { member_id: mId });
      if (msIdx >= 0) {
        window.state.memberMilestones[msIdx] = msData;
      } else {
        window.state.memberMilestones.push(msData);
      }

      var badgesArr = Array.from(selectedBadges || []).map(function(bName) {
        return { memberId: mId, member_id: mId, badgeName: bName, badge_name: bName };
      });
      window.state.badges = window.state.badges.filter(function(b) { return String(b.memberId || b.member_id) !== mId; }).concat(badgesArr);

      if (!window.state.badgeDefs.length && typeof badgeDefs !== "undefined") {
        window.state.badgeDefs = badgeDefs || [];
      }

      function triggerDownload() {
        if (typeof window.downloadMemberProfilePdf === "function") {
          window.downloadMemberProfilePdf(mId, true);
        } else {
          toast("PDF generator unavailable", "error");
        }
      }

      if (typeof window.downloadMemberProfilePdf === "function") {
        triggerDownload();
      } else {
        var script = document.createElement("script");
        script.src = "../../app.js";
        script.onload = function() {
          triggerDownload();
        };
        script.onerror = function() {
          toast("Failed to load PDF engine", "error");
        };
        document.head.appendChild(script);
      }
    }

    var dlPdfBtn = document.getElementById("downloadPassPdfBtn");
    if (dlPdfBtn) {
      dlPdfBtn.addEventListener("click", redirectAndDownloadProfilePdf);
    }
'''

regHtml = regHtml[:s1] + redirect_js.strip() + '\n\n      ' + regHtml[s2:]

with open(filePathRegister, 'w', encoding='utf-8') as f:
    f.write(regHtml)

print('Successfully redirected PDF download button on /mobile/register to app.js downloadMemberProfilePdf!')
