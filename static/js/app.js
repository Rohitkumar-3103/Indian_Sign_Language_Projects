/**
 * Indian Sign Language (ISL) Recognition - Core Application Controller
 * Handles live webcam detection, landmark rendering, dataset collection,
 * sentence accumulation, speech synthesis, and interactive dictionary practice.
 */

// Application State
const AppState = {
  classes: {},
  activeClass: "A",
  currentCategory: "all",
  dictCategory: "all",
  webcamRunning: false,
  studioWebcamRunning: false,
  showSkeleton: true,
  mediaPipeReady: false,
  mpHands: null,
  mpCamera: null,
  sentence: "",
  predictionBuffer: [],
  activeVotedSymbol: null,
  predictionHoldCount: 0,
  HOLD_THRESHOLD: 6, // ~350-450ms hold to register symbol
  lastAddedSymbol: null,
  commitCooldownUntil: 0,
  fps: 0,
  frameCount: 0,
  lastFpsTimestamp: Date.now(),
  practiceTarget: null,
  practiceHoldCount: 0,
  bursting: false,

  // Text to Sign Player State
  ttsSequence: [],
  ttsCurrentIndex: 0,
  ttsPlaying: false,
  ttsTimer: null,
  ttsSpeed: 1100,
  ttsMediaMode: "video",

  // Voice to Sign Player State
  voiceRecognition: null,
  voiceListening: false,
  voiceSequence: [],
  voiceCurrentIndex: 0,
  voicePlaying: false,
  voiceTimer: null,
  voiceMediaMode: "video"
};

// DOM Elements
const videoEl = document.getElementById("webcam-video");
const canvasEl = document.getElementById("camera-canvas");
const canvasCtx = canvasEl.getContext("2d");
const viewportContainer = document.getElementById("viewport-container");
const fpsEl = document.getElementById("fps-counter");
const cameraStatusBadge = document.getElementById("camera-status-badge");
const hudOverlay = document.getElementById("gesture-overlay");
const hudSymbol = document.getElementById("hud-symbol");
const hudName = document.getElementById("hud-name");
const hudHoldBar = document.getElementById("hud-hold-bar");
const hudCommitBadge = document.getElementById("hud-commit-badge");
const hudConfBar = document.getElementById("hud-confidence-bar");
const hudConfVal = document.getElementById("hud-confidence-val");
const sentenceTextEl = document.getElementById("sentence-text");
const sentenceDisplayBox = document.getElementById("sentence-display-box");
const predictionsListEl = document.getElementById("predictions-list");
const toastContainer = document.getElementById("toast-container");

// Studio Elements
const studioVideoEl = document.getElementById("studio-webcam");
const studioCanvasEl = document.getElementById("studio-canvas");
const studioCanvasCtx = studioCanvasEl.getContext("2d");

// ==========================================================================
// Initialization
// ==========================================================================

document.addEventListener("DOMContentLoaded", async () => {
  setupNavigation();
  setupSentenceControls();
  await loadClasses();
  await loadMetrics();
  setupMediaPipe();
  setupCameraButtons();
  setupTextToSign();
  setupVoiceToSign();
  setupYouTubeToSign();
  setupStudioControls();
  setupDictionary();
});


// Toast Notifications
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  const icon = type === "success" ? "fa-circle-check text-emerald" : "fa-circle-exclamation text-rose";
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(50px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Native Web Audio Synth Chime for responsive, futuristic audio feedback on commit
function playCommitChime() {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = "sine";
    const now = ctx.currentTime;
    osc.frequency.setValueAtTime(880, now); // A5 note
    osc.frequency.exponentialRampToValueAtTime(1318.5, now + 0.08); // E6 note

    gain.gain.setValueAtTime(0.06, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.15);
  } catch (err) {
    // Audio autoplay or permissions deferred
  }
}

// ==========================================================================
// Navigation
// ==========================================================================

function setupNavigation() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");
      tabBtns.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      document.getElementById(targetId).classList.add("active");

      // Auto start/pause cameras on tab switch
      if (targetId === "tab-studio") {
        startStudioCamera();
      } else if (targetId === "tab-translator") {
        if (!AppState.webcamRunning) startWebcam();
      }
    });
  });
}

// ==========================================================================
// Load Metadata & Metrics from Backend
// ==========================================================================

async function loadClasses() {
  try {
    const res = await fetch("/api/classes");
    const data = await res.json();
    AppState.classes = data.classes || {};
    if (data.total_samples) {
      const totEl = document.getElementById("studio-total-samples");
      if (totEl) totEl.textContent = Number(data.total_samples).toLocaleString();
    }
    renderStudioClassSelector();
    renderDictionary();
    updateStudioClassView(AppState.activeClass);
  } catch (err) {
    console.error("Failed to load classes:", err);
  }
}

async function loadMetrics() {
  try {
    const res = await fetch("/api/metrics");
    if (!res.ok) return;
    const data = await res.json();
    if (data.accuracy) {
      document.getElementById("bench-val-acc").textContent = `${(data.accuracy * 100).toFixed(1)}%`;
      document.getElementById("bench-total-samples").textContent = `${data.total_samples || 2925} Total Samples`;
    }
  } catch (err) {
    console.error("Failed to load metrics:", err);
  }
}

// ==========================================================================
// MediaPipe Initialization (Client-Side Detection)
// ==========================================================================

function setupMediaPipe() {
  if (typeof Hands === "undefined") {
    console.warn("MediaPipe Hands JS not loaded via CDN. Falling back to server-side frame processing.");
    AppState.mediaPipeReady = false;
    return;
  }

  try {
    AppState.mpHands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    AppState.mpHands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.65,
      minTrackingConfidence: 0.55
    });

    AppState.mpHands.onResults(onMediaPipeResults);
    AppState.mediaPipeReady = true;
    console.log("Client-side MediaPipe Hands successfully initialized.");
  } catch (e) {
    console.warn("MediaPipe Hands initialization error:", e);
    AppState.mediaPipeReady = false;
  }
}

// ==========================================================================
// Camera Management
// ==========================================================================

function setupCameraButtons() {
  const toggleBtn = document.getElementById("btn-toggle-webcam");
  const skeletonBtn = document.getElementById("btn-toggle-landmarks");

  toggleBtn.addEventListener("click", () => {
    if (AppState.webcamRunning) {
      stopWebcam();
      toggleBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start Camera';
      toggleBtn.classList.replace("btn-danger", "btn-primary");
    } else {
      startWebcam();
      toggleBtn.innerHTML = '<i class="fa-solid fa-stop"></i> Stop Camera';
      toggleBtn.classList.replace("btn-primary", "btn-danger");
    }
  });

  skeletonBtn.addEventListener("click", () => {
    AppState.showSkeleton = !AppState.showSkeleton;
    skeletonBtn.innerHTML = AppState.showSkeleton
      ? '<i class="fa-solid fa-draw-polygon"></i> Skeleton: ON'
      : '<i class="fa-solid fa-draw-polygon"></i> Skeleton: OFF';
    skeletonBtn.classList.toggle("btn-outline", !AppState.showSkeleton);
  });

  document.getElementById("btn-snapshot").addEventListener("click", () => {
    if (!AppState.webcamRunning) return;
    const a = document.createElement("a");
    a.href = canvasEl.toDataURL("image/jpeg");
    a.download = `isl_snapshot_${Date.now()}.jpg`;
    a.click();
    showToast("Snapshot saved!");
  });
}

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
      audio: false
    });

    videoEl.srcObject = stream;
    await videoEl.play();

    canvasEl.width = videoEl.videoWidth || 640;
    canvasEl.height = videoEl.videoHeight || 480;

    AppState.webcamRunning = true;
    cameraStatusBadge.textContent = "LIVE DETECTION";
    cameraStatusBadge.className = "hud-badge live-tag";

    if (AppState.mediaPipeReady && typeof Camera !== "undefined") {
      AppState.mpCamera = new Camera(videoEl, {
        onFrame: async () => {
          if (AppState.webcamRunning) {
            await AppState.mpHands.send({ image: videoEl });
          }
        },
        width: 640,
        height: 480
      });
      AppState.mpCamera.start();
    } else {
      // Server fallback loop
      requestAnimationFrame(serverProcessingLoop);
    }

    showToast("Webcam connected successfully.");
  } catch (err) {
    console.error("Camera access error:", err);
    showToast("Could not access camera. Please allow webcam permissions.", "error");
    cameraStatusBadge.textContent = "CAM ERROR";
  }
}

function stopWebcam() {
  AppState.webcamRunning = false;
  if (videoEl.srcObject) {
    videoEl.srcObject.getTracks().forEach(t => t.stop());
    videoEl.srcObject = null;
  }
  if (AppState.mpCamera) {
    AppState.mpCamera.stop();
  }
  canvasCtx.clearRect(0, 0, canvasEl.width, canvasEl.height);
  cameraStatusBadge.textContent = "CAMERA OFF";
  viewportContainer.classList.remove("hands-active");
  hudOverlay.style.display = "none";
}

// ==========================================================================
// Results Processing & Landmark Rendering
// ==========================================================================

let lastServerCall = 0;
const SERVER_CALL_INTERVAL = 70; // ~14 fps prediction calls

async function onMediaPipeResults(results) {
  if (!AppState.webcamRunning) return;

  // Calculate FPS
  AppState.frameCount++;
  const now = Date.now();
  if (now - AppState.lastFpsTimestamp >= 1000) {
    AppState.fps = AppState.frameCount;
    AppState.frameCount = 0;
    AppState.lastFpsTimestamp = now;
    fpsEl.innerHTML = `<i class="fa-solid fa-bolt"></i> ${AppState.fps} FPS`;
  }

  // Clear Canvas
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasEl.width, canvasEl.height);

  const numHands = results.multiHandLandmarks ? results.multiHandLandmarks.length : 0;
  viewportContainer.classList.toggle("hands-active", numHands > 0);

  // Draw Landmarks if enabled
  if (numHands > 0 && AppState.showSkeleton) {
    for (let idx = 0; idx < numHands; idx++) {
      const landmarks = results.multiHandLandmarks[idx];
      const handedness = results.multiHandedness && results.multiHandedness[idx]
        ? results.multiHandedness[idx].label
        : (idx === 0 ? "Right" : "Left");

      drawHandSkeleton(canvasCtx, landmarks, handedness, canvasEl.width, canvasEl.height);
    }
    if (numHands >= 2) {
      drawBimanualInteraction(canvasCtx, results.multiHandLandmarks[0], results.multiHandLandmarks[1], canvasEl.width, canvasEl.height);
    }
  }

  canvasCtx.restore();

  // Send landmarks for classification
  if (numHands > 0 && now - lastServerCall >= SERVER_CALL_INTERVAL) {
    lastServerCall = now;

    const handsPayload = results.multiHandLandmarks.map((lms, idx) => {
      const label = results.multiHandedness && results.multiHandedness[idx]
        ? results.multiHandedness[idx].label
        : (idx === 0 ? "Right" : "Left");
      return {
        label: label,
        landmarks: lms.map(p => [p.x, p.y, p.z || 0.0])
      };
    });

    try {
      const res = await fetch("/api/predict_landmarks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hands: handsPayload })
      });
      const data = await res.json();
      handlePredictionResult(data);
    } catch (e) {
      console.warn("Prediction request failed:", e);
    }
  } else if (numHands === 0) {
    hudOverlay.style.display = "none";
    AppState.predictionBuffer = [];
    AppState.predictionHoldCount = 0;
    AppState.activeVotedSymbol = null;
    if (hudHoldBar) hudHoldBar.style.width = "0%";
    if (hudCommitBadge) {
      hudCommitBadge.className = "hud-commit-badge";
      hudCommitBadge.innerHTML = '<i class="fa-solid fa-hand"></i> STEADY HAND';
    }
  }
}

// Fallback Server Frame Loop (if MediaPipe JS CDN fails)
async function serverProcessingLoop() {
  if (!AppState.webcamRunning) return;

  const now = Date.now();
  if (now - lastServerCall >= 90) {
    lastServerCall = now;

    canvasCtx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);
    const dataUrl = canvasEl.toDataURL("image/jpeg", 0.7);

    try {
      const res = await fetch("/api/predict_frame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataUrl })
      });
      const data = await res.json();
      handlePredictionResult(data);

      // Render server-returned landmarks
      if (data.hands && AppState.showSkeleton) {
        canvasCtx.clearRect(0, 0, canvasEl.width, canvasEl.height);
        data.hands.forEach(h => {
          drawPixelHandSkeleton(canvasCtx, h.pixel_pts, h.label);
        });
      }
    } catch (err) {
      console.warn("Server loop frame error:", err);
    }
  }

  if (AppState.webcamRunning && !AppState.mediaPipeReady) {
    requestAnimationFrame(serverProcessingLoop);
  }
}

// ==========================================================================
// Landmark Drawing Utilities
// ==========================================================================

const CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4],        // Thumb
  [0, 5], [5, 6], [6, 7], [7, 8],        // Index
  [0, 9], [5, 9], [9, 10], [10, 11], [11, 12], // Middle & Palm Web
  [9, 13], [13, 14], [14, 15], [15, 16], // Ring
  [0, 17], [13, 17], [17, 18], [18, 19], [19, 20] // Pinky & Outer Palm
];

const FINGER_PALETTES = {
  Right: {
    core: "#10b981",       // Neon Emerald
    glow: "#059669",
    light: "#34d399",
    bg: "rgba(16, 185, 129, 0.12)",
    label: "R • DOMINANT"
  },
  Left: {
    core: "#06b6d4",       // Electric Cyan
    glow: "#0891b2",
    light: "#38bdf8",
    bg: "rgba(6, 182, 212, 0.12)",
    label: "L • SECONDARY"
  }
};

function drawHandSkeleton(ctx, landmarks, label, w, h) {
  if (!landmarks || landmarks.length < 21) return;
  const isRight = label === "Right";
  const palette = isRight ? FINGER_PALETTES.Right : FINGER_PALETTES.Left;

  ctx.save();

  // 1. Holographic Translucent Palm Mesh Polygon
  ctx.beginPath();
  const palmIndices = [0, 1, 5, 9, 13, 17];
  ctx.moveTo(landmarks[0].x * w, landmarks[0].y * h);
  for (let i = 1; i < palmIndices.length; i++) {
    const idx = palmIndices[i];
    ctx.lineTo(landmarks[idx].x * w, landmarks[idx].y * h);
  }
  ctx.closePath();
  ctx.fillStyle = palette.bg;
  ctx.fill();

  // 2. Pass 1: Outer Neon Glow Laser Bones
  ctx.shadowColor = palette.core;
  ctx.shadowBlur = 14;
  ctx.lineWidth = 5.5;
  ctx.strokeStyle = palette.glow;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";

  CONNECTIONS.forEach(([start, end]) => {
    const p1 = landmarks[start];
    const p2 = landmarks[end];
    if (p1 && p2) {
      ctx.beginPath();
      ctx.moveTo(p1.x * w, p1.y * h);
      ctx.lineTo(p2.x * w, p2.y * h);
      ctx.stroke();
    }
  });

  // 3. Pass 2: High-Contrast Crisp Core Laser
  ctx.shadowBlur = 0;
  ctx.lineWidth = 2.4;
  ctx.strokeStyle = palette.light;

  CONNECTIONS.forEach(([start, end]) => {
    const p1 = landmarks[start];
    const p2 = landmarks[end];
    if (p1 && p2) {
      ctx.beginPath();
      ctx.moveTo(p1.x * w, p1.y * h);
      ctx.lineTo(p2.x * w, p2.y * h);
      ctx.stroke();
    }
  });

  // 4. Radiant Multi-Scale Joints & Sensors
  const tipIndices = [4, 8, 12, 16, 20];
  landmarks.forEach((pt, i) => {
    const px = pt.x * w;
    const py = pt.y * h;

    if (tipIndices.includes(i)) {
      // Fingertip Target Reticle
      ctx.save();
      // Outer radar aura
      ctx.beginPath();
      ctx.arc(px, py, 9, 0, 2 * Math.PI);
      ctx.strokeStyle = palette.core;
      ctx.lineWidth = 1.6;
      ctx.stroke();

      // Glowing solid core
      ctx.beginPath();
      ctx.arc(px, py, 4.5, 0, 2 * Math.PI);
      ctx.fillStyle = "#ffffff";
      ctx.shadowColor = palette.light;
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.restore();
    } else if (i === 0) {
      // Wrist Anatomical Anchor Hub
      ctx.save();
      ctx.beginPath();
      ctx.arc(px, py, 8, 0, 2 * Math.PI);
      ctx.strokeStyle = palette.light;
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px, py, 4, 0, 2 * Math.PI);
      ctx.fillStyle = palette.core;
      ctx.fill();
      ctx.restore();
    } else {
      // Articulated Knuckle Nodes
      ctx.beginPath();
      ctx.arc(px, py, 3.2, 0, 2 * Math.PI);
      ctx.fillStyle = "#ffffff";
      ctx.fill();

      ctx.beginPath();
      ctx.arc(px, py, 4.4, 0, 2 * Math.PI);
      ctx.strokeStyle = palette.core;
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }
  });

  // 5. Sci-Fi HUD Corner Brackets & Floating Tag
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  landmarks.forEach(p => {
    const x = p.x * w;
    const y = p.y * h;
    if (x < minX) minX = x;
    if (y < minY) minY = y;
    if (x > maxX) maxX = x;
    if (y > maxY) maxY = y;
  });

  const pad = 14;
  const bx1 = Math.max(6, minX - pad);
  const by1 = Math.max(6, minY - pad);
  const bx2 = Math.min(w - 6, maxX + pad);
  const by2 = Math.min(h - 6, maxY + pad);
  const cornerLen = 14;

  ctx.strokeStyle = palette.core;
  ctx.lineWidth = 2;

  // Top-Left ┌
  ctx.beginPath();
  ctx.moveTo(bx1, by1 + cornerLen);
  ctx.lineTo(bx1, by1);
  ctx.lineTo(bx1 + cornerLen, by1);
  ctx.stroke();

  // Top-Right ┐
  ctx.beginPath();
  ctx.moveTo(bx2 - cornerLen, by1);
  ctx.lineTo(bx2, by1);
  ctx.lineTo(bx2, by1 + cornerLen);
  ctx.stroke();

  // Bottom-Left └
  ctx.beginPath();
  ctx.moveTo(bx1, by2 - cornerLen);
  ctx.lineTo(bx1, by2);
  ctx.lineTo(bx1 + cornerLen, by2);
  ctx.stroke();

  // Bottom-Right ┘
  ctx.beginPath();
  ctx.moveTo(bx2 - cornerLen, by2);
  ctx.lineTo(bx2, by2);
  ctx.lineTo(bx2, by2 - cornerLen);
  ctx.stroke();

  // Floating Handedness Pill Tag
  const tagText = palette.label;
  ctx.font = "bold 10px 'JetBrains Mono', monospace";
  const tagWidth = ctx.measureText(tagText).width + 12;
  const tagHeight = 16;
  const tagX = bx1;
  const tagY = Math.max(16, by1 - 6);

  ctx.fillStyle = "rgba(10, 15, 25, 0.85)";
  ctx.beginPath();
  ctx.roundRect(tagX, tagY - tagHeight + 3, tagWidth, tagHeight, 4);
  ctx.fill();
  ctx.strokeStyle = palette.core;
  ctx.lineWidth = 1;
  ctx.stroke();

  ctx.fillStyle = palette.light;
  ctx.fillText(tagText, tagX + 6, tagY - 2);

  ctx.restore();
}

function drawBimanualInteraction(ctx, h1, h2, w, h) {
  if (!h1 || !h2) return;

  // 1. Inter-Wrist Geometric Reference Link
  const w1x = h1[0].x * w, w1y = h1[0].y * h;
  const w2x = h2[0].x * w, w2y = h2[0].y * h;
  const wristDist = Math.hypot(w1x - w2x, w1y - w2y);

  ctx.save();
  ctx.setLineDash([4, 6]);
  ctx.strokeStyle = "rgba(148, 163, 184, 0.45)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(w1x, w1y);
  ctx.lineTo(w2x, w2y);
  ctx.stroke();

  // Center Distance Gauge
  const midX = (w1x + w2x) / 2;
  const midY = (w1y + w2y) / 2;
  const distLabel = `Δd: ${Math.round(wristDist)}px`;
  ctx.font = "9px 'JetBrains Mono', monospace";
  ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
  const dw = ctx.measureText(distLabel).width + 8;
  ctx.beginPath();
  ctx.roundRect(midX - dw / 2, midY - 7, dw, 14, 3);
  ctx.fill();
  ctx.fillStyle = "#94a3b8";
  ctx.fillText(distLabel, midX - dw / 2 + 4, midY + 3);
  ctx.restore();

  // 2. Fingertip Proximity & Touch Arc
  const tips = [4, 8, 12, 16, 20];
  let minDist = Infinity;
  let bestP1 = null, bestP2 = null;

  tips.forEach(t1 => {
    tips.forEach(t2 => {
      const p1x = h1[t1].x * w, p1y = h1[t1].y * h;
      const p2x = h2[t2].x * w, p2y = h2[t2].y * h;
      const d = Math.hypot(p1x - p2x, p1y - p2y);
      if (d < minDist) {
        minDist = d;
        bestP1 = { x: p1x, y: p1y };
        bestP2 = { x: p2x, y: p2y };
      }
    });
  });

  // If fingertips are touching or in close contact (< 65px)
  if (minDist < 65 && bestP1 && bestP2) {
    ctx.save();
    // High-energy electric connection
    ctx.shadowColor = "#38bdf8";
    ctx.shadowBlur = 14;
    ctx.strokeStyle = "#fef08a";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(bestP1.x, bestP1.y);
    ctx.lineTo(bestP2.x, bestP2.y);
    ctx.stroke();

    // Pulse beacon at contact point
    const contactX = (bestP1.x + bestP2.x) / 2;
    const contactY = (bestP1.y + bestP2.y) / 2;

    ctx.beginPath();
    ctx.arc(contactX, contactY, 11, 0, 2 * Math.PI);
    ctx.strokeStyle = "rgba(254, 240, 138, 0.85)";
    ctx.lineWidth = 1.8;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(contactX, contactY, 4.5, 0, 2 * Math.PI);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    // Floating Contact Tag
    const cTag = "⚡ BIMANUAL CONTACT";
    ctx.font = "bold 9px 'Plus Jakarta Sans', sans-serif";
    const cw = ctx.measureText(cTag).width + 12;
    ctx.fillStyle = "rgba(245, 158, 11, 0.95)";
    ctx.beginPath();
    ctx.roundRect(contactX - cw / 2, contactY - 24, cw, 16, 4);
    ctx.fill();
    ctx.fillStyle = "#000000";
    ctx.fillText(cTag, contactX - cw / 2 + 6, contactY - 12);

    ctx.restore();
  }
}

function drawPixelHandSkeleton(ctx, pixelPts, label) {
  if (!pixelPts || pixelPts.length < 21) return;
  const isRight = label === "Right";
  const palette = isRight ? FINGER_PALETTES.Right : FINGER_PALETTES.Left;

  ctx.save();

  // Palm polygon
  const palmIndices = [0, 1, 5, 9, 13, 17];
  ctx.beginPath();
  ctx.moveTo(pixelPts[0][0], pixelPts[0][1]);
  for (let i = 1; i < palmIndices.length; i++) {
    const idx = palmIndices[i];
    if (pixelPts[idx]) ctx.lineTo(pixelPts[idx][0], pixelPts[idx][1]);
  }
  ctx.closePath();
  ctx.fillStyle = palette.bg;
  ctx.fill();

  // Bones
  ctx.shadowColor = palette.core;
  ctx.shadowBlur = 10;
  ctx.lineWidth = 4;
  ctx.strokeStyle = palette.core;
  ctx.lineCap = "round";

  CONNECTIONS.forEach(([start, end]) => {
    if (pixelPts[start] && pixelPts[end]) {
      ctx.beginPath();
      ctx.moveTo(pixelPts[start][0], pixelPts[start][1]);
      ctx.lineTo(pixelPts[end][0], pixelPts[end][1]);
      ctx.stroke();
    }
  });

  // Joints
  pixelPts.forEach((pt, i) => {
    const isTip = [4, 8, 12, 16, 20].includes(i);
    ctx.beginPath();
    ctx.arc(pt[0], pt[1], isTip ? 5 : 3.5, 0, 2 * Math.PI);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(pt[0], pt[1], isTip ? 7.5 : 4.5, 0, 2 * Math.PI);
    ctx.strokeStyle = palette.light;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });

  ctx.restore();
}

// ==========================================================================
// Prediction Handling & Sentence Assembly
// ==========================================================================

function handlePredictionResult(data) {
  if (!data || !data.detected || !data.prediction) {
    hudOverlay.style.display = "none";
    AppState.predictionBuffer = [];
    AppState.predictionHoldCount = 0;
    AppState.activeVotedSymbol = null;
    if (hudHoldBar) hudHoldBar.style.width = "0%";
    return;
  }

  const rawSymbol = data.prediction;
  const rawConf = Math.round(data.confidence * 100);
  const now = Date.now();

  // 1. Maintain sliding prediction buffer (last 6 frames)
  AppState.predictionBuffer.push({
    symbol: rawSymbol,
    conf: rawConf,
    timestamp: now
  });
  if (AppState.predictionBuffer.length > 6) {
    AppState.predictionBuffer.shift();
  }

  // 2. Confidence-weighted voting across the temporal window
  const voteWeights = {};
  let totalWeight = 0;
  for (const item of AppState.predictionBuffer) {
    voteWeights[item.symbol] = (voteWeights[item.symbol] || 0) + item.conf;
    totalWeight += item.conf;
  }

  let votedSymbol = rawSymbol;
  let maxWeight = 0;
  for (const s in voteWeights) {
    if (voteWeights[s] > maxWeight) {
      maxWeight = voteWeights[s];
      votedSymbol = s;
    }
  }

  const consistencyRatio = totalWeight > 0 ? (maxWeight / totalWeight) : 0;
  const symbol = votedSymbol;
  const conf = rawConf;
  const meta = data.metadata || AppState.classes[symbol] || {};

  // 3. Update HUD Display
  hudOverlay.style.display = "flex";
  hudSymbol.textContent = symbol;
  hudName.textContent = meta.name || symbol;
  hudConfBar.style.width = `${conf}%`;
  hudConfVal.textContent = `${conf}%`;

  // Update Sidebar Predictions List
  if (data.top_k) {
    predictionsListEl.innerHTML = data.top_k.map(p => `
      <div class="pred-row">
        <span class="pred-label">${p.label} (${AppState.classes[p.label]?.name || p.label})</span>
        <span class="pred-percent">${Math.round(p.confidence * 100)}%</span>
      </div>
    `).join("");
  }

  // Update Keras 5-Layer DNN comparison row
  const kerasEl = document.getElementById("keras-pred-val");
  if (kerasEl) {
    if (data.keras_model && data.keras_model.label) {
      const kConf = Math.round(data.keras_model.confidence * 100);
      const isMatch = data.keras_model.label === symbol;
      const matchBadge = isMatch ? ' <i class="fa-solid fa-check" style="color: #34d399; font-size: 0.72rem;"></i>' : '';
      kerasEl.innerHTML = `<span style="color: #67e8f9; font-weight: 700;">${data.keras_model.label}${matchBadge}</span> <span style="font-size: 0.72rem; color: #a5b4fc;">(${kConf}%)</span>`;
    } else {
      kerasEl.textContent = "Standby (Need 1 hand)";
    }
  }

  // Update Active Sign Guide Card
  const activeCard = document.getElementById("active-sign-card");
  if (meta.description) {
    activeCard.style.display = "flex";
    document.getElementById("guide-sign-title").textContent = `${symbol}: ${meta.name}`;
    document.getElementById("guide-sign-desc").textContent = meta.description;
    document.getElementById("guide-sign-tip").textContent = `Tip: ${meta.tips}`;
  }

  // Check Practice Mode
  if (AppState.practiceTarget && symbol === AppState.practiceTarget) {
    AppState.practiceHoldCount++;
    if (AppState.practiceHoldCount >= 6) {
      onPracticeSuccess();
    }
  } else {
    AppState.practiceHoldCount = 0;
  }

  // 4. Temporal Hold-to-Commit State Machine
  // Requires solid temporal consistency and reasonable confidence
  if (consistencyRatio >= 0.50 && conf >= 35) {
    if (symbol === AppState.activeVotedSymbol) {
      AppState.predictionHoldCount++;
    } else {
      AppState.activeVotedSymbol = symbol;
      AppState.predictionHoldCount = 1;
    }

    const progress = Math.min(100, Math.round((AppState.predictionHoldCount / AppState.HOLD_THRESHOLD) * 100));
    if (hudHoldBar) hudHoldBar.style.width = `${progress}%`;

    if (progress < 100) {
      if (hudCommitBadge) {
        hudCommitBadge.className = "hud-commit-badge holding";
        hudCommitBadge.innerHTML = `<i class="fa-solid fa-hourglass-half"></i> HOLDING (${progress}%)`;
      }
    } else {
      // 100% threshold reached
      if (now > AppState.commitCooldownUntil && AppState.lastAddedSymbol !== symbol) {
        appendSymbolToSentence(symbol);
        playCommitChime();
        AppState.commitCooldownUntil = now + 900;
        AppState.lastAddedSymbol = symbol;

        if (hudCommitBadge) {
          hudCommitBadge.className = "hud-commit-badge committed";
          hudCommitBadge.innerHTML = '<i class="fa-solid fa-check"></i> COMMITTED';
        }
      }
    }
  } else {
    // Unsteady gesture / transition
    AppState.predictionHoldCount = Math.max(0, AppState.predictionHoldCount - 1);
    const progress = Math.min(100, Math.round((AppState.predictionHoldCount / AppState.HOLD_THRESHOLD) * 100));
    if (hudHoldBar) hudHoldBar.style.width = `${progress}%`;
    if (hudCommitBadge && progress === 0) {
      hudCommitBadge.className = "hud-commit-badge";
      hudCommitBadge.innerHTML = '<i class="fa-solid fa-hand"></i> STEADY HAND';
    }
  }
}

function appendSymbolToSentence(symbol) {
  if (AppState.sentence.length === 0 || AppState.sentence === "Recognized gestures will assemble here...") {
    AppState.sentence = "";
  }

  // If word sign (e.g. HELLO, THANK_YOU, YES, NO), add with spaces
  const info = AppState.classes[symbol] || {};
  if (info.category === "word") {
    AppState.sentence += (AppState.sentence.length > 0 && !AppState.sentence.endsWith(" ") ? " " : "") + (info.name || symbol) + " ";
  } else {
    AppState.sentence += symbol;
  }

  renderSentence();

  // Flash commit effect on sentence box
  if (sentenceDisplayBox) {
    sentenceDisplayBox.classList.remove("flash-commit");
    void sentenceDisplayBox.offsetWidth; // Trigger reflow
    sentenceDisplayBox.classList.add("flash-commit");
    setTimeout(() => {
      if (sentenceDisplayBox) sentenceDisplayBox.classList.remove("flash-commit");
    }, 450);
  }

  // Reset lastAddedSymbol after cooldown to allow repeating after slight hand reset
  setTimeout(() => {
    AppState.lastAddedSymbol = null;
  }, 1000);
}

function renderSentence() {
  sentenceTextEl.textContent = AppState.sentence || "Recognized gestures will assemble here...";
}

// ==========================================================================
// Sentence Controls & Text-to-Speech
// ==========================================================================

function setupSentenceControls() {
  document.getElementById("btn-add-space").addEventListener("click", () => {
    if (AppState.sentence && AppState.sentence !== "Recognized gestures will assemble here...") {
      AppState.sentence += " ";
      renderSentence();
    }
  });

  document.getElementById("btn-backspace").addEventListener("click", () => {
    if (AppState.sentence && AppState.sentence !== "Recognized gestures will assemble here...") {
      AppState.sentence = AppState.sentence.slice(0, -1);
      renderSentence();
    }
  });

  document.getElementById("btn-clear-sentence").addEventListener("click", () => {
    AppState.sentence = "";
    renderSentence();
    showToast("Sentence cleared.");
  });

  document.getElementById("btn-speak-sentence").addEventListener("click", speakSentence);
}

function speakSentence() {
  const text = AppState.sentence.trim();
  if (!text || text === "Recognized gestures will assemble here...") {
    showToast("Sentence is empty. Perform gestures first!", "error");
    return;
  }

  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    
    // Pick English or Indian English voice if available
    const voices = window.speechSynthesis.getVoices();
    const indVoice = voices.find(v => v.lang.includes("en-IN") || v.name.includes("India"));
    if (indVoice) utterance.voice = indVoice;

    window.speechSynthesis.speak(utterance);
    showToast(`Speaking: "${text}"`);
  } else {
    showToast("Speech synthesis not supported in this browser.", "error");
  }
}

// ==========================================================================
// Tab 2: Text to Sign Translation & Animation Player
// ==========================================================================

function setupTextToSign() {
  const inputEl = document.getElementById("tts-input-text");
  const translateBtn = document.getElementById("btn-translate-text");
  const resetBtn = document.getElementById("btn-clear-tts-input");

  if (!inputEl || !translateBtn) return;

  translateBtn.addEventListener("click", () => {
    translateTextToSigns(inputEl.value.trim());
  });

  resetBtn.addEventListener("click", () => {
    inputEl.value = "";
    AppState.ttsSequence = [];
    renderSignPlayer(null, 0, 0);
    renderFilmstrip([]);
  });

  // Preset phrase chips
  document.querySelectorAll(".tts-preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      inputEl.value = btn.getAttribute("data-phrase");
      translateTextToSigns(inputEl.value);
    });
  });

  // Player controls
  document.getElementById("btn-player-toggle").addEventListener("click", toggleTtsPlayback);
  document.getElementById("btn-player-prev").addEventListener("click", prevTtsSign);
  document.getElementById("btn-player-next").addEventListener("click", nextTtsSign);
  document.getElementById("btn-player-replay").addEventListener("click", () => {
    AppState.ttsCurrentIndex = 0;
    playTtsSequence();
  });

  // Speed selector
  document.querySelectorAll(".speed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      AppState.ttsSpeed = parseInt(btn.getAttribute("data-speed"), 10) || 1100;
      if (AppState.ttsPlaying) {
        clearInterval(AppState.ttsTimer);
        AppState.ttsTimer = setInterval(advanceTtsSign, AppState.ttsSpeed);
      }
    });
  });

  // Media mode toggle (Video vs Image)
  const mediaToggleBtn = document.getElementById("btn-player-media-toggle");
  if (mediaToggleBtn) {
    mediaToggleBtn.addEventListener("click", () => {
      AppState.ttsMediaMode = AppState.ttsMediaMode === "video" ? "image" : "video";
      const lbl = document.getElementById("player-media-label");
      if (lbl) lbl.textContent = AppState.ttsMediaMode === "video" ? "Video" : "Image";
      showToast(`Text-to-Sign player mode: ${AppState.ttsMediaMode === "video" ? "HD Demonstration Video" : "Static Image"}`);
      if (AppState.ttsSequence && AppState.ttsSequence.length > 0) {
        renderSignPlayer(AppState.ttsSequence[AppState.ttsCurrentIndex], AppState.ttsCurrentIndex, AppState.ttsSequence.length);
      }
    });
  }

  // Initial translation
  if (inputEl.value.trim()) {
    translateTextToSigns(inputEl.value.trim());
  }
}

async function translateTextToSigns(text) {
  if (!text) {
    showToast("Please enter some text to translate", "error");
    return;
  }

  try {
    const res = await fetch("/api/text_to_sign", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    });
    const data = await res.json();

    if (!data.sequence || data.sequence.length === 0) {
      showToast("No matching signs found for this input.", "error");
      return;
    }

    AppState.ttsSequence = data.sequence;
    AppState.ttsCurrentIndex = 0;

    renderSignPlayer(AppState.ttsSequence[0], 0, AppState.ttsSequence.length);
    renderFilmstrip(AppState.ttsSequence);
    showToast(`Translated "${text}" into ${data.total_signs} gestures!`);

    // Auto-play the sequence
    playTtsSequence();
  } catch (err) {
    console.error("Text to sign translation error:", err);
    showToast("Translation request failed.", "error");
  }
}

function renderSignPlayer(signData, currentIndex, totalSigns) {
  const stage = document.getElementById("player-stage");
  const stepTag = document.getElementById("player-step-tag");
  const handsTag = document.getElementById("player-hands-tag");
  const imgEl = document.getElementById("player-sign-image");
  const vidEl = document.getElementById("player-sign-video");
  const videoBadge = document.getElementById("player-video-badge");
  const titleEl = document.getElementById("player-sign-title");
  const descEl = document.getElementById("player-sign-desc");
  const progBar = document.getElementById("player-progress-bar");

  if (!signData) {
    stepTag.textContent = "Sign 0 of 0";
    titleEl.textContent = "-";
    descEl.textContent = "Enter text above and click translate to start.";
    progBar.style.width = "0%";
    if (vidEl) { vidEl.style.display = "none"; vidEl.pause(); }
    if (imgEl) imgEl.style.display = "block";
    if (videoBadge) videoBadge.style.display = "none";
    return;
  }

  stepTag.textContent = `Sign ${currentIndex + 1} of ${totalSigns}`;
  handsTag.textContent = signData.hands === 2 ? "2 Hands" : "1 Hand";
  handsTag.className = `stage-hands-tag hand-tag ${signData.hands === 2 ? "two-hand" : "one-hand"}`;

  // Video or Image display mode
  const canPlayVideo = AppState.ttsMediaMode === "video" && signData.has_video && signData.video_url;
  if (canPlayVideo && vidEl) {
    imgEl.style.display = "none";
    vidEl.style.display = "block";
    if (vidEl.src !== signData.video_url) {
      vidEl.src = signData.video_url;
    }
    vidEl.currentTime = 0;
    vidEl.play().catch(e => console.log("Video auto-play deferred:", e));
    if (videoBadge) videoBadge.style.display = "flex";
  } else {
    if (vidEl) {
      vidEl.style.display = "none";
      vidEl.pause();
    }
    imgEl.style.display = "block";
    imgEl.src = signData.image_url;
    imgEl.classList.remove("anim-pop");
    void imgEl.offsetWidth; // trigger reflow
    imgEl.classList.add("anim-pop");
    if (videoBadge) videoBadge.style.display = "none";
  }

  titleEl.textContent = signData.token === signData.sign_key ? signData.name : `${signData.token} (${signData.name})`;
  descEl.textContent = signData.description || "Perform the designated hand pose.";

  const progressPct = ((currentIndex + 1) / totalSigns) * 100;
  progBar.style.width = `${progressPct}%`;

  // Highlight filmstrip item
  document.querySelectorAll("#filmstrip-scroller .filmstrip-thumb").forEach((thumb, idx) => {
    thumb.classList.toggle("active", idx === currentIndex);
    if (idx === currentIndex) {
      thumb.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }
  });
}

function renderFilmstrip(sequence) {
  const container = document.getElementById("filmstrip-scroller");
  const countEl = document.getElementById("filmstrip-count");
  container.innerHTML = "";
  countEl.textContent = `${sequence.length} Signs`;

  if (sequence.length === 0) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 0.85rem; padding: 1rem;">Translate text above to inspect sign sequence filmstrip.</div>`;
    return;
  }

  sequence.forEach((s, idx) => {
    const thumb = document.createElement("div");
    thumb.className = `filmstrip-thumb ${idx === 0 ? "active" : ""}`;
    thumb.innerHTML = `
      <img src="${s.image_url}" alt="${s.token}">
      <span class="filmstrip-thumb-label">${s.token}</span>
      <span style="font-size: 0.65rem; color: var(--text-muted);">${s.hands === 2 ? "2H" : "1H"}</span>
    `;

    thumb.addEventListener("click", () => {
      pauseTtsSequence();
      AppState.ttsCurrentIndex = idx;
      renderSignPlayer(AppState.ttsSequence[idx], idx, AppState.ttsSequence.length);
    });

    container.appendChild(thumb);
  });
}

function toggleTtsPlayback() {
  if (AppState.ttsPlaying) {
    pauseTtsSequence();
  } else {
    playTtsSequence();
  }
}

function playTtsSequence() {
  if (!AppState.ttsSequence || AppState.ttsSequence.length === 0) return;

  AppState.ttsPlaying = true;
  document.getElementById("player-stage").classList.add("playing");
  document.getElementById("btn-player-toggle").innerHTML = '<i class="fa-solid fa-pause"></i> Pause';

  clearInterval(AppState.ttsTimer);
  AppState.ttsTimer = setInterval(advanceTtsSign, AppState.ttsSpeed);
}

function pauseTtsSequence() {
  AppState.ttsPlaying = false;
  document.getElementById("player-stage").classList.remove("playing");
  document.getElementById("btn-player-toggle").innerHTML = '<i class="fa-solid fa-play"></i> Play';
  clearInterval(AppState.ttsTimer);
}

function advanceTtsSign() {
  if (AppState.ttsCurrentIndex + 1 < AppState.ttsSequence.length) {
    AppState.ttsCurrentIndex++;
    renderSignPlayer(AppState.ttsSequence[AppState.ttsCurrentIndex], AppState.ttsCurrentIndex, AppState.ttsSequence.length);
  } else {
    pauseTtsSequence();
  }
}

function prevTtsSign() {
  pauseTtsSequence();
  if (AppState.ttsCurrentIndex > 0) {
    AppState.ttsCurrentIndex--;
    renderSignPlayer(AppState.ttsSequence[AppState.ttsCurrentIndex], AppState.ttsCurrentIndex, AppState.ttsSequence.length);
  }
}

function nextTtsSign() {
  pauseTtsSequence();
  if (AppState.ttsCurrentIndex + 1 < AppState.ttsSequence.length) {
    AppState.ttsCurrentIndex++;
    renderSignPlayer(AppState.ttsSequence[AppState.ttsCurrentIndex], AppState.ttsCurrentIndex, AppState.ttsSequence.length);
  }
}

// ==========================================================================
// Tab 3: Voice to Sign Recognition & Translation
// ==========================================================================

function setupVoiceToSign() {
  const micBtn = document.getElementById("btn-voice-mic");
  const waveVis = document.getElementById("mic-wave-visualizer");
  const statusEl = document.getElementById("voice-mic-status");
  const transcriptEl = document.getElementById("voice-transcript-text");

  if (!micBtn) return;

  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRec) {
    AppState.voiceRecognition = new SpeechRec();
    AppState.voiceRecognition.continuous = false;
    AppState.voiceRecognition.interimResults = true;
    AppState.voiceRecognition.lang = "en-IN";

    AppState.voiceRecognition.onstart = () => {
      AppState.voiceListening = true;
      micBtn.classList.add("listening");
      waveVis.querySelectorAll(".wave-bar").forEach(b => b.classList.add("active"));
      statusEl.textContent = "Listening... Speak clearly now";
      statusEl.style.color = "var(--accent-rose)";
    };

    AppState.voiceRecognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      transcriptEl.textContent = finalTranscript || interimTranscript || "Listening...";
      transcriptEl.style.color = "#fff";
      transcriptEl.style.fontStyle = "normal";

      if (finalTranscript) {
        processSpokenVoice(finalTranscript.trim());
      }
    };

    AppState.voiceRecognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopVoiceListening();
      statusEl.textContent = `Mic status: ${event.error}. Use quick test phrases below!`;
      statusEl.style.color = "var(--accent-amber)";
    };

    AppState.voiceRecognition.onend = () => {
      stopVoiceListening();
    };

    micBtn.addEventListener("click", () => {
      if (AppState.voiceListening) {
        AppState.voiceRecognition.stop();
        stopVoiceListening();
      } else {
        try {
          AppState.voiceRecognition.start();
        } catch (e) {
          console.warn("Speech recognition start error:", e);
        }
      }
    });
  } else {
    statusEl.textContent = "Speech recognition not natively supported. Use quick test phrases below!";
    micBtn.addEventListener("click", () => {
      showToast("Speech Recognition API not supported in this browser. Try the quick buttons below!", "error");
    });
  }

  function stopVoiceListening() {
    AppState.voiceListening = false;
    micBtn.classList.remove("listening");
    waveVis.querySelectorAll(".wave-bar").forEach(b => b.classList.remove("active"));
    statusEl.textContent = "Click Microphone to Start Speaking";
    statusEl.style.color = "var(--accent-emerald-light)";
  }

  // Quick test voice buttons
  document.querySelectorAll(".voice-test-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const phrase = btn.getAttribute("data-voice");
      transcriptEl.textContent = `"${phrase}"`;
      transcriptEl.style.color = "#fff";
      transcriptEl.style.fontStyle = "normal";
      processSpokenVoice(phrase);
    });
  });

  // Replay voice sign sequence button
  document.getElementById("btn-replay-voice-sign").addEventListener("click", () => {
    AppState.voiceCurrentIndex = 0;
    playVoiceSequence();
  });

  document.getElementById("btn-voice-toggle").addEventListener("click", toggleVoicePlayback);
  document.getElementById("btn-voice-prev").addEventListener("click", prevVoiceSign);
  document.getElementById("btn-voice-next").addEventListener("click", nextVoiceSign);

  // Voice media toggle (Video vs Image)
  const voiceMediaToggleBtn = document.getElementById("btn-voice-media-toggle");
  if (voiceMediaToggleBtn) {
    voiceMediaToggleBtn.addEventListener("click", () => {
      AppState.voiceMediaMode = AppState.voiceMediaMode === "video" ? "image" : "video";
      const lbl = document.getElementById("voice-media-label");
      if (lbl) lbl.textContent = AppState.voiceMediaMode === "video" ? "Video" : "Image";
      showToast(`Voice-to-Sign mode: ${AppState.voiceMediaMode === "video" ? "HD Demonstration Video" : "Static Image"}`);
      if (AppState.voiceSequence && AppState.voiceSequence.length > 0) {
        renderVoicePlayer(AppState.voiceSequence[AppState.voiceCurrentIndex], AppState.voiceCurrentIndex, AppState.voiceSequence.length);
      }
    });
  }
}

async function processSpokenVoice(spokenText) {
  if (!spokenText) return;

  const displayArea = document.getElementById("voice-sign-display-area");
  document.getElementById("voice-display-sentence").textContent = spokenText;
  displayArea.style.display = "grid";

  try {
    const res = await fetch("/api/text_to_sign", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: spokenText })
    });
    const data = await res.json();

    if (!data.sequence || data.sequence.length === 0) {
      showToast("No signs found for spoken phrase.", "error");
      return;
    }

    AppState.voiceSequence = data.sequence;
    AppState.voiceCurrentIndex = 0;

    renderVoicePlayer(AppState.voiceSequence[0], 0, AppState.voiceSequence.length);
    renderVoiceFilmstrip(AppState.voiceSequence);
    showToast(`Voice translated: "${spokenText}" (${data.total_signs} gestures)`);

    // Auto-scroll and auto-play
    displayArea.scrollIntoView({ behavior: "smooth", block: "start" });
    playVoiceSequence();
  } catch (err) {
    console.error("Voice sign translation error:", err);
  }
}

function renderVoicePlayer(signData, currentIndex, totalSigns) {
  const stage = document.getElementById("voice-player-stage");
  const stepTag = document.getElementById("voice-step-tag");
  const handsTag = document.getElementById("voice-hands-tag");
  const imgEl = document.getElementById("voice-sign-image");
  const vidEl = document.getElementById("voice-sign-video");
  const videoBadge = document.getElementById("voice-video-badge");
  const titleEl = document.getElementById("voice-sign-title");
  const descEl = document.getElementById("voice-sign-desc");
  const progBar = document.getElementById("voice-progress-bar");

  if (!signData) return;

  stepTag.textContent = `Sign ${currentIndex + 1} of ${totalSigns}`;
  handsTag.textContent = signData.hands === 2 ? "2 Hands" : "1 Hand";
  handsTag.className = `stage-hands-tag hand-tag ${signData.hands === 2 ? "two-hand" : "one-hand"}`;

  // Video or Image display mode
  const canPlayVideo = AppState.voiceMediaMode === "video" && signData.has_video && signData.video_url;
  if (canPlayVideo && vidEl) {
    imgEl.style.display = "none";
    vidEl.style.display = "block";
    if (vidEl.src !== signData.video_url) {
      vidEl.src = signData.video_url;
    }
    vidEl.currentTime = 0;
    vidEl.play().catch(e => console.log("Voice video play deferred:", e));
    if (videoBadge) videoBadge.style.display = "flex";
  } else {
    if (vidEl) {
      vidEl.style.display = "none";
      vidEl.pause();
    }
    imgEl.style.display = "block";
    imgEl.src = signData.image_url;
    imgEl.classList.remove("anim-pop");
    void imgEl.offsetWidth;
    imgEl.classList.add("anim-pop");
    if (videoBadge) videoBadge.style.display = "none";
  }

  titleEl.textContent = signData.token === signData.sign_key ? signData.name : `${signData.token} (${signData.name})`;
  descEl.textContent = signData.description || "Hold gesture posture.";

  const progressPct = ((currentIndex + 1) / totalSigns) * 100;
  progBar.style.width = `${progressPct}%`;

  document.querySelectorAll("#voice-filmstrip-scroller .filmstrip-thumb").forEach((thumb, idx) => {
    thumb.classList.toggle("active", idx === currentIndex);
    if (idx === currentIndex) {
      thumb.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }
  });
}

function renderVoiceFilmstrip(sequence) {
  const container = document.getElementById("voice-filmstrip-scroller");
  const countEl = document.getElementById("voice-filmstrip-count");
  container.innerHTML = "";
  countEl.textContent = `${sequence.length} Signs`;

  sequence.forEach((s, idx) => {
    const thumb = document.createElement("div");
    thumb.className = `filmstrip-thumb ${idx === 0 ? "active" : ""}`;
    thumb.innerHTML = `
      <img src="${s.image_url}" alt="${s.token}">
      <span class="filmstrip-thumb-label">${s.token}</span>
      <span style="font-size: 0.65rem; color: var(--text-muted);">${s.hands === 2 ? "2H" : "1H"}</span>
    `;

    thumb.addEventListener("click", () => {
      pauseVoiceSequence();
      AppState.voiceCurrentIndex = idx;
      renderVoicePlayer(AppState.voiceSequence[idx], idx, AppState.voiceSequence.length);
    });

    container.appendChild(thumb);
  });
}

function toggleVoicePlayback() {
  if (AppState.voicePlaying) {
    pauseVoiceSequence();
  } else {
    playVoiceSequence();
  }
}

function playVoiceSequence() {
  if (!AppState.voiceSequence || AppState.voiceSequence.length === 0) return;
  AppState.voicePlaying = true;
  document.getElementById("voice-player-stage").classList.add("playing");
  document.getElementById("btn-voice-toggle").innerHTML = '<i class="fa-solid fa-pause"></i> Pause';

  clearInterval(AppState.voiceTimer);
  AppState.voiceTimer = setInterval(() => {
    if (AppState.voiceCurrentIndex + 1 < AppState.voiceSequence.length) {
      AppState.voiceCurrentIndex++;
      renderVoicePlayer(AppState.voiceSequence[AppState.voiceCurrentIndex], AppState.voiceCurrentIndex, AppState.voiceSequence.length);
    } else {
      pauseVoiceSequence();
    }
  }, 1100);
}

function pauseVoiceSequence() {
  AppState.voicePlaying = false;
  document.getElementById("voice-player-stage").classList.remove("playing");
  document.getElementById("btn-voice-toggle").innerHTML = '<i class="fa-solid fa-play"></i> Play';
  clearInterval(AppState.voiceTimer);
}

function prevVoiceSign() {
  pauseVoiceSequence();
  if (AppState.voiceCurrentIndex > 0) {
    AppState.voiceCurrentIndex--;
    renderVoicePlayer(AppState.voiceSequence[AppState.voiceCurrentIndex], AppState.voiceCurrentIndex, AppState.voiceSequence.length);
  }
}

function nextVoiceSign() {
  pauseVoiceSequence();
  if (AppState.voiceCurrentIndex + 1 < AppState.voiceSequence.length) {
    AppState.voiceCurrentIndex++;
    renderVoicePlayer(AppState.voiceSequence[AppState.voiceCurrentIndex], AppState.voiceCurrentIndex, AppState.voiceSequence.length);
  }
}

// ==========================================================================
// Tab 4: Dataset Studio & Collector
// ==========================================================================

function renderStudioClassSelector() {
  const container = document.getElementById("studio-class-selector");
  if (!container) return;
  container.innerHTML = "";
  const cat = AppState.currentCategory || "all";
  container.className = `class-grid-selector cat-${cat}`;

  const classes = Object.values(AppState.classes).filter(c => {
    if (AppState.currentCategory === "all") return true;
    return c.category === AppState.currentCategory;
  });

  classes.forEach(c => {
    const chip = document.createElement("div");
    chip.className = `class-chip ${c.label === AppState.activeClass ? "active" : ""}`;
    chip.textContent = c.label;
    chip.title = `${c.name} (${c.sample_count || 0} samples)`;

    chip.addEventListener("click", () => {
      document.querySelectorAll(".class-chip").forEach(el => el.classList.remove("active"));
      chip.classList.add("active");
      AppState.activeClass = c.label;
      updateStudioClassView(c.label);
    });

    container.appendChild(chip);
  });
}

function updateStudioClassView(label) {
  const info = AppState.classes[label] || { name: label, description: "", tips: "", sample_count: 0 };
  const chipEl = document.getElementById("studio-current-chip");
  if (chipEl) {
    chipEl.textContent = label;
    chipEl.classList.remove("chip-medium", "chip-long");
    if (label.length > 5) {
      chipEl.classList.add("chip-long");
    } else if (label.length > 2) {
      chipEl.classList.add("chip-medium");
    }
  }
  document.getElementById("studio-current-name").textContent = `${info.name} (${info.category.toUpperCase()})`;
  document.getElementById("studio-current-desc").textContent = info.description || "Hold steady in camera frame";
  document.getElementById("studio-class-samples").textContent = info.sample_count || 0;
}

function setupStudioControls() {
  // Category buttons
  document.querySelectorAll(".cat-btn[data-cat]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-btn[data-cat]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      AppState.currentCategory = btn.getAttribute("data-cat");
      renderStudioClassSelector();
    });
  });

  // Single Frame Capture
  document.getElementById("btn-studio-single-capture").addEventListener("click", () => {
    captureStudioSample();
  });

  // 3s Burst Capture
  document.getElementById("btn-studio-burst-capture").addEventListener("click", () => {
    triggerBurstCapture(30);
  });

  // SPACE key handler for fast burst trigger
  window.addEventListener("keydown", (e) => {
    if (e.code === "Space" && document.getElementById("tab-studio").classList.contains("active")) {
      e.preventDefault();
      triggerBurstCapture(30);
    }
  });

  // Retrain Model
  document.getElementById("btn-trigger-train").addEventListener("click", async () => {
    const statusMsg = document.getElementById("train-status-msg");
    const btn = document.getElementById("btn-trigger-train");

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Training in progress...';
    statusMsg.style.display = "block";
    statusMsg.textContent = "Fitting Random Forest ensemble across all classes...";

    try {
      const res = await fetch("/api/train", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_type: "random_forest" })
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Model successfully trained! Accuracy: ${data.accuracy}%`);
        statusMsg.innerHTML = `<span style="color: var(--accent-emerald);">Trained on ${data.total_samples} samples &bull; Acc: ${data.accuracy}%</span>`;
        loadMetrics();
      } else {
        showToast(`Training error: ${data.error}`, "error");
        statusMsg.textContent = data.error;
      }
    } catch (e) {
      showToast("Training request failed.", "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-gear"></i> Retrain Model Now';
    }
  });
}

async function startStudioCamera() {
  if (AppState.studioWebcamRunning) return;
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 },
      audio: false
    });
    studioVideoEl.srcObject = stream;
    await studioVideoEl.play();

    studioCanvasEl.width = studioVideoEl.videoWidth || 640;
    studioCanvasEl.height = studioVideoEl.videoHeight || 480;
    AppState.studioWebcamRunning = true;
  } catch (err) {
    console.error("Studio camera access error:", err);
  }
}

async function captureStudioSample() {
  if (!AppState.studioWebcamRunning && !AppState.webcamRunning) {
    showToast("Please enable webcam first!", "error");
    return;
  }

  const vEl = AppState.studioWebcamRunning ? studioVideoEl : videoEl;
  const cEl = AppState.studioWebcamRunning ? studioCanvasEl : canvasEl;
  const ctx = cEl.getContext("2d");

  ctx.drawImage(vEl, 0, 0, cEl.width, cEl.height);
  const dataUrl = cEl.toDataURL("image/jpeg", 0.85);

  try {
    // Collect using frame endpoint
    const res = await fetch("/api/collect_sample", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        label: AppState.activeClass,
        image: dataUrl
      })
    });
    const result = await res.json();
    if (result.success) {
      if (AppState.classes[AppState.activeClass]) {
        AppState.classes[AppState.activeClass].sample_count = result.sample_count;
      }
      updateStudioClassView(AppState.activeClass);
      document.getElementById("studio-total-samples").textContent = result.total_samples;
      showToast(`Saved sample for ${AppState.activeClass} (#${result.sample_count})`);
    }
  } catch (e) {
    console.error("Sample collection error:", e);
  }
}

async function triggerBurstCapture(totalCount = 30) {
  if (AppState.bursting) return;
  AppState.bursting = true;

  const hudTag = document.getElementById("studio-hud-tag");
  const burstCounter = document.getElementById("studio-burst-counter");

  // Countdown: 3, 2, 1
  for (let c = 3; c > 0; c--) {
    hudTag.textContent = `GET READY: ${c}`;
    hudTag.style.color = "var(--accent-amber)";
    await new Promise(r => setTimeout(r, 900));
  }

  hudTag.textContent = "RECORDING BURST";
  hudTag.style.color = "var(--accent-rose)";

  let captured = 0;
  for (let i = 0; i < totalCount; i++) {
    await captureStudioSample();
    captured++;
    burstCounter.textContent = `BURST: ${captured}/${totalCount}`;
    await new Promise(r => setTimeout(r, 90)); // ~11 fps burst
  }

  hudTag.textContent = "READY";
  hudTag.style.color = "var(--text-primary)";
  burstCounter.textContent = "BURST COMPLETE";
  AppState.bursting = false;
  showToast(`Captured ${totalCount} samples for class ${AppState.activeClass}!`);
}

// ==========================================================================
// Tab 3: ISL Visual Dictionary & Practice Challenge
// ==========================================================================

function setupDictionary() {
  const searchInput = document.getElementById("dict-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      renderDictionary(e.target.value.trim().toLowerCase());
    });
  }

  document.querySelectorAll(".cat-btn[data-dict-cat]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-btn[data-dict-cat]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      AppState.dictCategory = btn.getAttribute("data-dict-cat");
      const q = searchInput ? searchInput.value.trim().toLowerCase() : "";
      renderDictionary(q);
    });
  });

  // Practice Modal Close Button
  const closePracticeBtn = document.getElementById("btn-close-modal");
  if (closePracticeBtn) {
    closePracticeBtn.addEventListener("click", () => {
      document.getElementById("practice-modal").style.display = "none";
      const refVid = document.getElementById("practice-ref-video");
      if (refVid) refVid.pause();
      AppState.practiceTarget = null;
    });
  }

  // Video Showcase Modal Close Button
  const closeVideoBtn = document.getElementById("btn-close-video-modal");
  if (closeVideoBtn) {
    closeVideoBtn.addEventListener("click", () => {
      document.getElementById("video-modal").style.display = "none";
      const vidPlayer = document.getElementById("modal-video-player");
      if (vidPlayer) vidPlayer.pause();
    });
  }

  // Video Speed Selectors in Video Modal
  document.querySelectorAll(".vid-speed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".vid-speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const speed = parseFloat(btn.getAttribute("data-speed")) || 1.0;
      const vidPlayer = document.getElementById("modal-video-player");
      if (vidPlayer) vidPlayer.playbackRate = speed;
    });
  });
}

function renderDictionary(filterQuery = "") {
  const grid = document.getElementById("dictionary-cards-grid");
  if (!grid) return;
  grid.innerHTML = "";

  const entries = Object.entries(AppState.classes).filter(([key, val]) => {
    if (AppState.dictCategory === "video") {
      if (!val.has_video) return false;
    } else if (AppState.dictCategory !== "all" && val.category !== AppState.dictCategory) {
      return false;
    }
    if (filterQuery) {
      const matchKey = key.toLowerCase().includes(filterQuery);
      const matchName = (val.name || "").toLowerCase().includes(filterQuery);
      const matchDesc = (val.description || "").toLowerCase().includes(filterQuery);
      return matchKey || matchName || matchDesc;
    }
    return true;
  });

  if (entries.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No gestures found matching your query.</div>`;
    return;
  }

  entries.forEach(([key, val]) => {
    const card = document.createElement("div");
    card.className = "sign-card";

    const isTwoHand = val.hands === 2;
    const handTagClass = isTwoHand ? "two-hand" : "one-hand";
    const handTagText = isTwoHand ? "2 Hands" : "1 Hand";

    const hasVid = val.has_video && val.video_url;
    const vidBadgeHtml = hasVid ? `<span class="video-available-badge"><i class="fa-solid fa-play"></i> Video</span>` : '';
    const rawImgUrl = val.image_url || `/static/assets/signs/${key}.jpg`;
    const imgUrl = rawImgUrl.includes("?") ? rawImgUrl : `${rawImgUrl}?v=20261001`;

    const displayBadge = key.replace(/_/g, " ");
    let badgeClass = "sign-badge";
    if (key.length > 5) {
      badgeClass += " badge-long";
    } else if (key.length > 2) {
      badgeClass += " badge-medium";
    }

    card.innerHTML = `
      <div class="sign-card-top">
        <div class="${badgeClass}" title="${displayBadge}">${displayBadge}</div>
        <span class="hand-tag ${handTagClass}">${handTagText}</span>
      </div>
      <div class="sign-card-media">
        <img class="sign-card-thumb" src="${imgUrl}" alt="${val.name}" loading="lazy">
        ${vidBadgeHtml}
      </div>
      <div>
        <h3 style="font-family: var(--font-display); font-size: 1.05rem; font-weight: 700;">${val.name}</h3>
        <span style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">${val.category}</span>
      </div>
      <p class="sign-card-desc">${val.description || "Hold hands in designated pose."}</p>
      <div class="sign-card-tip"><i class="fa-solid fa-lightbulb"></i> ${val.tips || "Hold steady inside frame."}</div>
      <div class="sign-card-btns">
        ${hasVid ? `
          <button class="btn btn-secondary btn-sm" onclick="openVideoModal('${key}')">
            <i class="fa-solid fa-film"></i> Watch Video
          </button>
        ` : `
          <button class="btn btn-outline btn-sm" disabled style="opacity: 0.5;">
            <i class="fa-solid fa-image"></i> Static Pose
          </button>
        `}
        <button class="btn btn-primary btn-sm" onclick="openPracticeModal('${key}')">
          <i class="fa-solid fa-bullseye"></i> Practice
        </button>
      </div>
    `;

    grid.appendChild(card);
  });
}

window.openVideoModal = function(signKey) {
  const info = AppState.classes[signKey];
  if (!info || !info.video_url) return;

  const modal = document.getElementById("video-modal");
  const title = document.getElementById("video-modal-title");
  const videoPlayer = document.getElementById("modal-video-player");
  const handsTag = document.getElementById("video-modal-hands");
  const desc = document.getElementById("video-modal-desc");
  const tip = document.getElementById("video-modal-tip");
  const practiceBtn = document.getElementById("btn-video-modal-practice");

  title.textContent = `${signKey} - ${info.name}`;
  handsTag.textContent = info.hands === 2 ? "2 Hands" : "1 Hand";
  handsTag.className = `hand-tag ${info.hands === 2 ? "two-hand" : "one-hand"}`;
  desc.textContent = info.description || "Watch gesture demonstration in full HD.";
  tip.innerHTML = `<i class="fa-solid fa-lightbulb"></i> ${info.tips || "Observe hand formation and movement carefully."}`;

  videoPlayer.src = info.video_url;
  videoPlayer.playbackRate = 1.0;
  videoPlayer.play().catch(e => console.log("Video modal auto-play deferred:", e));

  practiceBtn.onclick = () => {
    videoPlayer.pause();
    modal.style.display = "none";
    openPracticeModal(signKey);
  };

  modal.style.display = "flex";
};

window.openPracticeModal = function(signKey) {
  const info = AppState.classes[signKey];
  if (!info) return;

  AppState.practiceTarget = signKey;
  AppState.practiceHoldCount = 0;

  // Close video modal if open
  const vidModal = document.getElementById("video-modal");
  if (vidModal) {
    vidModal.style.display = "none";
    const vidPlayer = document.getElementById("modal-video-player");
    if (vidPlayer) vidPlayer.pause();
  }

  document.getElementById("modal-sign-name").textContent = `${signKey} (${info.name})`;
  document.getElementById("modal-sign-desc").textContent = info.description;
  document.getElementById("modal-tip-box").innerHTML = `<i class="fa-solid fa-lightbulb"></i> Tip: ${info.tips}`;
  document.getElementById("modal-match-status").textContent = "Waiting for Pose...";
  document.getElementById("modal-match-status").style.color = "var(--accent-amber)";

  const refVideo = document.getElementById("practice-ref-video");
  const refImg = document.getElementById("practice-ref-img");

  if (info.has_video && info.video_url) {
    if (refImg) refImg.style.display = "none";
    if (refVideo) {
      refVideo.style.display = "block";
      refVideo.src = info.video_url;
      refVideo.playbackRate = 1.0;
      refVideo.play().catch(e => console.log("Practice video play deferred:", e));
    }
  } else {
    if (refVideo) {
      refVideo.style.display = "none";
      refVideo.pause();
    }
    if (refImg) {
      refImg.style.display = "block";
      const rawRefSrc = info.image_url || `/static/assets/signs/${signKey}.jpg`;
      refImg.src = rawRefSrc.includes("?") ? rawRefSrc : `${rawRefSrc}?v=20261001`;
    }
  }

  document.getElementById("practice-modal").style.display = "flex";

  // Ensure webcam is active
  if (!AppState.webcamRunning) {
    startWebcam();
  }
};

function onPracticeSuccess() {
  const statusEl = document.getElementById("modal-match-status");
  statusEl.textContent = "SUCCESS! MATCHED! 🎉";
  statusEl.style.color = "var(--accent-emerald)";

  // Celebrate with confetti!
  if (typeof confetti === "function") {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });
  }

  showToast(`Awesome! You performed sign ${AppState.practiceTarget} correctly!`);

  setTimeout(() => {
    document.getElementById("practice-modal").style.display = "none";
    const refVideo = document.getElementById("practice-ref-video");
    if (refVideo) refVideo.pause();
    AppState.practiceTarget = null;
  }, 2200);
}

// ==========================================================================
// YouTube Video to ISL Sign Language Controller
// ==========================================================================

let ytPlayer = null;
let ytIframeApiReady = false;
let ytWords = [];
let ytActiveWordIndex = -1;
let ytSyncInterval = null;
let ytIsPlaying = false;
let ytCurrentVideoId = null;

function ensureYouTubeIframeApi() {
  if (window.YT && window.YT.Player) {
    ytIframeApiReady = true;
    return;
  }
  if (!document.getElementById("yt-iframe-api-script")) {
    const tag = document.createElement("script");
    tag.id = "yt-iframe-api-script";
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName("script")[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    window.onYouTubeIframeAPIReady = () => {
      ytIframeApiReady = true;
      console.log("YouTube IFrame API ready.");
    };
  }
}

function setupYouTubeToSign() {
  ensureYouTubeIframeApi();

  const urlInput = document.getElementById("yt-url-input");
  const pasteBtn = document.getElementById("btn-yt-paste");
  const convertBtn = document.getElementById("btn-yt-convert");
  const statusBanner = document.getElementById("yt-status-banner");
  const statusText = document.getElementById("yt-status-text");
  const demoChips = document.querySelectorAll(".yt-demo-chip");
  const playToggleBtn = document.getElementById("btn-yt-play-toggle");
  const rewindBtn = document.getElementById("btn-yt-rewind");
  const forwardBtn = document.getElementById("btn-yt-forward");
  const speedBtns = document.querySelectorAll(".yt-speed-btn");

  if (!convertBtn) return;

  // Paste from clipboard
  if (pasteBtn && urlInput) {
    pasteBtn.addEventListener("click", async () => {
      try {
        const text = await navigator.clipboard.readText();
        urlInput.value = text;
        showToast("Pasted URL from clipboard");
      } catch (err) {
        showToast("Clipboard access denied or empty", "warning");
      }
    });
  }

  // Convert Button Click
  convertBtn.addEventListener("click", async () => {
    const url = (urlInput.value || "").trim();
    if (!url) {
      showToast("Please enter a valid YouTube video URL", "warning");
      return;
    }

    statusBanner.style.display = "flex";
    statusText.textContent = "Downloading audio stream & transcribing with Deepgram Speech AI...";
    convertBtn.disabled = true;
    convertBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Converting...`;

    try {
      const res = await fetch("/api/youtube_to_sign", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      const data = await res.json();

      if (data.status !== "success") {
        throw new Error(data.message || "Failed to transcribe YouTube video.");
      }

      showToast(`Transcription ready! ${data.total_words} words mapped to ISL.`);
      loadYouTubeTranslationData(data);
    } catch (err) {
      console.error("YouTube conversion error:", err);
      showToast(err.message || "Conversion failed", "warning");
    } finally {
      statusBanner.style.display = "none";
      convertBtn.disabled = false;
      convertBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Convert Video`;
    }
  });

  // Demo Chips
  demoChips.forEach(chip => {
    chip.addEventListener("click", async () => {
      const demoId = chip.getAttribute("data-demo");
      statusBanner.style.display = "flex";
      statusText.textContent = "Loading curated demo clip & synchronized timestamps...";

      try {
        const res = await fetch("/api/youtube_demos");
        const data = await res.json();
        const demo = (data.demos || []).find(d => d.id === demoId) || data.demos[0];
        if (demo) {
          loadYouTubeTranslationData({
            video_id: demo.video_id,
            title: demo.title,
            transcript: demo.transcript,
            words: demo.words,
            total_words: demo.words.length
          });
          showToast(`Demo loaded: "${demo.title}"`);
        }
      } catch (err) {
        showToast("Failed to load demo", "warning");
      } finally {
        statusBanner.style.display = "none";
      }
    });
  });

  // Player Play/Pause Toggle
  if (playToggleBtn) {
    playToggleBtn.addEventListener("click", () => {
      if (ytPlayer && ytPlayer.getPlayerState) {
        const state = ytPlayer.getPlayerState();
        if (state === 1) {
          ytPlayer.pauseVideo();
        } else {
          ytPlayer.playVideo();
        }
      } else {
        const html5Video = document.getElementById("yt-html5-player");
        if (html5Video && html5Video.src) {
          if (html5Video.paused) html5Video.play();
          else html5Video.pause();
        }
      }
    });
  }

  // Rewind / Forward
  if (rewindBtn) {
    rewindBtn.addEventListener("click", () => {
      seekRelative(-5);
    });
  }
  if (forwardBtn) {
    forwardBtn.addEventListener("click", () => {
      seekRelative(5);
    });
  }

  // Speed controls
  speedBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      speedBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const speed = parseFloat(btn.getAttribute("data-speed") || "1.0");
      if (ytPlayer && ytPlayer.setPlaybackRate) {
        ytPlayer.setPlaybackRate(speed);
      }
      const html5Video = document.getElementById("yt-html5-player");
      if (html5Video) html5Video.playbackRate = speed;
    });
  });
}

function seekRelative(seconds) {
  if (ytPlayer && ytPlayer.getCurrentTime) {
    const cur = ytPlayer.getCurrentTime();
    ytPlayer.seekTo(Math.max(0, cur + seconds), true);
  } else {
    const html5Video = document.getElementById("yt-html5-player");
    if (html5Video && html5Video.currentTime !== undefined) {
      html5Video.currentTime = Math.max(0, html5Video.currentTime + seconds);
    }
  }
}

function loadYouTubeTranslationData(data) {
  ytWords = data.words || [];
  ytCurrentVideoId = data.video_id;

  const titleEl = document.getElementById("yt-video-title");
  if (titleEl) titleEl.textContent = data.title || "YouTube Video";

  const wordCountEl = document.getElementById("yt-transcript-word-count");
  if (wordCountEl) wordCountEl.textContent = `(${ytWords.length} words)`;

  // Render Transcript Chips
  const transcriptFlow = document.getElementById("yt-transcript-flow");
  if (transcriptFlow) {
    transcriptFlow.innerHTML = "";
    ytWords.forEach((item, index) => {
      const chip = document.createElement("span");
      chip.className = "yt-transcript-chip";
      chip.id = `yt-chip-${index}`;
      chip.innerHTML = `${item.word} <span style="font-size: 0.7rem; opacity: 0.6;">${item.start}s</span>`;
      chip.title = `Seek to ${item.start}s (Sign: ${item.clean})`;
      chip.addEventListener("click", () => {
        seekToTimestamp(item.start);
      });
      transcriptFlow.appendChild(chip);
    });
  }

  // Load Video in YouTube IFrame or HTML5 Player
  if (ytCurrentVideoId) {
    loadIframeVideo(ytCurrentVideoId);
  } else if (data.video_url || data.audio_url) {
    loadHtml5Media(data.video_url || data.audio_url);
  }

  // Start Sync Loop
  startPlaybackSyncLoop();
}

function loadIframeVideo(videoId) {
  const html5Player = document.getElementById("yt-html5-player");
  const playerTarget = document.getElementById("yt-player-target");
  if (html5Player) html5Player.style.display = "none";
  if (playerTarget) playerTarget.style.display = "block";

  if (window.YT && window.YT.Player) {
    try {
      if (ytPlayer && typeof ytPlayer.loadVideoById === "function") {
        ytPlayer.loadVideoById(videoId);
        return;
      }
      ytPlayer = new window.YT.Player("yt-player-target", {
        videoId: videoId,
        playerVars: {
          autoplay: 1,
          controls: 1,
          modestbranding: 1,
          rel: 0
        },
        events: {
          onStateChange: onYouTubePlayerStateChange
        }
      });
    } catch (e) {
      console.log("YT Player init fallback:", e);
      playerTarget.innerHTML = `<iframe id="yt-direct-iframe" width="100%" height="100%" src="https://www.youtube.com/embed/${videoId}?enablejsapi=1&autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    }
  } else {
    playerTarget.innerHTML = `<iframe id="yt-direct-iframe" width="100%" height="100%" src="https://www.youtube.com/embed/${videoId}?enablejsapi=1&autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
  }
}

function loadHtml5Media(url) {
  const html5Player = document.getElementById("yt-html5-player");
  const playerTarget = document.getElementById("yt-player-target");
  if (playerTarget) playerTarget.style.display = "none";
  if (html5Player) {
    html5Player.style.display = "block";
    html5Player.src = url;
    html5Player.play().catch(e => console.log("HTML5 autoplay deferred:", e));
  }
}

function onYouTubePlayerStateChange(event) {
  const playToggleBtn = document.getElementById("btn-yt-play-toggle");
  if (event.data === 1) {
    ytIsPlaying = true;
    if (playToggleBtn) playToggleBtn.innerHTML = `<i class="fa-solid fa-pause"></i> Pause`;
  } else {
    ytIsPlaying = false;
    if (playToggleBtn) playToggleBtn.innerHTML = `<i class="fa-solid fa-play"></i> Play`;
  }
}

function seekToTimestamp(seconds) {
  if (ytPlayer && ytPlayer.seekTo) {
    ytPlayer.seekTo(seconds, true);
    ytPlayer.playVideo();
  } else {
    const html5 = document.getElementById("yt-html5-player");
    if (html5) {
      html5.currentTime = seconds;
      html5.play();
    }
  }
}

function startPlaybackSyncLoop() {
  if (ytSyncInterval) clearInterval(ytSyncInterval);

  ytSyncInterval = setInterval(() => {
    let currentTime = 0;
    let duration = 0;

    if (ytPlayer && ytPlayer.getCurrentTime && typeof ytPlayer.getCurrentTime === "function") {
      try {
        currentTime = ytPlayer.getCurrentTime() || 0;
        duration = ytPlayer.getDuration() || 0;
      } catch (e) {}
    } else {
      const html5 = document.getElementById("yt-html5-player");
      if (html5) {
        currentTime = html5.currentTime || 0;
        duration = html5.duration || 0;
      }
    }

    const timerEl = document.getElementById("yt-playback-timer");
    if (timerEl && duration > 0) {
      timerEl.textContent = `${formatTime(currentTime)} / ${formatTime(duration)}`;
    }

    syncWordWithTimestamp(currentTime);
  }, 100);
}

function syncWordWithTimestamp(time) {
  if (!ytWords || ytWords.length === 0) return;

  const foundIndex = ytWords.findIndex(w => time >= w.start && time <= w.end);
  if (foundIndex !== -1 && foundIndex !== ytActiveWordIndex) {
    ytActiveWordIndex = foundIndex;
    const active = ytWords[foundIndex];
    renderActiveSignPresentation(active, foundIndex);
  }
}

function renderActiveSignPresentation(activeWord, index) {
  const wordEl = document.getElementById("yt-active-word");
  const timingEl = document.getElementById("yt-word-timing");
  const confEl = document.getElementById("yt-word-confidence");
  const subtitleEl = document.getElementById("yt-live-subtitle");
  const lettersContainer = document.getElementById("yt-letters-container");
  const matchContainer = document.getElementById("yt-video-match-container");
  const islVideo = document.getElementById("yt-isl-demonstration-video");

  if (wordEl) wordEl.textContent = activeWord.clean || activeWord.word;
  if (timingEl) timingEl.textContent = `${activeWord.start}s - ${activeWord.end}s`;
  if (confEl) confEl.textContent = `${Math.round((activeWord.confidence || 1) * 100)}% Confidence`;
  if (subtitleEl) subtitleEl.textContent = activeWord.word;

  // 1. ISL Full Gesture Video Demonstration (if matched in 203 vocabulary dictionary)
  if (activeWord.has_video && activeWord.video_url) {
    if (matchContainer) matchContainer.style.display = "flex";
    if (islVideo) {
      if (islVideo.src !== window.location.origin + activeWord.video_url) {
        islVideo.src = activeWord.video_url;
        islVideo.play().catch(e => console.log("Loop video deferred:", e));
      }
    }
  } else {
    if (matchContainer) matchContainer.style.display = "none";
  }

  // 2. Dynamic Fingerspelling Sign Cards
  if (lettersContainer) {
    lettersContainer.innerHTML = "";
    (activeWord.letters || []).forEach(item => {
      const card = document.createElement("div");
      card.className = "yt-letter-card";
      card.innerHTML = `
        <img src="${item.img_url}" alt="${item.char}" onerror="this.src='/static/assets/signs/A.jpg'">
        <span>${item.char}</span>
      `;
      lettersContainer.appendChild(card);
    });
  }

  // 3. Highlight Transcript Chip
  document.querySelectorAll(".yt-transcript-chip").forEach(c => c.classList.remove("active-chip"));
  const activeChip = document.getElementById(`yt-chip-${index}`);
  if (activeChip) {
    activeChip.classList.add("active-chip");
    activeChip.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

