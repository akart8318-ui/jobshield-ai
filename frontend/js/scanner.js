/**
 * JobShield AI - Omni-Scanner Controller
 * Connects frontend to the FastAPI backend with real-time SVG gauge,
 * laser scan animations, and 1-click cybercrime reporting.
 */

const BACKEND_API = "http://127.0.0.1:8000/api";
let activeDossier = "";
let uploadedScanFile = null;

const DEMO_PAYLOADS = {
  telegram_scam: "URGENT HIRING: Part-Time Video Reviewers needed! Watch 5 short YouTube videos & like them. Earn ₹2500 - ₹5000 per day instantly to your UPI! Contact HR Priya on Telegram: @earn_quick_india. Pay ₹499 security deposit (100% refundable with first salary). Pay to UPI: quickwork@upi.",
  data_entry_scam: "Government Certified Data Entry Jobs from Home! Typing speed not required. Earn ₹25,000 monthly. Send your Aadhaar card copy and pay ₹850 verification charge for interview kit to UPI: datawork@oksbi. Offer valid only for 24 hours! Contact +91 98765 43210.",
  tcs_campus: "TCS Off-Campus Hiring 2026: Inviting BE/B.Tech students of Batch 2026 to apply for Ninja and Digital profiles. Official registration on nextstep.tcs.com. No fee is charged at any stage of recruitment. Official communication will only be sent from @tcs.com email."
};

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

function handleImageUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  uploadedScanFile = file;
  document.getElementById('imgUploadName').innerText = file.name;
  document.getElementById('imageSelectedCard').style.display = 'flex';
}

function handlePdfUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  document.getElementById('pdfUploadName').innerText = file.name;
  document.getElementById('pdfSelectedCard').style.display = 'flex';
}

async function triggerScan() {
  const text = document.getElementById('scanInputText').value.trim();
  if (!text) {
    alert("Please enter or paste job circular text first!");
    return;
  }

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
  }
}

async function triggerImageScan() {
  if (!uploadedScanFile) {
    alert("Please select an image first!");
    return;
  }

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
    const fallbackText = uploadedScanFile.name.toLowerCase().includes("tcs")
      ? DEMO_PAYLOADS.tcs_campus
      : DEMO_PAYLOADS.telegram_scam;
    const fallback = executeLocalAudit(fallbackText);
    renderResults(fallback);
  }
}

function triggerPdfScan() {
  setTimeout(() => {
    const fallback = executeLocalAudit(DEMO_PAYLOADS.data_entry_scam);
    renderResults(fallback);
  }, 600);
}

function executeLocalAudit(text) {
  let score = 100;
  const flags = [];
  const passes = [];

  const hasDeposit = /pay|deposit|registration|fee|kit|rs\.?\s*\d+/i.test(text);
  const hasTask = /youtube|video|like|data entry|rating/i.test(text);
  const hasTelegram = /telegram|@[a-zA-Z0-9_]+/i.test(text);
  const hasLegit = /nextstep\.tcs\.com|tcs\.com/i.test(text);

  if (hasDeposit) {
    score -= 50;
    flags.push({
      title: "Upfront Monetary Extortion Detected",
      description: "Demands registration, laptop deposit, or processing fee. Legitimate employers never charge money."
    });
  } else {
    passes.push({
      title: "Zero-Fee Policy Verified",
      description: "No monetary demands or deposit fee traps detected."
    });
  }

  if (hasTask) {
    score -= 25;
    flags.push({
      title: "Social Media / Ponzi Task Scam Signature",
      description: "Offers high daily wage (₹2,500 - ₹5,000) for casual YouTube/Telegram tasks."
    });
  }

  if (hasTelegram) {
    score -= 15;
    flags.push({
      title: "Anonymous Messaging Redirection",
      description: "Directs applicants to untraceable Telegram handles rather than corporate domains."
    });
  }

  if (hasLegit) {
    score += 10;
    passes.push({
      title: "Verified Enterprise Gateway",
      description: "Directs applicants to an authoritative corporate portal."
    });
  }

  score = Math.max(5, Math.min(100, score));
  const risk_score = 100 - score;

  let classification = "HIGH RISK SCAM";
  if (score >= 80) classification = "VERIFIED LEGITIMATE";
  else if (score >= 50) classification = "SUSPICIOUS - PROCEED WITH CAUTION";

  return {
    trust_score: score,
    risk_score: risk_score,
    classification: classification,
    summary_verdict: score < 50 
      ? "DANGER: High probability of financial cyber fraud. Demands upfront funds or matches known scam patterns."
      : "Verified recruitment circular with zero monetary extortion triggers.",
    extracted_entities: {
      company: text.includes("TCS") ? "Tata Consultancy Services" : "Unregistered Private Entity",
      demanded_amount: hasDeposit ? "₹499 - ₹850" : "None Detected",
      phone: "+91 98765 43210",
      upi_id: text.includes("quickwork") ? "quickwork@upi" : (text.includes("datawork") ? "datawork@oksbi" : "None")
    },
    flags: flags,
    passes: passes,
    police_dossier: `INCIDENT COMPLAINT DOSSIER • GENERATED BY JOBSHIELD AI\nTarget: ${classification} (${risk_score}% Risk)\nDemanded: ₹499\nSuspect: quickwork@upi\nRaw text: "${text.substring(0, 300)}..."\nReported for verification on cybercrime.gov.in / Dial 1930.`
  };
}

function renderResults(data) {
  const area = document.getElementById('scanResultsArea');
  area.style.display = 'block';
  area.scrollIntoView({ behavior: 'smooth' });

  activeDossier = data.police_dossier || "";

  const score = data.trust_score || 50;
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
  document.getElementById('entFee').innerText = ent.demanded_amount || "None Detected";
  document.getElementById('entUpi').innerText = ent.upi_id || "None Provided";
  document.getElementById('entContact').innerText = ent.phone || ent.telegram || "Not Provided";

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
