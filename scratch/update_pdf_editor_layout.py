filePath = r'c:\Users\PC\Documents\GitHub\testing\app.js'

with open(filePath, 'r', encoding='utf-8') as f:
    code = f.read()

s1 = code.find('function renderPdfEditorLivePreview() {')
s2 = code.find('function exportPdfFromEditor(')

if s1 >= 0 and s2 >= 0:
    new_func = r'''function renderPdfEditorLivePreview() {
  const container = $('#pdfLivePreviewContainer');
  if (!container) return;

  const color = pdfEditorState.color;
  const cols = pdfEditorState.cols;
  const initials = getInitials(pdfEditorState.fullName);
  const ageVal = ageDecimal(pdfEditorState.dob);
  const ageStr = ageVal !== null ? ageVal.toFixed(1) : '—';
  const badgeConfig = getBadgeGridConfig(pdfEditorState.badges.length, pdfEditorState.badgeSize, pdfEditorState.badgeGap);

  const badgesGridHtml = pdfEditorState.badges.length
    ? pdfEditorState.badges.map((b, idx) => {
        const rawName = (typeof b === 'string') ? b : (b.badgeName || b.badge_name || b.name || b.title || (state.badgeDefs.find(d => String(d.id) === String(b.badgeId || b.badge_id || b.badge_definition_id || b.id))?.name));
        const bName = String(rawName || 'شارة').trim();
        const def = state.badgeDefs.find(d => (d.name || '').toLowerCase() === (bName || '').toLowerCase());
        const logoUrl = (def && def.logoUrl) || (typeof badgeDefLogo === 'function' ? badgeDefLogo(bName) : null) || b.logoUrl || b.logo_url || window.DEFAULT_BADGE_ICON || 'badge-icon.png';
        
        const logoImg = `<img src="${escapeHtml(logoUrl)}" style="width:${badgeConfig.iconSize}; height:${badgeConfig.iconSize}; object-fit:contain; margin-bottom:2px; display:block;" onerror="this.onerror=null;this.src='badge-icon.png';" />`;

        return `
          <div draggable="true" data-badge-index="${idx}" class="pdf-editor-badge-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:${badgeConfig.padding}; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box; cursor:grab; transition:all 0.15s ease; position:relative;" title="Drag to reorder position">
            <span style="position:absolute; top:1px; right:4px; font-size:9px; color:#94a3b8; opacity:0.7; pointer-events:none;">⋮⋮</span>
            ${logoImg}
            <div contenteditable="true" dir="rtl" style="font-weight:700; font-size:${badgeConfig.fontSize}; color:#1e293b; font-family:'Cairo', sans-serif; line-height:1.2; white-space:normal; word-break:break-word; outline:none; max-width:100%; text-align:center;">${escapeHtml(bName)}</div>
          </div>
        `;
      }).join('')
    : '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">No badges earned yet.</div>';

  const showBadgesCard = pdfEditorState.showBadges;
  const p1Style = showBadgesCard
    ? 'min-height: 1010px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 24px; box-sizing: border-box;'
    : 'margin-bottom: 12px; box-sizing: border-box;';

  container.innerHTML = `
    <div>
      <!-- MAIN CONTAINER -->
      <div style="${p1Style}">
        <div>
          <!-- TOP HEADER BRANDING -->
          ${pdfEditorState.showHeader ? `
          <div class="pdf-section-card" style="display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid ${color}; padding-bottom: 10px; margin-bottom: 14px;">
            <div style="display:flex; align-items:center; gap:12px;">
              <img src="logo.png" style="height:52px; max-width:240px; object-fit:contain; display:block;" onerror="this.onerror=null;this.src='badge-icon.png';" alt="Logo" />
            </div>
            <div style="text-align:right;">
              <div style="font-size:9px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Generated</div>
              <div contenteditable="true" style="font-size:11px; font-weight:700; color:#475569; outline:none;">${new Date().toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' })}</div>
            </div>
          </div>` : ''}

          <!-- BANNER PROFILE CARD -->
          ${pdfEditorState.showBanner ? `
          <div class="pdf-section-card" style="background:#eef2ff; border-radius:10px; padding:12px 16px; display:flex; align-items:center; gap:14px; margin-bottom: 12px;">
            <div style="width:44px; height:44px; border-radius:50%; background:${color}; color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:17px; flex-shrink:0;">
              ${escapeHtml(initials)}
            </div>
            <div>
              <h2 contenteditable="true" style="margin:0; font-size:18px; font-weight:800; color:#0f172a; font-family:Outfit, sans-serif; outline:none;">${escapeHtml(pdfEditorState.fullName || 'Member Profile')}</h2>
              <div contenteditable="true" style="display:inline-block; margin-top:3px; padding:2px 8px; background:${color}; color:#ffffff; border-radius:5px; font-weight:800; font-size:9.5px; text-transform:uppercase; letter-spacing:.04em; outline:none;">
                ${escapeHtml(pdfEditorState.unit || 'Rovers')}
              </div>
            </div>
          </div>` : ''}

          <!-- DETAILS CARD SECTION -->
          ${pdfEditorState.showDetails ? `
          <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; margin-bottom: 12px; background:#fafafa;">
            <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px;">DETAILS</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 10px;">
              
              <div style="grid-column: 1 / -1; background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">FULL NAME</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.fullName || '—')}</div>
              </div>

              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">GENDER</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.gender || '—')}</div>
              </div>
              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">AGE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(ageStr)}</div>
              </div>

              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BIRTH DATE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.dob || '—')}</div>
              </div>
              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BLOOD TYPE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.bloodType || '—')}</div>
              </div>

              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PHONE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.phone || '—')}</div>
              </div>
              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">NATIONALITY</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.nationality || 'Lebanese')}</div>
              </div>

              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT TYPE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.parentType || 'Mother')}</div>
              </div>
              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT PHONE</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.parentPhone || '—')}</div>
              </div>

              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">UNIT</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; outline:none;">${escapeHtml(pdfEditorState.unit || 'Rovers')}</div>
              </div>
              <div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">
                <div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">EMAIL</div>
                <div contenteditable="true" style="font-size:11.5px; font-weight:800; color:#0f172a; word-break:break-all; outline:none;">${escapeHtml(pdfEditorState.email || '—')}</div>
              </div>

            </div>
          </div>` : ''}
        </div>

        <!-- BADGES CARD SECTION (When Badges card is enabled) -->
        ${showBadgesCard ? `
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; background:#fafafa; flex:1; display:flex; flex-direction:column; justify-content:flex-start;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em;">BADGES</div>
            <div contenteditable="true" style="font-size:10.5px; font-weight:700; color:${color}; outline:none;">${pdfEditorState.badges.length} earned</div>
          </div>
          <div style="display:grid; grid-template-columns: repeat(${cols}, 1fr); gap:${badgeConfig.gap}; align-content:start;">
            ${badgesGridHtml}
          </div>
        </div>` : ''}

        <!-- ARABIC MILESTONE CARD SECTION (Replaces Badges card when Badges is disabled) -->
        ${(!showBadgesCard && pdfEditorState.showMilestones) ? `
        <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#fafafa; margin-top:4px;">
          <div style="display:flex; justify-content:flex-end; align-items:center; margin-bottom:10px;">
            <h3 contenteditable="true" style="margin:0; font-size:15px; font-weight:900; color:#0f172a; font-family:'Cairo', sans-serif; outline:none;">المسيرة</h3>
          </div>
          <div contenteditable="true" style="outline:none;">
            ${pdfEditorState.milestonesHtml}
          </div>
        </div>` : ''}
      </div>

      <!-- ARABIC MILESTONE CARD SECTION (Page 2 when Badges card is enabled) -->
      ${(showBadgesCard && pdfEditorState.showMilestones) ? `
      <div class="pdf-section-card" style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#fafafa;">
        <div style="display:flex; justify-content:flex-end; align-items:center; margin-bottom:10px;">
          <h3 contenteditable="true" style="margin:0; font-size:15px; font-weight:900; color:#0f172a; font-family:'Cairo', sans-serif; outline:none;">المسيرة</h3>
        </div>
        <div contenteditable="true" style="outline:none;">
          ${pdfEditorState.milestonesHtml}
        </div>
      </div>` : ''}
    </div>

    <!-- FOOTER BRANDING -->
    ${pdfEditorState.showFooter ? `
    <div class="pdf-section-card" style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:10px; margin-top:16px; font-size:9.5px; color:#94a3b8;">
      <div contenteditable="true" style="outline:none;">Saida One · South District · Lebanese Scout Association</div>
      <div contenteditable="true" style="outline:none;">Confidential — internal use only</div>
    </div>` : ''}
  `;

  bindPdfEditorDragAndDrop(container);
}

'''
    code = code[:s1] + new_func + code[s2:]
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('Successfully updated PDF Profile Editor & Customizer layout!')
else:
    print('Could not find slice boundaries in app.js!')
