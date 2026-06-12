const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const contentEl = document.getElementById("content");
const dateEl = document.getElementById("today-date");

async function loadEvents() {
    try {
        const response = await fetch("/api/events");

        if (!response.ok) {
            throw new Error("Failed to fetch events");
        }

        const data = await response.json();

        dateEl.textContent = formatDate(data.month, data.day);

        renderList("events-list", data.events);
        renderList("births-list", data.births);
        renderList("deaths-list", data.deaths);

        loadingEl.hidden = true;
        contentEl.hidden = false;
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

function renderList(elementId, items) {
    const ul = document.getElementById(elementId);

    for (const item of items) {
        const li = document.createElement("li");
        li.innerHTML = "<strong>" + item.year + "</strong> " + item.text;
        ul.appendChild(li);
    }
}

loadEvents();
