"""
Opportunity Hunter 2.0 — Modern SaaS CSS Design System
Navy, Lavender, Off-White, Emerald, Amber, Rose palette with Glassmorphism,
Responsive Bento Grid, Kanban Pipeline, Calendar View, and Smooth Micro-interactions.
"""

def get_css():
    return """
/* MODERN SAAS THEME TOKENS */
:root {
  --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display: 'Outfit', var(--font-main);
  
  /* Color Palette: Navy, Lavender, Off-white & Accents */
  --bg-base: #0a0f1d;
  --bg-card: #11182c;
  --bg-card-elevated: #18223d;
  --bg-subtle: #1e2945;
  --border: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(99, 102, 241, 0.4);
  --border-focus: #6366f1;
  
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --primary-glow: rgba(99, 102, 241, 0.25);
  --lavender: #818cf8;
  --lavender-soft: #c7d2fe;
  
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  
  --success: #10b981;
  --success-bg: rgba(16, 185, 129, 0.12);
  --warning: #f59e0b;
  --warning-bg: rgba(245, 158, 11, 0.12);
  --danger: #ef4444;
  --danger-bg: rgba(239, 68, 68, 0.12);
  --info: #38bdf8;
  --info-bg: rgba(56, 189, 248, 0.12);
  
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.4);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  
  --header-h: 72px;
}

[data-theme="light"] {
  --bg-base: #f8fafc;
  --bg-card: #ffffff;
  --bg-card-elevated: #f1f5f9;
  --bg-subtle: #e2e8f0;
  --border: rgba(0, 0, 0, 0.08);
  --border-hover: rgba(99, 102, 241, 0.4);
  --border-focus: #6366f1;
  
  --text-main: #0f172a;
  --text-muted: #475569;
  --text-dim: #94a3b8;
  
  --primary-glow: rgba(99, 102, 241, 0.15);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.12);
}

/* BASE RESET */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-family: var(--font-main);
  background: var(--bg-base);
  color: var(--text-main);
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
}

body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  line-height: 1.5;
  overflow-x: hidden;
}

/* TOP NAVBAR */
header.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  height: var(--header-h);
  background: rgba(10, 15, 29, 0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  transition: all 0.3s ease;
}

[data-theme="light"] header.app-header {
  background: rgba(255, 255, 255, 0.88);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-main);
}

.brand-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, var(--primary), #a855f7);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 16px var(--primary-glow);
  color: #fff;
}

.brand-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 7px;
  background: var(--primary-glow);
  color: var(--lavender);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

/* NAV TABS */
.nav-tabs {
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--bg-card);
  padding: 4px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
}

.nav-tab-btn {
  background: transparent;
  border: none;
  padding: 8px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-muted);
  border-radius: var(--radius-full);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.nav-tab-btn:hover {
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.04);
}

.nav-tab-btn.active {
  background: var(--primary);
  color: #ffffff;
  box-shadow: 0 2px 10px var(--primary-glow);
}

.tab-badge {
  font-size: 0.72rem;
  padding: 1px 6px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.2);
  color: inherit;
  font-weight: 700;
}

/* HEADER CONTROLS */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 5px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  color: var(--text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--warning);
}

.status-dot.live {
  background: var(--success);
  box-shadow: 0 0 8px var(--success);
}

.icon-btn {
  background: var(--bg-card);
  border: 1px solid var(--border);
  width: 38px;
  height: 38px;
  border-radius: 10px;
  color: var(--text-main);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: var(--bg-card-elevated);
  border-color: var(--border-hover);
}

.header-avatar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  cursor: pointer;
  color: var(--text-main);
}

.avatar-disc {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--lavender));
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* MAIN CONTAINER */
main.app-main {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 24px 60px;
}

/* BENTO CARDS & SURFACES */
.bento-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: border-color 0.2s, box-shadow 0.2s;
  position: relative;
}

.bento-card:hover {
  border-color: var(--border-hover);
}

.card-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.card-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* BUTTONS */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 4px 14px var(--primary-glow);
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-subtle {
  background: var(--bg-card-elevated);
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-subtle:hover {
  border-color: var(--border-hover);
  background: var(--bg-subtle);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
  border-radius: var(--radius-sm);
}

.btn-danger {
  background: var(--danger-bg);
  color: var(--danger);
  border-color: rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
  background: var(--danger);
  color: #fff;
}

/* FORM ELEMENTS */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

input, select, textarea {
  width: 100%;
  font-family: inherit;
  font-size: 0.9rem;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--bg-card-elevated);
  border: 1px solid var(--border);
  color: var(--text-main);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--primary-glow);
}

/* PILLS & BADGES */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.badge-success { background: var(--success-bg); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.25); }
.badge-warning { background: var(--warning-bg); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.25); }
.badge-danger { background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.25); }
.badge-info { background: var(--info-bg); color: var(--info); border: 1px solid rgba(56, 189, 248, 0.25); }
.badge-lavender { background: rgba(99, 102, 241, 0.15); color: var(--lavender); border: 1px solid rgba(99, 102, 241, 0.3); }

/* DASHBOARD OVERVIEW */
.hero-deck {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.welcome-card {
  background: linear-gradient(135deg, var(--bg-card), #161e38);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.kpi-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-hover);
}

.kpi-icon-box {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  background: var(--bg-card-elevated);
}

.kpi-num {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1.1;
}

.kpi-label {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 600;
}

/* OPPORTUNITY CARDS */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.opp-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.25s ease;
  position: relative;
}

.opp-card:hover {
  border-color: var(--border-hover);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  transform: translateY(-2px);
}

.opp-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.opp-org-badge {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--lavender);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.opp-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.35;
  margin-top: 4px;
}

/* MATCH DIAL */
.match-dial {
  width: 56px;
  height: 56px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.match-dial svg {
  transform: rotate(-90deg);
  width: 100%;
  height: 100%;
}

.match-dial-text {
  position: absolute;
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 800;
}

/* KANBAN BOARD */
.kanban-board {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 20px;
  min-height: 600px;
}

.kanban-col {
  flex: 0 0 310px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  max-height: 800px;
}

.kanban-col-header {
  padding: 16px 18px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.88rem;
  font-weight: 700;
}

.kanban-col-body {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  flex: 1;
}

.kanban-item {
  background: var(--bg-card-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px;
  cursor: grab;
  transition: border-color 0.2s, transform 0.2s;
}

.kanban-item:hover {
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

/* RESUME ANALYZER */
.dropzone {
  border: 2px dashed var(--border-hover);
  background: var(--bg-card-elevated);
  border-radius: var(--radius-lg);
  padding: 40px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease;
}

.dropzone:hover, .dropzone.dragover {
  border-color: var(--primary);
  background: rgba(99, 102, 241, 0.06);
}

/* CAREER ASSISTANT CHAT */
.chat-window {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  height: 650px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-bubble {
  max-width: 80%;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  font-size: 0.92rem;
  line-height: 1.6;
}

.chat-bubble.bot {
  background: var(--bg-card-elevated);
  border: 1px solid var(--border);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chat-bubble.user {
  background: var(--primary);
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.chat-input-bar {
  padding: 16px 20px;
  background: var(--bg-card-elevated);
  border-top: 1px solid var(--border);
  display: flex;
  gap: 12px;
}

/* TOASTS */
#toast-box {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast-msg {
  background: #1e2945;
  color: #fff;
  border: 1px solid var(--border-hover);
  padding: 12px 18px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.88rem;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* MOBILE BOTTOM NAV */
.mobile-dock {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(10, 15, 29, 0.95);
  backdrop-filter: blur(16px);
  border-top: 1px solid var(--border);
  z-index: 100;
  align-items: center;
  justify-content: space-around;
  padding: 0 8px;
}

[data-theme="light"] .mobile-dock {
  background: rgba(255, 255, 255, 0.95);
}

.m-tab-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  padding: 6px;
}

.m-tab-btn.active {
  color: var(--primary);
}

/* MOBILE & RESPONSIVE COMPONENT CLASSES */
.dash-grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.profile-layout-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.search-input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.mobile-tab-scroll {
  display: none;
}

.modal-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(6px);
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.modal-card {
  max-width: 580px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: var(--radius-lg);
}

/* RESPONSIVE BREAKPOINTS */
@media (max-width: 1024px) {
  .hero-deck { grid-template-columns: 1fr; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .cards-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  /* HEADER & TOP NAVIGATION */
  header.app-header {
    height: 58px;
    padding: 0 14px;
  }
  .nav-tabs {
    display: none;
  }
  .brand-title {
    font-size: 1.05rem;
  }
  .brand-badge {
    display: none;
  }

  /* HORIZONTAL SWIPEABLE TAB BAR FOR ALL 8 VIEWS */
  .mobile-tab-scroll {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding: 8px 12px;
    gap: 8px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 58px;
    z-index: 95;
  }
  .mobile-tab-scroll::-webkit-scrollbar {
    display: none;
  }
  .m-scroll-btn {
    background: var(--bg-card-elevated);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: var(--radius-full);
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.2s ease;
    text-decoration: none;
  }
  .m-scroll-btn.active {
    background: var(--primary);
    color: #fff;
    border-color: var(--primary);
    box-shadow: 0 2px 8px var(--primary-glow);
  }

  /* MAIN CONTENT AREA */
  main.app-main {
    padding: 16px 12px calc(80px + env(safe-area-inset-bottom, 0px));
  }
  .bento-card {
    padding: 18px 14px;
    border-radius: var(--radius-md);
  }
  .card-title {
    font-size: 1.25rem;
  }

  /* 2X2 MOBILE KPI STATS WIDGET */
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 18px;
  }
  .kpi-card {
    padding: 14px 12px;
    gap: 10px;
  }
  .kpi-num {
    font-size: 1.45rem;
  }
  .kpi-label {
    font-size: 0.72rem;
  }
  .kpi-icon-box {
    width: 38px;
    height: 38px;
    font-size: 1.1rem;
    flex-shrink: 0;
  }

  /* RESPONSIVE LAYOUT GRIDS */
  .dash-grid-2col {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .profile-layout-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .form-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  /* SEARCH INPUT DECK */
  .search-input-group {
    flex-direction: column;
    gap: 10px;
  }
  .search-input-group button {
    width: 100%;
    height: 46px;
    justify-content: center;
  }

  /* MOBILE KANBAN SWIPE WITH SNAP */
  .kanban-board {
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    gap: 12px;
    padding-bottom: 24px;
  }
  .kanban-col {
    flex: 0 0 85vw;
    max-width: 330px;
    scroll-snap-align: center;
  }

  /* CHAT WINDOW */
  .chat-window {
    height: 520px;
  }
  .chat-messages {
    padding: 16px 12px;
  }
  .chat-bubble {
    max-width: 90%;
    font-size: 0.88rem;
  }
  .chat-input-bar {
    padding: 12px 14px;
  }

  /* RESUME DROPZONE */
  .dropzone {
    padding: 28px 16px;
  }

  /* BOTTOM MOBILE DOCK */
  .mobile-dock {
    display: flex;
    height: calc(60px + env(safe-area-inset-bottom, 0px));
    padding-bottom: env(safe-area-inset-bottom, 0px);
    z-index: 1000;
  }

  /* MODALS ON MOBILE */
  .modal-backdrop {
    padding: 12px !important;
  }
  .modal-card {
    width: 100% !important;
    max-height: 88vh !important;
    padding: 20px 14px !important;
  }

  /* TOASTS ON MOBILE */
  #toast-box {
    left: 14px;
    right: 14px;
    bottom: calc(72px + env(safe-area-inset-bottom, 0px));
  }
  .toast-msg {
    width: 100%;
    font-size: 0.82rem;
    padding: 10px 14px;
  }

  /* PREVENT UNWANTED SAFARI AUTO-ZOOM ON FORM FOCUS */
  input, select, textarea {
    font-size: 16px !important;
  }
}

@media (max-width: 480px) {
  header.app-header {
    padding: 0 10px;
  }
  .status-pill {
    padding: 4px 8px;
  }
  #srv-text {
    display: none;
  }
  .header-avatar-btn span {
    display: none;
  }
  .cards-grid {
    grid-template-columns: 1fr;
  }
  .opp-card {
    padding: 16px 14px;
  }
  .opp-title {
    font-size: 1.05rem;
  }
}
"""
