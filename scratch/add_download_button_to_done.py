filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

old_done = '''      <!-- ═════════ STEP 6: done ═════════ -->
      <section class="step" data-step="done">
        <div style="text-align:center;padding:40px 20px">
          <div style="font-size:72px;margin-bottom:12px">🎉</div>
          <h1 class="step-title" style="font-size:24px">Saved Successfully</h1>
          <p class="step-sub" style="font-size:14px">Thank you for updating your scouting profile. You can return at any
            time to edit your data — please keep your Security PIN safe.</p>
          <button type="button" class="secondary-btn" id="editAgainBtn"
            style="margin-top:20px;padding:12px 20px;border-radius:12px">Edit My Profile</button>
        </div>
      </section>'''

new_done = '''      <!-- ═════════ STEP 6: done ═════════ -->
      <section class="step" data-step="done">
        <div style="text-align:center;padding:40px 20px;display:flex;flex-direction:column;align-items:center;">
          <div style="font-size:72px;margin-bottom:12px">🎉</div>
          <h1 class="step-title" style="font-size:24px">Saved Successfully</h1>
          <p class="step-sub" style="font-size:14px">Thank you for updating your scouting profile. You can return at any time to edit your data — please keep your Security PIN safe.</p>

          <button type="button" class="primary-btn" id="downloadPassPdfBtn"
            style="margin-top:24px;padding:14px 24px;border-radius:12px;width:100%;max-width:320px;display:inline-flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:700;">
            📥 Download Your Profile (PDF)
          </button>

          <button type="button" class="secondary-btn" id="editAgainBtn"
            style="margin-top:12px;padding:12px 20px;border-radius:12px;width:100%;max-width:320px;">Edit My Profile</button>
        </div>
      </section>'''

if old_done in html:
    html = html.replace(old_done, new_done)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Successfully added Download Your Profile (PDF) button to step 6 (done)!')
else:
    print('Could not find old_done block in HTML!')
