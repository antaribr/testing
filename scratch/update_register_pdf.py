import os
import re

filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the broken downloadRegisterScoutPassPdf code first if it exists
broken_code_pattern = r'// ─── Single-Page Scout Pass PDF Generator ─────────────────────────.*?dlPdfBtn\.addEventListener\(\'click\', downloadRegisterScoutPassPdf\);'
html = re.sub(broken_code_pattern, '', html, flags=re.DOTALL)

# Clean PDF generator JS code with ZERO quote syntax errors
pdf_js_code = '''
    // ─── Single-Page Scout Pass PDF Generator ─────────────────────────
    function downloadRegisterScoutPassPdf() {
      if (!chosenMember) {
        toast("يرجى تحديد العضو أولاً", "error");
        return;
      }

      toast("جاري تجهيز وثيقة القيد الكشفية (PDF)...", "info");

      var m = chosenMember;
      var memberName = m.full_name || ((m.first_name || "") + " " + (m.last_name || "")).trim() || "Scout_Member";
      var initialsStr = initials(memberName);
      var unitName = chosenUnit || m.unit || "Scouts";

      var badgesArr = Array.from(selectedBadges || []);
      var badgesGridHtml = "";

      if (badgesArr.length > 0) {
        badgesGridHtml = badgesArr.map(function(bName) {
          var logoUrl = (typeof badgeDefLogo === "function" ? badgeDefLogo(bName) : null) || window.DEFAULT_BADGE_ICON || "../../logo.png";
          return '<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:8px 6px; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box;">' +
            '<img src="' + esc(logoUrl) + '" style="width:24px; height:24px; object-fit:contain; margin-bottom:2px; display:block;" alt="badge" />' +
            '<div dir="rtl" style="font-weight:700; font-size:10.5px; color:#1e293b; font-family:Cairo, sans-serif; line-height:1.2; text-align:center;">' + esc(bName) + '</div>' +
          '</div>';
        }).join('');
      } else {
        badgesGridHtml = '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">لم يتم تحديد شارات بعد</div>';
      }

      var milestonesSummaryHtml = "";
      if (milestones) {
        if (milestones.join_year) {
          milestonesSummaryHtml += '<div style="padding:8px 12px; background:rgba(0,0,0,0.02); border:1px solid #e2e8f0; border-radius:6px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;" dir="rtl">' +
            '<div style="font-weight:700; font-size:12px; color:#475569; font-family:Cairo,sans-serif;">سنة الانضمام إلى الجمعية</div>' +
            '<div style="font-weight:800; font-size:14px; color:#6366f1;">' + esc(milestones.join_year) + '</div>' +
          '</div>';
        }
        if (milestones.yellow_passed) {
          milestonesSummaryHtml += '<div style="padding:10px; background:#fffdf0; border:1px solid #fef08a; border-inline-start:4px solid #eab308; border-radius:6px; margin-bottom:6px;" dir="rtl">' +
            '<div style="font-weight:800; font-size:13px; color:#854d0e; font-family:Cairo,sans-serif;">الفرع الأصفر</div>' +
            (milestones.yellow_ranks && milestones.yellow_ranks.length ? '<div style="font-size:11.5px; color:#a16207; margin-top:4px;">الرتب: ' + esc(milestones.yellow_ranks.join(' · ')) + '</div>' : '') +
          '</div>';
        }
        if (milestones.green_passed) {
          milestonesSummaryHtml += '<div style="padding:10px; background:#f0fdf4; border:1px solid #bbf7d0; border-inline-start:4px solid #10b981; border-radius:6px; margin-bottom:6px;" dir="rtl">' +
            '<div style="font-weight:800; font-size:13px; color:#166534; font-family:Cairo,sans-serif;">الفرع الأخضر</div>' +
            (milestones.green_ranks && milestones.green_ranks.length ? '<div style="font-size:11.5px; color:#15803d; margin-top:4px;">الرتب: ' + esc(milestones.green_ranks.join(' · ')) + '</div>' : '') +
            (milestones.green_consecration_year ? '<div style="font-size:11.5px; color:#15803d; margin-top:2px;">التكريس: ' + esc(milestones.green_consecration_year) + '</div>' : '') +
          '</div>';
        }
        if (milestones.red_passed) {
          milestonesSummaryHtml += '<div style="padding:10px; background:#fef2f2; border:1px solid #fecaca; border-inline-start:4px solid #ef4444; border-radius:6px; margin-bottom:6px;" dir="rtl">' +
            '<div style="font-weight:800; font-size:13px; color:#991b1b; font-family:Cairo,sans-serif;">الفرع الأحمر</div>' +
            (milestones.red_ranks && milestones.red_ranks.length ? '<div style="font-size:11.5px; color:#b91c1c; margin-top:4px;">الرتب: ' + esc(milestones.red_ranks.join(' · ')) + '</div>' : '') +
            (milestones.red_consecration_year ? '<div style="font-size:11.5px; color:#b91c1c; margin-top:2px;">التكريس: ' + esc(milestones.red_consecration_year) + '</div>' : '') +
            (milestones.red_departure_year ? '<div style="font-size:11.5px; color:#b91c1c; margin-top:2px;">الرحيل: ' + esc(milestones.red_departure_year) + '</div>' : '') +
          '</div>';
        }
      }
      if (!milestonesSummaryHtml) {
        milestonesSummaryHtml = '<div style="text-align:center; padding:12px; color:#64748b; font-size:12px; font-family:Cairo,sans-serif;">لا يوجد سجل مسيرة مسجل حالياً</div>';
      }

      var container = document.createElement("div");
      container.style.cssText = "position:fixed; left:0; top:0; width:794px; padding:24px 28px; font-family:Inter, Cairo, sans-serif; color:#0f172a; background:#ffffff; box-sizing:border-box; z-index:99999; visibility:visible;";

      container.innerHTML = 
        '<div>' +
          '<div style="min-height: 1010px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 24px; box-sizing: border-box;">' +
            '<div>' +
              '<!-- TOP HEADER BRANDING -->' +
              '<div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #6366f1; padding-bottom: 10px; margin-bottom: 14px;">' +
                '<div style="display:flex; align-items:center; gap:12px;">' +
                  '<img src="../../logo.png" style="height:52px; max-width:240px; object-fit:contain; display:block;" alt="Logo" />' +
                '</div>' +
                '<div style="text-align:right;">' +
                  '<div style="font-size:9px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Generated</div>' +
                  '<div style="font-size:11px; font-weight:700; color:#475569;">' + new Date().toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' }) + '</div>' +
                '</div>' +
              '</div>' +

              '<!-- BANNER PROFILE CARD -->' +
              '<div style="background:#eef2ff; border-radius:10px; padding:12px 16px; display:flex; align-items:center; gap:14px; margin-bottom: 12px;">' +
                '<div style="width:44px; height:44px; border-radius:50%; background:#6366f1; color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:17px; flex-shrink:0;">' +
                  esc(initialsStr) +
                '</div>' +
                '<div>' +
                  '<h2 style="margin:0; font-size:18px; font-weight:800; color:#0f172a; font-family:Cairo, sans-serif;">' + esc(memberName) + '</h2>' +
                  '<div style="display:inline-block; margin-top:3px; padding:2px 8px; background:#6366f1; color:#ffffff; border-radius:5px; font-weight:800; font-size:9.5px; text-transform:uppercase; letter-spacing:.04em;">' +
                    esc(unitName) +
                  '</div>' +
                '</div>' +
              '</div>' +

              '<!-- DETAILS CARD SECTION -->' +
              '<div style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; margin-bottom: 12px; background:#fafafa;">' +
                '<div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px;">MEMBER DETAILS</div>' +
                '<div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 10px;">' +
                  '<div style="grid-column: 1 / -1; background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">FULL NAME</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(memberName) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">GENDER</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(m.gender || '—') + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BIRTH DATE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(m.dob || '—') + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BLOOD TYPE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(m.blood_type || m.bloodType || '—') + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PHONE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(m.phone || '—') + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">UNIT</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(unitName) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">EMAIL</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a; word-break:break-all;">' + esc(m.email || '—') + '</div>' +
                  '</div>' +
                '</div>' +
              '</div>' +

              '<!-- BADGES CARD SECTION -->' +
              '<div style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; background:#fafafa; flex:1; display:flex; flex-direction:column; justify-content:flex-start;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                  '<div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em;">BADGES</div>' +
                  '<div style="font-size:10.5px; font-weight:700; color:#6366f1;">' + badgesArr.length + ' earned</div>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:8px; align-content:start;">' +
                  badgesGridHtml +
                '</div>' +
              '</div>' +
            '</div>' +

            '<!-- ARABIC MILESTONE CARD SECTION -->' +
            '<div style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#fafafa; margin-top:12px;">' +
              '<div style="display:flex; justify-content:flex-end; align-items:center; margin-bottom:10px;">' +
                '<h3 style="margin:0; font-size:15px; font-weight:900; color:#0f172a; font-family:Cairo, sans-serif;">المسيرة</h3>' +
              '</div>' +
              '<div>' +
                milestonesSummaryHtml +
              '</div>' +
            '</div>' +
          '</div>' +

          '<!-- FOOTER BRANDING -->' +
          '<div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:10px; margin-top:16px; font-size:9.5px; color:#94a3b8;">' +
            '<div>Saida One · South District · Lebanese Scout Association</div>' +
            '<div>Confidential — internal use only</div>' +
          '</div>' +
        '</div>';

      document.body.appendChild(container);

      html2canvas(container, {
        scale: 2,
        useCORS: true,
        logging: false,
        allowTaint: true
      }).then(function(canvas) {
        container.remove();
        var imgData = canvas.toDataURL("image/jpeg", 0.95);
        var _jsPDF = window.jspdf ? window.jspdf.jsPDF : window.jsPDF;
        if (_jsPDF) {
          var pageW = 210;
          var pageH = (canvas.height * pageW) / canvas.width;
          var pdf = new _jsPDF({
            unit: "mm",
            format: [pageW, pageH],
            orientation: "portrait",
            compress: true
          });
          pdf.addImage(imgData, "JPEG", 0, 0, pageW, pageH);
          var safeFileName = memberName.replace(/\\s+/g, "_") + "_Scout_Pass_SinglePage.pdf";
          pdf.save(safeFileName);
          toast("تم تحميل وثيقة القيد الكشفية بنجاح! / Single-page PDF downloaded!", "success");
        } else {
          toast("تعذر العثور على مكتبة PDF", "error");
        }
      }).catch(function(err) {
        try { container.remove(); } catch (_) {}
        console.error("[PDF Error]", err);
        toast("خطأ في تحميل PDF: " + (err.message || err), "error");
      });
    }

    var dlPdfBtn = document.getElementById("downloadPassPdfBtn");
    if (dlPdfBtn) {
      dlPdfBtn.addEventListener("click", downloadRegisterScoutPassPdf);
    }
'''

done_listener_target = "document.getElementById('editAgainBtn').addEventListener('click', function(){"
if done_listener_target in html:
    html = html.replace(done_listener_target, pdf_js_code + '\n    ' + done_listener_target)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated mobile/register/index.html cleanly!')
