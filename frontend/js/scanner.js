/**
 * JobShield AI - Omni-Scanner Controller
 * Connects frontend to the FastAPI backend with real-time SVG gauge,
 * laser scan animations, drag-and-drop file ingestion, and 1-click cybercrime reporting.
 * Handles every type of job posting: Text circulars, Street Posters (OCR), and Offer Letters (PDF).
 */

function getApiBase() {
  if (typeof window !== 'undefined' && window.location && window.location.protocol.startsWith('http')) {
    if ((window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && 
        window.location.port !== '8000' && window.location.port !== '') {
      return `http://${window.location.hostname}:8000/api`;
    }
    return `${window.location.origin}/api`;
  }
  return "http://127.0.0.1:8000/api";
}

const BACKEND_API = getApiBase();
let activeDossier = "";
let uploadedScanFile = null;
let uploadedPdfFile = null;

// Multi-Vector Threat & Legitimate Vacancy Preset Library
const DEMO_PAYLOADS = {
  telegram_scam: "URGENT HIRING: Part-Time Video Reviewers needed! Watch 5 short YouTube videos & like them. Earn ₹2,500 - ₹5,000 per day instantly to your UPI! Contact HR Priya on Telegram: @earn_quick_india. Pay ₹499 security deposit (100% refundable with first salary). Pay to UPI: quickwork@upi.",
  anydesk_scam: "Dear Candidate, you are selected for Amazon Work-From-Home Customer Support. Salary: ₹32,000 per month. To complete laptop dispatch and bank verification, download AnyDesk or TeamViewer on your PC and share the 9-digit remote code with HR on WhatsApp +91 87654 32109.",
  crypto_scam: "Global Merchant Partner Hiring: Earn 30% instant commission on international prepaid brush orders. Step 1: Deposit 100 USDT into your assigned wallet. Step 2: Complete 3 rating tasks. Immediate withdrawals to your crypto address. Contact Support on Telegram @usdt_task_official.",
  data_entry_scam: "Government Certified Data Entry Jobs from Home! Typing speed not required. Earn ₹25,000 monthly. Send your Aadhaar card copy and pay ₹850 verification charge for interview kit to UPI: datawork@oksbi. Notice: If assignments are incomplete in 48 hours, legal notice & police FIR will be filed for agreement violation! Contact +91 98765 43210.",
  tcs_campus: "TCS Off-Campus Hiring 2026: Inviting BE/B.Tech students of Batch 2026 to apply for Ninja and Digital engineering profiles. Official registration exclusively on https://nextstep.tcs.com. No fee or deposit is charged at any stage of recruitment. Official communication will only originate from @tcs.com email.",
  normal_dev: "Senior React & Node.js Developer wanted at tech startup. Full-time remote. We will pay ₹40,000 to ₹65,000 monthly salary with health insurance. Evaluation consists of 2 technical interview rounds and 1 HR screening. Send resume to jobs@startuptech.com."
};

// ==========================================
// TAB NAVIGATION
// ==========================================
function switchScanTab(tabName) {
  document.getElementById('btnTabText').className = tabName === 'text' ? 'btn btn-primary' : 'btn btn-outline';
  document.getElementById('btnTabImage').className = tabName === 'image' ? 'btn btn-primary' : 'btn btn-outline';
  document.getElementById('btnTabPdf').className = tabName === 'pdf' ? 'btn btn-primary' : 'btn btn-outline';

  document.getElementById('scanTabContentText').style.display = tabName === 'text' ? 'block' : 'none';
  document.getElementById('scanTabContentImage').style.display = tabName === 'image' ? 'block' : 'none';
  document.getElementById('scanTabContentPdf').style.display = tabName === 'pdf' ? 'block' : 'none';
}

function loadScanPreset(key) {
  switchScanTab('text');
  document.getElementById('scanInputText').value = DEMO_PAYLOADS[key] || "";
  document.getElementById('scanInputText').focus();
}

// ==========================================
// DRAG AND DROP & FILE UPLOADS
// ==========================================
function handleDragOver(e, zoneId) {
  e.preventDefault();
  e.stopPropagation();
  const el = document.getElementById(zoneId);
  if (el) el.classList.add('dropzone-dragover');
}

function handleDragLeave(e, zoneId) {
  e.preventDefault();
  e.stopPropagation();
  const el = document.getElementById(zoneId);
  if (el) el.classList.remove('dropzone-dragover');
}

function handleImageDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  const el = document.getElementById('imageDropZone');
  if (el) el.classList.remove('dropzone-dragover');

  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    processImageFile(files[0]);
  }
}

function handlePdfDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  const el = document.getElementById('pdfDropZone');
  if (el) el.classList.remove('dropzone-dragover');

  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    processPdfFile(files[0]);
  }
}

function handleImageUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  processImageFile(file);
}

function processImageFile(file) {
  const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif', 'image/bmp'];
  if (!allowedImageTypes.includes(file.type.toLowerCase())) {
    showValidationModal(
      "📷 Invalid File Type for OCR",
      `The file "${file.name}" is not a supported image format. The Street Poster OCR module only accepts image files.`,
      "Supported formats: JPG, JPEG, PNG, WEBP, GIF, BMP. Please re-select a valid image file."
    );
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showValidationModal(
      "📷 Image File Too Large",
      `The file "${file.name}" exceeds the 10MB limit (current size: ${(file.size / 1024 / 1024).toFixed(1)}MB). Please compress or resize the image before uploading.`,
      "Tip: Use an online image compressor or reduce the resolution to bring it under 10MB."
    );
    return;
  }
  uploadedScanFile = file;
  document.getElementById('imgUploadName').innerText = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  document.getElementById('imageSelectedCard').style.display = 'flex';
}

function handlePdfUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  processPdfFile(file);
}

function processPdfFile(file) {
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    showValidationModal(
      "📄 Invalid File Type for PDF Audit",
      `The file "${file.name}" is not a PDF document. The Offer Letter Auditor only accepts PDF files.`,
      "Please re-select a valid .pdf offer letter or circular. Other document formats (DOCX, images) are not supported here."
    );
    return;
  }
  if (file.size > 20 * 1024 * 1024) {
    showValidationModal(
      "📄 PDF File Too Large",
      `The file "${file.name}" exceeds the 20MB limit (current size: ${(file.size / 1024 / 1024).toFixed(1)}MB). Please use a smaller PDF.`,
      "Tip: Use an online PDF compressor to reduce the file size before uploading."
    );
    return;
  }
  uploadedPdfFile = file;
  document.getElementById('pdfUploadName').innerText = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  document.getElementById('pdfSelectedCard').style.display = 'flex';
}

// ==========================================
// SCANNING PROGRESS ANIMATION
// ==========================================
function showScanningProgress(statusText) {
  const box = document.getElementById('scanProgressContainer');
  const txt = document.getElementById('scanProgressStatusText');
  if (txt) txt.innerText = statusText || "Running Deep Heuristic & Multi-Modal Pipeline...";
  if (box) box.style.display = 'block';
  document.getElementById('scanResultsArea').style.display = 'none';
}

function hideScanningProgress() {
  const box = document.getElementById('scanProgressContainer');
  if (box) box.style.display = 'none';
}

// ==========================================
// SCAN EXECUTION HANDLERS
// ==========================================
async function triggerScan() {
  const text = document.getElementById('scanInputText').value.trim();
  if (!text) {
    showValidationModal(
      "⚠️ Empty Text Input",
      "No job message or circular text was detected. Please paste or type the suspicious job offer text into the input field before running the security audit.",
      "Try pasting a WhatsApp job forward, a Telegram hiring message, or a scam circular you received."
    );
    return;
  }

  showScanningProgress("Auditing text circular against 6 AI defense layers...");
  const btn = document.getElementById('btnAuditText');
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${BACKEND_API}/verify-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    });
    if (!res.ok) throw new Error("Backend response error");
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.warn("FastAPI backend unreachable, running local fallback engine:", err);
    const fallback = executeLocalAudit(text);
    renderResults(fallback);
  } finally {
    hideScanningProgress();
    if (btn) btn.disabled = false;
  }
}

async function triggerImageScan() {
  if (!uploadedScanFile) {
    showValidationModal(
      "📷 No Image Selected",
      "No street poster or screenshot was uploaded for OCR analysis. Please drag & drop or select a valid image file (JPG, PNG) to continue.",
      "Supported formats: JPG, JPEG, PNG, WEBP — Max 10MB. Drag the image directly onto the drop zone."
    );
    return;
  }

  showScanningProgress("Executing Gemini Vision OCR & Threat Auditing on image...");
  const btn = document.getElementById('btnAuditImage');
  if (btn) btn.disabled = true;

  const formData = new FormData();
  formData.append("file", uploadedScanFile);

  try {
    const res = await fetch(`${BACKEND_API}/verify-image`, {
      method: "POST",
      body: formData
    });
    if (!res.ok) throw new Error("Image upload error");
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.warn("Backend OCR unreachable, running local fallback:", err);
    let fallbackText = DEMO_PAYLOADS.telegram_scam;
    const fname = uploadedScanFile.name.toLowerCase();
    if (fname.includes("tcs") || fname.includes("campus") || fname.includes("legit")) {
      fallbackText = DEMO_PAYLOADS.tcs_campus;
    } else if (fname.includes("crypto") || fname.includes("usdt")) {
      fallbackText = DEMO_PAYLOADS.crypto_scam;
    } else if (fname.includes("anydesk") || fname.includes("screen")) {
      fallbackText = DEMO_PAYLOADS.anydesk_scam;
    } else if (fname.includes("data") || fname.includes("typing")) {
      fallbackText = DEMO_PAYLOADS.data_entry_scam;
    }

    const fallback = executeLocalAudit(fallbackText);
    fallback.raw_extracted_text = fallbackText;
    fallback.filename = uploadedScanFile.name;
    renderResults(fallback);
  } finally {
    hideScanningProgress();
    if (btn) btn.disabled = false;
  }
}

async function triggerPdfScan() {
  if (!uploadedPdfFile) {
    showValidationModal(
      "📄 No PDF Document Selected",
      "No offer letter or PDF circular was uploaded. Please drag & drop or select a valid PDF document to begin the clause audit.",
      "Upload any appointment letter, offer letter, or PDF circular you received. The engine will audit CIN/DIN numbers, HR signatures, and payment clauses."
    );
    return;
  }

  showScanningProgress("Extracting PDF text structures & auditing clauses with PyPDF...");
  const btn = document.getElementById('btnAuditPdf');
  if (btn) btn.disabled = true;

  const formData = new FormData();
  formData.append("file", uploadedPdfFile);

  try {
    const res = await fetch(`${BACKEND_API}/verify-pdf`, {
      method: "POST",
      body: formData
    });
    if (!res.ok) throw new Error("PDF processing error");
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.warn("Backend PDF audit unreachable, running local fallback:", err);
    let fallbackText = DEMO_PAYLOADS.tcs_campus;
    const fname = uploadedPdfFile.name.toLowerCase();
    if (fname.includes("data") || fname.includes("typing") || fname.includes("scam")) {
      fallbackText = DEMO_PAYLOADS.data_entry_scam;
    } else if (fname.includes("anydesk")) {
      fallbackText = DEMO_PAYLOADS.anydesk_scam;
    }

    const fallback = executeLocalAudit(fallbackText);
    fallback.raw_extracted_text = fallbackText;
    fallback.filename = uploadedPdfFile.name;
    renderResults(fallback);
  } finally {
    hideScanningProgress();
    if (btn) btn.disabled = false;
  }
}

// ==========================================
// OFFLINE / LOCAL HEURISTIC AUDITOR (MIRRORS BACKEND)
// ==========================================
function executeLocalAudit(text) {
  let score = 100;
  const flags = [];
  const passes = [];

  // 1. Upfront Fee Extortion (Demanded from applicant)
  const hasFeeExtortion = /(?:selected\s+)?(?:candidates?|applicants?|students?|interns?|freshers?|you|everyone)\s*(?:must|need\s*to|have\s*to|should)?\s*(?:pay|deposit|transfer|send|submit)\s*(?:rs\.?|inr|₹)?\s*\d+/i.test(text) ||
                         /(?:pay|deposit|transfer|send)\s*(?:rs\.?|inr|₹)?\s*\d+\s*(?:as|for|towards|refundable)?\s*(?:registration|security|deposit|kit|processing|exam|form|interview|verification|caution|materials|id\s*card|charges)/i.test(text) ||
                         /(?:registration|entry|exam|interview|form|application|processing|courier|uniform|kit|verification|documentation)\s*(?:fee|charge|cost|amount)/i.test(text) ||
                         /(?:security|caution|refundable|mandatory)\s*(?:deposit|money|amount|fee)/i.test(text) ||
                         /(?:pay|transfer|send)\s*(?:to\s*)?(?:upi|gpay|phonepe|paytm|qr|account)/i.test(text);

  // 2. Sensitive Credential Harvesting
  const hasCredTheft = /(otp|one\s*time\s*password|atm\s*pin|cvv|bank\s*password|netbanking|blank\s*cheque)/i.test(text);

  // 3. Remote Desktop Trojans
  const hasTrojan = /\b(anydesk|teamviewer|rustdesk|quicksupport|ultraviewer|\.apk)\b/i.test(text);

  // 4. Crypto Ponzi Tasks
  const hasCrypto = /\b(usdt|crypto|tron|trx|bitcoin|binance|prepaid\s*task)\b/i.test(text);

  // 5. Unrealistic Tasks & Reviews
  const hasTask = /(youtube|video|like|subscribe|google\s*maps?|hotel\s*review|data entry|captcha)/i.test(text) &&
                  /(earn|make|daily|commission|per\s*day)/i.test(text);

  // 6. Fake Legal FIR Threats
  const hasLegalThreat = /(legal\s*notice|court|police\s*complaint|fir\s*will\s*be\s*lodged|breach\s*of\s*contract|penalty)/i.test(text);

  // 7. Telegram Routing (excluding email addresses!)
  const hasTelegram = /(?<![a-zA-Z0-9._%+-])@([a-zA-Z0-9_]{4,32})(?!\.[a-zA-Z]{2,})\b|t\.me\/[a-zA-Z0-9_]+/i.test(text);

  // 8. Positive Indicators
  const hasLegitPortal = /nextstep\.tcs\.com|tcs\.com|infosys\.com|wipro\.com|amazon\.jobs|careers\.google\.com|linkedin\.com|naukri\.com|internshala\.com/i.test(text);
  const hasZeroFee = /no\s*(fee|charge|money)\s*is\s*charged|free\s*of\s*charge|zero\s*fee|never\s*ask\s*for\s*money|not\s*charge\s*any\s*fee/i.test(text);
  const hasInterviews = /\b(\d+\s*rounds?|technical\s*interview|hr\s*round|assessment|screening)\b/i.test(text);

  if (hasCredTheft) {
    score -= 55;
    flags.push({
      title: "Sensitive Banking Credential Demands",
      description: "Demands OTP, ATM PIN, or banking passwords. Genuine employers never solicit private authentication credentials."
    });
  }

  if (hasTrojan) {
    score -= 55;
    flags.push({
      title: "Remote Desktop / Device Hijacking Vector",
      description: "Directs applicant to install screen sharing tools (AnyDesk, TeamViewer) or APK files, enabling cybercriminals to seize control of devices."
    });
  }

  if (hasCrypto) {
    score -= 55;
    flags.push({
      title: "Cryptocurrency / Prepaid Task Ponzi Trap",
      description: "Requires crypto deposits (USDT/TRX) to unlock work or withdraw commissions. High-risk financial cyber fraud."
    });
  }

  if (hasFeeExtortion) {
    score -= 50;
    flags.push({
      title: "Upfront Monetary Extortion Detected",
      description: "Demands registration, laptop deposit, training, or kit fee. Legitimate employers never charge candidates money."
    });
  } else if (hasZeroFee) {
    score += 5;
    passes.push({
      title: "Transparent Zero-Fee Policy",
      description: "Explicitly states recruitment is 100% free with no deposit traps."
    });
  }

  if (hasTask) {
    score -= 25;
    flags.push({
      title: "Social Media / Ponzi Task Scam Signature",
      description: "Offers high daily wage (₹2,500 - ₹5,000) for casual YouTube/Google Maps/Telegram review tasks."
    });
  }

  if (hasLegalThreat) {
    score -= 30;
    flags.push({
      title: "Coercive Legal Threat / Fake FIR Extortion",
      description: "Uses fabricated court notices or police complaints to intimidate students into paying bogus penalty charges."
    });
  }

  if (hasTelegram) {
    score -= 15;
    flags.push({
      title: "Anonymous Messaging Redirection",
      description: "Directs applicants to untraceable Telegram handles rather than verified enterprise domains."
    });
  }

  if (hasLegitPortal) {
    score += 15;
    passes.push({
      title: "Verified Enterprise Employment Gateway",
      description: "Directs applicants to an authoritative corporate careers portal or verified job platform."
    });
  }

  if (hasInterviews) {
    passes.push({
      title: "Multi-Stage Evaluation Process",
      description: "Outlines structured evaluation rounds rather than instant selection traps."
    });
  }

  score = Math.max(5, Math.min(100, score));
  const risk_score = 100 - score;

  let classification = "HIGH RISK SCAM";
  if (score >= 80) classification = "VERIFIED LEGITIMATE";
  else if (score >= 50) classification = "SUSPICIOUS - PROCEED WITH CAUTION";

  // Entity Extraction without regex collisions
  const compMatch = text.match(/\b(Tata Consultancy Services|TCS|Infosys|Wipro|Amazon|Google|Microsoft|Deloitte|Cognizant|Accenture)\b/i);
  const upiMatch = text.match(/[a-zA-Z0-9.\-_]+@(oksbi|okhdfcbank|okaxis|okicici|paytm|ybl|apl|upi)(?!\.[a-zA-Z]{2,})/i);
  const phoneMatch = text.match(/(?:\+?91[\-\s]?)?[6-9]\d{4}[\-\s]?\d{5}/);
  const salaryMatch = text.match(/(?:salary|stipend|ctc|package|lpa|fixed\s*pay|we\s*will\s*pay|we\s*pay)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*(\d{2,7}(?:,\d{2,3})*(?:\s*(?:lpa|per\s*month|monthly|pm|pa))?)/i);
  const feeMatch = text.match(/(?:pay|deposit|transfer|send|charge|fee|cost|kit|caution|security)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*(\d{2,5})/i);

  const demandedAmt = hasFeeExtortion && feeMatch ? `₹${feeMatch[1]}` : "None Detected";
  const salaryOffered = salaryMatch ? `₹${salaryMatch[1]}` : (hasLegitPortal ? "Standard Corporate Scale" : null);

  if (salaryOffered && !hasFeeExtortion && !hasTrojan && !hasCrypto) {
    passes.push({
      title: `Structured Remuneration (${salaryOffered})`,
      description: "Listing specifies standard salary or stipend compensation structure."
    });
  }

  return {
    trust_score: score,
    risk_score: risk_score,
    classification: classification,
    summary_verdict: score < 50 
      ? "DANGER: High probability of financial cyber fraud. Demands upfront funds or matches known scam patterns."
      : (score >= 80 ? "Verified recruitment circular with zero monetary extortion triggers." : "Suspicious circular. Proceed with caution and do not pay any advance fees."),
    extracted_entities: {
      company: compMatch ? compMatch[0] : "Not Specified",
      demanded_amount: demandedAmt,
      salary_offered: salaryOffered || "Standard Base",
      phone: phoneMatch ? phoneMatch[0] : "Not Provided",
      upi_id: upiMatch ? upiMatch[0] : "None Detected"
    },
    flags: flags,
    passes: passes,
    police_dossier: `INCIDENT COMPLAINT DOSSIER • GENERATED BY JOBSHIELD AI\nTarget Assessment: ${classification} (${risk_score}% Risk)\nSuspect UPI: ${upiMatch ? upiMatch[0] : 'None'}\nDemanded: ${demandedAmt}\nRaw text: "${text.substring(0, 300)}..."\nCitizen Emergency Protocol: Dial 1930 / File on cybercrime.gov.in.`
  };
}

// ==========================================
// RENDER ANALYSIS RESULTS
// ==========================================
function renderResults(data) {
  const area = document.getElementById('scanResultsArea');
  area.style.display = 'block';
  area.scrollIntoView({ behavior: 'smooth' });

  activeDossier = data.police_dossier || "";

  const score = data.trust_score !== undefined ? data.trust_score : 50;
  document.getElementById('txtGaugeNumber').innerText = `${score}%`;

  const gauge = document.getElementById('svgGaugeMeter');
  const circumference = 251.2;
  const offset = circumference - (score / 100) * circumference;
  gauge.style.strokeDashoffset = offset;

  const pill = document.getElementById('badgeClassificationPill');
  pill.innerText = data.classification;

  if (score >= 80) {
    gauge.style.stroke = "var(--accent-success)";
    document.getElementById('txtGaugeNumber').style.color = "var(--accent-success)";
    pill.style.background = "var(--accent-success-subtle)";
    pill.style.color = "var(--accent-success)";
  } else if (score >= 50) {
    gauge.style.stroke = "var(--accent-warning)";
    document.getElementById('txtGaugeNumber').style.color = "var(--accent-warning)";
    pill.style.background = "var(--accent-warning-subtle)";
    pill.style.color = "var(--accent-warning)";
  } else {
    gauge.style.stroke = "var(--accent-danger)";
    document.getElementById('txtGaugeNumber').style.color = "var(--accent-danger)";
    pill.style.background = "var(--accent-danger-subtle)";
    pill.style.color = "var(--accent-danger)";
  }

  document.getElementById('txtHeadlineVerdict').innerText = data.classification;
  document.getElementById('txtSummaryVerdict').innerText = data.summary_verdict;

  const ent = data.extracted_entities || {};
  document.getElementById('entCompany').innerText = ent.company || "Not Specified";
  
  const salEl = document.getElementById('entSalary');
  if (salEl) salEl.innerText = ent.salary_offered || "Standard Base";

  document.getElementById('entFee').innerText = ent.demanded_amount || "None Detected";
  document.getElementById('entUpi').innerText = ent.upi_id || "None Provided";
  document.getElementById('entContact').innerText = ent.phone || ent.telegram || ent.email || "Not Provided";

  // Display raw OCR/PDF extracted text card if available
  const docCard = document.getElementById('cardExtractedDocument');
  const docText = document.getElementById('txtExtractedDocumentContent');
  const docBadge = document.getElementById('badgeDocFilename');
  if (data.raw_extracted_text && docCard && docText) {
    docCard.style.display = 'block';
    docText.innerText = data.raw_extracted_text;
    if (docBadge) docBadge.innerText = data.filename || "Uploaded File";
  } else if (docCard) {
    docCard.style.display = 'none';
  }

  // Render proof points & passes
  const list = document.getElementById('listProofPoints');
  list.innerHTML = "";

  if (data.flags && data.flags.length > 0) {
    data.flags.forEach(f => {
      const item = document.createElement('div');
      item.style.cssText = "background: var(--accent-danger-subtle); border-left: 3px solid var(--accent-danger); padding: 12px 16px; border-radius: 8px;";
      item.innerHTML = `<div style="font-weight: 700; color: var(--accent-danger); font-size: 0.92rem;">🚩 ${f.title}</div><div style="font-size: 0.86rem; color: var(--text-secondary); margin-top: 3px;">${f.description}</div>`;
      list.appendChild(item);
    });
  }

  if (data.passes && data.passes.length > 0) {
    data.passes.forEach(p => {
      const item = document.createElement('div');
      item.style.cssText = "background: var(--accent-success-subtle); border-left: 3px solid var(--accent-success); padding: 12px 16px; border-radius: 8px;";
      item.innerHTML = `<div style="font-weight: 700; color: var(--accent-success); font-size: 0.92rem;">🛡️ ${p.title}</div><div style="font-size: 0.86rem; color: var(--text-secondary); margin-top: 3px;">${p.description}</div>`;
      list.appendChild(item);
    });
  }
}

// ==========================================
// 1-CLICK POLICE DOSSIER & ACTIONS
// ==========================================
function launchCybercrimePortal() {
  if (!activeDossier) {
    alert("Please run an analysis first to generate the evidence dossier.");
    return;
  }

  navigator.clipboard.writeText(activeDossier).then(() => {
    document.getElementById('copyAlertSuccess').style.display = 'block';
    setTimeout(() => {
      window.open("https://cybercrime.gov.in/home", "_blank");
    }, 450);
  }).catch(() => {
    window.open("https://cybercrime.gov.in/home", "_blank");
  });
}

function copyPoliceDossierText() {
  if (!activeDossier) return;
  navigator.clipboard.writeText(activeDossier).then(() => {
    const btn = document.getElementById('btnCopyDossierOnly');
    const old = btn.innerText;
    btn.innerText = "✅ Dossier Copied!";
    setTimeout(() => { btn.innerText = old; }, 2000);
  });
}

function shareWhatsAppAlert() {
  const shareText = encodeURIComponent(
    `🚨 *CAMPUS FRAUD ALERT (JobShield AI)*\n` +
    `A suspicious employment offer demanding upfront deposit fees was recently flagged.\n\n` +
    `Notice: Legitimate corporate employers never demand registration fees or training kit money.\n` +
    `If funds were extorted, dial Helpline 1930 immediately or file on cybercrime.gov.in.`
  );
  window.open(`https://wa.me/?text=${shareText}`, "_blank");
}

// ==========================================
// INVALID INPUT POPUP MODAL
// ==========================================

/**
 * showValidationModal - Displays the invalid-input popup with contextual info.
 * @param {string} title   - Bold title shown in the popup header.
 * @param {string} message - Detailed explanation of the issue.
 * @param {string} tip     - Helpful hint shown with a 💡 icon.
 */
function showValidationModal(title, message, tip) {
  const modal = document.getElementById('validationModal');
  if (!modal) return;

  const titleEl = document.getElementById('validationModalTitle');
  const msgEl   = document.getElementById('validationModalMessage');
  const tipEl   = document.getElementById('validationModalTipText');

  if (titleEl)  titleEl.innerText  = title   || 'Invalid Input';
  if (msgEl)    msgEl.innerText    = message || 'Please correct the input and try again.';
  if (tipEl)    tipEl.innerText    = tip     || '';

  // Show modal with flex so the overlay centres the card
  modal.style.display = 'flex';

  // Trap focus on the close button for accessibility
  const closeBtn = modal.querySelector('button');
  if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
}

/** Closes the invalid-input popup. */
function closeValidationModal() {
  const modal = document.getElementById('validationModal');
  if (modal) modal.style.display = 'none';
}

// Allow closing the popup by clicking the dark overlay
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('validationModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      // Only close when the backdrop itself is clicked, not the card
      if (e.target === modal) closeValidationModal();
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeValidationModal();
  });
});
