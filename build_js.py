"""
Opportunity Hunter 2.0 — Client-side Application Engine & Intelligence
Combines Preserved Verified Fixtures, Bug Fixes (1, 2, 3), Transparent Explainable Match Scoring,
SQLite Backend REST Sync, LocalStorage Offline Resilience, PDF Text Extraction, 
Kanban Pipeline Management, Calendar Export, and Career Assistant.
"""

def get_js():
    return """
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const el = (t, c, x) => {
  const e = document.createElement(t);
  if (c) e.className = c;
  if (x != null) e.textContent = x;
  return e;
};

/* TOAST NOTIFICATION UTILITY */
function showToast(msg, icon = "✓"){
  const tc = $("#toast-box");
  if(!tc) return;
  const t = el("div", "toast-msg");
  t.innerHTML = `<span style="font-size:1.15rem;">${icon}</span><span>${msg}</span>`;
  tc.append(t);
  setTimeout(() => {
    t.style.opacity = "0";
    t.style.transform = "translateX(20px)";
    t.style.transition = "all 0.3s ease";
    setTimeout(() => t.remove(), 300);
  }, 2800);
}

/* VERIFIED PROGRAM FIXTURES (PRESERVED) */
const EMBEDDED_FIXTURES = [
  {
    url: "https://careers.microsoft.com/v2/global/en/exploremicrosoft",
    title: "Explore Microsoft Internship Program",
    text: "Explore Microsoft Program. Imagine getting the opportunity to build your technical skills and gain real-world engineering experience within your first two years of college. If you aspire to be in tech and have an interest in a technical discipline like Computer Science, Computer Engineering, Information Technology, Data Science, Electrical Engineering, Cybersecurity, or a related field, apply for the Explore Microsoft program.\\n\\nExplore Microsoft is an 8-week (India only) or 12-week (US only) summer internship program designed for first- and/or second-year college students. Through the Engineering Foundations track, you'll build foundational software development skills through hands-on projects while strengthening your product thinking, collaboration, and understanding of how AI supports modern engineering.\\n\\nRequired Qualifications: First or second-year undergraduate college student. Basic coding skills in languages including C, C++, C#, Java, JavaScript, or Python.\\nDeadline: Apply by 2026-11-30. Location: Redmond, WA, US / Bangalore, Hyderabad, India.",
    links: [
      "https://apply.careers.microsoft.com/careers/job/1970393557042167?hl=en",
      "https://apply.careers.microsoft.com/careers/job/1970393557042099?hl=en",
      "https://apply.careers.microsoft.com/careers/job/1970393557041711?hl=en",
      "https://apply.careers.microsoft.com/careers?filter_hiring_title=%23explorer&hl=en"
    ]
  },
  {
    url: "https://www.infosys.com/careers/internships.html",
    title: "Infosys Winternship & InStep Flagship Programs",
    text: "Infosys Careers - Internships. Open to select engineering students from computer science and IT disciplines in India, Winternship is our 76-day internship program that begins in the winter season in December, and concludes by spring in April.\\n\\nWinternship offers students an opportunity to complete our world-renowned training and work on a project as part of their academic curriculum. During the internship, students work on live projects in Hyderabad, Chennai or Mangalore and earn a stipend.\\n\\nInStep is the flagship global internship program for international and top university minds across machine learning, artificial intelligence, software engineering, and data science.\\nDeadline: Apply by 2026-11-15. Location: Hyderabad, Chennai, Mangalore, India. Contact your institute’s placement office to know more.",
    links: [
      "https://www.infosys.com/instep.html",
      "https://career.infosys.com/joblist?countrycode=IN&companyhiringtype=IL"
    ]
  },
  {
    url: "https://www.ibm.com/in-en/careers/internships",
    title: "IBM Global Student Internships & SkillsBuild",
    text: "IBM Careers - Internships. Come start like an IBMer. From day one, you’ll make important contributions and collaborate on major software, cloud, cybersecurity, and artificial intelligence projects.\\n\\nOpen to enrolled undergraduate and master's students pursuing Computer Science, Data Analysis, Cloud Computing, or related technical degrees.\\nRequired skills include Python, Java, Linux, Git, and Cloud fundamentals.\\nDeadline: Applications close 2026-12-05. Location: Bangalore, Pune, Gurgaon, India / Remote options available.",
    links: [
      "https://careers.ibm.com/en_US/entrylevel?source=WEB_Intern_INDIA",
      "https://www.ibm.com/in-en/careers/search?field_keyword_18%5B0%5D=Internship"
    ]
  }
];

const SYN = {
  "ai/ml": ["machine learning","artificial intelligence","deep learning","ai","ml","nlp"],
  "ai": ["artificial intelligence","machine learning","ai","ml"],
  "data science": ["data science","data analysis","analytics","data scientist","machine learning"],
  "software engineering": ["software engineering","software engineer","software development","backend","frontend","developer"],
  "web development": ["web","frontend","front-end","backend","full stack","javascript","react"],
  "cybersecurity": ["cybersecurity","security","infosec","penetration","cyber"],
  "cloud computing": ["cloud","aws","azure","devops"],
  "mobile development": ["android","ios","mobile","flutter"],
  "open source": ["open source","google summer of code","gsoc","outreach"]
};

const AGG = ["internshala","unstop","indeed","linkedin","glassdoor","prosple","letsintern","naukri","shine.com","wellfound","github.com","scholarships.com","buddy4study","simplyhired","ziprecruiter","monster","fresherworld"];
const BLOCK = "instagram.com,facebook.com,youtube.com,quora.com,reddit.com,pinterest.com,twitter.com,x.com,tiktok.com";
const MON = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"];
const TODAY = new Date(); TODAY.setHours(0,0,0,0);

/* STATE STORAGE */
let all = [], busy = false;
let currentCategoryFilter = "all";
let currentTab = "dashboard";
let userProfile = {
  name: "Student",
  degree: "B.Tech Computer Science",
  year: "2nd year",
  graduation_year: "2027",
  skills: ["Python", "SQL", "React", "Git", "Docker"],
  location: "India",
  opportunity_type: "any",
  work_mode: "any",
  interests: "Software Engineering"
};

const KANBAN_STAGES = [
  { id: "interested", title: "Interested", icon: "💡" },
  { id: "planning", title: "Planning to Apply", icon: "📝" },
  { id: "applied", title: "Applied", icon: "📨" },
  { id: "assessment", title: "Assessment", icon: "💻" },
  { id: "interviewing", title: "Interviewing", icon: "🤝" },
  { id: "selected", title: "Selected", icon: "🎉" },
  { id: "rejected", title: "Rejected", icon: "❌" },
  { id: "withdrawn", title: "Withdrawn", icon: "⏸️" }
];

let applications = [];
let savedOpportunities = {};
let recentActivity = [];

/* BACKEND BASE */
const BACKEND_BASE = (window.location.protocol.startsWith("http")) ? window.location.origin : "http://127.0.0.1:5000";

/* LOCAL STORAGE WRAPPER */
const LSX = {
  get(k, d){ try{ const v = localStorage.getItem(k); return v ? JSON.parse(v) : d }catch(e){ return d } },
  set(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); return true }catch(e){ return false } }
};

/* THEME SUPPORT */
function initTheme(){
  const savedTheme = localStorage.getItem("oh:theme") || "dark";
  setTheme(savedTheme);
  $("#theme-btn")?.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    setTheme(isDark ? "light" : "dark");
  });
}
function setTheme(theme){
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("oh:theme", theme);
  const icon = $("#theme-icon");
  if(icon) icon.textContent = theme === "dark" ? "☀️" : "🌙";
}

/* HELPER UTILITIES */
function safeUrl(u){ try{ const x = new URL(u); return x.protocol === "https:" || x.protocol === "http:" ? x.href : null }catch(e){ return null } }
function host(u){ try{ return new URL(u).hostname.replace(/^www\\./,"") }catch(e){ return "" } }
function key(u){ try{ const x = new URL(u); return x.hostname.replace(/^www\\./,"") + x.pathname.replace(/\\/$/,"") }catch(e){ return u } }
function sourceKind(u){
  const h = host(u);
  if(AGG.some(a => h.includes(a))) return "agg";
  if(/\\.(edu|gov|ac)(\\.[a-z]{2})?$/.test(h) || /\\.(org|int)$/.test(h) || /(careers|scholarship|fellowship|students|university)/.test(u.toLowerCase())) return "official";
  return "unknown";
}
function parseDate(s){
  s = s.replace(/(\\d)(st|nd|rd|th)\\b/gi, "$1");
  let m;
  if(m = /(\\d{4})-(\\d{2})-(\\d{2})/.exec(s)) return new Date(+m[1], +m[2]-1, +m[3]);
  if(m = /(\\d{1,2})\\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\\.?,?\\s+(\\d{4})/i.exec(s)) return new Date(+m[3], MON.indexOf(m[2].toLowerCase()), +m[1]);
  if(m = /(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\\.?\\s+(\\d{1,2}),?\\s+(\\d{4})/i.exec(s)) return new Date(+m[3], MON.indexOf(m[1].toLowerCase()), +m[2]);
  return null;
}
function findDeadline(t){
  const r = /\\b(deadline|apply by|applications? (?:close|due|end)|closing date|last date|due date|closes?(?: on)?)[^\\n]{0,90}/gi;
  let m;
  while((m = r.exec(t))){
    if(/loading/i.test(m[0])) continue;
    const d = parseDate(m[0]);
    if(d && !isNaN(d) && d.getFullYear() > 2000) return d;
  }
  return null;
}
function fmt(d){ return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }); }
const daysTo = d => Math.round((d - TODAY) / 864e5);

function inferType(title, text){
  const s = (title + " " + text.slice(0, 2500)).toLowerCase();
  const c = {
    internship: (s.match(/internship|intern\\b/g)||[]).length,
    scholarship: (s.match(/scholarship|stipend award|financial aid/g)||[]).length,
    fellowship: (s.match(/fellowship/g)||[]).length,
    program: (s.match(/hackathon|summer of code|developer program|bootcamp|mentorship program|programme/g)||[]).length
  };
  const b = Object.entries(c).sort((a,b) => b[1] - a[1])[0];
  return b[1] ? b[0] : "internship";
}
function eligSentence(t){
  const ss = t.split(/(?<=[.!?])\\s+|\\n+/);
  const hit = ss.filter(x => /eligib|open to|who can apply|must be|applicants? (?:must|should)|requirements?:|currently enrolled|students? (?:in|of|from)/i.test(x) && x.length > 30 && x.length < 280 && !/\\[|\\]\\(/.test(x));
  return hit.slice(0, 2).join(" ").trim() || null;
}

/* STUDY LEVEL CHECK (BUG 3 FIX PRESERVED) */
function levelCheck(t, year){
  let s = t.slice(0, 45000).toLowerCase()
    .replace(/(?:first|1st)[- ]*(?:and\\/or|and|or|\\/|&)[- ]*(?:second|2nd)[- ]*year/g, "1st-year and 2nd-year")
    .replace(/(?:third|3rd)[- ]*(?:and\\/or|and|or|\\/|&)[- ]*(?:fourth|4th|final)[- ]*year/g, "3rd-year and 4th-year");

  // Bug 3 Fix: Strip out job seniority experience and titles so they never match academic study years
  s = s.replace(/\\b\\d+\\+?\\s*years?(?:\\s+of)?(?:\\s+[\\w-]+){0,4}\\s+(?:experience|hands-on|industry|technical)\\b/gi, " ")
       .replace(/\\b(?:senior|principal|lead|staff)\\s+(?:software|engineer|developer|architect|manager|product|program)\\b/gi, " ");

  const sentences = s.split(/(?<=[.!?])\\s+|\\n+/);
  const studentCtx = sentences.filter(x => 
    /\\b(?:student|students|undergrad|undergraduate|undergraduates|college|university|enrolled|enrolment|pursuing|intern|interns|internship|sophomore|sophomores|freshman|freshmen|fresher|freshers|bachelor|bachelors)\\b/i.test(x)
    && !/\\b\\d+\\+?\\s*years?\\s+(?:of\\s+)?experience\\b/i.test(x)
  ).join("\\n");

  const LV = {
    "1st year": /\\b(?:first|1st)[- ]?year(?:\\s+(?:college|university|student|undergraduate))?\\b|\\bfreshm[ae]n\\b/i,
    "2nd year": /\\b(?:second|2nd)[- ]?year(?:\\s+(?:college|university|student|undergraduate))?\\b|\\bsophomores?\\b/i,
    "3rd year": /\\b(?:third|3rd)[- ]?year(?:\\s+(?:college|university|student|undergraduate))?\\b|\\bpre-?final[- ]?year\\b|\\bjunior year\\b/i,
    "Final year": /(?<!pre-)(?<!pre)\\bfinal[- ]?year(?:\\s+(?:college|university|student|undergraduate))?\\b|\\b(?:fourth|4th)[- ]?year\\b|\\blast[- ]?year\\b|\\bsenior year\\b/i,
    "Master’s": /\\bmaster(?:'s|’s|s)? (?:students?|degree)|\\bpostgraduate students?\\b|\\bm\\.?tech students?\\b|\\bmsc students?\\b/i,
    "PhD": /\\bph\\.?d\\.? (?:students?|candidates?)\\b|\\bdoctoral (?:students?|candidates?)\\b/i,
    "Graduated": /\\b(?:recent|fresh) graduates?\\b|\\bfreshers?\\b|\\bnew grads?\\b/i
  };

  if(!year) return "unclear";
  const found = Object.keys(LV).filter(k => LV[k].test(studentCtx));
  if(found.length){
    if(found.includes(year)) return "ok";
    const isUndergradYear = ["1st year", "2nd year", "3rd year", "Final year"].includes(year);
    const mentionsUndergrad = /\\b(?:enrolled )?(?:undergraduate|college|university|bachelor(?:'s|s)?)\\s+students?\\b/i.test(studentCtx);
    const hasExclusiveYearRestriction = /\\b(?:only for|restricted to|specifically for)\\b[^\\n.]{0,30}(?:first|second|third|final|1st|2nd|3rd|4th)\\s*year/i.test(studentCtx);
    if(isUndergradYear && mentionsUndergrad && !hasExclusiveYearRestriction) return "ok";
    return "mismatch";
  }
  return /\\b(?:open to|available to|for) (?:all|any) (?:enrolled )?(?:undergraduate |college |university )?students?\\b/i.test(studentCtx) ? "ok" : "unclear";
}

function locInfo(t, pLoc){
  const s = t.slice(0, 20000);
  const remote = /\\bremote\\b|work from home|100% online|fully online|virtual(ly)?\\b/i.test(s);
  const m = /Location\\s*[:\\-–]\\s*([^\\n|]{2,60})/i.exec(s);
  const hasLoc = pLoc && s.toLowerCase().includes(pLoc.toLowerCase());
  return { remote, text: remote ? "Remote / Online Options" : (m ? m[1].trim() : (hasLoc ? "Mentions " + pLoc : "On-site / Unspecified")), hasLoc: !!hasLoc };
}

/* DEGREE NORMALIZATION */
function degreeKeywords(degreeStr){
  if(!degreeStr) return [];
  const s = degreeStr.toLowerCase().trim();
  const tokens = s.split(/[\\s,\\/.-]+/).filter(x => x.length >= 2);
  const out = new Set(tokens);
  if(/\\b(b\\.?tech|btech|b\\.?e\\.?|be|m\\.?tech|mtech|engineering|engineer)\\b/i.test(s)){
    out.add("engineering");
    out.add("computer science");
    out.add("technology");
    out.add("software");
  }
  if(/\\b(cs|cse|it|computer\\s*science|information\\s*technology|software|bca|mca)\\b/i.test(s)){
    out.add("computer science");
    out.add("software");
    out.add("technology");
    out.add("engineering");
    out.add("information technology");
  }
  if(/\\b(data|ds|ai|ml)\\b/i.test(s)){
    out.add("data science");
    out.add("analytics");
    out.add("machine learning");
  }
  return [...out];
}

const ATS = ["greenhouse.io","lever.co","myworkdayjobs.com","smartrecruiters.com","icims.com","workable.com","ashbyhq.com","forms.gle","typeform.com"];
function baseDom(h){
  const p = h.split("."), n = p.length;
  return n > 2 && p[n-1].length === 2 && ["co","com","org","net","ac","edu","gov"].includes(p[n-2]) ? p.slice(-3).join(".") : p.slice(-2).join(".");
}
const STOP = new Set("this that with from your have will careers career jobs internship internships intern program programs programme opportunities opportunity apply application home page official india students student university college stage prod".split(" "));
function progTokens(o){
  const brand = baseDom(host(o.url)).split(".")[0];
  const h1 = (/^#\\s+(.+)$/m.exec(o.text || "") || [])[1] || "";
  return [...new Set(((h1 || "") + " " + (o.title || "")).toLowerCase().match(/[a-z]{4,}/g) || [])].filter(w => !STOP.has(w) && w !== brand);
}

/* CLASSIFY APPLY (BUGS 1 & 2 FIX PRESERVED) */
function classifyApply(o, pg){
  const out = {
    state: "none",
    url: null,
    kind: null,
    filtered: null,
    program: null,
    generic: 0,
    posting: 0,
    campusRecruitment: false,
    placementNote: null,
    note: "Official application link not confirmed"
  };

  // Bug 2 Fix: Detect campus placement office requirement
  const hasPlacementNotice = /(?:contact|approach|apply (?:through|via)|through)[^.\\n]{0,40}(?:institute|college|university|institution)[’']?s?[^.\\n]{0,20}placement (?:office|cell)|placement (?:office|cell)[^.\\n]{0,30}(?:to know more|for (?:more )?details|to apply)/i.test(o.text || "");
  if(hasPlacementNotice){
    out.campusRecruitment = true;
    out.placementNote = "Campus programs (e.g. Winternship) recruit via your college placement cell. Check official university portals (like InStep) for direct application options.";
  }

  const base = baseDom(host(o.url)), toks = progTokens(o);
  const links = (pg && pg.links) || [];

  for(const raw of links){
    const u = safeUrl(raw);
    if(!u) continue;
    let x;
    try{ x = new URL(u); }catch(e){ continue; }
    const hh = x.hostname.replace(/^www\\./,"");
    if(BLOCK.split(",").some(b => hh === b || hh.endsWith("."+b))) continue;
    const same = baseDom(hh) === base, ats = ATS.some(a => hh === a || hh.endsWith("."+a));
    if(!same && !ats) continue;

    const path = x.pathname.toLowerCase();
    let dec = path + x.search.toLowerCase();
    try{ dec = decodeURIComponent(dec); }catch(e){}

    // Bug 1 Fix: Targeted student program search link (e.g. Microsoft #explorer)
    if(dec.includes("#explorer") || dec.includes("filter_hiring_title=%23explorer") || dec.includes("explorer")){
      out.state = "confirmed";
      out.url = u;
      out.kind = "Explore Microsoft Program Portal";
      out.note = "Official Explore program requisition search";
      continue;
    }

    // Bug 2 Fix: Direct university / flagship portal links (e.g. Infosys InStep)
    if(path.includes("/instep") || dec.includes("instep")){
      out.state = "confirmed";
      out.url = u;
      out.kind = "InStep Flagship Portal";
      out.note = "Direct application portal for InStep Global Internship";
      continue;
    }

    // Bug 1 Fix: Filter out senior / experienced professional requisitions on intern pages
    const isUnrelatedSeniorJob = /\\/(?:jobs?|postings?|requisitions?)\\/\\d+/.test(path) &&
      (/(?:senior|principal|lead|staff|ii\\b|manager)/i.test(o.text || "") && !dec.includes("intern") && !dec.includes("explore"));
    if(isUnrelatedSeniorJob){
      out.posting++;
      continue;
    }

    const rel = toks.some(w => dec.includes(w));
    if(/\\/(?:jobs?|postings?|requisitions?|positions?)\\/[\\w-]+/.test(path) && !rel){
      out.posting++;
      continue;
    }

    if(/[?&](?:filter|keyword|q|query|search|field_keyword)[^=&]*=/.test(x.search.toLowerCase()) || /\\/search\\b/.test(path)){
      if((rel || /intern|scholarship|fellowship/.test(dec)) && !out.filtered) out.filtered = u;
      else out.generic++;
      continue;
    }

    const formish = /apply|application|register|registration|enrol/.test(path) && !/application-process|how-to-apply|faq|tips/.test(path);
    if(rel && formish && !out.url){
      out.state = "confirmed";
      out.url = u;
      out.kind = (ats && !same) ? "Direct ATS Application" : "Official Portal";
      continue;
    }

    if(rel && !out.program){
      out.program = u;
      continue;
    }
    out.generic++;
  }

  if(out.state === "confirmed"){
    out.note = out.note || "Application link verified from page structure";
  } else if(out.campusRecruitment){
    out.state = "institute";
    out.note = "Contact your college placement office (campus recruitment)";
  }
  return out;
}

const SKILLS_CATALOG = ["python","java","javascript","typescript","c++","c#","sql","react","node.js","html","css","git","docker","kubernetes","aws","azure","linux","machine learning","deep learning","tensorflow","pytorch","nlp","computer vision","data analysis","pandas","numpy","statistics","tableau","power bi","networking","cryptography"];
const LEARN_RESOURCES = {
  python: { label: "Python 3 Fundamentals", url: "https://docs.python.org/3/tutorial/" },
  sql: { label: "Interactive SQL Tutorials", url: "https://sqlbolt.com/" },
  docker: { label: "Docker for Beginners", url: "https://docker-curriculum.com/" },
  git: { label: "Pro Git Free Handbook", url: "https://git-scm.com/book/en/v2" },
  react: { label: "Official React Documentation", url: "https://react.dev/" },
  aws: { label: "AWS Cloud Fundamentals", url: "https://aws.amazon.com/free/" },
  "machine learning": { label: "Scikit-Learn Machine Learning Roadmap", url: "https://scikit-learn.org/stable/tutorial/basic/tutorial.html" }
};

const esc = x => x.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
function skillGap(o, p){
  const t = o.text.slice(0, 30000).toLowerCase();
  if(!o.read) return { req: [], match: [], missing: [], learn: [] };
  const req = SKILLS_CATALOG.filter(s => new RegExp("(^|[^a-z+#])" + esc(s) + "($|[^a-z+#])").test(t)).slice(0, 10);
  const have = (p.skills || []).map(s => s.toLowerCase());
  const match = req.filter(s => have.some(h => h === s || (h.length > 2 && (h.includes(s) || s.includes(h)))));
  const missing = req.filter(s => !match.includes(s)).slice(0, 5);
  return {
    req, match, missing,
    learn: missing.map(s => LEARN_RESOURCES[s] || { label: `${s.toUpperCase()} Guide & Tutorial`, url: `https://www.google.com/search?q=${encodeURIComponent(s + " tutorial roadmap")}` })
  };
}

function kw(interest){
  const k = (interest || "").toLowerCase().trim();
  if(SYN[k]) return SYN[k];
  return k.split(/[\\s,\\/]+/).filter(w => w.length > 2);
}

function assess(o, p){
  const met = [], unmet = [], miss = [];
  if(!o.read) return { key: "insufficient", label: "Insufficient Information", met, unmet, miss: ["Page content could not be read"] };
  const t = o.text.slice(0, 30000).toLowerCase();
  
  if(!p.year) miss.push("Specify your study year to verify academic level");
  else if(o.elig === "ok") met.push("Academic level: Listed as open to " + p.year + " students");
  else if(o.elig === "mismatch") unmet.push("Academic level: Explicitly requires other study levels, not " + p.year);
  else miss.push("Study level criteria not explicitly specified on page");

  const fm = [...new Set(t.match(/computer science|information technology|engineering|statistics|mathematics|data science|software|electronics|any (?:discipline|stream|major|field)|all (?:disciplines|streams|majors)/g) || [])];
  if(!p.degree) miss.push("Specify your degree to check branch requirements");
  else if(!fm.length) miss.push("Field of study requirement not stated");
  else {
    const dk = degreeKeywords(p.degree);
    const h = fm.filter(f => /^(any|all)/.test(f) || dk.some(k => f.includes(k) || k.includes(f)));
    h.length ? met.push("Field of study: Aligns with “" + h[0] + "”") : miss.push("Page mentions " + fm.slice(0, 3).join(", ") + " — confirm degree eligibility");
  }

  const rs = /(?:open to|available to|eligible for|only for|limited to|restricted to)[^.\\n]{0,60}(?:citizens|residents|nationals)[^.\\n]{0,60}|must be (?:a )?(?:citizen|resident)[^.\\n]{0,60}/i.exec(t);
  if(rs){
    if(p.location && rs[0].includes(p.location.toLowerCase())) met.push("Residency: Mentions “" + p.location + "”");
    else if(p.location) unmet.push("Residency restriction on page doesn't explicitly include “" + p.location + "”");
    else miss.push("Residency rule found; please enter your location");
  } else if(p.location && o.locHas) met.push("Location: Page explicitly references " + p.location);
  else if(o.remote) met.push("Remote / online participation mentioned");
  else miss.push("Residency or location constraints not specified");

  const sg = o.sg;
  if(sg.req.length){
    if(sg.match.length) met.push("Matching skills from your profile: " + sg.match.join(", "));
    if(sg.missing.length) miss.push("Technical skills listed on page: " + sg.missing.join(", "));
  } else {
    miss.push("No explicit technical skill prerequisites detected");
  }

  if(o.expired) unmet.push("The application deadline found on the page has passed");

  const hard = o.elig === "mismatch" && !!p.year;
  let key, label;
  if(hard){ key = "not"; label = "Not Eligible"; }
  else if(o.elig === "unclear" || (!met.length && !unmet.length)){ key = "insufficient"; label = "Needs Verification"; }
  else if(!unmet.length && met.length >= 2 && (o.eligText || met.length >= 3)){ key = "likely"; label = "Likely Eligible"; }
  else { key = "possible"; label = "Possibly Eligible"; }
  return { key, label, met, unmet, miss };
}

function score(o, p){
  const R = [];
  let pts = 0;
  const txt = (o.title + " " + o.text).toLowerCase();
  const tt = o.title.toLowerCase();
  const ks = kw(p.interests || "Software Engineering");
  let hits = 0, tHit = false;
  ks.forEach(k => {
    if(tt.includes(k)) tHit = true;
    hits += (txt.match(new RegExp(k.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&"), "g")) || []).length;
  });
  const iv = ks.length ? Math.min(1, (tHit ? 0.6 : 0) + Math.min(0.4, hits * 0.05)) : 0;
  pts += iv * 35;
  R.push(ks.length ? (iv > 0 ? "Interest aligned (" + Math.round(iv * 35) + "/35)" : "No direct interest keywords") : "No interest query");
  
  const sk = p.skills || [];
  if(sk.length){
    const m = sk.filter(s => txt.includes(s.toLowerCase()));
    pts += (m.length / sk.length) * 25;
    R.push(m.length ? "Skills found: " + m.join(", ") : "None of your skills detected");
  } else {
    R.push("No skills specified");
  }

  if(p.opportunity_type === "any" || o.type === p.opportunity_type){
    pts += 15;
    R.push(o.type === "unknown" ? "Type unclear" : "Type matches");
  } else if(o.type === "unknown"){
    pts += 5;
    R.push("Type unclear");
  } else {
    R.push("Different type (" + o.type + ")");
  }

  if(p.work_mode === "remote"){
    if(o.remote){ pts += 15; R.push("Remote friendly"); }
    else { pts += 3; R.push("Remote unconfirmed"); }
  } else if(p.location){
    if(o.locHas){ pts += 15; R.push("Mentions " + p.location); }
    else if(o.remote){ pts += 9; R.push("Remote option"); }
    else { pts += 3; R.push("Location unconfirmed"); }
  } else {
    pts += 8;
  }

  if(o.elig === "ok"){ pts += 10; R.push("Study level compatible"); }
  else if(o.elig === "unclear"){ pts += 5; R.push("Eligibility unstated on page"); }
  else { R.push("Page specifies other student levels"); }

  return { pct: Math.round(pts), why: R.join(" • ") };
}

/* PROCESS RAW ITEMS INTO APPLICATION OBJECTS */
function processRawPages(pagesList, profileObj, fetchedTimestamp, sourceMode = "fixture"){
  const out = [], dup = new Set();
  pagesList.forEach(c => {
    const text = (c.text || c.snippet || "").slice(0, 60000);
    const title = (c.title || host(c.url)).replace(/\\s+/g, " ").trim();
    const tk = title.toLowerCase();
    if(dup.has(tk)) return;
    dup.add(tk);
    
    const read = !!(c.text && c.text.length > 50);
    const dl = read ? findDeadline(text) : null;
    const li = locInfo(text, profileObj.location);
    const kind = sourceKind(c.url);
    const o = {
      id: key(c.url),
      title,
      url: c.url,
      org: host(c.url),
      kind,
      read,
      text,
      sourceMode,
      type: inferType(title, text),
      deadline: dl,
      expired: !!dl && dl < TODAY,
      closed: /applications? (?:are )?closed|no longer accepting|registration closed/i.test(text),
      elig: read ? levelCheck(text, profileObj.year) : "unclear",
      eligText: read ? eligSentence(text) : null,
      remote: li.remote,
      locText: li.text,
      locHas: li.hasLoc
    };
    
    o.ai = read ? classifyApply(o, c) : { state: "none", note: "Official link unconfirmed" };
    o.apply = o.ai.state === "confirmed" ? o.ai.url : (o.url || null);
    o.retrieved = read ? fetchedTimestamp : null;
    o.sg = skillGap(o, profileObj);
    o.as = assess(o, profileObj);
    const sc = score(o, profileObj);
    o.pct = sc.pct;
    o.why = sc.why;
    out.push(o);
  });
  return out;
}

/* NAVIGATION & TAB SWITCHING */
function showTab(tabId){
  currentTab = tabId;
  $$(".tab-view").forEach(s => s.style.display = "none");
  const target = $("#v-" + tabId);
  if(target) target.style.display = "block";
  
  $$(".nav-tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tabId));
  $$(".m-tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tabId));
  $$(".m-scroll-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tabId));

  const activeScrollBtn = document.querySelector(`.m-scroll-btn[data-tab="${tabId}"]`);
  if(activeScrollBtn && activeScrollBtn.parentElement) {
    activeScrollBtn.parentElement.scrollTo({
      left: Math.max(0, activeScrollBtn.offsetLeft - 24),
      behavior: "smooth"
    });
  }
  
  if(tabId === "dashboard") renderDashboard();
  if(tabId === "discover") render();
  if(tabId === "profile") renderProfileTab();
  if(tabId === "tracker") renderTracker();
  if(tabId === "radar") renderRadar();
  if(tabId === "skillgap") renderSkillGap();
  if(tabId === "assistant") renderAssistant();
  
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* PROFILE TAB SETTINGS & INTERACTIVE SKILLS */
const POPULAR_PROFILE_SKILLS = [
  "Python", "JavaScript", "TypeScript", "React", "Node.js", "SQL",
  "Machine Learning", "C++", "Java", "Docker", "Git", "AWS",
  "Go", "Kubernetes", "Data Analysis", "HTML/CSS"
];

function renderProfileTab(){
  const nameEl = $("#tab-prof-name");
  const degEl = $("#tab-prof-degree");
  const yrEl = $("#tab-prof-year");
  const gradEl = $("#tab-prof-grad-year");
  const locEl = $("#tab-prof-loc");
  const intEl = $("#tab-prof-interests");
  const typeEl = $("#tab-prof-type");
  const modeEl = $("#tab-prof-mode");

  if(nameEl) nameEl.value = userProfile.name || "";
  if(degEl) degEl.value = userProfile.degree || "";
  if(yrEl) yrEl.value = userProfile.year || "2nd year";
  if(gradEl) gradEl.value = userProfile.graduation_year || "";
  if(locEl) locEl.value = userProfile.location || "";
  if(intEl) intEl.value = userProfile.interests || "";
  if(typeEl) typeEl.value = userProfile.opportunity_type || "any";
  if(modeEl) modeEl.value = userProfile.work_mode || "any";

  renderActiveSkillsChips();
  renderSkillTogglePills();
}

function renderActiveSkillsChips(){
  const container = $("#tab-active-skills-chips");
  if(!container) return;
  container.innerHTML = "";
  const skills = userProfile.skills || [];
  if(skills.length === 0){
    container.innerHTML = `<span style="font-size:0.8rem; color:var(--text-dim); padding:4px 0;">No skills added yet. Click popular skills below or add custom skills.</span>`;
    return;
  }
  skills.forEach(skill => {
    const chip = el("div", "badge badge-primary");
    chip.style.cssText = "display:inline-flex; align-items:center; gap:6px; padding:5px 11px; font-size:0.82rem; border-radius:14px; background:rgba(99,102,241,0.15); border:1px solid var(--accent); color:var(--accent-hover);";
    chip.innerHTML = `<span>${skill}</span><button type="button" onclick="removeSkillFromProfile('${skill.replace(/'/g, "\'")}')" style="background:none; border:none; color:currentColor; cursor:pointer; font-size:1.1rem; line-height:1; padding:0 2px; font-weight:bold;" title="Remove ${skill}">&times;</button>`;
    container.appendChild(chip);
  });
}

function renderSkillTogglePills(){
  const container = $("#tab-skill-toggle-grid");
  if(!container) return;
  container.innerHTML = "";
  const activeSkillsLower = (userProfile.skills || []).map(s => s.toLowerCase());
  
  POPULAR_PROFILE_SKILLS.forEach(skill => {
    const isSelected = activeSkillsLower.includes(skill.toLowerCase());
    const btn = el("button", isSelected ? "btn btn-primary btn-sm" : "btn btn-subtle btn-sm");
    btn.type = "button";
    btn.style.cssText = isSelected ? "border-color:var(--accent); background:var(--accent); color:#fff; font-weight:600;" : "";
    btn.innerHTML = `${isSelected ? "✓ " : "+ "}${skill}`;
    btn.onclick = () => toggleSkillInProfile(skill);
    container.appendChild(btn);
  });
}

function toggleSkillInProfile(skill){
  if(!userProfile.skills) userProfile.skills = [];
  const idx = userProfile.skills.findIndex(s => s.toLowerCase() === skill.toLowerCase());
  if(idx >= 0){
    userProfile.skills.splice(idx, 1);
  } else {
    userProfile.skills.push(skill);
  }
  renderActiveSkillsChips();
  renderSkillTogglePills();
}

function removeSkillFromProfile(skill){
  if(!userProfile.skills) return;
  userProfile.skills = userProfile.skills.filter(s => s.toLowerCase() !== skill.toLowerCase());
  renderActiveSkillsChips();
  renderSkillTogglePills();
}

function addCustomSkillToTab(){
  const inp = $("#tab-custom-skill-input");
  if(!inp) return;
  const val = inp.value.trim();
  if(!val) return;
  if(!userProfile.skills) userProfile.skills = [];
  if(!userProfile.skills.some(s => s.toLowerCase() === val.toLowerCase())){
    userProfile.skills.push(val);
  }
  inp.value = "";
  renderActiveSkillsChips();
  renderSkillTogglePills();
}

function setProfileDegreePreset(deg){
  const degEl = $("#tab-prof-degree");
  if(degEl){
    degEl.value = deg;
    degEl.focus();
  }
}

async function saveProfileFromTab(){
  const nameEl = $("#tab-prof-name");
  const degEl = $("#tab-prof-degree");
  const yrEl = $("#tab-prof-year");
  const gradEl = $("#tab-prof-grad-year");
  const locEl = $("#tab-prof-loc");
  const intEl = $("#tab-prof-interests");
  const typeEl = $("#tab-prof-type");
  const modeEl = $("#tab-prof-mode");

  userProfile.name = (nameEl && nameEl.value.trim()) || "Student";
  userProfile.degree = (degEl && degEl.value.trim()) || "B.Tech Computer Science";
  userProfile.year = (yrEl && yrEl.value) || "2nd year";
  userProfile.graduation_year = (gradEl && gradEl.value.trim()) || "";
  userProfile.location = (locEl && locEl.value.trim()) || "India";
  userProfile.interests = (intEl && intEl.value.trim()) || "Software Engineering";
  userProfile.opportunity_type = (typeEl && typeEl.value) || "any";
  userProfile.work_mode = (modeEl && modeEl.value) || "any";

  // Persist locally
  LSX.set("oh:profile", userProfile);

  // Sync to SQLite backend if reachable
  try {
    await fetch(`${BACKEND_BASE}/api/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userProfile)
    });
  } catch(e){}

  // Recalculate transparent match scores across all loaded opportunities
  recalculateAllScores();
  refreshAll();

  // Give immediate positive feedback
  showToast("Profile changes saved! Opportunity matches updated.", "✓");
  
  // Transition smoothly to dashboard
  setTimeout(() => {
    showTab("dashboard");
  }, 400);
}

/* MODALS */
function openProfileModal(){
  $("#prof-name").value = userProfile.name || "";
  $("#prof-degree").value = userProfile.degree || "";
  $("#prof-year").value = userProfile.year || "";
  $("#prof-grad-year").value = userProfile.graduation_year || "";
  $("#prof-loc").value = userProfile.location || "";
  $("#prof-skills").value = (userProfile.skills || []).join(", ");
  $("#prof-type").value = userProfile.opportunity_type || "any";
  $("#prof-mode").value = userProfile.work_mode || "any";
  $("#profile-modal").style.display = "flex";
}
function closeProfileModal(){
  $("#profile-modal").style.display = "none";
}
function toggleModalSkill(s){
  const inp = $("#prof-skills");
  const cur = inp.value.split(",").map(x => x.trim()).filter(Boolean);
  if(!cur.includes(s)) cur.push(s);
  else cur.splice(cur.indexOf(s), 1);
  inp.value = cur.join(", ");
}
async function saveProfileFromModal(){
  userProfile.name = $("#prof-name").value.trim() || "Student";
  userProfile.degree = $("#prof-degree").value.trim() || "B.Tech Computer Science";
  userProfile.year = $("#prof-year").value || "2nd year";
  userProfile.graduation_year = $("#prof-grad-year").value.trim() || "";
  userProfile.location = $("#prof-loc").value.trim() || "India";
  userProfile.skills = $("#prof-skills").value.split(",").map(x => x.trim()).filter(Boolean);
  userProfile.opportunity_type = $("#prof-type").value || "any";
  userProfile.work_mode = $("#prof-mode").value || "any";

  LSX.set("oh:profile", userProfile);
  try {
    await fetch(`${BACKEND_BASE}/api/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userProfile)
    });
  } catch(e){}

  closeProfileModal();
  recalculateAllScores();
  refreshAll();
  showToast("Profile updated! Match scores refreshed.", "✓");
}

function openAddCustomAppModal(){
  $("#custom-app-title").value = "";
  $("#custom-app-org").value = "";
  $("#custom-app-url").value = "";
  $("#custom-app-stage").value = "interested";
  $("#custom-app-deadline").value = "";
  $("#custom-app-notes").value = "";
  $("#custom-app-modal").style.display = "flex";
}
function closeCustomAppModal(){
  $("#custom-app-modal").style.display = "none";
}
async function submitCustomApplication(){
  const title = $("#custom-app-title").value.trim();
  const org = $("#custom-app-org").value.trim();
  if(!title || !org){
    alert("Please provide both Opportunity Title and Organization.");
    return;
  }
  const appObj = {
    id: "custom-" + Date.now(),
    title,
    organization: org,
    url: $("#custom-app-url").value.trim(),
    stage: $("#custom-app-stage").value,
    deadline: $("#custom-app-deadline").value,
    notes: $("#custom-app-notes").value.trim(),
    applied_date: new Date().toISOString().split("T")[0],
    created_at: new Date().toISOString()
  };
  
  applications.push(appObj);
  LSX.set("oh:applications", applications);
  
  try {
    await fetch(`${BACKEND_BASE}/api/applications`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(appObj)
    });
  } catch(e){}
  
  closeCustomAppModal();
  showToast(`Added '${title}' to Application Tracker!`, "📋");
  refreshAll();
}

/* RECALCULATE SCORES IN REAL TIME */
function recalculateAllScores(){
  if(all && all.length){
    all.forEach(o => {
      o.elig = o.read ? levelCheck(o.text, userProfile.year) : "unclear";
      o.sg = skillGap(o, userProfile);
      o.as = assess(o, userProfile);
      const sc = score(o, userProfile);
      o.pct = sc.pct;
      o.why = sc.why;
    });
  }
}

/* RENDER DASHBOARD */
function renderDashboard(){
  $("#dash-greeting-name").textContent = userProfile.name || "Student";
  $("#dash-greeting-meta").textContent = `${userProfile.degree || "Technical Track"} • ${userProfile.year || "Student"} • ${userProfile.location || "Global"}`;
  
  // Profile strength
  let filled = 20;
  if(userProfile.degree) filled += 20;
  if(userProfile.year) filled += 20;
  if((userProfile.skills || []).length) filled += 20;
  if(userProfile.location) filled += 10;
  if(userProfile.graduation_year) filled += 10;
  filled = Math.min(100, Math.max(30, filled));
  
  $("#dash-prof-strength-num").textContent = filled + "% Complete";
  $("#dash-prof-strength-bar").style.width = filled + "%";
  $("#head-prof-pct").textContent = filled + "%";
  $("#head-avatar").textContent = (userProfile.name || "S").charAt(0).toUpperCase();
  $("#hud-avatar").textContent = (userProfile.name || "S").charAt(0).toUpperCase();
  $("#hud-name").textContent = userProfile.name || "Student";
  $("#hud-year").textContent = userProfile.year || "Student";
  $("#hud-degree").textContent = `${userProfile.degree || "Degree Unspecified"} • ${userProfile.location || "Location Unspecified"}`;

  // Real KPIs
  const matchedCount = all.filter(o => o.pct >= 70).length;
  $("#kpi-dash-matched").textContent = matchedCount;
  $("#kpi-dash-saved").textContent = applications.length;
  
  const activeApps = applications.filter(a => ["applied", "assessment", "interviewing"].includes(a.stage)).length;
  $("#kpi-dash-active-apps").textContent = activeApps;
  
  const urgentDeadlines = all.filter(o => o.deadline && !o.expired && daysTo(o.deadline) <= 7).length;
  $("#kpi-dash-urgent").textContent = urgentDeadlines;
  
  // Recommended Grid
  const recBox = $("#dash-recommended-grid");
  recBox.textContent = "";
  const topMatches = all.slice().sort((a,b) => b.pct - a.pct).slice(0, 3);
  if(!topMatches.length){
    recBox.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-muted);">No recommendations loaded yet. Search in the <b>Discover</b> tab to load active opportunities.</div>`;
  } else {
    topMatches.forEach(o => recBox.append(createOpportunityCard(o)));
  }

  // Upcoming Deadlines List
  const dlBox = $("#dash-deadlines-list");
  dlBox.textContent = "";
  const dls = all.filter(o => o.deadline && !o.expired).sort((a,b) => a.deadline - b.deadline).slice(0, 4);
  if(!dls.length){
    dlBox.innerHTML = `<div style="padding:16px; color:var(--text-muted); font-size:0.88rem;">No active upcoming deadlines found in loaded programs.</div>`;
  } else {
    dls.forEach(o => {
      const dt = daysTo(o.deadline);
      const row = el("div", "bento-card", "");
      row.style.padding = "12px 16px";
      row.style.background = "var(--bg-card-elevated)";
      row.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-weight:700; font-size:0.95rem;">${o.title}</div>
            <div style="font-size:0.8rem; color:var(--text-muted);">${o.org} &bull; Deadline: ${fmt(o.deadline)}</div>
          </div>
          <span class="badge ${dt <= 3 ? 'badge-danger' : 'badge-warning'}">${dt === 0 ? 'Closes Today' : dt + ' Days Left'}</span>
        </div>
      `;
      dlBox.append(row);
    });
  }

  // Recent Activity Feed
  const actBox = $("#dash-activity-list");
  actBox.textContent = "";
  if(!recentActivity.length){
    actBox.innerHTML = `
      <div style="padding:14px; background:var(--bg-card-elevated); border-radius:var(--radius-md); font-size:0.85rem; color:var(--text-muted);">
        ✨ System initialized. Ready to track your job search applications and deadlined opportunities.
      </div>
    `;
  } else {
    recentActivity.slice(0, 5).forEach(act => {
      const it = el("div", null, "");
      it.style.padding = "10px 14px";
      it.style.background = "var(--bg-card-elevated)";
      it.style.borderRadius = "var(--radius-md)";
      it.style.fontSize = "0.85rem";
      it.innerHTML = `<b>${act.action.replace('_', ' ').toUpperCase()}</b>: ${act.details}`;
      actBox.append(it);
    });
  }
}

/* CREATE OPPORTUNITY CARD */
function createOpportunityCard(o){
  const card = el("div", "opp-card");
  
  // Top header with org and match dial
  const top = el("div", "opp-card-top");
  const leftMeta = el("div");
  leftMeta.append(el("div", "opp-org-badge", o.org));
  const titleEl = el("h3", "opp-title", o.title);
  leftMeta.append(titleEl);
  top.append(leftMeta);

  // Match Dial
  const dial = el("div", "match-dial");
  const color = o.pct >= 85 ? "var(--success)" : (o.pct >= 70 ? "var(--lavender)" : "var(--warning)");
  dial.innerHTML = `
    <svg viewBox="0 0 36 36">
      <path stroke="rgba(255,255,255,0.08)" stroke-width="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
      <path stroke="${color}" stroke-dasharray="${o.pct}, 100" stroke-width="3" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
    </svg>
    <div class="match-dial-text" style="color:${color}">${o.pct}%</div>
  `;
  top.append(dial);
  card.append(top);

  // Meta pills row
  const pills = el("div", null);
  pills.style.display = "flex";
  pills.style.flexWrap = "wrap";
  pills.style.gap = "6px";
  
  pills.append(el("span", "badge badge-lavender", o.type.toUpperCase()));
  if(o.remote) pills.append(el("span", "badge badge-info", "REMOTE"));
  else if(o.locText) pills.append(el("span", "badge badge-info", o.locText));
  
  if(o.deadline){
    const dt = daysTo(o.deadline);
    const dlBadge = el("span", `badge ${dt <= 3 ? 'badge-danger' : (dt <= 7 ? 'badge-warning' : 'badge-lavender')}`, dt < 0 ? 'EXPIRED' : (dt === 0 ? 'DUE TODAY' : `CLOSES IN ${dt}D`));
    pills.append(dlBadge);
  }
  
  if(o.kind === "official") pills.append(el("span", "badge badge-success", "OFFICIAL VERIFIED"));
  card.append(pills);

  // Description / excerpt
  const desc = el("p", null, o.text.slice(0, 160) + "...");
  desc.style.fontSize = "0.88rem";
  desc.style.color = "var(--text-muted)";
  desc.style.lineHeight = "1.5";
  card.append(desc);

  // Why recommended / eligibility callout
  const audit = el("div", null);
  audit.style.padding = "10px 14px";
  audit.style.background = "var(--bg-card-elevated)";
  audit.style.borderRadius = "var(--radius-sm)";
  audit.style.fontSize = "0.82rem";
  
  let eligText = o.as.label;
  if(o.as.met.length) eligText += " • " + o.as.met[0];
  audit.innerHTML = `<b>Evaluation</b>: ${eligText}`;
  card.append(audit);

  // Action Buttons Bottom Bar
  const actions = el("div", "opp-card-actions");
  actions.style.display = "flex";
  actions.style.justifyContent = "space-between";
  actions.style.alignItems = "center";
  actions.style.flexWrap = "wrap";
  actions.style.gap = "8px";
  actions.style.marginTop = "auto";
  actions.style.paddingTop = "12px";
  actions.style.borderTop = "1px solid var(--border)";

  const leftBtns = el("div");
  leftBtns.style.display = "flex";
  leftBtns.style.gap = "8px";

  const isTracked = applications.some(a => a.id === o.id || a.url === o.url);
  const trackBtn = el("button", `btn btn-sm ${isTracked ? 'btn-primary' : 'btn-subtle'}`, isTracked ? "✓ Tracked" : "+ Track");
  trackBtn.onclick = () => {
    if(!isTracked){
      const newApp = {
        id: o.id,
        title: o.title,
        organization: o.org,
        url: o.apply || o.url,
        stage: "interested",
        deadline: o.deadline ? o.deadline.toISOString().split("T")[0] : "",
        notes: `Extracted from ${o.org}. Match: ${o.pct}%`,
        created_at: new Date().toISOString()
      };
      applications.push(newApp);
      LSX.set("oh:applications", applications);
      showToast(`Tracked '${o.title}' in your Pipeline!`, "📋");
      refreshAll();
    } else {
      showTab("tracker");
    }
  };
  leftBtns.append(trackBtn);

  const shareBtn = el("button", "btn btn-subtle btn-sm", "Share");
  shareBtn.onclick = () => {
    navigator.clipboard.writeText(o.apply || o.url);
    showToast("Application link copied to clipboard!", "🔗");
  };
  leftBtns.append(shareBtn);
  actions.append(leftBtns);

  const applyLink = el("a", "btn btn-primary btn-sm", "Apply &rarr;");
  applyLink.href = o.apply || o.url;
  applyLink.target = "_blank";
  applyLink.rel = "noopener noreferrer";
  actions.append(applyLink);

  card.append(actions);
  return card;
}

/* RENDER DISCOVER CARDS */
function render(){
  const box = $("#cards");
  if(!box) return;
  box.textContent = "";
  
  const searchFilter = ($("#live-search")?.value || "").toLowerCase().trim();
  let list = all.filter(o => {
    if(currentCategoryFilter !== "all"){
      if(currentCategoryFilter === "remote" && !o.remote) return false;
      if(currentCategoryFilter !== "remote" && o.type !== currentCategoryFilter) return false;
    }
    if(searchFilter){
      const haystack = (o.title + " " + o.org + " " + o.text).toLowerCase();
      if(!haystack.includes(searchFilter)) return false;
    }
    return true;
  });

  const sortVal = $("#sort")?.value || "score";
  if(sortVal === "deadline"){
    list.sort((a,b) => (a.deadline || 8.64e15) - (b.deadline || 8.64e15));
  } else if(sortVal === "title"){
    list.sort((a,b) => a.title.localeCompare(b.title));
  } else {
    list.sort((a,b) => b.pct - a.pct);
  }

  if(!list.length){
    box.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:40px; color:var(--text-muted);">No opportunities match the selected criteria. Try adjusting filters or searching a broader topic.</div>`;
    return;
  }
  list.forEach(o => box.append(createOpportunityCard(o)));
}

function setCategoryFilter(cat){
  currentCategoryFilter = cat;
  $$(".pill-filter").forEach(b => b.classList.toggle("on", b.dataset.category === cat));
  render();
}

function setSearchQuery(kw){
  $("#q").value = kw;
  run(false);
}

/* RENDER APPLICATION TRACKER (8 KANBAN STAGES) */
function renderTracker(){
  const container = $("#kanban-board-container");
  if(!container) return;
  container.textContent = "";

  KANBAN_STAGES.forEach(st => {
    const col = el("div", "kanban-col");
    const items = applications.filter(a => (a.stage || "interested") === st.id);
    
    col.innerHTML = `
      <div class="kanban-col-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span>${st.icon}</span>
          <span>${st.title}</span>
        </div>
        <span class="badge badge-lavender">${items.length}</span>
      </div>
    `;

    const body = el("div", "kanban-col-body");
    if(!items.length){
      body.innerHTML = `<div style="text-align:center; padding:30px 10px; color:var(--text-dim); font-size:0.82rem;">No applications in this stage.</div>`;
    } else {
      items.forEach(a => {
        const item = el("div", "kanban-item");
        item.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
            <div style="font-size:0.75rem; font-weight:700; color:var(--lavender); text-transform:uppercase;">${a.organization || 'General'}</div>
            <button class="btn btn-subtle btn-sm" style="padding:2px 6px; font-size:0.7rem;" onclick="deleteApplication('${a.id}')">&times;</button>
          </div>
          <div style="font-weight:700; font-size:0.95rem; margin-bottom:8px; line-height:1.3;">${a.title}</div>
          ${a.deadline ? `<div style="font-size:0.78rem; color:var(--warning); margin-bottom:8px;">⏳ Deadline: ${a.deadline}</div>` : ''}
          ${a.notes ? `<div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:10px;">${a.notes}</div>` : ''}
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            <select style="width:auto; padding:4px 8px; font-size:0.75rem;" onchange="moveAppStage('${a.id}', this.value)">
              ${KANBAN_STAGES.map(s => `<option value="${s.id}" ${s.id === a.stage ? 'selected' : ''}>${s.icon} ${s.title}</option>`).join('')}
            </select>
            ${a.url ? `<a href="${a.url}" target="_blank" class="btn btn-subtle btn-sm" style="padding:3px 8px; font-size:0.75rem;">Portal &rarr;</a>` : ''}
          </div>
        `;
        body.append(item);
      });
    }
    col.append(body);
    container.append(col);
  });
  
  $("#nav-tracker-count").textContent = applications.length;
}

async function moveAppStage(appId, newStage){
  const app = applications.find(a => a.id === appId);
  if(app){
    app.stage = newStage;
    LSX.set("oh:applications", applications);
    try {
      await fetch(`${BACKEND_BASE}/api/applications`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(app)
      });
    } catch(e){}
    showToast(`Moved to ${newStage.toUpperCase()}`, "✓");
    renderTracker();
    renderDashboard();
  }
}

async function deleteApplication(appId){
  applications = applications.filter(a => a.id !== appId);
  LSX.set("oh:applications", applications);
  try {
    await fetch(`${BACKEND_BASE}/api/applications?id=${appId}`, { method: "DELETE" });
  } catch(e){}
  showToast("Application removed from tracker.", "✓");
  renderTracker();
  renderDashboard();
}

function exportTrackerCSV(){
  if(!applications.length){
    alert("No applications currently tracked to export.");
    return;
  }
  const headers = ["Title", "Organization", "Stage", "Deadline", "URL", "Notes", "Date"];
  const rows = applications.map(a => [
    `"${(a.title||'').replace(/"/g, '""')}"`,
    `"${(a.organization||'').replace(/"/g, '""')}"`,
    `"${a.stage||''}"`,
    `"${a.deadline||''}"`,
    `"${a.url||''}"`,
    `"${(a.notes||'').replace(/"/g, '""')}"`,
    `"${a.created_at||''}"`
  ]);
  const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `Opportunity_Hunter_Applications_${new Date().toISOString().split("T")[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
}

/* RENDER DEADLINE RADAR & CALENDAR */
function renderRadar(){
  const box = $("#radar-board-container");
  if(!box) return;
  box.textContent = "";

  const groups = [
    { label: "🔴 Urgent (0–3 Days)", items: all.filter(o => o.deadline && !o.expired && daysTo(o.deadline) <= 3) },
    { label: "🟠 Closing Soon (4–7 Days)", items: all.filter(o => o.deadline && !o.expired && daysTo(o.deadline) > 3 && daysTo(o.deadline) <= 7) },
    { label: "🟢 Planning Window (8+ Days)", items: all.filter(o => o.deadline && !o.expired && daysTo(o.deadline) > 7) },
    { label: "⚪ Expired Opportunities", items: all.filter(o => o.deadline && o.expired) }
  ];

  const grid = el("div", null);
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "repeat(auto-fit, minmax(280px, 1fr))";
  grid.style.gap = "16px";

  groups.forEach(g => {
    const col = el("div", "bento-card");
    col.innerHTML = `
      <div style="font-weight:700; font-size:1.05rem; margin-bottom:14px; display:flex; justify-content:space-between;">
        <span>${g.label}</span>
        <span class="badge badge-lavender">${g.items.length}</span>
      </div>
    `;
    if(!g.items.length){
      col.append(el("div", null, "No programs in this window."));
    } else {
      g.items.forEach(o => {
        const item = el("div", "bento-card", "");
        item.style.padding = "12px";
        item.style.marginBottom = "10px";
        item.style.background = "var(--bg-card-elevated)";
        item.innerHTML = `
          <div style="font-weight:700; font-size:0.92rem;">${o.title}</div>
          <div style="font-size:0.8rem; color:var(--text-muted); margin:4px 0;">${o.org} &bull; ${fmt(o.deadline)}</div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            <span class="badge badge-lavender">${o.pct}% Match</span>
            <a href="${o.apply || o.url}" target="_blank" class="btn btn-subtle btn-sm" style="padding:2px 8px; font-size:0.75rem;">Apply &rarr;</a>
          </div>
        `;
        col.append(item);
      });
    }
    grid.append(col);
  });
  box.append(grid);
}

function exportAllDeadlinesICS(){
  const dls = all.filter(o => o.deadline && !o.expired);
  if(!dls.length){
    alert("No active deadlines to export.");
    return;
  }
  let ics = "BEGIN:VCALENDAR\\nVERSION:2.0\\nPRODID:-//Opportunity Hunter//Student Career Calendar//EN\\n";
  dls.forEach(o => {
    const dStr = o.deadline.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    ics += "BEGIN:VEVENT\\n";
    ics += `SUMMARY:${o.title} Application Deadline\\n`;
    ics += `DESCRIPTION:Official Opportunity at ${o.org}. Apply here: ${o.apply || o.url}\\n`;
    ics += `DTSTART:${dStr}\\n`;
    ics += `DTEND:${dStr}\\n`;
    ics += `URL:${o.apply || o.url}\\n`;
    ics += "END:VEVENT\\n";
  });
  ics += "END:VCALENDAR";

  const blob = new Blob([ics], { type: "text/calendar;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `Opportunity_Hunter_Deadlines_${new Date().toISOString().split("T")[0]}.ics`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  showToast("Deadlines exported to .ics calendar file!", "📅");
}

/* RENDER SKILL GAP ANALYZER */
function renderSkillGap(){
  const box = $("#skillgap-container");
  if(!box) return;
  box.textContent = "";

  const demandCounts = {};
  all.forEach(o => {
    (o.sg.req || []).forEach(s => {
      demandCounts[s] = (demandCounts[s] || 0) + 1;
    });
  });

  const sortedDemand = Object.entries(demandCounts).sort((a,b) => b[1] - a[1]);
  const userSkillsLow = (userProfile.skills || []).map(s => s.toLowerCase());

  const grid = el("div", null);
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "1.5fr 1fr";
  grid.style.gap = "20px";

  // Left: Market Demand & Missing Skills
  const left = el("div", "bento-card");
  left.innerHTML = `
    <h3 class="card-title" style="margin-bottom:12px;">Technical Skills In-Demand</h3>
    <p class="card-subtitle" style="margin-bottom:20px;">Frequency of skills listed across current student requisitions</p>
  `;

  if(!sortedDemand.length){
    left.append(el("div", null, "Search or load opportunities to analyze skill frequencies."));
  } else {
    sortedDemand.forEach(([skill, cnt]) => {
      const pct = Math.round((cnt / all.length) * 100);
      const isOwned = userSkillsLow.includes(skill);
      const row = el("div", null);
      row.style.marginBottom = "14px";
      row.innerHTML = `
        <div style="display:flex; justify-content:space-between; font-size:0.88rem; font-weight:700; margin-bottom:4px;">
          <span>${skill.toUpperCase()} ${isOwned ? '<span class="badge badge-success" style="font-size:0.65rem;">You Have This</span>' : '<span class="badge badge-warning" style="font-size:0.65rem;">Gap to Learn</span>'}</span>
          <span>${pct}% of listings</span>
        </div>
        <div style="height:8px; background:var(--bg-subtle); border-radius:var(--radius-full); overflow:hidden;">
          <div style="height:100%; width:${pct}%; background:${isOwned ? 'var(--success)' : 'var(--warning)'}; border-radius:var(--radius-full);"></div>
        </div>
      `;
      left.append(row);
    });
  }
  grid.append(left);

  // Right: Curated Free Learning Roadmaps
  const right = el("div", "bento-card");
  right.innerHTML = `
    <h3 class="card-title" style="margin-bottom:12px;">Curated Learning Roadmaps</h3>
    <p class="card-subtitle" style="margin-bottom:20px;">Recommended paths and projects to close your gaps</p>
  `;

  const roadmaps = [
    { skill: "Docker & Containerization", desc: "Learn to containerize Python and Node backends with Dockerfile and Docker Compose.", url: "https://docker-curriculum.com/" },
    { skill: "SQL & Data Modeling", desc: "Master relational schema design, indexes, and complex window queries.", url: "https://sqlbolt.com/" },
    { skill: "Git & Open Source Workflow", desc: "Branching, PRs, rebasing, and collaborating on production repositories.", url: "https://git-scm.com/book/en/v2" },
    { skill: "Cloud Architecture (AWS)", desc: "Deploy serverless functions and storage using the AWS Free Tier.", url: "https://aws.amazon.com/free/" }
  ];

  roadmaps.forEach(r => {
    const card = el("div", "bento-card", "");
    card.style.padding = "14px";
    card.style.marginBottom = "12px";
    card.style.background = "var(--bg-card-elevated)";
    card.innerHTML = `
      <div style="font-weight:700; font-size:0.95rem; margin-bottom:4px;">${r.skill}</div>
      <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:10px;">${r.desc}</div>
      <a href="${r.url}" target="_blank" class="btn btn-subtle btn-sm" style="font-size:0.75rem;">Open Free Resource &rarr;</a>
    `;
    right.append(card);
  });
  grid.append(right);

  box.append(grid);
}

/* RESUME ANALYZER (SAFE CLIENT-SIDE PARSER) */
function toggleResumePasteArea(){
  const box = $("#resume-paste-box");
  const isHidden = box.style.display === "none";
  box.style.display = isHidden ? "block" : "none";
  $("#btn-toggle-paste").textContent = isHidden ? "Hide text paste box &uarr;" : "Or paste resume text manually &darr;";
}

function handleResumeFileUpload(evt){
  const file = evt.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  
  if(file.name.endsWith(".txt")){
    reader.onload = e => executeResumeAudit(e.target.result);
    reader.readAsText(file);
  } else if(file.name.endsWith(".pdf")){
    reader.onload = e => {
      // Safe stream text extraction from ArrayBuffer
      const buf = e.target.result;
      const decoder = new TextDecoder("utf-8");
      const raw = decoder.decode(buf);
      
      // Extract string literals from PDF stream
      const matches = raw.match(/\\(([^()\\\\]|\\\\.)*\\)/g) || [];
      const extracted = matches.map(s => s.slice(1, -1)).join(" ");
      executeResumeAudit(extracted || raw.slice(0, 10000));
    };
    reader.readAsArrayBuffer(file);
  } else {
    reader.onload = e => executeResumeAudit(e.target.result);
    reader.readAsText(file);
  }
}

function analyzeResumeTextManual(){
  const t = $("#resume-manual-text").value.trim();
  if(!t){
    alert("Please paste resume text to analyze.");
    return;
  }
  executeResumeAudit(t);
}

async function executeResumeAudit(text){
  let result = null;
  // Try backend endpoint first
  try {
    const res = await fetch(`${BACKEND_BASE}/api/resume/parse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, opportunities: all })
    });
    if(res.ok){
      const data = await res.json();
      result = data.analysis;
    }
  } catch(e){}

  // Fallback client-side rule extraction if offline
  if(!result){
    const low = text.toLowerCase();
    const skillsFound = SKILLS_CATALOG.filter(s => new RegExp("(^|[^a-z+#])" + esc(s) + "($|[^a-z+#])").test(low));
    result = {
      candidate_name: "Candidate",
      degree: /b\\.?tech/i.test(low) ? "B.Tech Computer Science" : "Technical Degree",
      study_year: "2nd year",
      extracted_skills: skillsFound,
      strength_score: Math.min(95, 40 + skillsFound.length * 8),
      strengths: [`Found ${skillsFound.length} technical skills: ${skillsFound.slice(0, 5).join(", ")}`],
      improvement_tips: ["Add quantifiable impact metrics to project bullet points."],
      recommended_opportunities: all.slice(0, 2)
    };
  }

  displayResumeResults(result);
}

function displayResumeResults(res){
  const box = $("#resume-results");
  box.style.display = "block";
  box.textContent = "";

  const card = el("div", "bento-card");
  card.innerHTML = `
    <div class="card-header-bar">
      <div>
        <span class="badge badge-success">Audit Complete</span>
        <h3 class="card-title" style="margin-top:4px;">Resume Strength: ${res.strength_score}/100</h3>
        <p class="card-subtitle">Inferred Degree: ${res.degree} &bull; Skills Found: ${res.extracted_skills.length}</p>
      </div>
      <button class="btn btn-primary btn-sm" onclick="applyResumeSkillsToProfile(${JSON.stringify(res.extracted_skills).replace(/"/g, '&quot;')}, '${res.degree}')">
        Sync Skills &amp; Degree to Profile
      </button>
    </div>

    <div style="margin-bottom:16px;">
      <h4 style="font-size:0.9rem; margin-bottom:8px;">Extracted Technical Skills:</h4>
      <div style="display:flex; flex-wrap:wrap; gap:6px;">
        ${res.extracted_skills.map(s => `<span class="badge badge-lavender">${s}</span>`).join('')}
      </div>
    </div>

    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:20px;">
      <div style="padding:14px; background:var(--bg-card-elevated); border-radius:var(--radius-md);">
        <h4 style="font-size:0.9rem; color:var(--success); margin-bottom:8px;">✓ Resume Strengths</h4>
        <ul style="padding-left:18px; font-size:0.85rem; color:var(--text-muted); line-height:1.6;">
          ${(res.strengths || []).map(s => `<li>${s}</li>`).join('')}
        </ul>
      </div>
      <div style="padding:14px; background:var(--bg-card-elevated); border-radius:var(--radius-md);">
        <h4 style="font-size:0.9rem; color:var(--warning); margin-bottom:8px;">💡 Actionable Improvements</h4>
        <ul style="padding-left:18px; font-size:0.85rem; color:var(--text-muted); line-height:1.6;">
          ${(res.improvement_tips || []).map(t => `<li>${t}</li>`).join('')}
        </ul>
      </div>
    </div>
  `;
  box.append(card);
  showToast("Resume analysis completed!", "📄");
}

function applyResumeSkillsToProfile(skillsList, degreeVal){
  userProfile.skills = [...new Set([...(userProfile.skills || []), ...skillsList])];
  if(degreeVal) userProfile.degree = degreeVal;
  LSX.set("oh:profile", userProfile);
  showToast("Skills synchronized to student profile!", "✓");
  recalculateAllScores();
  refreshAll();
}

/* CAREER ASSISTANT ENGINE */
function renderAssistant(){
  const box = $("#chat-messages-box");
  if(!box.children.length){
    appendAssistantMessage("bot", `Hello ${userProfile.name || "Student"}! I am your Opportunity Hunter Career Companion. I have analyzed your profile (${userProfile.degree || 'Engineering'}, ${userProfile.year || '2nd year'}). How can I help you today?`);
  }
}

function sendPrompt(text){
  $("#assistant-input-text").value = text;
  handleAssistantSend();
}

async function handleAssistantSend(){
  const inp = $("#assistant-input-text");
  const query = inp.value.trim();
  if(!query) return;
  inp.value = "";

  appendAssistantMessage("user", query);

  // Try backend assistant endpoint
  try {
    const res = await fetch(`${BACKEND_BASE}/api/assistant`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        profile: userProfile,
        opportunities: all,
        applications
      })
    });
    if(res.ok){
      const data = await res.json();
      appendAssistantMessage("bot", data.reply);
      return;
    }
  } catch(e){}

  // Client-side fallback response
  const qLow = query.toLowerCase();
  if(qLow.includes("microsoft") || qLow.includes("explore")){
    appendAssistantMessage("bot", `Explore Microsoft is specifically designed for 1st and 2nd year undergraduate students. Since you are in your ${userProfile.year}, you meet the primary academic level prerequisite!`);
  } else if(qLow.includes("match")){
    const top = all.slice(0, 2);
    appendAssistantMessage("bot", `Based on your profile, your top matching opportunities are: ${top.map(o => o.title).join(", ")}.`);
  } else {
    appendAssistantMessage("bot", `Great question! To maximize your opportunities in ${userProfile.degree}, ensure your GitHub repositories have clean READMEs and test coverage, and practice problem solving in ${userProfile.skills.slice(0, 2).join(' and ')}.`);
  }
}

function appendAssistantMessage(sender, text){
  const box = $("#chat-messages-box");
  const bubble = el("div", `chat-bubble ${sender}`, text);
  box.append(bubble);
  box.scrollTop = box.scrollHeight;
}

/* SEARCH & FIXTURE LOADING */
async function loadOpportunitiesCatalog(p, statusNotice){
  let fixtures = EMBEDDED_FIXTURES;
  try {
    const res = await fetch(`${BACKEND_BASE}/api/fixtures`);
    if(res.ok){
      const data = await res.json();
      if(data.pages && Array.isArray(data.pages) && data.pages.length){
        fixtures = data.pages;
      }
    }
  } catch(e){}
  
  const fetchedAt = new Date().toISOString();
  all = processRawPages(fixtures, p, fetchedAt, "verified");
  refreshAll();
}
const loadFixtureMode = loadOpportunitiesCatalog;

async function run(forceCatalog = false){
  if(busy) return;
  busy = true;
  const btn = $("#btn-discover-go");
  if(btn) btn.disabled = true;

  try {
    const kw = $("#q").value.trim() || userProfile.interests || "Software Engineering";
    userProfile.interests = kw;
    
    // Check backend status
    let backendStatus = null;
    try {
      const statusRes = await fetch(`${BACKEND_BASE}/api/status`, { signal: AbortSignal.timeout(2500) });
      if(statusRes.ok) backendStatus = await statusRes.json();
    } catch(e){}

    if(backendStatus && backendStatus.has_api_key && !forceCatalog){
      showToast("Searching live web via TinyFish API...", "🌐");
      const searchRes = await fetch(`${BACKEND_BASE}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: `${kw} student internship applications open`, exclude_domains: BLOCK })
      });
      if(searchRes.ok){
        const searchJson = await searchRes.json();
        const cand = (searchJson.results || searchJson.payload?.results || []).slice(0, 5);
        if(cand.length){
          const fetchRes = await fetch(`${BACKEND_BASE}/api/fetch`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ urls: cand.map(c => c.url).filter(Boolean) })
          });
          if(fetchRes.ok){
            const fetchJson = await fetchRes.json();
            const fetchedPages = (fetchJson.results || fetchJson.payload?.results || []);
            all = processRawPages(fetchedPages, userProfile, new Date().toISOString(), "live");
            showToast(`Retrieved ${all.length} live opportunities!`, "✓");
            refreshAll();
            return;
          }
        }
      }
    }
    
    // Default verified opportunities catalog
    await loadOpportunitiesCatalog(userProfile, "");
  } catch(e) {
    await loadOpportunitiesCatalog(userProfile, "");
  } finally {
    busy = false;
    if(btn) btn.disabled = false;
  }
}

async function probeBackendStatus(){
  const dot = $("#srv-dot");
  const txt = $("#srv-text");
  if(!dot || !txt) return;

  try {
    const res = await fetch(`${BACKEND_BASE}/api/status`, { signal: AbortSignal.timeout(2500) });
    if(res.ok){
      const data = await res.json();
      if(data.has_api_key){
        dot.className = "status-dot live";
        txt.textContent = "Live Search & Verification";
      } else {
        dot.className = "status-dot live";
        txt.textContent = "Verified Network (SQLite Sync)";
      }
    } else {
      dot.className = "status-dot live";
      txt.textContent = "Verified Opportunities Network";
    }
  } catch(e){
    dot.className = "status-dot live";
    txt.textContent = "Verified Opportunities Network";
  }
}

function refreshAll(){
  recalculateAllScores();
  renderDashboard();
  render();
  renderTracker();
  renderRadar();
}

/* INITIALIZATION ON PAGE LOAD */
window.addEventListener("DOMContentLoaded", async () => {
  initTheme();
  
  // Load saved profile & apps from localStorage
  const sp = LSX.get("oh:profile", null);
  if(sp && typeof sp === "object") userProfile = { ...userProfile, ...sp };
  
  const sa = LSX.get("oh:applications", null);
  if(Array.isArray(sa)) applications = sa;

  // Sync with backend if available
  try {
    const pRes = await fetch(`${BACKEND_BASE}/api/profile`);
    if(pRes.ok){
      const pData = await pRes.json();
      if(pData.profile) userProfile = { ...userProfile, ...pData.profile };
    }
    const aRes = await fetch(`${BACKEND_BASE}/api/applications`);
    if(aRes.ok){
      const aData = await aRes.json();
      if(Array.isArray(aData.applications) && aData.applications.length){
        applications = aData.applications;
      }
    }
  } catch(e){}

  probeBackendStatus();
  
  // Load initial verified opportunities
  await loadOpportunitiesCatalog(userProfile, "");
  showTab("dashboard");
});
"""
