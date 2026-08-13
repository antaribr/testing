filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

s1 = html.find('function downloadRegisterScoutRecordPdf()')
s2 = html.find('var dlPdfBtn = document.getElementById("downloadPassPdfBtn");')

if s1 >= 0 and s2 >= 0:
    pdf_exact_js = r'''
    // ─── Age decimal helper ───────────────────────────────────────────
    function ageDecimal(dob) {
      if (!dob) return null;
      var d = new Date(dob);
      if (isNaN(d.getTime())) return null;
      var now = new Date();
      var diffMs = now - d;
      return diffMs / (1000 * 60 * 60 * 24 * 365.25);
    }

    function formatAnyDateValue(val) {
      if (!val) return "";
      var str = String(val).trim();
      return str || "";
    }

    function getAdaptiveBadgeGridConfig(badgeCount) {
      if (badgeCount <= 12) {
        return { cols: 4, padding: "10px 8px", fontSize: "11.5px", iconSize: "26px", gap: "10px" };
      } else if (badgeCount <= 24) {
        return { cols: 5, padding: "8px 6px", fontSize: "10.5px", iconSize: "22px", gap: "8px" };
      } else if (badgeCount <= 42) {
        return { cols: 6, padding: "7px 5px", fontSize: "10px", iconSize: "20px", gap: "7px" };
      } else {
        return { cols: 7, padding: "6px 4px", fontSize: "9px", iconSize: "18px", gap: "6px" };
      }
    }

    function buildMemberMilestonesHtmlForRegister(m, row) {
      if (!row) {
        return '<div style="padding:16px; text-align:center; color:#64748b; font-size:12px;">No milestones recorded yet</div>';
      }

      var html = '<div style="display:flex; flex-direction:column; gap:12px;" dir="rtl">';

      if (row.join_year) {
        html += '<div style="padding:12px 14px; background:rgba(0,0,0,0.02); border:1px solid #e2e8f0; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
          '<div style="font-weight:700; font-size:13px; color:#475569; font-family:Cairo,sans-serif;">سنة الانضمام إلى الجمعية</div>' +
          '<div style="font-weight:800; font-size:15px; color:#6366f1;">' + esc(row.join_year) + '</div>' +
        '</div>';
      }

      function branchBlock(color, title, passedFlag, ranksArr, consecrationYear, departureYear, leadershipArr, rankDatesMap) {
        var hasLead = !!(leadershipArr && leadershipArr.length);
        var hasRanks = !!(ranksArr && ranksArr.length);
        if (!passedFlag && !hasRanks && !consecrationYear && !departureYear && !hasLead) return "";
        var dates = (rankDatesMap && typeof rankDatesMap === "object") ? rankDatesMap : {};

        var chips = hasRanks
          ? '<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">' + ranksArr.map(function(r) {
              var d = formatAnyDateValue(dates[r]);
              var dHtml = d
                ? '<span style="opacity:.85; font-weight:600; margin-inline-start:6px; padding-inline-start:6px; border-inline-start:1px solid rgba(255,255,255,.4);">' + esc(d) + '</span>'
                : '';
              return '<span style="font-size:11.5px; font-weight:700; padding:5px 10px; border-radius:999px; background:' + color + '; color:#fff; display:inline-flex; align-items:center;">' + esc(r) + dHtml + '</span>';
            }).join("") + '</div>'
          : '<div style="font-size:12px; color:#94a3b8; margin-top:6px; font-family:Cairo,sans-serif;">لم يتم تحديد رتب</div>';

        var years = "";
        if (consecrationYear) {
          years += '<div style="font-size:12.5px; color:#475569; margin-top:6px; font-family:Cairo,sans-serif;">🎯 <strong>التكريس:</strong> ' + esc(formatAnyDateValue(consecrationYear)) + '</div>';
        }
        if (departureYear) {
          years += '<div style="font-size:12.5px; color:#475569; margin-top:4px; font-family:Cairo,sans-serif;">🚶 <strong>الرحيل:</strong> ' + esc(formatAnyDateValue(departureYear)) + '</div>';
        }

        var leadHtml = "";
        if (hasLead) {
          leadHtml = '<div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0;" dir="rtl">' +
            '<div style="font-size:12px; font-weight:800; color:#475569; margin-bottom:6px; text-align:right; font-family:Cairo,sans-serif;">المراكز</div>' +
            '<div style="display:flex; flex-direction:column; gap:6px;">' +
              leadershipArr.map(function(l) {
                if (!l || !l.role) return "";
                var meta = [];
                if (l.name) meta.push('<span style="color:#475569; font-weight:700;">' + esc(l.name) + '</span>');
                if (l.year) meta.push('<span style="color:#94a3b8; font-weight:700;">' + esc(l.year) + '</span>');
                var metaHtml = meta.length
                  ? '<div style="font-size:11.5px; display:flex; gap:6px; align-items:center; font-family:Cairo,sans-serif;">' + meta.join('<span style="color:#cbd5e1;">·</span>') + '</div>'
                  : '';
                var campHtml = "";
                if (l.camp && l.camp.organized) {
                  var lines = [];
                  if (l.camp.name) lines.push({label:"اسم المخيم", value:l.camp.name});
                  if (l.camp.place) lines.push({label:"مكان المخيم", value:l.camp.place});
                  if (l.camp.date) lines.push({label:"تاريخ المخيم", value:l.camp.date});
                  campHtml = '<div style="margin-top:6px; padding:8px 10px; background:rgba(0,0,0,0.02); border:1px dashed #e2e8f0; border-radius:6px; font-family:Cairo,sans-serif;">' +
                    '<div style="font-size:12px; font-weight:900; color:#0f172a; margin-bottom:4px;">نظّم مخيماً</div>' +
                    (lines.length
                      ? lines.map(function(x) { return '<div style="display:flex; justify-content:space-between; gap:8px; font-size:11.5px; margin-top:2px;"><span style="color:#94a3b8; font-weight:700;">' + esc(x.label) + '</span><span style="color:#0f172a; font-weight:700; text-align:left;">' + esc(x.value) + '</span></div>'; }).join("")
                      : '<div style="font-size:11px; color:#94a3b8;">نعم (بدون تفاصيل)</div>') +
                  '</div>';
                }
                return '<div style="padding:8px 10px; background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; font-family:Cairo,sans-serif;">' +
                  '<div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">' +
                    '<div style="font-size:12.5px; font-weight:800; color:#0f172a;">' + esc(l.role) + '</div>' +
                    metaHtml +
                  '</div>' +
                  campHtml +
                '</div>';
              }).join("") +
            '</div>' +
          '</div>';
        }

        return '<div style="padding:14px 16px; background:rgba(0,0,0,0.02); border:1px solid #e2e8f0; border-inline-start:4px solid ' + color + '; border-radius:8px;">' +
          '<div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">' +
            '<span style="width:10px; height:10px; border-radius:50%; background:' + color + '; display:inline-block;"></span>' +
            '<h4 style="margin:0; font-size:14px; font-weight:800; color:#0f172a; font-family:Cairo,sans-serif;">' + esc(title) + '</h4>' +
          '</div>' +
          chips + years + leadHtml +
        '</div>';
      }

      html += branchBlock("#eab308", "الفرع الأصفر", row.yellow_passed, row.yellow_ranks || [], null, null, null, row.yellow_rank_dates || {});
      html += branchBlock("#10b981", "الفرع الأخضر", row.green_passed, row.green_ranks || [], row.green_consecration_year, null, row.green_leadership || [], row.green_rank_dates || {});
      html += branchBlock("#ef4444", "الفرع الأحمر", row.red_passed, row.red_ranks || [], row.red_consecration_year, row.red_departure_year, row.red_leadership || [], row.red_rank_dates || {});

      html += '</div>';
      return html;
    }

    // ─── Single-Page Scout Record PDF Generator (100% Exact to Member Profile) ──
    function downloadRegisterScoutRecordPdf() {
      if (!chosenMember) {
        toast("Please select a member first", "error");
        return;
      }

      toast("Preparing Scout Record PDF...", "info");

      var m = chosenMember;
      var memberName = m.full_name || m.fullName || [m.first_name, m.middle_name, m.last_name].filter(Boolean).join(" ") || "Member Profile";
      var initialsStr = initials(memberName);
      var unitName = m.unit || chosenUnit || "Rovers";

      var ageVal = ageDecimal(m.dob);
      var ageStr = ageVal !== null ? ageVal.toFixed(1) : "—";
      var genderStr = m.gender || "—";
      var dobStr = m.dob || "—";
      var bloodStr = m.blood_type || m.bloodType || "—";
      var phoneStr = m.phone || "—";
      var natStr = m.nationality || "Lebanese";
      var parentTypeStr = m.parent_type || m.parentType || "Mother";
      var parentPhoneStr = m.parent_phone || m.parentPhone || "—";
      var emailStr = m.email || "—";

      var badgesArr = Array.from(selectedBadges || []);
      var badgeConfig = getAdaptiveBadgeGridConfig(badgesArr.length);
      var badgesGridHtml = "";

      if (badgesArr.length > 0) {
        badgesGridHtml = badgesArr.map(function(bName) {
          var logoUrl = (typeof badgeDefLogo === "function" ? badgeDefLogo(bName) : null) || window.DEFAULT_BADGE_ICON || "../../logo.png";
          return '<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:' + badgeConfig.padding + '; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box;">' +
            '<img src="' + esc(logoUrl) + '" style="width:' + badgeConfig.iconSize + '; height:' + badgeConfig.iconSize + '; object-fit:contain; margin-bottom:2px; display:block;" alt="badge" />' +
            '<div dir="rtl" style="font-weight:700; font-size:' + badgeConfig.fontSize + '; color:#1e293b; font-family:Cairo, sans-serif; line-height:1.2; text-align:center;">' + esc(bName) + '</div>' +
          '</div>';
        }).join("");
      } else {
        badgesGridHtml = '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">No badges earned yet.</div>';
      }

      var milestonesHtml = buildMemberMilestonesHtmlForRegister(m, milestones);

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
                '<div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px;">DETAILS</div>' +
                '<div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 10px;">' +
                  '<div style="grid-column: 1 / -1; background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">FULL NAME</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(memberName) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">GENDER</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(genderStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">AGE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(ageStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BIRTH DATE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(dobStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">BLOOD TYPE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(bloodStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PHONE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(phoneStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">NATIONALITY</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(natStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT TYPE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(parentTypeStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">PARENT PHONE</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(parentPhoneStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">UNIT</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a;">' + esc(unitStr) + '</div>' +
                  '</div>' +
                  '<div style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:6px; padding:5px 10px;">' +
                    '<div style="font-size:8.5px; font-weight:800; color:#94a3b8; text-transform:uppercase;">EMAIL</div>' +
                    '<div style="font-size:11.5px; font-weight:800; color:#0f172a; word-break:break-all;">' + esc(emailStr) + '</div>' +
                  '</div>' +
                '</div>' +
              '</div>' +

              '<!-- BADGES CARD SECTION -->' +
              '<div style="border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; background:#fafafa; flex:1; display:flex; flex-direction:column; justify-content:flex-start;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                  '<div style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:.06em;">BADGES</div>' +
                  '<div style="font-size:10.5px; font-weight:700; color:#6366f1;">' + badgesArr.length + ' earned</div>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns: repeat(' + badgeConfig.cols + ', 1fr); gap:' + badgeConfig.gap + '; align-content:start;">' +
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
                milestonesHtml +
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
          var safeFileName = memberName.replace(/\s+/g, "_") + "_Scout_Record_SinglePage.pdf";
          pdf.save(safeFileName);
          toast("Scout Record PDF downloaded successfully!", "success");
        } else {
          toast("PDF library not available", "error");
        }
      }).catch(function(err) {
        try { container.remove(); } catch (_) {}
        console.error("[PDF Error]", err);
        toast("PDF Download Error: " + (err.message || err), "error");
      });
    }
'''

html = html[:s1] + pdf_exact_js.strip() + '\n\n    ' + html[s2:]
with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully upgraded PDF generator to match Member Profile 100%!')
