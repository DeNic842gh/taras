<<<<<<< HEAD
const PLACEHOLDER_IMG =
  "data:image/svg+xml," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="560" viewBox="0 0 400 560">' +
      '<rect fill="#f5f0eb" width="400" height="560"/>' +
      '<text x="200" y="280" text-anchor="middle" fill="#7a1f2e" font-family="sans-serif" font-size="18">Marine</text>' +
      "</svg>"
  );

const GALLERY = Array.from({ length: 10 }, (_, i) => {
  const num = String(i + 1).padStart(2, "0");
  return `assets/Houshou-Marine_pr-img_${num}.png`;
});

function bindImageFallback(img) {
  img.addEventListener(
    "error",
    () => {
      if (img.src !== PLACEHOLDER_IMG) img.src = PLACEHOLDER_IMG;
    },
    { once: true }
  );
}

const API_BASE = `${window.location.origin}/api/v1`;
const STORAGE_TOKEN = "marine_auth_token";
const STORAGE_USER = "marine_auth_user";

const mainVisual = document.getElementById("main-visual");
const visualWatermark = document.getElementById("visual-watermark");
const thumbList = document.getElementById("thumb-list");
const treasureBtn = document.getElementById("treasure-btn");
const laughBtn = document.getElementById("laugh-btn");
const marineAudio = document.getElementById("marine-audio");
const laughAudio = document.getElementById("laugh-audio");

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
    bindImageFallback(img);
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

function spawnButtonBurst(btn) {
  const item = btn.closest(".action-item");
  const container = item?.querySelector(".button-burst");
  const imgSrc = btn.querySelector("img")?.src;
  if (!container || !imgSrc) return;

  container.innerHTML = "";
  const count = 12;
  for (let i = 0; i < count; i += 1) {
    const mini = document.createElement("img");
    mini.className = "burst-mini";
    mini.src = imgSrc;
    mini.alt = "";
    const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.35;
    const distance = 65 + Math.random() * 55;
    mini.style.setProperty("--tx", `${Math.cos(angle) * distance}px`);
    mini.style.setProperty("--ty", `${Math.sin(angle) * distance}px`);
    mini.style.setProperty("--rot", `${Math.floor(Math.random() * 360 - 180)}deg`);
    mini.style.setProperty("--scale", `${0.22 + Math.random() * 0.12}`);
    container.appendChild(mini);
  }
  window.setTimeout(() => {
    container.innerHTML = "";
  }, 850);
}

function playSound(btn, audio) {
  btn.classList.remove("treasure-hit");
  void btn.offsetWidth;
  btn.classList.add("treasure-hit");
  spawnButtonBurst(btn);
  if (audio) {
    audio.currentTime = 0;
    audio.play().catch(() => {});
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

bindImageFallback(mainVisual);
bindImageFallback(treasureBtn.querySelector("img"));
bindImageFallback(laughBtn.querySelector("img"));

buildGallery();
treasureBtn.addEventListener("click", () => playSound(treasureBtn, marineAudio));
laughBtn.addEventListener("click", () => playSound(laughBtn, laughAudio));
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
=======
const PLACEHOLDER_IMG =
  "data:image/svg+xml," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="560" viewBox="0 0 400 560">' +
      '<rect fill="#f5f0eb" width="400" height="560"/>' +
      '<text x="200" y="280" text-anchor="middle" fill="#7a1f2e" font-family="sans-serif" font-size="18">Marine</text>' +
      "</svg>"
  );

const GALLERY = Array.from({ length: 10 }, (_, i) => {
  const num = String(i + 1).padStart(2, "0");
  return `assets/Houshou-Marine_pr-img_${num}.png`;
});

function bindImageFallback(img) {
  img.addEventListener(
    "error",
    () => {
      if (img.src !== PLACEHOLDER_IMG) img.src = PLACEHOLDER_IMG;
    },
    { once: true }
  );
}

const API_BASE = `${window.location.origin}/api/v1`;
const STORAGE_TOKEN = "marine_auth_token";
const STORAGE_USER = "marine_auth_user";

const mainVisual = document.getElementById("main-visual");
const visualWatermark = document.getElementById("visual-watermark");
const thumbList = document.getElementById("thumb-list");
const treasureBtn = document.getElementById("treasure-btn");
const laughBtn = document.getElementById("laugh-btn");
const marineAudio = document.getElementById("marine-audio");
const laughAudio = document.getElementById("laugh-audio");

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
    bindImageFallback(img);
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

function spawnButtonBurst(btn) {
  const item = btn.closest(".action-item");
  const container = item?.querySelector(".button-burst");
  const imgSrc = btn.querySelector("img")?.src;
  if (!container || !imgSrc) return;

  container.innerHTML = "";
  const count = 12;
  for (let i = 0; i < count; i += 1) {
    const mini = document.createElement("img");
    mini.className = "burst-mini";
    mini.src = imgSrc;
    mini.alt = "";
    const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.35;
    const distance = 65 + Math.random() * 55;
    mini.style.setProperty("--tx", `${Math.cos(angle) * distance}px`);
    mini.style.setProperty("--ty", `${Math.sin(angle) * distance}px`);
    mini.style.setProperty("--rot", `${Math.floor(Math.random() * 360 - 180)}deg`);
    mini.style.setProperty("--scale", `${0.22 + Math.random() * 0.12}`);
    container.appendChild(mini);
  }
  window.setTimeout(() => {
    container.innerHTML = "";
  }, 850);
}

function playSound(btn, audio) {
  btn.classList.remove("treasure-hit");
  void btn.offsetWidth;
  btn.classList.add("treasure-hit");
  spawnButtonBurst(btn);
  if (audio) {
    audio.currentTime = 0;
    audio.play().catch(() => {});
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

bindImageFallback(mainVisual);
bindImageFallback(treasureBtn.querySelector("img"));
bindImageFallback(laughBtn.querySelector("img"));

buildGallery();
treasureBtn.addEventListener("click", () => playSound(treasureBtn, marineAudio));
laughBtn.addEventListener("click", () => playSound(laughBtn, laughAudio));
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
>>>>>>> 3fd317d37b7cea1ba60607af56a3a56bc53120a9
