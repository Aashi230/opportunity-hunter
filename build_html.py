"""
Opportunity Hunter 2.0 — Modern HTML Layout Structure
Defines the semantic structure for the 8 platform views:
Dashboard, Discover, Profile Settings, Resume Analyzer, Skill Gap, Application Tracker, Deadline Radar, and Career Assistant.
"""

def get_html_body():
    return """
<!-- APPLICATION HEADER -->
<header class="app-header">
  <div style="display:flex; align-items:center; gap:24px;">
    <a href="#" class="brand" onclick="showTab('dashboard'); return false;">
      <div class="brand-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
      </div>
      <div class="brand-title">
        Opportunity Hunter
        <span class="brand-badge">2.0 Pro</span>
      </div>
    </a>

    <!-- TOP NAVIGATION TABS (DESKTOP) -->
    <nav class="nav-tabs" aria-label="Main Navigation">
      <button class="nav-tab-btn active" data-tab="dashboard" onclick="showTab('dashboard')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        Dashboard
      </button>
      <button class="nav-tab-btn" data-tab="discover" onclick="showTab('discover')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        Discover
      </button>
      <button class="nav-tab-btn" data-tab="profile" onclick="showTab('profile')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        Profile
      </button>
      <button class="nav-tab-btn" data-tab="resume" onclick="showTab('resume')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/></svg>
        Resume Analyzer
      </button>
      <button class="nav-tab-btn" data-tab="skillgap" onclick="showTab('skillgap')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20v-6M6 20V10M18 20V4"/></svg>
        Skill Gap
      </button>
      <button class="nav-tab-btn" data-tab="tracker" onclick="showTab('tracker')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="m14 9 2 2 4-4"/></svg>
        Tracker
        <span class="tab-badge" id="nav-tracker-count">0</span>
      </button>
      <button class="nav-tab-btn" data-tab="radar" onclick="showTab('radar')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="m12 12 5-5"/></svg>
        Radar
      </button>
      <button class="nav-tab-btn" data-tab="assistant" onclick="showTab('assistant')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Career Assistant
      </button>
    </nav>
  </div>

  <!-- RIGHT CONTROLS -->
  <div class="header-actions">
    <div class="status-pill" id="srv-indicator" title="Backend Server & Network Status">
      <span class="status-dot live" id="srv-dot"></span>
      <span id="srv-text">Verified Opportunities Network</span>
    </div>

    <button class="icon-btn" id="theme-btn" title="Toggle Dark / Light Theme" aria-label="Toggle Theme">
      <span id="theme-icon">☀️</span>
    </button>

    <div class="header-avatar-btn" onclick="showTab('profile')" title="View and Edit Student Profile">
      <div class="avatar-disc" id="head-avatar">A</div>
      <span style="font-size:0.82rem; font-weight:700;" id="head-prof-pct">85%</span>
    </div>
  </div>
</header>

<!-- MAIN CONTAINER -->
<main class="app-main">

  <!-- ======================================================== -->
  <!-- TAB 1: EXECUTIVE DASHBOARD OVERVIEW -->
  <!-- ======================================================== -->
  <section id="v-dashboard" class="tab-view">
    <!-- WELCOME HERO BENTO -->
    <div class="hero-deck">
      <div class="welcome-card">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <span class="badge badge-lavender" style="margin-bottom:10px;">Personal Career Hub</span>
              <h1 style="font-family:var(--font-display); font-size:1.85rem; font-weight:800; letter-spacing:-0.02em; margin-bottom:6px;">
                Welcome back, <span id="dash-greeting-name" style="color:var(--lavender);">Student</span>!
              </h1>
              <p style="color:var(--text-muted); font-size:0.95rem;" id="dash-greeting-meta">
                B.Tech Computer Science &bull; 2nd year &bull; Software Engineering Track
              </p>
            </div>
            <button class="btn btn-subtle btn-sm" onclick="showTab('profile')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              Edit Profile
            </button>
          </div>
        </div>

        <div style="margin-top:24px;">
          <div style="display:flex; justify-content:space-between; font-size:0.82rem; font-weight:700; margin-bottom:8px;">
            <span style="color:var(--text-muted);">Profile Match Strength</span>
            <span id="dash-prof-strength-num" style="color:var(--lavender);">85% Complete</span>
          </div>
          <div style="height:8px; background:var(--bg-subtle); border-radius:var(--radius-full); overflow:hidden;">
            <div id="dash-prof-strength-bar" style="height:100%; width:85%; background:linear-gradient(90deg, var(--primary), #a855f7); border-radius:var(--radius-full); transition:width 0.4s ease;"></div>
          </div>
        </div>
      </div>

      <!-- QUICK ACTION DOCK -->
      <div class="bento-card" style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="card-title-group">
          <h3 class="card-title">Quick Actions</h3>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; margin:16px 0;">
          <button class="btn btn-primary" onclick="showTab('resume')" style="justify-content:flex-start;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
            Upload Resume for Instant Audit
          </button>
          <button class="btn btn-subtle" onclick="showTab('discover')" style="justify-content:flex-start;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            Explore Opportunities
          </button>
          <button class="btn btn-subtle" onclick="showTab('tracker')" style="justify-content:flex-start;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>
            Open Kanban Application Pipeline
          </button>
        </div>
        <div style="font-size:0.78rem; color:var(--text-dim); text-align:center;">
          Verified programs updated regularly from official career portals.
        </div>
      </div>
    </div>

    <!-- REAL STATS KPIS -->
    <div class="kpi-grid">
      <div class="kpi-card" onclick="showTab('discover')">
        <div class="kpi-icon-box" style="color:var(--success);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg></div>
        <div>
          <div class="kpi-num" id="kpi-dash-matched">0</div>
          <div class="kpi-label">Matching Opportunities</div>
        </div>
      </div>
      <div class="kpi-card" onclick="showTab('tracker')">
        <div class="kpi-icon-box" style="color:var(--lavender);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></div>
        <div>
          <div class="kpi-num" id="kpi-dash-saved">0</div>
          <div class="kpi-label">Saved in Tracker</div>
        </div>
      </div>
      <div class="kpi-card" onclick="showTab('tracker')">
        <div class="kpi-icon-box" style="color:var(--info);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div>
        <div>
          <div class="kpi-num" id="kpi-dash-active-apps">0</div>
          <div class="kpi-label">Active Applications</div>
        </div>
      </div>
      <div class="kpi-card" onclick="showTab('radar')">
        <div class="kpi-icon-box" style="color:var(--warning);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
        <div>
          <div class="kpi-num" id="kpi-dash-urgent">0</div>
          <div class="kpi-label">Deadlines Within 7 Days</div>
        </div>
      </div>
    </div>

    <!-- RECOMMENDED OPPORTUNITIES GRID -->
    <div class="bento-card" style="margin-bottom:24px;">
      <div class="card-header-bar">
        <div>
          <h3 class="card-title">Recommended Opportunities for You</h3>
          <p class="card-subtitle">Personalized opportunities scoring 70%+ match against your degree and skills</p>
        </div>
        <button class="btn btn-subtle btn-sm" onclick="showTab('discover')">View All Matches &rarr;</button>
      </div>
      <div class="cards-grid" id="dash-recommended-grid"></div>
    </div>

    <!-- SPLIT DECK: UPCOMING DEADLINES & RECENT ACTIVITY -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
      <!-- UPCOMING DEADLINES WIDGET -->
      <div class="bento-card">
        <div class="card-header-bar">
          <div>
            <h3 class="card-title">Upcoming Deadlines</h3>
            <p class="card-subtitle">Keep track of closing dates</p>
          </div>
          <button class="btn btn-subtle btn-sm" onclick="showTab('radar')">Radar &rarr;</button>
        </div>
        <div id="dash-deadlines-list" style="display:flex; flex-direction:column; gap:12px;"></div>
      </div>

      <!-- RECENT ACTIVITY FEED -->
      <div class="bento-card">
        <div class="card-header-bar">
          <div>
            <h3 class="card-title">Recent Activity &amp; Pipeline Updates</h3>
            <p class="card-subtitle">Tracked events from your job search</p>
          </div>
          <button class="btn btn-subtle btn-sm" onclick="showTab('tracker')">Tracker &rarr;</button>
        </div>
        <div id="dash-activity-list" style="display:flex; flex-direction:column; gap:12px;"></div>
      </div>
    </div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 2: ADVANCED OPPORTUNITY DISCOVERY -->
  <!-- ======================================================== -->
  <section id="v-discover" class="tab-view" style="display:none;">
    <!-- SEARCH & COMMAND DECK -->
    <div class="bento-card" style="margin-bottom:24px; padding:28px;">
      <h2 style="font-family:var(--font-display); font-size:1.6rem; font-weight:800; letter-spacing:-0.02em; margin-bottom:8px;">
        Find Verified Student Opportunities
      </h2>
      <p style="color:var(--text-muted); font-size:0.92rem; margin-bottom:20px;">
        Discover internships, fellowships, hackathons, and research scholarships with transparent eligibility verification.
      </p>

      <!-- INPUT GROUP -->
      <div style="display:flex; gap:12px; margin-bottom:16px;">
        <div style="position:relative; flex:1;">
          <input type="text" id="q" placeholder="Search by role or domain (e.g. Software Engineering, AI/ML, Data Science, Web Development)..." style="padding-left:42px; font-size:1rem; height:48px;">
          <svg style="position:absolute; left:14px; top:15px; color:var(--text-dim);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </div>
        <button class="btn btn-primary" id="btn-discover-go" style="padding:0 24px; height:48px;" onclick="run(false)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          Search Opportunities
        </button>
      </div>

      <!-- DOMAIN QUICK TAGS -->
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
        <span style="font-size:0.78rem; font-weight:700; color:var(--text-dim);">Popular Tracks:</span>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Software Engineering')">Software Engineering</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('AI/ML')">AI / Machine Learning</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Data Science')">Data Science</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Web Development')">Web Development</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Cloud Computing')">Cloud &amp; DevOps</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Cybersecurity')">Cybersecurity</button>
        <button type="button" class="btn btn-subtle btn-sm" onclick="setSearchQuery('Open Source')">Open Source</button>
      </div>
    </div>

    <!-- STUDENT PROFILE HUD STRIP -->
    <div class="bento-card" style="margin-bottom:24px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:16px;">
          <div class="avatar-disc" id="hud-avatar" style="width:42px; height:42px; font-size:1.1rem;">A</div>
          <div>
            <div style="display:flex; align-items:center; gap:8px;">
              <h4 id="hud-name" style="font-size:1.05rem; font-weight:700;">Student Profile</h4>
              <span class="badge badge-lavender" id="hud-year">2nd year</span>
            </div>
            <p style="font-size:0.85rem; color:var(--text-muted);" id="hud-degree">B.Tech Computer Science &bull; Location: India</p>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <button class="btn btn-subtle btn-sm" onclick="showTab('profile')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit Profile
          </button>
        </div>
      </div>
    </div>

    <!-- STATUS NOTICES -->
    <div id="status"></div>

    <!-- FILTER TOOLBAR -->
    <div class="bento-card" style="margin-bottom:20px; padding:16px 20px;">
      <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px;">
        <!-- CATEGORY PILLS -->
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
          <button class="pill-filter on" data-category="all" onclick="setCategoryFilter('all')">All</button>
          <button class="pill-filter" data-category="internship" onclick="setCategoryFilter('internship')">💼 Internships</button>
          <button class="pill-filter" data-category="scholarship" onclick="setCategoryFilter('scholarship')">🎓 Scholarships</button>
          <button class="pill-filter" data-category="fellowship" onclick="setCategoryFilter('fellowship')">🌟 Fellowships</button>
          <button class="pill-filter" data-category="program" onclick="setCategoryFilter('program')">🚀 Programs &amp; Hackathons</button>
          <button class="pill-filter" data-category="remote" onclick="setCategoryFilter('remote')">🌐 Remote</button>
        </div>

        <div style="display:flex; align-items:center; gap:12px;">
          <input type="text" id="live-search" placeholder="Filter by keyword..." style="width:200px; padding:6px 12px; font-size:0.85rem;" oninput="render()">
          <select id="sort" style="width:180px; padding:6px 12px; font-size:0.85rem;" onchange="render()">
            <option value="score">Sort: Highest Match</option>
            <option value="deadline">Sort: Earliest Deadline</option>
            <option value="title">Sort: Title (A-Z)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- CARDS RESULTS SECTION -->
    <div id="cards" class="cards-grid"></div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 3: DEDICATED STUDENT PROFILE SETTINGS -->
  <!-- ======================================================== -->
  <section id="v-profile" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:24px;">
      <div class="card-header-bar" style="margin-bottom:0;">
        <div>
          <span class="badge badge-lavender" style="margin-bottom:6px;">Account &amp; Career Preferences</span>
          <h2 class="card-title" style="font-size:1.6rem; margin-top:4px;">Student Career Profile</h2>
          <p class="card-subtitle">
            Configure your academic background, target roles, and technical stack to receive verified, transparent opportunity matches.
          </p>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
          <button class="btn btn-primary" onclick="saveProfileFromTab()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            Save Profile Changes
          </button>
        </div>
      </div>
    </div>

    <!-- PROFILE FORM BENTO GRID -->
    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:24px;">
      <!-- LEFT FORM -->
      <div class="bento-card">
        <h3 class="card-title" style="font-size:1.2rem; margin-bottom:18px;">Academic &amp; Personal Credentials</h3>
        <div class="form-grid">
          <div class="form-group" style="grid-column: 1 / -1;">
            <label for="tab-prof-name">Full Name *</label>
            <input type="text" id="tab-prof-name" placeholder="e.g. Aashi Srivastava">
          </div>

          <div class="form-group" style="grid-column: 1 / -1;">
            <label for="tab-prof-degree">Degree &amp; Major *</label>
            <input type="text" id="tab-prof-degree" placeholder="e.g. B.Tech Computer Science">
            <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">
              <span style="font-size:0.75rem; color:var(--text-dim); align-self:center; font-weight:700;">Presets:</span>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('B.Tech Computer Science')">B.Tech CSE</button>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('B.Tech Information Technology')">B.Tech IT</button>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('B.E. Computer Engineering')">B.E. Computer</button>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('M.Tech Software Engineering')">M.Tech</button>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('BCA / MCA')">BCA / MCA</button>
              <button type="button" class="btn btn-subtle btn-sm" onclick="setProfileDegreePreset('B.Sc Computer Science')">B.Sc CS</button>
            </div>
          </div>

          <div class="form-group">
            <label for="tab-prof-year">Current Year of Study *</label>
            <select id="tab-prof-year">
              <option value="">Select Year</option>
              <option value="1st year">1st year (Freshman)</option>
              <option value="2nd year">2nd year (Sophomore)</option>
              <option value="3rd year">3rd year (Junior / Pre-final)</option>
              <option value="Final year">Final year (Senior)</option>
              <option value="Master’s">Master’s / Postgraduate</option>
              <option value="PhD">PhD / Doctoral</option>
              <option value="Graduated">Graduated / Fresher</option>
            </select>
          </div>

          <div class="form-group">
            <label for="tab-prof-grad-year">Expected Graduation Year</label>
            <input type="text" id="tab-prof-grad-year" placeholder="e.g. 2027">
          </div>

          <div class="form-group">
            <label for="tab-prof-loc">Location / Target Country</label>
            <input type="text" id="tab-prof-loc" placeholder="e.g. India, Remote, Bangalore">
          </div>

          <div class="form-group">
            <label for="tab-prof-interests">Primary Career Track</label>
            <input type="text" id="tab-prof-interests" placeholder="e.g. Software Engineering, AI/ML, Full Stack">
          </div>

          <div class="form-group">
            <label for="tab-prof-type">Preferred Opportunity Type</label>
            <select id="tab-prof-type">
              <option value="any">Any Opportunity</option>
              <option value="internship">Internship</option>
              <option value="scholarship">Scholarship</option>
              <option value="fellowship">Fellowship</option>
              <option value="program">Developer Program / Hackathon</option>
            </select>
          </div>

          <div class="form-group">
            <label for="tab-prof-mode">Preferred Work Mode</label>
            <select id="tab-prof-mode">
              <option value="any">No preference</option>
              <option value="remote">Remote Only</option>
              <option value="onsite">On-site / Hybrid</option>
            </select>
          </div>
        </div>

        <div style="margin-top:24px; padding-top:20px; border-top:1px solid var(--border);">
          <button class="btn btn-primary" onclick="saveProfileFromTab()" style="padding:12px 28px; font-size:1rem;">
            Save Profile Changes
          </button>
        </div>
      </div>

      <!-- RIGHT: SKILLS HUB -->
      <div class="bento-card" style="display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <h3 class="card-title" style="font-size:1.2rem; margin-bottom:8px;">Technical Stack Hub</h3>
          <p class="card-subtitle" style="margin-bottom:16px;">Click technology tags to add or remove them from your profile.</p>

          <!-- ACTIVE SKILLS CHIPS -->
          <div style="margin-bottom:16px;">
            <label style="display:block; margin-bottom:8px;">Active Profile Skills:</label>
            <div id="tab-active-skills-chips" style="display:flex; flex-wrap:wrap; gap:6px; min-height:40px; padding:10px; background:var(--bg-card-elevated); border-radius:var(--radius-md); border:1px solid var(--border);"></div>
          </div>

          <!-- QUICK SKILL TOGGLE PILLS -->
          <label style="display:block; margin-bottom:8px;">Popular Technical Skills:</label>
          <div style="display:flex; flex-wrap:wrap; gap:6px;" id="tab-skill-toggle-grid"></div>

          <!-- CUSTOM SKILL INPUT -->
          <div style="display:flex; gap:8px; margin-top:18px;">
            <input type="text" id="tab-custom-skill-input" placeholder="Add custom skill (e.g. Next.js, FastAPI)..." onkeydown="if(event.key === 'Enter'){ addCustomSkillToTab(); event.preventDefault(); }">
            <button class="btn btn-subtle" onclick="addCustomSkillToTab()">+ Add</button>
          </div>
        </div>

        <div style="margin-top:24px; padding:16px; background:var(--bg-card-elevated); border-radius:var(--radius-md); font-size:0.82rem; color:var(--text-muted); line-height:1.5;">
          💡 <b>Tip</b>: Adding in-demand skills like Python, Docker, and SQL increases your match score and unlocks verified program recommendations.
        </div>
      </div>
    </div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 4: RESUME ANALYZER MODULE -->
  <!-- ======================================================== -->
  <section id="v-resume" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:24px;">
      <div class="card-header-bar">
        <div>
          <span class="badge badge-lavender" style="margin-bottom:6px;">Intelligent Career Module</span>
          <h2 class="card-title" style="font-size:1.6rem; margin-top:4px;">Resume Analyzer &amp; Skill Extractor</h2>
          <p class="card-subtitle">
            Upload your resume to extract technical skills, calculate resume strength, discover gaps, and find suitable opportunities.
          </p>
        </div>
      </div>

      <!-- RESUME DROPZONE -->
      <div class="dropzone" id="resume-dropzone" onclick="$('#resume-file-input').click()">
        <input type="file" id="resume-file-input" accept=".pdf,.txt,.docx" style="display:none;" onchange="handleResumeFileUpload(event)">
        <div style="width:54px; height:54px; border-radius:50%; background:var(--primary-glow); color:var(--primary); display:flex; align-items:center; justify-content:center; margin:0 auto 16px;">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
        </div>
        <h4 style="font-family:var(--font-display); font-size:1.15rem; font-weight:700; margin-bottom:6px;">
          Upload your Resume (PDF, DOCX, or TXT)
        </h4>
        <p style="font-size:0.88rem; color:var(--text-muted); max-width:440px; margin:0 auto 12px;">
          Drag and drop your file here, or click to browse. Processing is performed securely and your private data is never exposed.
        </p>
        <div style="display:flex; justify-content:center; gap:8px;">
          <span class="badge badge-info">PDF Safe Parsing</span>
          <span class="badge badge-success">Privacy Guaranteed</span>
        </div>
      </div>

      <!-- OR TEXT PASTE -->
      <div style="margin-top:20px;">
        <button class="btn btn-subtle btn-sm" onclick="toggleResumePasteArea()" id="btn-toggle-paste">Or paste resume text manually &darr;</button>
        <div id="resume-paste-box" style="display:none; margin-top:12px;">
          <textarea id="resume-manual-text" rows="8" placeholder="Paste your resume contents or project summary here..."></textarea>
          <button class="btn btn-primary btn-sm" style="margin-top:10px;" onclick="analyzeResumeTextManual()">Analyze Pasted Resume</button>
        </div>
      </div>
    </div>

    <!-- RESUME RESULTS CONTAINER -->
    <div id="resume-results" style="display:none;"></div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 5: SKILL GAP ANALYZER -->
  <!-- ======================================================== -->
  <section id="v-skillgap" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:24px;">
      <span class="badge badge-lavender" style="margin-bottom:6px;">Market Intelligence</span>
      <h2 class="card-title" style="font-size:1.6rem; margin-top:4px;">Skill Gap &amp; Career Roadmap</h2>
      <p class="card-subtitle">
        Compare your profile skills against the technical prerequisites of top verified student programs.
      </p>
    </div>

    <div id="skillgap-container"></div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 6: APPLICATION TRACKER (8-STAGE KANBAN) -->
  <!-- ======================================================== -->
  <section id="v-tracker" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:20px; padding:20px 24px;">
      <div class="card-header-bar" style="margin-bottom:0;">
        <div>
          <span class="badge badge-lavender" style="margin-bottom:6px;">Application Pipeline</span>
          <h2 class="card-title" style="font-size:1.5rem; margin-top:2px;">Student Application Tracker</h2>
          <p class="card-subtitle">Manage your opportunities across 8 structured Kanban stages</p>
        </div>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-subtle btn-sm" onclick="exportTrackerCSV()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
            Export CSV
          </button>
          <button class="btn btn-primary btn-sm" onclick="openAddCustomAppModal()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Add Custom Opportunity
          </button>
        </div>
      </div>
    </div>

    <!-- 8 KANBAN STAGES BOARD -->
    <div class="kanban-board" id="kanban-board-container"></div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 7: DEADLINE RADAR & CALENDAR -->
  <!-- ======================================================== -->
  <section id="v-radar" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:24px;">
      <div class="card-header-bar" style="margin-bottom:0;">
        <div>
          <span class="badge badge-warning" style="margin-bottom:6px;">Time Management</span>
          <h2 class="card-title" style="font-size:1.5rem; margin-top:2px;">Deadline Radar &amp; Calendar</h2>
          <p class="card-subtitle">Stay ahead of application closing dates with urgency bands and calendar export</p>
        </div>
        <button class="btn btn-primary btn-sm" onclick="exportAllDeadlinesICS()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
          Export Deadlines (.ics Calendar)
        </button>
      </div>
    </div>

    <div id="radar-board-container"></div>
  </section>

  <!-- ======================================================== -->
  <!-- TAB 8: CAREER ASSISTANT -->
  <!-- ======================================================== -->
  <section id="v-assistant" class="tab-view" style="display:none;">
    <div class="bento-card" style="margin-bottom:20px;">
      <span class="badge badge-lavender" style="margin-bottom:6px;">Contextual AI Companion</span>
      <h2 class="card-title" style="font-size:1.5rem; margin-top:2px;">Opportunity Hunter Career Assistant</h2>
      <p class="card-subtitle">
        Ask intelligent questions regarding your opportunity eligibility, technical resume improvements, and interview preparation.
      </p>
    </div>

    <div class="chat-window">
      <!-- QUICK PROMPT CHIPS -->
      <div style="padding:12px 20px; background:var(--bg-subtle); display:flex; flex-wrap:wrap; gap:8px; border-bottom:1px solid var(--border);">
        <button class="btn btn-subtle btn-sm" onclick="sendPrompt('Which internships match my profile best?')">🎯 Which internships match me best?</button>
        <button class="btn btn-subtle btn-sm" onclick="sendPrompt('Am I eligible for Microsoft Explore?')">🏛️ Am I eligible for Explore Microsoft?</button>
        <button class="btn btn-subtle btn-sm" onclick="sendPrompt('Which skills should I learn next?')">📈 What skills should I learn next?</button>
        <button class="btn btn-subtle btn-sm" onclick="sendPrompt('How can I improve my resume for technical roles?')">📄 How to improve my resume?</button>
        <button class="btn btn-subtle btn-sm" onclick="sendPrompt('What should I prepare for an internship interview?')">💼 Technical interview prep tips</button>
      </div>

      <!-- MESSAGES CONTAINER -->
      <div class="chat-messages" id="chat-messages-box"></div>

      <!-- INPUT BAR -->
      <div class="chat-input-bar">
        <input type="text" id="assistant-input-text" placeholder="Type a career question or ask about an opportunity..." onkeydown="if(event.key === 'Enter') handleAssistantSend()">
        <button class="btn btn-primary" onclick="handleAssistantSend()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          Send
        </button>
      </div>
    </div>
  </section>
</main>

<!-- PROFILE MODAL (FOR INSTANT POPUP) -->
<div id="profile-modal" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(0,0,0,0.75); backdrop-filter:blur(6px); align-items:center; justify-content:center; padding:16px;" onclick="if(event.target === this) closeProfileModal()">
  <div class="bento-card" style="max-width:580px; width:100%; max-height:90vh; overflow-y:auto;">
    <div class="card-header-bar">
      <h3 class="card-title">Quick Profile Editor</h3>
      <button class="icon-btn" onclick="closeProfileModal()">&times;</button>
    </div>
    <div class="form-grid">
      <div class="form-group" style="grid-column: 1 / -1;">
        <label for="prof-name">Full Name</label>
        <input type="text" id="prof-name" placeholder="e.g. Aashi Srivastava">
      </div>
      <div class="form-group">
        <label for="prof-degree">Degree &amp; Major</label>
        <input type="text" id="prof-degree" placeholder="B.Tech Computer Science">
      </div>
      <div class="form-group">
        <label for="prof-year">Academic Study Year</label>
        <select id="prof-year">
          <option value="">Not Specified</option>
          <option value="1st year">1st year</option>
          <option value="2nd year">2nd year</option>
          <option value="3rd year">3rd year</option>
          <option value="Final year">Final year</option>
          <option value="Master’s">Master’s</option>
          <option value="PhD">PhD</option>
          <option value="Graduated">Graduated / Fresher</option>
        </select>
      </div>
      <div class="form-group">
        <label for="prof-grad-year">Graduation Year</label>
        <input type="text" id="prof-grad-year" placeholder="e.g. 2027">
      </div>
      <div class="form-group">
        <label for="prof-loc">Location / Country</label>
        <input type="text" id="prof-loc" placeholder="e.g. India">
      </div>
      <div class="form-group" style="grid-column: 1 / -1;">
        <label for="prof-skills">Technical Skills (Comma separated or click below)</label>
        <input type="text" id="prof-skills" placeholder="Python, SQL, React, Git, Docker, Machine Learning">
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('Python')">+ Python</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('SQL')">+ SQL</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('React')">+ React</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('Machine Learning')">+ ML</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('C++')">+ C++</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('Java')">+ Java</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('Docker')">+ Docker</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('Git')">+ Git</button>
          <button type="button" class="btn btn-subtle btn-sm" onclick="toggleModalSkill('AWS')">+ AWS</button>
        </div>
      </div>
      <div class="form-group">
        <label for="prof-type">Preferred Opportunity Type</label>
        <select id="prof-type">
          <option value="any">Any Opportunity</option>
          <option value="internship">Internship</option>
          <option value="scholarship">Scholarship</option>
          <option value="fellowship">Fellowship</option>
          <option value="program">Developer Program / Hackathon</option>
        </select>
      </div>
      <div class="form-group">
        <label for="prof-mode">Work Mode</label>
        <select id="prof-mode">
          <option value="any">Any Mode</option>
          <option value="remote">Remote Only</option>
          <option value="onsite">On-site / Hybrid</option>
        </select>
      </div>
    </div>
    <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:24px;">
      <button class="btn btn-subtle" onclick="closeProfileModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveProfileFromModal()">Save Profile</button>
    </div>
  </div>
</div>

<!-- ADD CUSTOM APPLICATION MODAL -->
<div id="custom-app-modal" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(0,0,0,0.75); backdrop-filter:blur(6px); align-items:center; justify-content:center; padding:16px;" onclick="if(event.target === this) closeCustomAppModal()">
  <div class="bento-card" style="max-width:500px; width:100%;">
    <div class="card-header-bar">
      <h3 class="card-title">Track New Application</h3>
      <button class="icon-btn" onclick="closeCustomAppModal()">&times;</button>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;">
      <div class="form-group">
        <label for="custom-app-title">Opportunity Title *</label>
        <input type="text" id="custom-app-title" placeholder="e.g. Summer Software Intern">
      </div>
      <div class="form-group">
        <label for="custom-app-org">Company / Organization *</label>
        <input type="text" id="custom-app-org" placeholder="e.g. Google, Microsoft, Infosys">
      </div>
      <div class="form-group">
        <label for="custom-app-url">Application URL</label>
        <input type="url" id="custom-app-url" placeholder="https://careers...">
      </div>
      <div class="form-group">
        <label for="custom-app-stage">Initial Pipeline Stage</label>
        <select id="custom-app-stage">
          <option value="interested">💡 Interested</option>
          <option value="planning">📝 Planning to Apply</option>
          <option value="applied">📨 Applied</option>
          <option value="assessment">💻 Assessment</option>
          <option value="interviewing">🤝 Interviewing</option>
        </select>
      </div>
      <div class="form-group">
        <label for="custom-app-deadline">Deadline Date</label>
        <input type="date" id="custom-app-deadline">
      </div>
      <div class="form-group">
        <label for="custom-app-notes">Notes &amp; Links</label>
        <textarea id="custom-app-notes" rows="3" placeholder="Requisition ID, recruiter contact, referral notes..."></textarea>
      </div>
    </div>
    <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:20px;">
      <button class="btn btn-subtle" onclick="closeCustomAppModal()">Cancel</button>
      <button class="btn btn-primary" onclick="submitCustomApplication()">Save to Tracker</button>
    </div>
  </div>
</div>

<!-- TOAST CONTAINER -->
<div id="toast-box"></div>

<!-- MOBILE BOTTOM DOCK -->
<nav class="mobile-dock" aria-label="Mobile Navigation">
  <button class="m-tab-btn active" data-tab="dashboard" onclick="showTab('dashboard')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
    <span>Home</span>
  </button>
  <button class="m-tab-btn" data-tab="discover" onclick="showTab('discover')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
    <span>Discover</span>
  </button>
  <button class="m-tab-btn" data-tab="profile" onclick="showTab('profile')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    <span>Profile</span>
  </button>
  <button class="m-tab-btn" data-tab="tracker" onclick="showTab('tracker')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>
    <span>Tracker</span>
  </button>
  <button class="m-tab-btn" data-tab="assistant" onclick="showTab('assistant')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <span>Assistant</span>
  </button>
</nav>
"""
