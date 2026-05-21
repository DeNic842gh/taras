const GALLERY = Array.from({ length: 10 }, (_, i) => {
  const num = String(i + 1).padStart(2, "0");
  return `assets/Houshou-Marine_pr-img_${num}.png`;
});

const API_BASE = `${window.location.origin}/api/v1`;
const STORAGE_TOKEN = "marine_auth_token";
const STORAGE_USER = "marine_auth_user";

const mainVisual = document.getElementById("main-visual");
const visualWatermark = document.getElementById("visual-watermark");
const thumbList = document.getElementById("thumb-list");
const treasureBtn = document.getElementById("treasure-btn");
const treasureBurst = document.getElementById("treasure-burst");
const marineAudio = document.getElementById("marine-audio");

const userBadge = document.getElementById("user-badge");
const userDisplayName = document.getElementById("user-display-name");
const authOpenBtn = document.getElementById("auth-open-btn");
const logoutBtn = document.getElementById("logout-btn");
const authOverlay = document.getElementById("auth-overlay");
const authClose = document.getElementById("auth-close");
const authError = document.getElementById("auth-error");
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const authTabs = document.querySelectorAll(".auth-tab");

function setMainImage(src) {
  mainVisual.src = src;
  mainVisual.alt = "Houshou Marine";
  visualWatermark.style.backgroundImage = `url("${src}")`;
}

function buildGallery() {
  GALLERY.forEach((src, index) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.setAttribute("aria-label", `Outfit ${index + 1}`);
    if (index === 0) btn.classList.add("active");

    const img = document.createElement("img");
    img.src = src;
    img.alt = "";
    btn.appendChild(img);

    btn.addEventListener("click", () => {
      document.querySelectorAll(".thumb-list button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      setMainImage(src);
    });

    li.appendChild(btn);
    thumbList.appendChild(li);
  });
  setMainImage(GALLERY[0]);
}

function spawnBurst() {
  treasureBurst.innerHTML = "";
  const count = 14;
  for (let i = 0; i < count; i += 1) {
    const particle = document.createElement("span");
    particle.className = "burst-particle";
    const angle = (Math.PI * 2 * i) / count;
    const distance = 80 + Math.random() * 40;
    particle.style.setProperty("--tx", `${Math.cos(angle) * distance}px`);
    particle.style.setProperty("--ty", `${Math.sin(angle) * distance}px`);
    treasureBurst.appendChild(particle);
  }
  window.setTimeout(() => {
    treasureBurst.innerHTML = "";
  }, 750);
}

function playTreasure() {
  treasureBtn.classList.remove("treasure-hit");
  void treasureBtn.offsetWidth;
  treasureBtn.classList.add("treasure-hit");
  spawnBurst();
  if (marineAudio) {
    marineAudio.currentTime = 0;
    marineAudio.play().catch(() => {});
  }
}

function getStoredAuth() {
  const token = localStorage.getItem(STORAGE_TOKEN);
  const raw = localStorage.getItem(STORAGE_USER);
  if (!token || !raw) return null;
  try {
    return { token, user: JSON.parse(raw) };
  } catch {
    return null;
  }
}

function setAuthUI(user) {
  if (user) {
    userBadge.hidden = false;
    userDisplayName.textContent = user.username;
    authOpenBtn.hidden = true;
    logoutBtn.hidden = false;
  } else {
    userBadge.hidden = true;
    authOpenBtn.hidden = false;
    logoutBtn.hidden = true;
    authOpenBtn.textContent = "Log in";
  }
}

function saveAuth(token, user) {
  localStorage.setItem(STORAGE_TOKEN, token);
  localStorage.setItem(STORAGE_USER, JSON.stringify(user));
  setAuthUI(user);
}

function clearAuth() {
  localStorage.removeItem(STORAGE_TOKEN);
  localStorage.removeItem(STORAGE_USER);
  setAuthUI(null);
}

function showAuthError(message) {
  authError.textContent = message;
  authError.hidden = !message;
}

function openAuth(tab = "login") {
  authOverlay.hidden = false;
  switchAuthTab(tab);
  showAuthError("");
}

function closeAuth() {
  authOverlay.hidden = true;
  showAuthError("");
}

function switchAuthTab(tab) {
  authTabs.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tab);
  });
  loginForm.hidden = tab !== "login";
  registerForm.hidden = tab !== "register";
}

async function apiAuth(path, body) {
  const response = await fetch(`${API_BASE}/auth/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    const message = Array.isArray(detail)
      ? detail.map((e) => e.msg).join(", ")
      : detail || "Request failed";
    throw new Error(message);
  }
  return data;
}

async function verifySession(token) {
  const response = await fetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) return null;
  return response.json();
}

async function handleLogin(event) {
  event.preventDefault();
  showAuthError("");
  const form = new FormData(loginForm);
  try {
    const data = await apiAuth("login", {
      email: form.get("email"),
      password: form.get("password"),
    });
    saveAuth(data.access_token, data.user);
    closeAuth();
  } catch (err) {
    showAuthError(err.message);
  }
}

async function handleRegister(event) {
  event.preventDefault();
  showAuthError("");
  const form = new FormData(registerForm);
  try {
    const data = await apiAuth("register", {
      username: form.get("username"),
      email: form.get("email"),
      password: form.get("password"),
    });
    saveAuth(data.access_token, data.user);
    closeAuth();
  } catch (err) {
    showAuthError(err.message);
  }
}

async function initAuth() {
  const stored = getStoredAuth();
  if (!stored) {
    setAuthUI(null);
    return;
  }
  const user = await verifySession(stored.token);
  if (user) {
    saveAuth(stored.token, user);
  } else {
    clearAuth();
  }
}

buildGallery();
treasureBtn.addEventListener("click", playTreasure);
authOpenBtn.addEventListener("click", () => openAuth("login"));
authClose.addEventListener("click", closeAuth);
authOverlay.addEventListener("click", (e) => {
  if (e.target === authOverlay) closeAuth();
});
logoutBtn.addEventListener("click", clearAuth);
loginForm.addEventListener("submit", handleLogin);
registerForm.addEventListener("submit", handleRegister);
authTabs.forEach((tab) => {
  tab.addEventListener("click", () => switchAuthTab(tab.dataset.tab));
});

initAuth();
