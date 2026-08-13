filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

s1 = appCode.find('function downloadMemberProfilePdf(memberId, isSinglePage = false) {')
s2 = appCode.find('function downloadLeaderProfilePdf(leaderId, isSinglePage = false) {')

if s1 >= 0 and s2 >= 0:
    new_dl_member = r'''function downloadMemberProfilePdf(memberId, isSinglePage = false) {
  const membersList = (window.state && window.state.members && window.state.members.length) ? window.state.members : state.members;
  const m = membersList.find(x => String(x.id) === String(memberId));
  if (!m) {
    showToast('Member not found (ID: ' + memberId + ')', 'error');
    return;
  }

  showToast('Generating PDF...', 'info');

  const badgesList = (window.state && window.state.badges) ? window.state.badges : state.badges;
  const badges = badgesList.filter(b => String(b.memberId || b.member_id) === String(memberId));
  const rawMilestonesHtml = buildMemberMilestonesHtml(m.id);
  const milestonesHtml = cleanHtmlForPdf(rawMilestonesHtml);

  const initials = getInitials(m.fullName);
  const ageVal = ageDecimal(m.dob);
  const ageStr = ageVal !== null ? ageVal.toFixed(1) : '—';

  const badgeConfig = getAdaptiveBadgeGridConfig(badges.length);

  const badgesGridHtml = badges.length
    ? badges.map(b => {
        const rawName = (typeof b === 'string') ? b : (b.badgeName || b.badge_name || b.name || b.title || (state.badgeDefs.find(d => String(d.id) === String(b.badgeId || b.badge_id || b.badge_definition_id || b.id))?.name));
        const bName = String(rawName || 'شارة').trim();
        const def = state.badgeDefs.find(d => (d.name || '').toLowerCase() === (bName || '').toLowerCase());
        const logoUrl = (def && def.logoUrl) || (typeof badgeDefLogo === 'function' ? badgeDefLogo(bName) : null) || b.logoUrl || b.logo_url || window.DEFAULT_BADGE_ICON || 'badge-icon.png';
        
        const logoImg = `<img src="${escapeHtml(logoUrl)}" style="width:${badgeConfig.iconSize}; height:${badgeConfig.iconSize}; object-fit:contain; margin-bottom:2px; display:block;" crossorigin="anonymous" onerror="this.onerror=null;this.src='badge-icon.png';" />`;

        return `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:${badgeConfig.padding}; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box;">
            ${logoImg}
            <div dir="rtl" style="font-weight:700; font-size:${badgeConfig.fontSize}; color:#1e293b; font-family:'Cairo', sans-serif; line-height:1.2; white-space:normal; word-break:break-word; max-width:100%; text-align:center;">${escapeHtml(bName)}</div>
          </div>
        `;
      }).join('')
    : '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">No badges earned yet.</div>';

  const container = document.createElement('div');
  container.setAttribute('dir', 'rtl');
  container.style.cssText = 'position:fixed; left:0; top:0; width:794px; padding:24px 28px; font-family:\'Cairo\', Inter, sans-serif; color:#0f172a; background:#ffffff; box-sizing:border-box; z-index:99999; visibility:visible; text-align:right;';

  container.innerHTML = `
    <div dir="rtl" style="text-align:right;">
      <!-- MAIN PAGE CARDS CONTAINER (100% RTL) -->
      <div style="margin-bottom: 16px; box-sizing: border-box;" dir="rtl">
        
        <!-- TOP HEADER BRANDING (Logo RIGHT, Date LEFT) -->
        <div class="pdf-section-card" style="display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #6366f1; padding-bottom: 10px; margin-bottom: 14px;" dir="rtl">
          <div style="display:flex; align-items:center; gap:12px;">
            <img src="../../logo.png" style="height:52px; max-width:240px; object-fit:contain; display:block;" crossorigin="anonymous" onerror="this.onerror=null;this.src='/logo.png';" alt="Logo" />
          </div>
          <div style="text-align:left;" dir="ltr">
            <div style="font-size:9px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:.05em;">GENERATED</div>
            <div style="font-size:11px; font-weight:700; color:#475569;">${new Date().toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' })}</div>
          </div>
        </div>

        <!-- BANNER PROFILE CARD (All elements RIGHT-aligned) -->
        <div class="pdf-section-card" style="background:#eef2ff; border-radius:10px; padding:12px 16px; display:flex; align-items:center; justify-content:flex-start; gap:14px; margin-bottom: 14px;" dir="rtl">
          <div style="width:48px; height:48px; border-radius:50%; background:#6366f1; color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:18px; flex-shrink:0;">
            ${escapeHtml(initials)}
          </div>
          <div style="text-align:right; display:flex; flex-direction:column; align-items:flex-start;">
            <h2 style="margin:0; font-size:18px; font-weight:800; color:#0f172a; font-family:'Cairo', sans-serif;">${escapeHtml(m.fullName || 'Member Profile')}</h2>
            <div style="display:inline-block; margin-top:4px; padding:2px 10px; background:#6366f1; color:#ffffff; border-radius:5px; font-weight:800; font-size:9.5px; text-transform:uppercase; letter-spacing:.04em;">
              ${escapeHtml(m.unit || 'Rovers')}
            </div>
          </div>
        </div>

        <!-- DETAILS CARD SECTION (RTL aligned) -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; margin-bottom: 14px; background:#fafafa;" dir="rtl">
          <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px; text-align:right;">DETAILS / التفاصيل</div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 10px;" dir="rtl">
            
            <div style="grid-column: 1 / -1; background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">FULL NAME / الاسم الكامل</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.fullName || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">GENDER / الجنس</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.gender || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">AGE / العمر</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(ageStr)}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BIRTH DATE / تاريخ الميلاد</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.dob || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BLOOD TYPE / زمرة الدم</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.bloodType || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PHONE / رقم الهاتف</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.phone || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">NATIONALITY / الجنسية</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.nationality || 'Lebanese')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT TYPE / صلة ولي الأمر</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.parentType || 'Mother')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT PHONE / هاتف ولي الأمر</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.parentPhone || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">UNIT / الوحدة</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a;">${escapeHtml(m.unit || 'Rovers')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px; text-align:right;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">EMAIL / البريد الإلكتروني</div>
              <div style="font-size:11.5px; font-weight:800; color:#0f172a; word-break:break-all;">${escapeHtml(m.email || '—')}</div>
            </div>

          </div>
        </div>

        <!-- BADGES CARD SECTION (RTL aligned) -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; background:#fafafa; margin-bottom: 14px;" dir="rtl">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;" dir="rtl">
            <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em;">BADGES / الأوسمة</div>
            <div style="font-size:10.5px; font-weight:700; color:#6366f1;">${badges.length} earned</div>
          </div>
          <div style="display:grid; grid-template-columns: repeat(${badgeConfig.cols}, 1fr); gap:${badgeConfig.gap}; align-content:start;" dir="rtl">
            ${badgesGridHtml}
          </div>
        </div>

        <!-- ARABIC MILESTONE CARD SECTION (RTL aligned) -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#fafafa;" dir="rtl">
          <div style="display:flex; justify-content:flex-start; align-items:center; margin-bottom:10px;">
            <h3 style="margin:0; font-size:16px; font-weight:900; color:#0f172a; font-family:'Cairo', sans-serif;">المسيرة</h3>
          </div>
          <div style="text-align:right;">
            ${milestonesHtml}
          </div>
        </div>

      </div>

      <!-- FOOTER BRANDING (RTL aligned) -->
      <div class="pdf-section-card" style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:10px; margin-top:16px; font-size:9.5px; color:#94a3b8;" dir="rtl">
        <div>الكشاف المسلم في لبنان · مفوضية الجنوب · فوج صيدا الأول</div>
        <div>Confidential — internal use only</div>
      </div>
    </div>
  `;

  exportElementToPdf(container, m.fullName.replace(/\s+/g, '_') + '_Scout_Record_SinglePage.pdf', isSinglePage);
}

'''
    appCode = appCode[:s1] + new_dl_member + appCode[s2:]
    with open(filePathApp, 'w', encoding='utf-8') as f:
        f.write(appCode)
    print('Successfully updated PDF layout to 100% RTL!')
else:
    print('Could not find downloadMemberProfilePdf in app.js')
