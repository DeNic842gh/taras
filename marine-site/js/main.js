const OUTFITS = [
  {
    id: "pirate",
    nameEn: "Classic Pirate Captain",
    nameJp: "定番パイレーツ",
    emoji: "🏴‍☠️",
    bg: "linear-gradient(165deg, #0d1b3e 0%, #ca3c28 70%)",
    image:
      "https://hololive.hololivepro.com/wp-content/uploads/2020/06/463ab1fa7f0b84d0c3391ea1a679aecb.png",
  },
  {
    id: "newyear",
    nameEn: "New Year Kimono",
    nameJp: "謹賀新年・振袖",
    emoji: "🎍",
    bg: "linear-gradient(165deg, #1a0a14 0%, #ca3c28 45%, #f5c542 100%)",
    image: "https://img.youtube.com/vi/OjD0m6SSdh8/hqdefault.jpg",
  },
  {
    id: "gothic",
    nameEn: "Gothic Lolita",
    nameJp: "堕天使ゴシック",
    emoji: "🦇",
    bg: "linear-gradient(165deg, #120818 0%, #4a1942 50%, #ca3c28 100%)",
    image: "https://img.youtube.com/vi/QfGuQELt1Tk/hqdefault.jpg",
  },
  {
    id: "swimsuit",
    nameEn: "Summer Sailor Swimsuit",
    nameJp: "盛夏の水着マリン",
    emoji: "⛱️",
    bg: "linear-gradient(165deg, #0d4d7a 0%, #ca3c28 55%, #f5c542 100%)",
    image: "https://img.youtube.com/vi/vV-5W7SFHDc/hqdefault.jpg",
  },
  {
    id: "office",
    nameEn: "Office Captain",
    nameJp: "マリン社長・OL",
    emoji: "💼",
    bg: "linear-gradient(165deg, #1c2838 0%, #ca3c28 60%)",
    image: "https://img.youtube.com/vi/u_hUpHUTJwQ/hqdefault.jpg",
  },
  {
    id: "marching",
    nameEn: "Marching Band Marine",
    nameJp: "マーチングバンド",
    emoji: "🎺",
    bg: "linear-gradient(165deg, #0d1b3e 0%, #ca3c28 40%, #f5c542 90%)",
    image: "https://img.youtube.com/vi/gZL4-f3jRoE/hqdefault.jpg",
  },
  {
    id: "sister",
    nameEn: "Sister Marine",
    nameJp: "シスターマリン",
    emoji: "✝️",
    bg: "linear-gradient(165deg, #1a1a2e 0%, #2d2d5a 50%, #ca3c28 100%)",
    image: "https://img.youtube.com/vi/KfZR9jVP6tw/hqdefault.jpg",
  },
  {
    id: "treasure",
    nameEn: "Treasure Box Gala",
    nameJp: "トレジャーボックス",
    emoji: "💎",
    bg: "linear-gradient(165deg, #2a1050 0%, #ca3c28 50%, #f5c542 100%)",
    image: "https://img.youtube.com/vi/vV-5W7SFHDc/hqdefault.jpg",
  },
];

const SONGS = [
  {
    title: "Ahoy!! We are Houshou Pirates",
    titleJp: "Ahoy!! 我ら宝鐘海賊団☆",
    description:
      "Marine's first original — a catchy pirate anthem that hit a million views in ten days. Signature Ahoy! energy.",
    url: "https://www.youtube.com/watch?v=gZL4-f3jRoE",
  },
  {
    title: "Unison",
    titleJp: "Unison",
    description:
      "Second single with Yunomi. A genre-bending track with an MV animated by six artists — wildly addictive.",
    url: "https://www.youtube.com/watch?v=OjD0m6SSdh8",
  },
  {
    title: "Bishoujo Muzai ♡ Pirates",
    titleJp: "美少女無罪♡パイレーツ",
    description:
      "Full anime MV love song — one of her biggest hits with stunning animation and pirate charm.",
    url: "https://www.youtube.com/watch?v=KfZR9jVP6tw",
  },
  {
    title: "Marine Set Sail!!",
    titleJp: "マリン出航！！",
    description:
      "Original animation MV — Marine launches on a grand voyage with cinematic production.",
    url: "https://www.youtube.com/watch?v=u_hUpHUTJwQ",
  },
  {
    title: "Ghost Ship Battle",
    titleJp: "幽霊船戦",
    description:
      "Epic original anime MV with music by Toby Fox. Retro adventure on the ghost seas.",
    url: "https://www.youtube.com/watch?v=QfGuQELt1Tk",
  },
  {
    title: "I'm Your Treasure Box",
    titleJp: "あなたはマリン船長をたからばこから見つけた",
    description:
      "Birthday MV treasure hunt — lavish animation and a fan-favorite celebration stream tie-in.",
    url: "https://www.youtube.com/watch?v=vV-5W7SFHDc",
  },
  {
    title: "SHINKIRO",
    titleJp: "SHINKIRO",
    description:
      "Showa-flavored city pop duet with Gawr Gura — stylish retro MV with millions of views.",
    url: "https://www.youtube.com/watch?v=9ehwhQJ50gs",
  },
];

let currentOutfit = OUTFITS[0];

function setOutfit(outfit) {
  currentOutfit = outfit;
  const frame = document.getElementById("hero-outfit-frame");
  const img = document.getElementById("hero-outfit-img");
  document.getElementById("outfit-name-en").textContent = outfit.nameEn;
  document.getElementById("outfit-name-jp").textContent = outfit.nameJp;
  frame.style.setProperty("--outfit-bg", outfit.bg);

  img.style.display = "block";
  frame.classList.remove("show-emoji");
  frame.dataset.fallback = outfit.emoji;
  img.style.opacity = "0";
  img.onload = () => {
    img.style.opacity = "1";
  };
  img.onerror = () => {
    img.style.display = "none";
    frame.classList.add("show-emoji");
  };
  img.src = outfit.image;
  img.alt = `Houshou Marine — ${outfit.nameEn}`;

  document.querySelectorAll(".outfit-btn, .outfit-card").forEach((el) => {
    el.classList.toggle("active", el.dataset.id === outfit.id);
  });
}

function buildOutfitPicker() {
  const picker = document.getElementById("outfit-picker");
  const gallery = document.getElementById("outfit-gallery");

  OUTFITS.forEach((outfit) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "outfit-btn";
    btn.dataset.id = outfit.id;
    btn.textContent = outfit.nameEn.split(" ")[0];
    btn.title = outfit.nameEn;
    btn.addEventListener("click", () => setOutfit(outfit));
    picker.appendChild(btn);

    const card = document.createElement("article");
    card.className = "outfit-card";
    card.dataset.id = outfit.id;
    card.innerHTML = `
      <div class="outfit-card-thumb" style="--card-bg: ${outfit.bg}">${outfit.emoji}</div>
      <div class="outfit-card-body">
        <h3>${outfit.nameEn}</h3>
        <p>${outfit.nameJp}</p>
      </div>
    `;
    card.addEventListener("click", () => {
      setOutfit(outfit);
      document.getElementById("top").scrollIntoView({ behavior: "smooth" });
    });
    gallery.appendChild(card);
  });
}

function buildSongs() {
  const grid = document.getElementById("song-grid");
  SONGS.forEach((song) => {
    const card = document.createElement("article");
    card.className = "song-card";
    card.innerHTML = `
      <h3>${song.title}</h3>
      <p><em>${song.titleJp}</em></p>
      <p>${song.description}</p>
      <a href="${song.url}" target="_blank" rel="noopener">Watch on YouTube →</a>
    `;
    grid.appendChild(card);
  });
}

buildOutfitPicker();
buildSongs();
setOutfit(OUTFITS[0]);
