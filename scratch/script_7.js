
  (function(){
    'use strict';

    // ─── State ────────────────────────────────────────────────────────
    // The step order after 'pin' depends on the member's unit:
    //   - Boyscouts Girlscouts : pin → badges → milestones → done
    //   - Everyone else          : pin → milestones → badges → done
    //     AND the 'badges' step is SKIPPED entirely unless the member
    //     ticked "Yes" for Green Branch (green_passed) — non-boyscout
    //     units only earn badges once they reach the green branch.
    // STEPS is rebuilt dynamically by computeSteps() whenever the unit
    // or green_passed flag changes.
    var STEPS = ['unit','name','pin','badges','milestones','done'];
    var STEP_LABELS = {
      unit:'اختر وحدتك / Select Unit', name:'اختر الاسم / Select Name', pin:'رمز الأمان / Security PIN',
      badges:'شاراتك / Your Badges', milestones:'مسيرتك الكشفية / Your Journey', done:'Done!'
    };
    var current = 'unit';

    var LEADER_RANKS_OPTS = [
      "مرشح للقيادة",
      "مساعد قائد وحدة",
      "قائد وحدة",
      "مساعد قائد تدريب",
      "قائد تدريب"
    ];

    var LEADER_COURSES_OPTS = [
      "الدراسة التمهيدية للشارة الخشبية",
      "دراسة الشارة الخشبية - الجزء الأول (نظري)",
      "دراسة الشارة الخشبية - الجزء الثاني (عملي)",
      "شهادة الشارة الخشبية (حامل الشارة الخشبية)",
      "دراسة مساعد قائد تدريب",
      "دراسة قائد تدريب"
    ];

    var leaderRanksData = [];
    var leaderTrainingsData = [];

    function isBoyscoutFamily(){
      return chosenUnit === 'Boyscouts' || chosenUnit === 'Girlscouts';
    }
    // Recompute the ordered step list based on unit + milestone state.
    function computeSteps(){
      var base = ['unit','name','pin'];
      if(chosenUnit === 'Leaders'){
        // Leaders have: PIN, Journeys (milestones), and Badges (only if green_passed is true)
        var arr = base.concat(['milestones']);
        if(milestones && milestones.green_passed) {
          arr.splice(3, 0, 'badges'); // Insert badges step
        }
        arr.push('done');
        return arr;
      }
      if(isBoyscoutFamily()){
        // Badges always available; milestones after.
        return base.concat(['badges','milestones','done']);
      }
      // Cubs Beavers Pioneers Rovers: journey first, badges only
      // if green_passed is true.
      var arr = base.concat(['milestones']);
      if(milestones && milestones.green_passed) arr.push('badges');
      arr.push('done');
      return arr;
    }
    function refreshSteps(){
      STEPS = computeSteps();
      // Keep the progress bar in sync if we're already past 'pin'
      var idx = STEPS.indexOf(current);
      if(idx >= 0){
        document.getElementById('progressFill').style.width = ((idx+1)/STEPS.length*100) + '%';
      }
    }
    // First content step AFTER pin — differs per unit.
    // Boyscouts/Girlscouts land on 'badges' first, everyone else on 'milestones'.
    function firstContentStep(){
      if(chosenUnit === 'Leaders') {
        return (milestones && milestones.green_passed) ? 'badges' : 'milestones';
      }
      return isBoyscoutFamily() ? 'badges' : 'milestones';
    }

    var chosenUnit = null;
    var chosenMember = null;    // full member row
    var isReturningUser = false; // did they already have a pin?
    var enteredPin = '';         // building pin input
    var pinStage = 'set';        // 'set' or 'enter' (returning user)
    var members = [];
    var badgeDefs = [];
    var selectedBadges = new Set();   // badge names
    var existingBadges = new Set();   // originally saved (for diff)
    var milestones = {};              // in-memory model
    var saveTimer = null;

    var supabase = null;

    // ─── Supabase ─────────────────────────────────────────────────────
    if(window.supabase && window.supabase.createClient && window.SUPABASE_URL){
      supabase = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
    }

    // ─── Helpers ──────────────────────────────────────────────────────
    function esc(v){ return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
    function initials(n){ return String(n||'').split(/\s+/).filter(Boolean).slice(0,2).map(function(w){return w[0].toUpperCase();}).join('') || '?'; }
    function toast(msg, kind){
      var el = document.getElementById('toast');
      el.textContent = msg;
      el.className = 'toast show ' + (kind||'');
      clearTimeout(el._t);
      el._t = setTimeout(function(){ el.className='toast '+(kind||''); }, 2600);
    }
    function canonicalUnit(raw){
      if(!raw) return null;
      var s = String(raw).toLowerCase().replace(/[\s_\-]+/g,'');
      var m = {beavers:'Beavers',beaver:'Beavers',cubs:'Cubs',cub:'Cubs',cubscouts:'Cubs',
               boyscouts:'Boyscouts',boyscout:'Boyscouts',scouts:'Boyscouts',
               girlscouts:'Girlscouts',girlscout:'Girlscouts',girls:'Girlscouts',
               pioneers:'Pioneers',pioneer:'Pioneers',rovers:'Rovers',rover:'Rovers'};
      return m[s]||null;
    }
    function markHint(id, mode){
      var el = document.getElementById(id);
      if(!el) return;
      var lbl = { saving:'Saving...', saved:'Saved', idle:'Auto-saving', error:'Error saving' }[mode] || '';
      el.className = 'save-hint ' + (mode==='saving'?'saving': mode==='saved'?'saved': mode==='error'?'saving':'');
      var sp = el.querySelector('span'); if(sp) sp.textContent = lbl;
    }

    // ─── Navigation ───────────────────────────────────────────────────
    function goto(step){
      // Always rebuild the step list right before navigating so late
      // decisions (e.g. user just toggled green_passed) are honoured.
      refreshSteps();
      if(STEPS.indexOf(step) === -1) step = 'unit';
      current = step;
      document.querySelectorAll('.step').forEach(function(s){
        s.classList.toggle('active', s.getAttribute('data-step')===step);
      });
      var idx = STEPS.indexOf(step);
      document.getElementById('progressFill').style.width = ((idx+1)/STEPS.length*100) + '%';
      document.getElementById('stepHeading').textContent = STEP_LABELS[step] || 'Registration';
      document.getElementById('backBtn').hidden = (idx === 0 || step === 'done');
      // Show/hide the sticky action bar per step
      var actions = document.getElementById('stepActions');
      if(step === 'pin' || step === 'name' || step === 'unit' || step === 'done'){
        actions.hidden = true;
      } else {
        actions.hidden = false;
        var btn = document.getElementById('nextBtn');
        // "Finish" appears on whatever the LAST content step is (before 'done').
        var isLastContentStep = (idx === STEPS.length - 2);
        btn.textContent = isLastContentStep ? 'Finish' : 'Next';
      }
      window.scrollTo({top:0, behavior:'auto'});
    }
    document.getElementById('backBtn').addEventListener('click', function(){
      refreshSteps();
      var idx = STEPS.indexOf(current);
      if(idx > 0){
        goto(STEPS[idx-1]);
      }
    });
    document.getElementById('nextBtn').addEventListener('click', function(){
      refreshSteps();
      var idx = STEPS.indexOf(current);
      var isLastContentStep = (idx === STEPS.length - 2);
      if(isLastContentStep){
        if(chosenUnit === 'Leaders'){
          saveLeaderProfileNow(true).then(function(){ goto('done'); });
        } else {
          // Whatever the last content step is (badges or milestones),
          // treat "Finish" the same way: force save then go to 'done'.
          saveMilestonesNow(true).then(function(){ goto('done'); });
        }
      } else if(idx >= 0 && idx < STEPS.length - 1){
        goto(STEPS[idx+1]);
      }
    });

    // ─── STEP 1: Units ────────────────────────────────────────────────
    // Unit names + brand colors (pink yellow light-green dark-green light-red dark-red)
    var UNITS = [
      {key:'Beavers',   ar:'القنادس / Beavers',   color:'#ec4899', ink:'#fff'}, // زهري
      {key:'Cubs',      ar:'الجراميز والزهرات / Cubs', color:'#facc15', ink:'#5b3a00'}, // اصفر
      {key:'Girlscouts',ar:'المرشدات / Girl Scouts',  color:'#86efac', ink:'#14532d'}, // اخضر فاتح
      {key:'Boyscouts', ar:'الكشافة / Boy Scouts',   color:'#166534', ink:'#fff'},   // اخضر غامق
      {key:'Pioneers',  ar:'الرائدات / Pioneers',  color:'#fca5a5', ink:'#7f1d1d'}, // احمر فاتح
      {key:'Rovers',    ar:'الجوالة / Rovers', color:'#991b1b', ink:'#fff'},  // احمر غامق
      {key:'Leaders',   ar:'القادة / Leaders', color:'#4f46e5', ink:'#fff'}
    ];
    function renderUnits(){
      var grid = document.getElementById('unitGrid');
      grid.innerHTML = UNITS.map(function(u){
        return '<button type="button" class="unit-tile" data-unit="'+u.key+'"'+
                 ' style="background:'+u.color+';color:'+u.ink+';border-color:'+u.color+';">'+
                 '<div style="font-size:18px;font-weight:800">'+esc(u.ar)+'</div>'+
               '</button>';
      }).join('');
      grid.querySelectorAll('.unit-tile').forEach(function(t){
        t.addEventListener('click', function(){
          chosenUnit = t.getAttribute('data-unit');
          loadMembersInUnit();
        });
      });
    }

    // ─── STEP 2: People ───────────────────────────────────────────────
    function loadMembersInUnit(){
      if(!supabase){ toast('Database connection failed', 'error'); return; }
      var tableToQuery = chosenUnit === 'Leaders' ? 'leaders' : 'members';
      toast(chosenUnit === 'Leaders' ? 'Loading leaders...' : 'Loading members...');
      supabase.from(tableToQuery).select('*').then(function(res){
        if(res.error){ toast('Error: '+res.error.message, 'error'); return; }
        var all;
        if(chosenUnit === 'Leaders'){
          all = res.data || [];
        } else {
          all = (res.data || []).filter(function(m){ return canonicalUnit(m.unit) === chosenUnit; });
        }
        all.sort(function(a,b){
          var na = (a.full_name || ((a.first_name||'')+' '+(a.last_name||''))).trim();
          var nb = (b.full_name || ((b.first_name||'')+' '+(b.last_name||''))).trim();
          return na.localeCompare(nb);
        });
        members = all;
        document.getElementById('unitNameSub').textContent =
          (UNITS.find(function(u){return u.key===chosenUnit;}) || {ar:''}).ar +
          ' — ' + members.length + ' ' + (chosenUnit === 'Leaders' ? 'Leaders' : 'Members');
        renderPeople('');
        goto('name');
      });
    }
    function renderPeople(q){
      var el = document.getElementById('peopleList');
      var qq = String(q||'').trim().toLowerCase();
      var list = members.filter(function(m){
        if(!qq) return true;
        var name = ((m.first_name||'')+' '+(m.middle_name||'')+' '+(m.last_name||'')).toLowerCase();
        return name.indexOf(qq) >= 0;
      });
      if(!list.length){
        el.innerHTML = '<div class="empty">No matching members found</div>';
        return;
      }
      el.innerHTML = list.map(function(m){
        var full = m.full_name || [m.first_name, m.middle_name, m.last_name].filter(Boolean).join(' ');
        var meta = [m.role || m.gender || '', m.dob || ''].filter(Boolean).join(' · ');
        var av = m.avatar_url ? '<img src="'+esc(m.avatar_url)+'" alt="" />' : esc(initials(full));
        return '<div class="person-row" data-id="'+esc(m.id)+'">'+
                 '<div class="person-avatar">'+av+'</div>'+
                 '<div class="person-info"><div class="person-name">'+esc(full||'—')+'</div><div class="person-meta">'+esc(meta)+'</div></div>'+
               '</div>';
      }).join('');
      el.querySelectorAll('.person-row').forEach(function(r){
        r.addEventListener('click', function(){
          var id = r.getAttribute('data-id');
          chosenMember = members.find(function(m){ return m.id === id; });
          if(!chosenMember) return;
          startPinFlow();
        });
      });
    }
    document.getElementById('peopleSearch').addEventListener('input', function(e){
      renderPeople(e.target.value);
    });

    // ─── STEP 3: PIN ──────────────────────────────────────────────────
    function startPinFlow(){
      isReturningUser = !!(chosenMember && chosenMember.pin);
      pinStage = isReturningUser ? 'enter' : 'set';
      enteredPin = '';
      updatePinDisplay();
      document.getElementById('pinError').textContent = '';
      document.getElementById('pinTitle').textContent = isReturningUser ? 'إدخال رمز الأمان / Enter Security PIN' : 'إنشاء رمز الأمان / Create Security PIN';
      document.getElementById('pinSub').textContent   = isReturningUser
        ? 'أدخل رمز الأمان الخاص بك للتعديل / Enter your previously chosen PIN to edit profile.'
        : 'رمز مكون من 4 أرقام لحماية ملفك الشخصي / A 4-digit PIN to secure your profile.';
      goto('pin');
    }
    function updatePinDisplay(){
      var el = document.getElementById('pinDisplay');
      var h = '';
      for(var i=0;i<4;i++){
        h += '<div class="pin-dot '+(i<enteredPin.length?'filled':'')+'"></div>';
      }
      el.innerHTML = h;
    }
    document.querySelectorAll('#pinKeypad .pin-key').forEach(function(k){
      k.addEventListener('click', function(){
        var v = k.getAttribute('data-k');
        if(v === 'clear'){ enteredPin = ''; document.getElementById('pinError').textContent=''; }
        else if(v === 'back'){ enteredPin = enteredPin.slice(0,-1); document.getElementById('pinError').textContent=''; }
        else if(enteredPin.length < 4){ enteredPin += v; document.getElementById('pinError').textContent=''; }
        updatePinDisplay();
        if(enteredPin.length === 4) handlePinComplete();
      });
    });
    function handlePinComplete(){
      var pin = enteredPin;
      if(pinStage === 'enter'){
        if(String(chosenMember.pin) !== pin){
          document.getElementById('pinError').textContent = 'رمز غير صحيح، يرجى المحاولة مجدداً / Incorrect PIN, please try again';
          enteredPin = '';
          setTimeout(updatePinDisplay, 300);
          return;
        }
        // Correct — proceed
        loadExistingProfile().then(function(){ refreshSteps(); goto(firstContentStep()); });
      } else {
        // 'set' — save pin to DB then proceed
        savePin(pin).then(function(ok){
          if(ok){
            chosenMember.pin = pin;
            loadExistingProfile().then(function(){ refreshSteps(); goto(firstContentStep()); });
          } else {
            enteredPin = '';
            updatePinDisplay();
          }
        });
      }
    }
    function savePin(pin){
      var table = chosenUnit === 'Leaders' ? 'leaders' : 'members';
      return supabase.from(table).update({ pin: pin }).eq('id', chosenMember.id).then(function(res){
        if(res.error){ toast('Error saving PIN: '+res.error.message, 'error'); return false; }
        return true;
      });
    }

    // ─── Load existing badges + milestones for this member ────────────
    function loadExistingProfile(){
      selectedBadges = new Set();
      existingBadges = new Set();
      milestones = {};
      
      var badgeTable = chosenUnit === 'Leaders' ? 'leader_badges' : 'badges';
      var idField = chosenUnit === 'Leaders' ? 'leader_id' : 'member_id';

      if (chosenUnit === 'Leaders') {
        return Promise.all([
          supabase.from('badge_definitions').select('id, name, logo_url, category'),
          supabase.from(badgeTable).select('id, badge_name, awarded_date').eq(idField, chosenMember.id),
          supabase.from('leader_ranks').select('rank_name, effective_date').eq('leader_id', chosenMember.id),
          supabase.from('leader_milestones').select('title, effective_date, notes').eq('leader_id', chosenMember.id),
          supabase.from('member_milestones').select('*').eq('member_id', chosenMember.id).maybeSingle()
        ]).then(function(results){
          var defsRes = results[0], badgesRes = results[1], ranksRes = results[2], msRes = results[3], memberMsRes = results[4];
          badgeDefs = (defsRes.data || []).slice().sort(function(a,b){
            return String(a.category||'zz').localeCompare(String(b.category||'zz'))
                || String(a.name||'').localeCompare(String(b.name||''));
          });
          (badgesRes.data || []).forEach(function(b){
            selectedBadges.add(b.badge_name);
            existingBadges.add(b.badge_name);
          });
          leaderRanksData = ranksRes.data || [];
          leaderTrainingsData = msRes.data || [];

          if (memberMsRes && memberMsRes.data) {
            milestones = memberMsRes.data;
          } else {
            var yj = leaderTrainingsData.find(function(r) { return r.title === 'leader_youth_journey'; });
            if (yj && yj.notes) {
              try { milestones = JSON.parse(yj.notes) || {}; } catch (_) {}
            }
          }

          milestones.green_consecrated = milestones.green_consecration_year != null;
          milestones.red_consecrated   = milestones.red_consecration_year   != null;
          milestones.red_departed      = milestones.red_departure_year      != null;

          renderBadges();
          hydrateLeaderMilestones();
          hydrateMilestones();
        });
      } else {
        return Promise.all([
          supabase.from('badge_definitions').select('id, name, logo_url, category'),
          supabase.from(badgeTable).select('id, badge_name, awarded_date').eq(idField, chosenMember.id),
          supabase.from('member_milestones').select('member_id, join_year, yellow_passed, yellow_ranks, green_passed, green_ranks, green_consecration_year, red_passed, red_ranks, red_consecration_year, red_departure_year, updated_at, green_leadership, red_leadership, yellow_rank_dates, green_rank_dates, red_rank_dates').eq(idField, chosenMember.id).maybeSingle()
        ]).then(function(results){
          var defsRes = results[0], badgesRes = results[1], msRes = results[2];
          badgeDefs = (defsRes.data || []).slice().sort(function(a,b){
            return String(a.category||'zz').localeCompare(String(b.category||'zz'))
                || String(a.name||'').localeCompare(String(b.name||''));
          });
          (badgesRes.data || []).forEach(function(b){
            selectedBadges.add(b.badge_name);
            existingBadges.add(b.badge_name);
          });
          if(msRes.data){
            milestones = msRes.data;
            // derived flags for the UI
            milestones.green_consecrated = milestones.green_consecration_year != null;
            milestones.red_consecrated   = milestones.red_consecration_year   != null;
            milestones.red_departed      = milestones.red_departure_year      != null;
          }
          renderBadges();
          hydrateMilestones();
        });
      }
    }

    // ─── STEP 4: Badges ───────────────────────────────────────────────
    function renderBadges(){
      var wrap = document.getElementById('badgesByCat');
      if(!badgeDefs.length){
        wrap.innerHTML = '<div class="empty">No badges defined yet. Please ask your leader to populate the list.</div>';
        return;
      }
      var byCat = {};
      badgeDefs.forEach(function(b){
        var c = b.category || 'Other';
        (byCat[c] = byCat[c] || []).push(b);
      });
      var html = '';
      Object.keys(byCat).forEach(function(cat){
        html += '<div class="badges-cat-title">'+esc(cat)+'</div>';
        html += '<div class="badge-grid">' + byCat[cat].map(function(b){
          var sel = selectedBadges.has(b.name);
          var logo = b.logo_url || window.DEFAULT_BADGE_ICON || '';
          return '<div class="badge-card '+(sel?'selected':'')+'" data-name="'+esc(b.name)+'">'+
                   '<span class="badge-tick">'+(sel?'✓':'')+'</span>'+
                   '<img src="'+esc(logo)+'" alt="" onerror="this.onerror=null;this.src=window.DEFAULT_BADGE_ICON||\'\';" />'+
                   '<div class="b-name">'+esc(b.name)+'</div>'+
                 '</div>';
        }).join('') + '</div>';
      });
      wrap.innerHTML = html;
      wrap.querySelectorAll('.badge-card').forEach(function(c){
        c.addEventListener('click', function(){
          var name = c.getAttribute('data-name');
          if(selectedBadges.has(name)){ selectedBadges.delete(name); c.classList.remove('selected'); c.querySelector('.badge-tick').textContent=''; }
          else                          { selectedBadges.add(name);    c.classList.add('selected');    c.querySelector('.badge-tick').textContent='✓'; }
          scheduleBadgesSave();
        });
      });
    }
    function scheduleBadgesSave(){
      markHint('badgesSaveHint','saving');
      clearTimeout(saveTimer);
      saveTimer = setTimeout(saveBadgesNow, 600);
    }
    function saveBadgesNow(){
      // Diff selectedBadges vs existingBadges → insert new, delete removed.
      var toAdd = [], toRemove = [];
      selectedBadges.forEach(function(n){ if(!existingBadges.has(n)) toAdd.push(n); });
      existingBadges.forEach(function(n){ if(!selectedBadges.has(n)) toRemove.push(n); });
      var ops = [];
      var badgeTable = chosenUnit === 'Leaders' ? 'leader_badges' : 'badges';
      var idField = chosenUnit === 'Leaders' ? 'leader_id' : 'member_id';

      if(toAdd.length){
        ops.push(supabase.from(badgeTable).insert(toAdd.map(function(n){
          return { [idField]: chosenMember.id, badge_name: n, awarded_date: new Date().toISOString().slice(0,10) };
        })));
      }
      if(toRemove.length){
        ops.push(supabase.from(badgeTable).delete().eq(idField, chosenMember.id).in('badge_name', toRemove));
      }
      if(!ops.length){ markHint('badgesSaveHint','saved'); return; }
      Promise.all(ops).then(function(reses){
        var err = reses.find(function(r){ return r && r.error; });
        if(err){ markHint('badgesSaveHint','error'); toast('Error saving badges', 'error'); return; }
        // Sync existing = selected
        existingBadges = new Set(selectedBadges);
        markHint('badgesSaveHint','saved');
      });
    }

    // ─── STEP 5: Milestones ───────────────────────────────────────────
    function setYN(section, val){
      milestones[section] = !!val;
      // If turning OFF the parent, clear the dependent fields too
      if(!val){
        if(section === 'yellow_passed'){
          milestones.yellow_ranks = [];
          milestones.yellow_rank_dates = {};
        }
        if(section === 'green_passed'){
          milestones.green_ranks = [];
          milestones.green_rank_dates = {};
          milestones.green_leadership = [];
          milestones.green_consecrated = false;
          milestones.green_consecration_year = null;
        }
        if(section === 'green_consecrated'){
          milestones.green_consecration_year = null;
        }
        if(section === 'red_passed'){
          milestones.red_ranks = [];
          milestones.red_rank_dates = {};
          milestones.red_leadership = [];
          milestones.red_consecrated = false;
          milestones.red_departed = false;
          milestones.red_consecration_year = null;
          milestones.red_departure_year = null;
        }
        if(section === 'red_consecrated'){ milestones.red_consecration_year = null; }
        if(section === 'red_departed'){    milestones.red_departure_year    = null; }
      }
      renderYNStates();
      renderConditionalVisibility();
      renderLeadershipRoles();
      hydrateInputsFromModel();
      // If green_passed changed, the step order for non-boyscout units
      // shifts (badges is only visible if green_passed=true), so refresh.
      if(section === 'green_passed') refreshSteps();
      scheduleMilestonesSave();
    }
    function renderYNStates(){
      document.querySelectorAll('.yn-toggle').forEach(function(g){
        var key = g.getAttribute('data-yn');
        var v = !!milestones[key];
        g.querySelector('.yes').classList.toggle('active', v === true);
        g.querySelector('.no').classList.toggle('active',  v === false && milestones.hasOwnProperty(key));
      });
    }
    function renderConditionalVisibility(){
      document.querySelectorAll('[data-shows-when]').forEach(function(el){
        var key = el.getAttribute('data-shows-when');
        el.style.display = milestones[key] ? '' : 'none';
      });
    }
    function renderRankChips(){
      document.querySelectorAll('.rank-chips[data-multi]').forEach(function(wrap){
        var opts       = (wrap.getAttribute('data-options')||'').split('|');
        var field      = wrap.getAttribute('data-multi');
        var dateField  = wrap.getAttribute('data-dates'); // optional
        // Ensure a sibling container for per-rank date inputs exists.
        var dateWrap = null;
        if(dateField){
          dateWrap = wrap.nextElementSibling;
          if(!dateWrap || !dateWrap.classList.contains('rank-dates')){
            dateWrap = document.createElement('div');
            dateWrap.className = 'rank-dates';
            wrap.parentNode.insertBefore(dateWrap, wrap.nextSibling);
          }
        }
        if(!wrap.dataset.rendered){
          wrap.innerHTML = opts.map(function(o, idx){
            return '<button type="button" class="rank-chip" data-val="'+esc(o)+'" data-idx="'+idx+'">'+esc(o)+'</button>';
          }).join('');
          wrap.dataset.rendered = '1';
          wrap.querySelectorAll('.rank-chip').forEach(function(chip){
            chip.addEventListener('click', function(){
              // Ranks are an ORDERED progression. You can't have rank N
              // without also having ranks 0..N-1.
              //   - Clicking a chip to SELECT it auto-selects all lower ranks.
              //   - Clicking a chip to DESELECT it auto-deselects all higher ranks.
              var clickedIdx = parseInt(chip.getAttribute('data-idx'), 10);
              var v = chip.getAttribute('data-val');
              var current = Array.isArray(milestones[field]) ? milestones[field] : [];
              var isSelected = current.indexOf(v) >= 0;
              var newSet;
              if(isSelected){
                newSet = opts.slice(0, clickedIdx);
              } else {
                newSet = opts.slice(0, clickedIdx + 1);
              }
              milestones[field] = newSet;
              // If we have a dates map, prune years for ranks we just removed
              if(dateField){
                var map = (milestones[dateField] && typeof milestones[dateField] === 'object') ? milestones[dateField] : {};
                Object.keys(map).forEach(function(k){
                  if(newSet.indexOf(k) < 0) delete map[k];
                });
                milestones[dateField] = map;
              }
              wrap.querySelectorAll('.rank-chip').forEach(function(c){
                c.classList.toggle('selected', newSet.indexOf(c.getAttribute('data-val')) >= 0);
              });
              renderRankDates(wrap, dateWrap, field, dateField);
              scheduleMilestonesSave();
            });
          });
        }
        // Reflect selection on the chips
        var arr = Array.isArray(milestones[field]) ? milestones[field] : [];
        wrap.querySelectorAll('.rank-chip').forEach(function(chip){
          chip.classList.toggle('selected', arr.indexOf(chip.getAttribute('data-val')) >= 0);
        });
        // Render refresh date inputs if this wrap uses them
        if(dateField) renderRankDates(wrap, dateWrap, field, dateField);
      });
    }

    // Render one date input per currently-selected rank, in the sibling
    // .rank-dates container. Value is optional; empty = no date recorded.
    function renderRankDates(chipsWrap, dateWrap, ranksField, datesField){
      if(!dateWrap) return;
      var selected = Array.isArray(milestones[ranksField]) ? milestones[ranksField] : [];
      var map      = (milestones[datesField] && typeof milestones[datesField] === 'object') ? milestones[datesField] : {};
      if(!selected.length){
        dateWrap.classList.remove('active');
        dateWrap.innerHTML = '';
        return;
      }
      dateWrap.classList.add('active');
      dateWrap.innerHTML = selected.map(function(rank){
        var v = map[rank] != null ? map[rank] : '';
        return '<div class="rank-date-row">'+
                 '<span class="rank-date-label">'+esc(rank)+'</span>'+
                 '<input type="text" inputmode="numeric" dir="ltr" data-rank="'+esc(rank)+'" '+
                        'placeholder="YYYY أو DD/MM/YYYY (اختياري)" value="'+esc(v)+'" />'+
               '</div>';
      }).join('');
      dateWrap.querySelectorAll('input[data-rank]').forEach(function(inp){
        inp.addEventListener('input', function(){
          var rank = inp.getAttribute('data-rank');
          var val  = normalizeFlexibleDate(inp.value);
          var m    = (milestones[datesField] && typeof milestones[datesField] === 'object') ? milestones[datesField] : {};
          if(val) m[rank] = val; else delete m[rank];
          milestones[datesField] = m;
          scheduleMilestonesSave();
        });
        inp.addEventListener('blur', function(){
          // Show validation feedback on blur (not while typing)
          var val = String(inp.value||'').trim();
          if(val && !normalizeFlexibleDate(val)){
            inp.classList.add('invalid');
          } else {
            inp.classList.remove('invalid');
          }
        });
      });
    }

    // Accepts DD/MM/YYYY (or D/M/YYYY, dashes ok) OR just YYYY (1900-2100).
    // Returns the canonical string ("DD/MM/YYYY" or "YYYY") if valid, else "".
    function normalizeFlexibleDate(raw){
      var s = String(raw||'').trim();
      if(!s) return '';
      // Year-only: 4 digits between 1900 and 2100
      if(/^\d{4}$/.test(s)){
        var y = parseInt(s,10);
        return (y >= 1900 && y <= 2100) ? String(y) : '';
      }
      // Full date: D/M/YYYY, DD/MM/YYYY, with or -
      var m = s.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
      if(m){
        var d = parseInt(m[1],10), mo = parseInt(m[2],10), yr = parseInt(m[3],10);
        if(d>=1 && d<=31 && mo>=1 && mo<=12 && yr>=1900 && yr<=2100){
          return (d<10?'0':'')+d + '/' + (mo<10?'0':'')+mo + '/' + yr;
        }
      }
      return '';
    }

    // Leadership roles: each role is a togglable card. When selected, it
    // reveals name + optional year fields. Data model: milestones[field] is
    // an array of {role, name, year} objects (only roles the user selected).
    function renderLeadershipRoles(){
      document.querySelectorAll('.leadership-roles[data-lead]').forEach(function(wrap){
        var field       = wrap.getAttribute('data-lead');
        var options     = (wrap.getAttribute('data-options')||'').split('|');
        var nameFor     = (wrap.getAttribute('data-name-for')||'').split(',');
        var nameLbl     = wrap.getAttribute('data-name-label') || 'Patrol Name Patrol Name ';
        var campFor     = (wrap.getAttribute('data-camp-for')||'').split(',').map(function(s){return s.trim();}).filter(Boolean);
        var campQ       = wrap.getAttribute('data-camp-q')          || 'هل نظمت مخيماً؟';
        var campNameLbl = wrap.getAttribute('data-camp-name-label') || 'Camp Name';
        var campPlaceLbl= wrap.getAttribute('data-camp-place-label')|| 'Camp Location';
        var campDateLbl = wrap.getAttribute('data-camp-date-label') || 'Camp Date';

        if(!wrap.dataset.rendered){
          wrap.innerHTML = options.map(function(role){
            var wantsName = nameFor.indexOf(role) >= 0;
            var wantsCamp = campFor.indexOf(role) >= 0;
            var nameFieldHtml = wantsName
              ? '<div class="lead-row-body-field">'+
                  '<span class="lead-row-body-label">'+esc(nameLbl)+'</span>'+
                  '<input type="text" data-lead-name="1" placeholder="'+esc(nameLbl)+'" />'+
                '</div>'
              : '';
            // Camp sub-block: yes/no toggle + revealed fields
            var campHtml = wantsCamp
              ? '<div class="lead-camp" data-camp="1">'+
                  '<div class="lead-row-body-field">'+
                    '<span class="lead-row-body-label">'+esc(campQ)+'</span>'+
                    '<div class="yn-toggle" data-camp-yn="1">'+
                      '<button type="button" class="yes">Yes</button>'+
                      '<button type="button" class="no">No</button>'+
                    '</div>'+
                  '</div>'+
                  '<div class="lead-camp-fields">'+
                    '<div class="lead-row-body-field">'+
                      '<span class="lead-row-body-label">'+esc(campNameLbl)+'</span>'+
                      '<input type="text" data-camp-name="1" placeholder="'+esc(campNameLbl)+'" />'+
                    '</div>'+
                    '<div class="lead-row-body-field">'+
                      '<span class="lead-row-body-label">'+esc(campPlaceLbl)+'</span>'+
                      '<input type="text" data-camp-place="1" placeholder="'+esc(campPlaceLbl)+'" />'+
                    '</div>'+
                    '<div class="lead-row-body-field">'+
                      '<span class="lead-row-body-label">'+esc(campDateLbl)+'</span>'+
                      '<input type="text" inputmode="numeric" dir="ltr" data-camp-date="1" placeholder="YYYY أو DD/MM/YYYY (اختياري)" />'+
                    '</div>'+
                  '</div>'+
                '</div>'
              : '';
            return '<div class="lead-row" data-role="'+esc(role)+'">'+
                     '<div class="lead-row-head">'+
                       '<span class="lead-row-name">'+esc(role)+'</span>'+
                       '<span class="lead-row-check">✓</span>'+
                     '</div>'+
                     '<div class="lead-row-body">'+
                       nameFieldHtml +
                       '<div class="lead-row-body-field">'+
                         '<span class="lead-row-body-label">التاريخ أو السنة (اختياري)</span>'+
                         '<input type="text" inputmode="numeric" dir="ltr" data-lead-year="1" placeholder="YYYY أو DD/MM/YYYY" />'+
                       '</div>'+
                       campHtml +
                     '</div>'+
                   '</div>';
          }).join('');
          wrap.dataset.rendered = '1';

          // Toggle role card on header click
          wrap.querySelectorAll('.lead-row').forEach(function(row){
            var head = row.querySelector('.lead-row-head');
            head.addEventListener('click', function(){
              row.classList.toggle('selected');
              syncLeadFromDom(wrap, field);
            });
            // Camp yes/no toggle inside a role card
            var campYn = row.querySelector('.yn-toggle[data-camp-yn]');
            if(campYn){
              campYn.querySelector('.yes').addEventListener('click', function(ev){
                ev.stopPropagation();
                campYn.querySelector('.yes').classList.add('active');
                campYn.querySelector('.no').classList.remove('active');
                var f = row.querySelector('.lead-camp-fields');
                if(f) f.classList.add('active');
                syncLeadFromDom(wrap, field);
              });
              campYn.querySelector('.no').addEventListener('click', function(ev){
                ev.stopPropagation();
                campYn.querySelector('.no').classList.add('active');
                campYn.querySelector('.yes').classList.remove('active');
                var f = row.querySelector('.lead-camp-fields');
                if(f){
                  f.classList.remove('active');
                  f.querySelectorAll('input').forEach(function(i){ i.value=''; });
                }
                syncLeadFromDom(wrap, field);
              });
            }
            // Any input change saves
            row.querySelectorAll('input').forEach(function(inp){
              inp.addEventListener('input', function(){
                syncLeadFromDom(wrap, field);
              });
              inp.addEventListener('click', function(ev){ ev.stopPropagation(); });
            });
          });
        }

        // Reflect current state from the model
        var current = Array.isArray(milestones[field]) ? milestones[field] : [];
        wrap.querySelectorAll('.lead-row').forEach(function(row){
          var role = row.getAttribute('data-role');
          var found = current.find(function(x){ return x && x.role === role; });
          row.classList.toggle('selected', !!found);
          var nameInp = row.querySelector('input[data-lead-name]');
          var yearInp = row.querySelector('input[data-lead-year]');
          if(nameInp) nameInp.value = (found && found.name)  || '';
          if(yearInp) yearInp.value = (found && found.year != null) ? found.year : '';
          // Camp reflection
          var campYn = row.querySelector('.yn-toggle[data-camp-yn]');
          var campF  = row.querySelector('.lead-camp-fields');
          if(campYn){
            var camp = (found && found.camp) || null;
            var organized = !!(camp && camp.organized);
            campYn.querySelector('.yes').classList.toggle('active', organized === true);
            campYn.querySelector('.no').classList.toggle('active',  camp && !organized);
            if(campF){
              campF.classList.toggle('active', organized);
              var nameI  = row.querySelector('input[data-camp-name]');
              var placeI = row.querySelector('input[data-camp-place]');
              var dateI  = row.querySelector('input[data-camp-date]');
              if(nameI)  nameI.value  = (camp && camp.name)  || '';
              if(placeI) placeI.value = (camp && camp.place) || '';
              if(dateI)  dateI.value  = (camp && camp.date)  || '';
            }
          }
        });
      });
    }

    function syncLeadFromDom(wrap, field){
      var arr = [];
      wrap.querySelectorAll('.lead-row.selected').forEach(function(row){
        var role = row.getAttribute('data-role');
        var nameInp = row.querySelector('input[data-lead-name]');
        var yearInp = row.querySelector('input[data-lead-year]');
        var entry = { role: role };
        if(nameInp && String(nameInp.value||'').trim()) entry.name = String(nameInp.value).trim();
        // Flexible year field: accepts YYYY or DD/MM/YYYY. Stored as string.
        // Legacy rows with an integer `year` still hydrate correctly.
        if(yearInp){
          var normalized = normalizeFlexibleDate(yearInp.value);
          if(normalized) entry.year = normalized;
          yearInp.classList.toggle('invalid', !!String(yearInp.value||'').trim() && !normalized);
        }
        // Camp — attach only if the role has camp UI and user answered
        var campYn = row.querySelector('.yn-toggle[data-camp-yn]');
        if(campYn){
          var yesActive = campYn.querySelector('.yes').classList.contains('active');
          var noActive  = campYn.querySelector('.no').classList.contains('active');
          if(yesActive){
            var nameI  = row.querySelector('input[data-camp-name]');
            var placeI = row.querySelector('input[data-camp-place]');
            var dateI  = row.querySelector('input[data-camp-date]');
            var camp   = { organized: true };
            if(nameI  && nameI.value.trim())  camp.name  = nameI.value.trim();
            if(placeI && placeI.value.trim()) camp.place = placeI.value.trim();
            if(dateI){
              var normalizedCamp = normalizeFlexibleDate(dateI.value);
              if(normalizedCamp) camp.date = normalizedCamp;
              dateI.classList.toggle('invalid', !!String(dateI.value||'').trim() && !normalizedCamp);
            }
            entry.camp = camp;
          } else if(noActive){
            entry.camp = { organized: false };
          }
        }
        arr.push(entry);
      });
      milestones[field] = arr;
      scheduleMilestonesSave();
    }

    function hydrateInputsFromModel(){
      var jy = document.getElementById('msJoinYear');
      if(jy) jy.value = milestones.join_year || '';
      document.querySelectorAll('input[data-year]').forEach(function(el){
        var k = el.getAttribute('data-year');
        el.value = milestones[k] != null ? milestones[k] : '';
      });
    }
    function hydrateMilestones(){
      // The red branch is only for Pioneers Rovers members.
      // Boyscouts and Girlscouts haven't reached it yet — hide it.
      var redSection = document.getElementById('msRedSection');
      var hideRed = (chosenUnit === 'Boyscouts' || chosenUnit === 'Girlscouts');
      if(redSection) redSection.style.display = hideRed ? 'none' : '';
      if(hideRed){
        // Also reset any red_* fields so we don't accidentally save stale data
        milestones.red_passed = false;
        milestones.red_ranks  = [];
        milestones.red_rank_dates = {};
        milestones.red_leadership = [];
        milestones.red_consecrated = false;
        milestones.red_consecration_year = null;
        milestones.red_departed = false;
        milestones.red_departure_year = null;
      }
      renderYNStates();
      renderConditionalVisibility();
      renderRankChips();
      renderLeadershipRoles();
      hydrateInputsFromModel();
      refreshSteps();
    }
    // Bind YN buttons
    document.querySelectorAll('.yn-toggle').forEach(function(g){
      var key = g.getAttribute('data-yn');
      g.querySelector('.yes').addEventListener('click', function(){ setYN(key, true); });
      g.querySelector('.no').addEventListener ('click', function(){ setYN(key, false); });
    });
    // Bind number inputs
    document.getElementById('msJoinYear').addEventListener('input', function(e){
      milestones.join_year = parseIntSafe(e.target.value);
      scheduleMilestonesSave();
    });
    document.querySelectorAll('input[data-year]').forEach(function(el){
      el.addEventListener('input', function(){
        var k = el.getAttribute('data-year');
        milestones[k] = parseIntSafe(el.value);
        scheduleMilestonesSave();
      });
    });
    function parseIntSafe(v){
      var n = parseInt(String(v).replace(/\D/g,''),10);
      return isNaN(n) ? null : n;
    }
    function scheduleMilestonesSave(){
      if (chosenUnit === 'Leaders') {
        scheduleLeaderMilestonesSave();
        return;
      }
      markHint('msSaveHint','saving');
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function(){ saveMilestonesNow(false); }, 700);
    }
    function saveMilestonesNow(showToastOnDone){
      if(!chosenMember) return Promise.resolve();
      if(chosenUnit === 'Leaders'){
        return saveLeaderProfileNow(showToastOnDone);
      }
      var payload = {
        member_id: chosenMember.id,
        join_year: milestones.join_year || null,
        yellow_passed: !!milestones.yellow_passed,
        yellow_ranks:  milestones.yellow_passed ? (milestones.yellow_ranks || []) : [],
        green_passed:  !!milestones.green_passed,
        green_ranks:   milestones.green_passed  ? (milestones.green_ranks  || []) : [],
        // Per-rank optional dates (YYYY or DD/MM/YYYY, stored as string)
        yellow_rank_dates: milestones.yellow_passed ? (milestones.yellow_rank_dates || {}) : {},
        green_rank_dates:  milestones.green_passed  ? (milestones.green_rank_dates  || {}) : {},
        green_leadership: milestones.green_passed ? (milestones.green_leadership || []) : [],
        green_consecration_year: (milestones.green_passed && milestones.green_consecrated) ? (milestones.green_consecration_year || null) : null,
        red_passed:    !!milestones.red_passed,
        red_ranks:     milestones.red_passed    ? (milestones.red_ranks    || []) : [],
        red_rank_dates: milestones.red_passed   ? (milestones.red_rank_dates || {}) : {},
        red_leadership: milestones.red_passed    ? (milestones.red_leadership || []) : [],
        red_consecration_year:  (milestones.red_passed && milestones.red_consecrated) ? (milestones.red_consecration_year || null) : null,
        red_departure_year:     (milestones.red_passed && milestones.red_departed)    ? (milestones.red_departure_year    || null) : null,
        updated_at: new Date().toISOString()
      };
      return supabase.from('member_milestones').upsert(payload, { onConflict:'member_id' }).then(function(res){
        if(res.error){
          // If the DB doesn't yet have any of the newer JSONB columns,
          // strip them and retry. Admin should run:
          //   alter table member_milestones
          //     add column if not exists green_leadership  jsonb default '[]'::jsonb,
          //     add column if not exists red_leadership    jsonb default '[]'::jsonb,
          //     add column if not exists yellow_rank_dates jsonb default '{}'::jsonb,
          //     add column if not exists green_rank_dates  jsonb default '{}'::jsonb,
          //     add column if not exists red_rank_dates    jsonb default '{}'::jsonb;
          var msg = String(res.error.message || '');
          if(/green_leadership|red_leadership|yellow_rank_dates|green_rank_dates|red_rank_dates/.test(msg)){
            console.warn('[milestones] optional JSONB columns missing — retrying without them');
            var fallback = Object.assign({}, payload);
            delete fallback.green_leadership;
            delete fallback.red_leadership;
            delete fallback.yellow_rank_dates;
            delete fallback.green_rank_dates;
            delete fallback.red_rank_dates;
            return supabase.from('member_milestones').upsert(fallback, { onConflict:'member_id' }).then(function(res2){
              if(res2.error){
                markHint('msSaveHint','error');
                toast('Error saving journey: '+res2.error.message, 'error');
                return false;
              }
              markHint('msSaveHint','saved');
              if(showToastOnDone){
                toast('Data saved (excluding roles — please update the database)','warn');
              }
              return true;
            });
          }
          markHint('msSaveHint','error');
          toast('Error saving journey: '+msg, 'error');
          return false;
        }
        markHint('msSaveHint','saved');
        if(showToastOnDone) toast('All your data has been saved ✓','success');
        return true;
      });
    }

    // ─── LEADERS SCOUTING JOURNEY ─────────────────────────────────────
    function hydrateLeaderMilestones() {
      document.getElementById('milestonesTitle').textContent = "Leader's Scouting Journey ";
      document.getElementById('milestonesSub').textContent = "Record your leader ranks, training courses, and previous assignments.";

      // Display BOTH the leader-specific journey AND the youth milestones!
      var youthWrap = document.getElementById('youthMilestonesWrap');
      var leaderWrap = document.getElementById('leaderMilestonesWrap');
      if (youthWrap) youthWrap.style.display = 'block';
      if (leaderWrap) leaderWrap.style.display = 'block';

      // Read leader's scout title details, current rank, and custom ranks list
      var curRankRow = leaderTrainingsData.find(function(r) { return r.title === 'leader_current_rank'; });
      var curRankInp = document.getElementById('leaderCurrentRank');
      var curRankDateInp = document.getElementById('leaderCurrentRankDate');
      if (curRankInp) curRankInp.value = curRankRow ? (curRankRow.notes || '') : '';
      if (curRankDateInp) curRankDateInp.value = curRankRow ? (curRankRow.effective_date || '') : '';

      var scoutTitleRow = leaderTrainingsData.find(function(r) { return r.title === 'leader_scout_title'; });
      var scoutTitle = null;
      if (scoutTitleRow && scoutTitleRow.notes) {
        try { scoutTitle = JSON.parse(scoutTitleRow.notes); } catch (_) {}
      }
      scoutTitle = scoutTitle || { title: '', location: '', godfather: '', date: '' };
      
      var tInp = document.getElementById('leaderTitle');
      var pInp = document.getElementById('leaderTitlePlace');
      var gInp = document.getElementById('leaderTitleGodfather');
      var dInp = document.getElementById('leaderTitleDate');
      if (tInp) tInp.value = scoutTitle.title || '';
      if (pInp) pInp.value = scoutTitle.location || '';
      if (gInp) gInp.value = scoutTitle.godfather || '';
      if (dInp) dInp.value = scoutTitle.date || '';

      var consecrationRow = leaderTrainingsData.find(function(r) { return r.title === 'leader_consecration'; });
      var cDateInp = document.getElementById('leaderConsecrationDate');
      if (cDateInp) cDateInp.value = consecrationRow ? (consecrationRow.effective_date || '') : '';

      // Clear and populate previous custom ranks list
      var customRanksRow = leaderTrainingsData.find(function(r) { return r.title === 'leader_custom_ranks_list'; });
      var customRanksList = null;
      if (customRanksRow && customRanksRow.notes) {
        try { customRanksList = JSON.parse(customRanksRow.notes); } catch (_) {}
      }
      customRanksList = customRanksList || [];
      var customContainer = document.getElementById('leaderCustomRanksContainer');
      if (customContainer) {
        customContainer.innerHTML = '';
        customRanksList.forEach(function(rank) {
          if (rank) {
            addCustomRankRow(rank.name, rank.start_date, rank.end_date);
          }
        });
      }

      // Bind leader journey form inputs to save once
      if (!window.__leaderInputsBound) {
        window.__leaderInputsBound = true;
        if (curRankInp) curRankInp.addEventListener('input', scheduleLeaderMilestonesSave);
        if (curRankDateInp) curRankDateInp.addEventListener('change', scheduleLeaderMilestonesSave);
        if (tInp) tInp.addEventListener('input', scheduleLeaderMilestonesSave);
        if (pInp) pInp.addEventListener('input', scheduleLeaderMilestonesSave);
        if (gInp) gInp.addEventListener('input', scheduleLeaderMilestonesSave);
        if (dInp) dInp.addEventListener('change', scheduleLeaderMilestonesSave);
        if (cDateInp) cDateInp.addEventListener('change', scheduleLeaderMilestonesSave);
      }
    }

    // Function to add a previous custom rank row
    function addCustomRankRow(rankName, startDate, endDate) {
      var container = document.getElementById('leaderCustomRanksContainer');
      if (!container) return;
      var row = document.createElement('div');
      row.className = 'custom-rank-entry-row';
      row.style.display = 'grid';
      row.style.gridTemplateColumns = '1fr 1fr 1fr auto';
      row.style.gap = '8px';
      row.style.alignItems = 'end';
      row.style.marginBottom = '12px';
      row.style.borderBottom = '1px dashed var(--line)';
      row.style.paddingBottom = '8px';
      
      row.innerHTML = 
        '<div>' +
          '<label style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:2px;">اسم Rank</label>' +
          '<input type="text" class="rank-name-input" value="'+esc(rankName||'')+'" placeholder="Rank" style="width:100%; padding:8px; border:1px solid var(--line); border-radius:var(--radius-sm); font-size:13px; font-family:inherit; background:var(--bg);" />' +
        '</div>' +
        '<div>' +
          '<label style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:2px;">البدء</label>' +
          '<input type="date" class="rank-start-input" value="'+esc(startDate||'')+'" style="width:100%; padding:8px; border:1px solid var(--line); border-radius:var(--radius-sm); font-size:13px; font-family:inherit; background:var(--bg);" />' +
        '</div>' +
        '<div>' +
          '<label style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:2px;">اNoنتهاء</label>' +
          '<input type="date" class="rank-end-input" value="'+esc(endDate||'')+'" style="width:100%; padding:8px; border:1px solid var(--line); border-radius:var(--radius-sm); font-size:13px; font-family:inherit; background:var(--bg);" />' +
        '</div>' +
        '<div>' +
          '<button type="button" class="delete-rank-row-btn" style="padding: 8px 12px; background:var(--primary-tint); color:var(--danger); border-radius:var(--radius-sm); border:none; cursor:pointer; font-weight:bold; font-size:13px;">✕</button>' +
        '</div>';
        
      container.appendChild(row);
      
      // Bind auto-save to inputs
      row.querySelector('.rank-name-input').addEventListener('input', scheduleLeaderMilestonesSave);
      row.querySelector('.rank-start-input').addEventListener('change', scheduleLeaderMilestonesSave);
      row.querySelector('.rank-end-input').addEventListener('change', scheduleLeaderMilestonesSave);
      row.querySelector('.delete-rank-row-btn').addEventListener('click', function() {
        row.remove();
        scheduleLeaderMilestonesSave();
      });
    }

    var addBtn = document.getElementById('addLeaderRankBtn');
    if (addBtn) {
      addBtn.addEventListener('click', function() {
        addCustomRankRow('', '', '');
        scheduleLeaderMilestonesSave();
      });
    }

    var leaderSaveTimer = null;
    function scheduleLeaderMilestonesSave() {
      markHint('msSaveHint', 'saving');
      clearTimeout(leaderSaveTimer);
      leaderSaveTimer = setTimeout(function() {
        saveLeaderProfileNow(false);
      }, 700);
    }

    function saveLeaderProfileNow(showToastOnDone) {
      if (!chosenMember || chosenUnit !== 'Leaders') return Promise.resolve(true);
      markHint('msSaveHint', 'saving');

      // 1. Get current rank
      var curRankEl = document.getElementById('leaderCurrentRank');
      var curRankDateEl = document.getElementById('leaderCurrentRankDate');
      var curRankName = curRankEl ? curRankEl.value.trim() : '';
      var curRankDate = curRankDateEl ? (curRankDateEl.value || null) : null;

      // 2. Get custom ranks list
      var customRanks = [];
      document.querySelectorAll('.custom-rank-entry-row').forEach(function(row) {
        var nameEl = row.querySelector('.rank-name-input');
        var startEl = row.querySelector('.rank-start-input');
        var endEl = row.querySelector('.rank-end-input');
        var name = nameEl ? nameEl.value.trim() : '';
        var start = startEl ? (startEl.value || null) : null;
        var end = endEl ? (endEl.value || null) : null;
        if (name) {
          customRanks.push({ name: name, start_date: start, end_date: end });
        }
      });

      // 3. Get scout title
      var tEl = document.getElementById('leaderTitle');
      var pEl = document.getElementById('leaderTitlePlace');
      var gEl = document.getElementById('leaderTitleGodfather');
      var dEl = document.getElementById('leaderTitleDate');

      var scoutTitle = {
        title: tEl ? tEl.value.trim() : '',
        location: pEl ? pEl.value.trim() : '',
        godfather: gEl ? gEl.value.trim() : '',
        date: dEl ? (dEl.value || null) : null
      };

      // 4. Get consecration date
      var consecrationDateEl = document.getElementById('leaderConsecrationDate');
      var consecrationDate = consecrationDateEl ? (consecrationDateEl.value || null) : null;

      var payload = [
        { leader_id: chosenMember.id, title: 'leader_current_rank', notes: curRankName || null, effective_date: curRankDate || null },
        { leader_id: chosenMember.id, title: 'leader_custom_ranks_list', notes: JSON.stringify(customRanks) || null, effective_date: null },
        { leader_id: chosenMember.id, title: 'leader_scout_title', notes: JSON.stringify(scoutTitle) || null, effective_date: null },
        { leader_id: chosenMember.id, title: 'leader_consecration', notes: null, effective_date: consecrationDate || null },
        { leader_id: chosenMember.id, title: 'leader_youth_journey', notes: JSON.stringify(milestones) || null, effective_date: null }
      ];

      return supabase
        .from('leader_milestones')
        .delete()
        .eq('leader_id', chosenMember.id)
        .then(function() {
          return supabase.from('leader_milestones').insert(payload);
        })
        .then(function(res) {
          if (res.error) {
            console.error('[Leader Milestones Save Error]', res.error);
            markHint('msSaveHint', 'error');
            toast('Error saving leader journey: ' + res.error.message, 'error');
            return false;
          }
          markHint('msSaveHint', 'saved');
          if (showToastOnDone) toast('All your leader details have been saved ✓', 'success');
          return true;
        });
    }

    // ─── Done ─────────────────────────────────────────────────────────
    // ─── Single-Page Scout Pass PDF Generator ─────────────────────────
    // ─── Age decimal helper ───────────────────────────────────────────
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

      function branchBlock(color, title, passedFlag, ranksRaw, consecrationYear, departureYear, leadershipRaw, rankDatesMap) {
        var ranksArr = Array.isArray(ranksRaw) ? ranksRaw : [];
        var leadershipArr = [];
        if (Array.isArray(leadershipRaw)) {
          leadershipArr = leadershipRaw;
        } else if (leadershipRaw && typeof leadershipRaw === "object") {
          leadershipArr = Object.keys(leadershipRaw).map(function(k) {
            var item = leadershipRaw[k];
            if (typeof item === "string") return { role: k, name: item };
            return Object.assign({ role: k }, item || {});
          });
        }

        var hasLead = leadershipArr.length > 0;
        var hasRanks = ranksArr.length > 0;
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
                if (l.camp && (l.camp.organized || l.camp.name || l.camp.place || l.camp.date)) {
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

    // ─── Single-Page Scout Record PDF Generator (Failsafe & Robust) ─────────
    function downloadRegisterScoutRecordPdf() {
      try {
        if (!chosenMember) {
          toast("Please select a member first", "error");
          return;
        }

        toast("Preparing Scout Record PDF...", "info");

        var m = chosenMember;
        var memberName = m.full_name || m.fullName || [m.first_name, m.middle_name, m.last_name].filter(Boolean).join(" ") || "Member Profile";
        var initialsStr = initials(memberName);
        var unitName = m.unit || chosenUnit || "Rovers";
        var unitStr = unitName;

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
              '<img src="' + esc(logoUrl) + '" style="width:' + badgeConfig.iconSize + '; height:' + badgeConfig.iconSize + '; object-fit:contain; margin-bottom:2px; display:block;" alt="badge" crossorigin="anonymous" onerror="this.onerror=null;this.style.display=\'none\';" />' +
              '<div dir="rtl" style="font-weight:700; font-size:' + badgeConfig.fontSize + '; color:#1e293b; font-family:Cairo, sans-serif; line-height:1.2; text-align:center;">' + esc(bName) + '</div>' +
            '</div>';
          }).join("");
        } else {
          badgesGridHtml = '<div style="grid-column: 1 / -1; text-align:center; padding:12px; color:#64748b; font-size:12px;">No badges earned yet.</div>';
        }

        var milestonesHtml = buildMemberMilestonesHtmlForRegister(m, milestones);

        var container = document.createElement("div");
        container.style.cssText = "position:fixed; left:-9999px; top:0; width:794px; padding:24px 28px; font-family:Inter, Cairo, sans-serif; color:#0f172a; background:#ffffff; box-sizing:border-box; z-index:99999; visibility:visible;";

        container.innerHTML = 
          '<div>' +
            '<div style="min-height: 1010px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 24px; box-sizing: border-box;">' +
              '<div>' +
                '<!-- TOP HEADER BRANDING -->' +
                '<div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #6366f1; padding-bottom: 10px; margin-bottom: 14px;">' +
                  '<div style="display:flex; align-items:center; gap:12px;">' +
                    '<img src="../../logo.png" style="height:52px; max-width:240px; object-fit:contain; display:block;" alt="Logo" crossorigin="anonymous" onerror="this.onerror=null;this.style.display=\'none\';" />' +
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

        setTimeout(function() {
          html2canvas(container, {
            scale: 2,
            useCORS: true,
            logging: false,
            allowTaint: true
          }).then(function(canvas) {
            try { container.remove(); } catch (_) {}
            var imgData = canvas.toDataURL("image/jpeg", 0.95);
            var _jsPDF = window.jspdf ? window.jspdf.jsPDF : (window.jsPDF || (window.html2pdf && window.html2pdf().jsPDF));
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
        }, 150);

      } catch (err) {
        console.error("[PDF Setup Error]", err);
        toast("PDF Error: " + (err.message || err), "error");
      }
    }

    var dlPdfBtn = document.getElementById("downloadPassPdfBtn");
    if (dlPdfBtn) {
      dlPdfBtn.addEventListener("click", downloadRegisterScoutRecordPdf);
    }

    document.getElementById('editAgainBtn').addEventListener('click', function(){
      refreshSteps();
      goto(firstContentStep());
    });

    // ─── Bidi: give text elements dir="auto" so mixed EN/AR labels
    // resolve direction + alignment from their own content.
    // We do this in JS (not per-element in HTML) so it also picks up
    // any content injected later by renderers (badges, ranks, etc.).
    function applyAutoDir(root){
      var scope = root || document;
      var sel = [
        '.step-title','.step-sub','.heading','.eyebrow',
        '.ms-field-label','.ms-section-header h3',
        '.lead-row-name','.lead-row-body-label',
        '.badge-name','.badge-cat','.rank-chip','.unit-tile',
        '.primary-btn','.secondary-btn','.toast','.save-hint span',
        '.empty','.pin-error'
      ].join(',');
      scope.querySelectorAll(sel).forEach(function(el){
        if(!el.hasAttribute('dir')) el.setAttribute('dir','auto');
      });
    }
    // Watch for dynamically-inserted content and re-apply.
    var _bidiMO = new MutationObserver(function(muts){
      muts.forEach(function(m){
        m.addedNodes.forEach(function(n){
          if(n.nodeType === 1) applyAutoDir(n.parentNode || n);
        });
      });
    });
    _bidiMO.observe(document.body, { childList:true, subtree:true });

    // ─── Boot ─────────────────────────────────────────────────────────
    renderUnits();
    goto('unit');
    applyAutoDir();
  })();
  