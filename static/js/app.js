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
  lastPrediction: null,
  predictionHoldCount: 0,
  HOLD_THRESHOLD: 8, // ~0.5s hold to register symbol
  lastAddedSymbol: null,
  fps: 0,
  frameCount: 0,
  lastFpsTimestamp: Date.now(),
  practiceTarget: null,
  practiceHoldCount: 0,
  bursting: false
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
const hudConfBar = document.getElementById("hud-confidence-bar");
const hudConfVal = document.getElementById("hud-confidence-val");
const sentenceTextEl = document.getElementById("sentence-text");
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
    AppState.predictionHoldCount = 0;
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
  [5, 9], [9, 10], [10, 11], [11, 12],   // Middle
  [9, 13], [13, 14], [14, 15], [15, 16], // Ring
  [13, 17], [17, 18], [18, 19], [19, 20],// Pinky
  [0, 17]                                // Base
];

function drawHandSkeleton(ctx, landmarks, label, w, h) {
  // Right hand = Emerald, Left hand = Cyan
  const boneColor = label === "Right" ? "#10b981" : "#06b6d4";
  const jointColor = "#ffffff";

  ctx.lineWidth = 3;
  ctx.strokeStyle = boneColor;
  ctx.lineCap = "round";

  // Draw Bones
  CONNECTIONS.forEach(([start, end]) => {
    const p1 = landmarks[start];
    const p2 = landmarks[end];
    ctx.beginPath();
    ctx.moveTo(p1.x * w, p1.y * h);
    ctx.lineTo(p2.x * w, p2.y * h);
    ctx.stroke();
  });

  // Draw Joints
  landmarks.forEach((pt, i) => {
    const px = pt.x * w;
    const py = pt.y * h;
    const radius = [4, 8, 12, 16, 20].includes(i) ? 5.5 : 4; // Bigger fingertips

    ctx.beginPath();
    ctx.arc(px, py, radius, 0, 2 * Math.PI);
    ctx.fillStyle = jointColor;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(px, py, radius + 1.5, 0, 2 * Math.PI);
    ctx.strokeStyle = boneColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });
}

function drawPixelHandSkeleton(ctx, pixelPts, label) {
  const boneColor = label === "Right" ? "#10b981" : "#06b6d4";
  ctx.lineWidth = 3;
  ctx.strokeStyle = boneColor;

  CONNECTIONS.forEach(([start, end]) => {
    if (pixelPts[start] && pixelPts[end]) {
      ctx.beginPath();
      ctx.moveTo(pixelPts[start][0], pixelPts[start][1]);
      ctx.lineTo(pixelPts[end][0], pixelPts[end][1]);
      ctx.stroke();
    }
  });

  pixelPts.forEach(pt => {
    ctx.beginPath();
    ctx.arc(pt[0], pt[1], 4, 0, 2 * Math.PI);
    ctx.fillStyle = "#fff";
    ctx.fill();
  });
}

// ==========================================================================
// Prediction Handling & Sentence Assembly
// ==========================================================================

function handlePredictionResult(data) {
  if (!data || !data.detected || !data.prediction) {
    hudOverlay.style.display = "none";
    return;
  }

  const symbol = data.prediction;
  const conf = Math.round(data.confidence * 100);
  const meta = data.metadata || AppState.classes[symbol] || {};

  // Update HUD
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
    if (AppState.practiceHoldCount >= 8) {
      onPracticeSuccess();
    }
  } else {
    AppState.practiceHoldCount = 0;
  }

  // Smart Sentence Accumulator
  if (conf >= 60) {
    if (symbol === AppState.lastPrediction) {
      AppState.predictionHoldCount++;
      if (AppState.predictionHoldCount === AppState.HOLD_THRESHOLD) {
        appendSymbolToSentence(symbol);
      }
    } else {
      AppState.lastPrediction = symbol;
      AppState.predictionHoldCount = 1;
    }
  }
}

function appendSymbolToSentence(symbol) {
  if (AppState.lastAddedSymbol === symbol) return; // Prevent repeated character spam

  if (AppState.sentence.length === 0 || AppState.sentence === "Recognized gestures will assemble here...") {
    AppState.sentence = "";
  }

  // If word sign (e.g. HELLO, THANK_YOU, YES, NO), add with spaces
  const info = AppState.classes[symbol] || {};
  if (info.category === "word") {
    AppState.sentence += (AppState.sentence.length > 0 ? " " : "") + (info.name || symbol) + " ";
  } else {
    AppState.sentence += symbol;
  }

  AppState.lastAddedSymbol = symbol;
  renderSentence();

  // Reset lastAddedSymbol after short cooldown to allow repeating after slight hand reset
  setTimeout(() => {
    AppState.lastAddedSymbol = null;
  }, 1200);
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
// Tab 2: Dataset Studio & Collector
// ==========================================================================

function renderStudioClassSelector() {
  const container = document.getElementById("studio-class-selector");
  container.innerHTML = "";

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
  document.getElementById("studio-current-chip").textContent = label;
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
  searchInput.addEventListener("input", (e) => {
    renderDictionary(e.target.value.trim().toLowerCase());
  });

  document.querySelectorAll(".cat-btn[data-dict-cat]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-btn[data-dict-cat]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      AppState.dictCategory = btn.getAttribute("data-dict-cat");
      renderDictionary(searchInput.value.trim().toLowerCase());
    });
  });

  document.getElementById("btn-close-modal").addEventListener("click", () => {
    document.getElementById("practice-modal").style.display = "none";
    AppState.practiceTarget = null;
  });
}

function renderDictionary(filterQuery = "") {
  const grid = document.getElementById("dictionary-cards-grid");
  grid.innerHTML = "";

  const entries = Object.entries(AppState.classes).filter(([key, val]) => {
    if (AppState.dictCategory !== "all" && val.category !== AppState.dictCategory) {
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

    card.innerHTML = `
      <div class="sign-card-top">
        <div class="sign-badge">${key}</div>
        <span class="hand-tag ${handTagClass}">${handTagText}</span>
      </div>
      <div>
        <h3 style="font-family: var(--font-display); font-size: 1.05rem; font-weight: 700;">${val.name}</h3>
        <span style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">${val.category}</span>
      </div>
      <p class="sign-card-desc">${val.description || "Hold hands in designated pose."}</p>
      <div class="sign-card-tip"><i class="fa-solid fa-lightbulb"></i> ${val.tips || "Hold steady inside frame."}</div>
      <div class="sign-card-actions">
        <button class="btn btn-secondary btn-sm" style="width: 100%;" onclick="openPracticeModal('${key}')">
          <i class="fa-solid fa-bullseye"></i> Practice In Camera
        </button>
      </div>
    `;

    grid.appendChild(card);
  });
}

window.openPracticeModal = function(signKey) {
  const info = AppState.classes[signKey];
  if (!info) return;

  AppState.practiceTarget = signKey;
  AppState.practiceHoldCount = 0;

  document.getElementById("modal-sign-name").textContent = `${signKey} (${info.name})`;
  document.getElementById("modal-sign-desc").textContent = info.description;
  document.getElementById("modal-tip-box").textContent = `Tip: ${info.tips}`;
  document.getElementById("modal-match-status").textContent = "Waiting for Pose...";
  document.getElementById("modal-match-status").style.color = "var(--accent-amber)";

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
    AppState.practiceTarget = null;
  }, 2200);
}
