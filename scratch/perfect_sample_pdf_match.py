filePathApp = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePathApp, 'r', encoding='utf-8') as f:
    appCode = f.read()

# 1. Update buildMemberMilestonesHtml rank chip rendering date order to match sample PDF
old_chip_render = """          const dHtml = d
            ? `<span style="opacity:.85;font-weight:600;margin-inline-start:6px;padding-inline-start:6px;border-inline-start:1px solid rgba(255,255,255,.4);">${escapeHtml(d)}</span>`
            : '';
          return `<span style="font-size:11.5px;font-weight:700;padding:5px 10px;border-radius:999px;background:${color};color:#fff;display:inline-flex;align-items:center;">${escapeHtml(r)}${dHtml}</span>`;"""

new_chip_render = """          const dHtml = d
            ? `<span style="opacity:.85;font-weight:600;margin-inline-end:6px;padding-inline-end:6px;border-inline-end:1px solid rgba(255,255,255,.4);">${escapeHtml(d)}</span>`
            : '';
          return `<span style="font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;background:${color};color:#fff;display:inline-flex;align-items:center;font-family:'Cairo',sans-serif;">${dHtml}${escapeHtml(r)}</span>`;"""

if old_chip_render in appCode:
    appCode = appCode.replace(old_chip_render, new_chip_render)
    print('Updated rank chip rendering in buildMemberMilestonesHtml!')

# 2. Replace downloadMemberProfilePdf with exact 1-to-1 template from sample PDF
s1 = appCode.find('function downloadMemberProfilePdf(memberId, isSinglePage = false) {')
s2 = appCode.find('function downloadLeaderProfilePdf(leaderId, isSinglePage = false) {')

if s1 >= 0 and s2 >= 0:
    new_dl_func = r'''function downloadMemberProfilePdf(memberId, isSinglePage = false) {
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
        
        const logoImg = `<img src="${escapeHtml(logoUrl)}" style="width:${badgeConfig.iconSize}; height:${badgeConfig.iconSize}; object-fit:contain; margin-bottom:4px; display:block;" crossorigin="anonymous" onerror="this.onerror=null;this.src='badge-icon.png';" />`;

        return `
          <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:${badgeConfig.padding}; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box; box-shadow: 0 1px 2px rgba(0,0,0,0.01);">
            ${logoImg}
            <div dir="rtl" style="font-weight:700; font-size:${badgeConfig.fontSize}; color:#1e293b; font-family:'Cairo', sans-serif; line-height:1.2; white-space:normal; word-break:break-word; max-width:100%; text-align:center;">${escapeHtml(bName)}</div>
          </div>
        `;
      }).join('')
    : '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">No badges earned yet.</div>';

  const container = document.createElement('div');
  container.style.cssText = 'position:fixed; left:0; top:0; width:794px; padding:28px 32px; font-family:Inter, Cairo, sans-serif; color:#0f172a; background:#ffffff; box-sizing:border-box; z-index:99999; visibility:visible;';

  container.innerHTML = `
    <div>
      <!-- MAIN CONTAINER -->
      <div style="margin-bottom: 20px; box-sizing: border-box;">
        
        <!-- TOP HEADER BRANDING (Logo LEFT, Date RIGHT, Full Width Purple Line) -->
        <div class="pdf-section-card" style="margin-bottom: 16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom: 8px;">
            <div style="display:flex; align-items:center; gap:12px;">
              <img src="../../logo.png" style="height:48px; max-width:240px; object-fit:contain; display:block;" crossorigin="anonymous" onerror="this.onerror=null;this.src='/logo.png';" alt="Logo" />
            </div>
            <div style="text-align:right;">
              <div style="font-size:8.5px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing:.08em;">GENERATED</div>
              <div style="font-size:11px; font-weight:800; color:#334155; margin-top:2px;">${new Date().toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' })}</div>
            </div>
          </div>
          <div style="height:2px; background:#6366f1; width:100%; margin-top:6px;"></div>
        </div>

        <!-- BANNER PROFILE CARD (Avatar LEFT, Name & Unit Pill LEFT) -->
        <div class="pdf-section-card" style="background:#eef2ff; border-radius:12px; padding:16px 20px; display:flex; align-items:center; gap:16px; margin-bottom: 16px;">
          <div style="width:50px; height:50px; border-radius:50%; background:#6366f1; color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:20px; flex-shrink:0;">
            ${escapeHtml(initials)}
          </div>
          <div style="text-align:left;">
            <h2 style="margin:0; font-size:20px; font-weight:900; color:#0f172a; font-family:'Outfit', 'Inter', sans-serif; letter-spacing:-0.02em;">${escapeHtml(m.fullName || 'Member Profile')}</h2>
            <div style="display:inline-block; margin-top:4px; padding:3px 10px; background:#6366f1; color:#ffffff; border-radius:6px; font-weight:800; font-size:10px; text-transform:uppercase; letter-spacing:.04em;">
              ${escapeHtml(m.unit || 'Rovers')}
            </div>
          </div>
        </div>

        <!-- DETAILS CARD SECTION -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:12px; padding:16px 18px; margin-bottom: 16px; background:#ffffff; box-shadow: 0 1px 2px rgba(0,0,0,0.01);">
          <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; margin-bottom:12px;">DETAILS</div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px 12px;">
            
            <div style="grid-column: 1 / -1; background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">FULL NAME</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.fullName || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">GENDER</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.gender || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">AGE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(ageStr)}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">BIRTH DATE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.dob || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">BLOOD TYPE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.bloodType || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">PHONE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.phone || '—')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">NATIONALITY</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.nationality || 'Lebanese')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">PARENT TYPE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.parentType || 'Mother')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">PARENT PHONE</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.parentPhone || '—')}</div>
            </div>

            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">UNIT</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px;">${escapeHtml(m.unit || 'Rovers')}</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:8px 12px;">
              <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em;">EMAIL</div>
              <div style="font-size:12px; font-weight:800; color:#0f172a; margin-top:2px; word-break:break-all;">${escapeHtml(m.email || '—')}</div>
            </div>

          </div>
        </div>

        <!-- BADGES CARD SECTION (BADGES on LEFT, Count on RIGHT) -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:12px; padding:16px 18px; background:#ffffff; margin-bottom: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em;">BADGES</div>
            <div style="font-size:11px; font-weight:700; color:#6366f1;">${badges.length} earned</div>
          </div>
          <div style="display:grid; grid-template-columns: repeat(${badgeConfig.cols}, 1fr); gap:${badgeConfig.gap}; align-content:start;">
            ${badgesGridHtml}
          </div>
        </div>

        <!-- ARABIC MILESTONE CARD SECTION (المسيرة Title RIGHT, Timeline RTL) -->
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:12px; padding:20px; background:#ffffff;" dir="rtl">
          <div style="display:flex; justify-content:flex-start; align-items:center; margin-bottom:14px;">
            <h3 style="margin:0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Cairo', sans-serif;">المسيرة</h3>
          </div>
          <div style="text-align:right;">
            ${milestonesHtml}
          </div>
        </div>

      </div>

      <!-- FOOTER BRANDING -->
      <div class="pdf-section-card" style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:12px; margin-top:24px; font-size:10px; color:#94a3b8; font-weight:600;">
        <div>Saida One · South District · Lebanese Scout Association</div>
        <div>Confidential — internal use only</div>
      </div>
    </div>
  `;

  exportElementToPdf(container, m.fullName.replace(/\s+/g, '_') + '_Scout_Record_SinglePage.pdf', isSinglePage);
}

'''
    appCode = appCode[:s1] + new_dl_func + appCode[s2:]
    with open(filePathApp, 'w', encoding='utf-8') as f:
        f.write(appCode)
    print('Successfully updated downloadMemberProfilePdf!')

