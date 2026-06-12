const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const carouselEl = document.getElementById("carousel");
let dateText = "";
const track = document.getElementById("carousel-track");
const dotsEl = document.getElementById("dots");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");

let currentIndex = 0;
let totalCards = 0;

// --- Fetch data and kick off rendering ---

async function loadEvents() {
    try {
        const response = await fetch("/api/events");

        if (!response.ok) {
            throw new Error("Failed to fetch events");
        }

        const data = await response.json();

        dateText = formatDate(data.month, data.day);
        renderCards(data.facts);

        loadingEl.hidden = true;
        carouselEl.hidden = false;
    } catch (err) {
        loadingEl.hidden = true;
        errorEl.hidden = false;
        errorEl.textContent = "Something went wrong. Please try again later.";
    }
}

function formatDate(month, day) {
    const date = new Date(2000, month - 1, day);
    return date.toLocaleDateString("en-US", { month: "long", day: "numeric" });
}

// --- Build the cards and dots ---

function renderCards(facts) {
    totalCards = facts.length;

    for (const fact of facts) {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML =
            '<h1 class="card-title">On This Day</h1>' +
            '<p class="card-date">' + dateText + "</p>" +
            '<h2 class="card-year">Year ' + fact.year + "</h2>" +
            '<p class="card-text">' + fact.text + "</p>";
        track.appendChild(card);
    }

    // Create one dot per card
    for (let i = 0; i < totalCards; i++) {
        const dot = document.createElement("button");
        dot.className = "dot";
        dot.addEventListener("click", function () {
            goToCard(i);
        });
        dotsEl.appendChild(dot);
    }

    updateDots();
}

// --- Navigation ---

function goToCard(index) {
    currentIndex = index;
    track.style.transform = "translateX(-" + (currentIndex * 100) + "%)";
    updateDots();
}

function updateDots() {
    const dots = dotsEl.querySelectorAll(".dot");
    for (let i = 0; i < dots.length; i++) {
        if (i === currentIndex) {
            dots[i].classList.add("active");
        } else {
            dots[i].classList.remove("active");
        }
    }
}

prevBtn.addEventListener("click", function () {
    if (currentIndex > 0) {
        goToCard(currentIndex - 1);
    }
});

nextBtn.addEventListener("click", function () {
    if (currentIndex < totalCards - 1) {
        goToCard(currentIndex + 1);
    }
});

// --- Touch swipe support for mobile ---

let touchStartX = 0;

track.addEventListener("touchstart", function (e) {
    touchStartX = e.touches[0].clientX;
});

track.addEventListener("touchend", function (e) {
    const touchEndX = e.changedTouches[0].clientX;
    const diff = touchStartX - touchEndX;

    // Swipe left (next) if moved more than 50px
    if (diff > 50 && currentIndex < totalCards - 1) {
        goToCard(currentIndex + 1);
    }

    // Swipe right (prev) if moved more than 50px
    if (diff < -50 && currentIndex > 0) {
        goToCard(currentIndex - 1);
    }
});

// --- Start ---

loadEvents();
