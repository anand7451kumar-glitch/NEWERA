
// ==========================================
// CLIPNEST — Your Personal Code Library
// ==========================================

const STORAGE_KEY = "clipnest-snippets-v1";

// DOM helper
const $ = (id) => document.getElementById(id);

// App state
let snippets = loadSnippets();
let currentFilter = "all";
let currentLanguage = null;

// ==========================================
// 1. STORAGE
// ==========================================

function loadSnippets() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch (error) {
    console.error("Could not load snippets:", error);
    return [];
  }
}

function saveSnippets() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(snippets));
}

// ==========================================
// 2. SECURITY HELPER
// Prevent user-entered text from becoming HTML
// ==========================================

function escapeHTML(value = "") {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  })[char]);
}

// ==========================================
// 3. STATISTICS
// ==========================================

function renderStats() {
  $("totalSnippets").textContent = snippets.length;

  const languages = new Set(
    snippets.map((snippet) => snippet.language)
  );

  $("totalLanguages").textContent = languages.size;

  $("totalFavorites").textContent = snippets.filter(
    (snippet) => snippet.favorite
  ).length;
}

// ==========================================
// 4. FILTERING AND SEARCH
// ==========================================

function getFilteredSnippets() {
  let result = [...snippets];

  if (currentFilter === "favorites") {
    result = result.filter((snippet) => snippet.favorite);
  }

  if (currentLanguage) {
    result = result.filter(
      (snippet) => snippet.language === currentLanguage
    );
  }

  const search = $("searchInput").value.trim().toLowerCase();

  if (search) {
    result = result.filter((snippet) => {
      const searchableText = [
        snippet.title,
        snippet.description,
        snippet.language,
        snippet.code,
        ...(snippet.tags || [])
      ].join(" ").toLowerCase();

      return searchableText.includes(search);
    });
  }

  const sort = $("sortSelect").value;

  if (sort === "newest") {
    result.sort((a, b) => b.createdAt - a.createdAt);
  } else if (sort === "oldest") {
    result.sort((a, b) => a.createdAt - b.createdAt);
  } else if (sort === "az") {
    result.sort((a, b) => a.title.localeCompare(b.title));
  }

  return result;
}

// ==========================================
// 5. RENDER SNIPPETS
// ==========================================

function renderSnippets() {
  const grid = $("snippetsGrid");
  const filtered = getFilteredSnippets();

  $("snippetCount").textContent =
    `${filtered.length} ${filtered.length === 1 ? "item" : "items"}`;

  if (currentFilter === "favorites") {
    $("libraryTitle").textContent = "Favourites";
  } else if (currentLanguage) {
    $("libraryTitle").textContent = currentLanguage;
  } else {
    $("libraryTitle").textContent = "All snippets";
  }

  if (filtered.length === 0) {
    const isEmpty = snippets.length === 0;

    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">${isEmpty ? "⌘" : "⌕"}</div>
        <h3>${isEmpty ? "Your library is empty" : "No snippets found"}</h3>
        <p>
          ${isEmpty
            ? "Save your first useful piece of code and keep it close."
            : "Try another search or change your filters."}
        </p>
        ${isEmpty
          ? '<button class="primary-button" id="emptyAddButton">＋ Add your first snippet</button>'
          : ""}
      </div>
    `;

    return;
  }

  grid.innerHTML = filtered.map((snippet) => {
    const tags = (snippet.tags || []).map((tag) =>
      `<span class="tag">${escapeHTML(tag)}</span>`
    ).join("");

    const favoriteClass = snippet.favorite ? "is-favorite" : "";

    return `
      <article class="snippet-card" data-id="${escapeHTML(snippet.id)}">

        <div class="snippet-card-top">
          <span class="language-badge">
            ${escapeHTML(snippet.language)}
          </span>

          <button
            class="favorite-button ${favoriteClass}"
            data-action="favorite"
            data-id="${escapeHTML(snippet.id)}"
            title="Toggle favourite"
            aria-label="Toggle favourite"
          >${snippet.favorite ? "★" : "☆"}</button>
        </div>

        <h3 class="snippet-title">${escapeHTML(snippet.title)}</h3>

        <p class="snippet-description">
          ${escapeHTML(snippet.description || "No description added.")}
        </p>

        <div class="code-preview">
          <pre>${escapeHTML(snippet.code)}</pre>
        </div>

        <div class="snippet-card-bottom">
          <div class="snippet-tags">${tags}</div>

          <div class="card-actions">
            <button
              class="card-action"
              data-action="copy"
              data-id="${escapeHTML(snippet.id)}"
            >Copy</button>

            <button
              class="card-action"
              data-action="edit"
              data-id="${escapeHTML(snippet.id)}"
            >Edit</button>

            <button
              class="card-action"
              data-action="delete"
              data-id="${escapeHTML(snippet.id)}"
            >×</button>
          </div>
        </div>

      </article>
    `;
  }).join("");
}

// ==========================================
// 6. RENDER EVERYTHING
// ==========================================

function renderApp() {
  renderStats();
  renderSnippets();
}

// ==========================================
// 7. MODAL CONTROLS
// ==========================================

function openModal(snippet = null) {
  $("snippetForm").reset();
  $("snippetId").value = "";

  if (snippet) {
    $("modalTitle").textContent = "Edit snippet";

    $("snippetId").value = snippet.id;
    $("snippetName").value = snippet.title;
    $("snippetDescription").value = snippet.description || "";
    $("snippetLanguage").value = snippet.language;
    $("snippetTags").value = (snippet.tags || []).join(", ");
    $("snippetCode").value = snippet.code;
  } else {
    $("modalTitle").textContent = "Add a snippet";
    $("snippetLanguage").value = "Python";
  }

  $("snippetModal").classList.remove("hidden");
  $("snippetName").focus();
}

function closeModal() {
  $("snippetModal").classList.add("hidden");
}

// ==========================================
// 8. ADD AND EDIT SNIPPETS
// ==========================================

function handleFormSubmit(event) {
  event.preventDefault();

  const id = $("snippetId").value;

  const title = $("snippetName").value.trim();
  const description = $("snippetDescription").value.trim();
  const language = $("snippetLanguage").value;
  const code = $("snippetCode").value.trim();

  const tags = $("snippetTags").value
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

  if (!title || !code) {
    showToast("Please enter a title and some code.");
    return;
  }

  if (id) {
    const existing = snippets.find((item) => item.id === id);

    if (!existing) return;

    existing.title = title;
    existing.description = description;
    existing.language = language;
    existing.code = code;
    existing.tags = tags;

    showToast("Snippet updated successfully.");
  } else {
    const newSnippet = {
      id: crypto.randomUUID(),
      title,
      description,
      language,
      code,
      tags,
      favorite: false,
      createdAt: Date.now()
    };

    snippets.unshift(newSnippet);
    showToast("Snippet saved to your library.");
  }

  saveSnippets();
  closeModal();
  renderApp();
}

// ==========================================
// 9. FAVORITES
// ==========================================

function toggleFavorite(id) {
  const snippet = snippets.find((item) => item.id === id);

  if (!snippet) return;

  snippet.favorite = !snippet.favorite;

  saveSnippets();
  renderApp();

  showToast(
    snippet.favorite
      ? "Added to favourites."
      : "Removed from favourites."
  );
}

// ==========================================
// 10. DELETE SNIPPETS
// ==========================================

function deleteSnippet(id) {
  const snippet = snippets.find((item) => item.id === id);

  if (!snippet) return;

  const confirmed = window.confirm(
    `Delete "${snippet.title}" permanently?`
  );

  if (!confirmed) return;

  snippets = snippets.filter((item) => item.id !== id);

  saveSnippets();
  renderApp();

  showToast("Snippet deleted.");
}

// ==========================================
// 11. COPY CODE
// ==========================================

async function copySnippet(id) {
  const snippet = snippets.find((item) => item.id === id);

  if (!snippet) return;

  try {
    await navigator.clipboard.writeText(snippet.code);
    showToast("Code copied to clipboard!");
  } catch (error) {
    console.error("Clipboard error:", error);
    showToast("Clipboard access failed. Try localhost or HTTPS.");
  }
}

// ==========================================
// 12. NAVIGATION
// ==========================================

function setFilter(filter, language = null) {
  currentFilter = filter;
  currentLanguage = language;

  document.querySelectorAll(".nav-link").forEach((button) => {
    button.classList.remove("active");
  });

  const activeButton = language
    ? document.querySelector(`[data-language="${CSS.escape(language)}"]`)
    : document.querySelector(`[data-filter="${filter}"]`);

  if (activeButton) {
    activeButton.classList.add("active");
  }

  renderSnippets();
}

// ==========================================
// 13. TOAST NOTIFICATIONS
// ==========================================

let toastTimeout;

function showToast(message) {
  const toast = $("toast");

  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(toastTimeout);

  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2400);
}

// ==========================================
// 14. EVENT LISTENERS
// ==========================================

function setupEvents() {
  $("addSnippetButton").addEventListener("click", () => {
    openModal();
  });

  $("closeModal").addEventListener("click", closeModal);
  $("cancelModal").addEventListener("click", closeModal);

  $("snippetModal").addEventListener("click", (event) => {
    if (event.target === $("snippetModal")) {
      closeModal();
    }
  });

  $("snippetForm").addEventListener("submit", handleFormSubmit);

  $("searchInput").addEventListener("input", renderSnippets);
  $("sortSelect").addEventListener("change", renderSnippets);

  // All snippets and favourites
  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      setFilter(button.dataset.filter);
    });
  });

  // Language filters
  document.querySelectorAll("[data-language]").forEach((button) => {
    button.addEventListener("click", () => {
      setFilter("language", button.dataset.language);
    });
  });

  // Actions inside snippet cards
  $("snippetsGrid").addEventListener("click", (event) => {
    const button = event.target.closest("[data-action]");

    if (button) {
      const id = button.dataset.id;
      const action = button.dataset.action;

      if (action === "favorite") {
        toggleFavorite(id);
      }

      if (action === "copy") {
        copySnippet(id);
      }

      if (action === "edit") {
        const snippet = snippets.find((item) => item.id === id);

        if (snippet) {
          openModal(snippet);
        }
      }

      if (action === "delete") {
        deleteSnippet(id);
      }

      return;
    }

    if (event.target.id === "emptyAddButton") {
      openModal();
    }
  });

  // Keyboard shortcuts
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      $("searchInput").focus();
    }

    if (event.key === "Escape") {
      closeModal();
    }
  });
}

// ==========================================
// 15. START APPLICATION
// ==========================================

function init() {
  setupEvents();
  renderApp();
}

document.addEventListener("DOMContentLoaded", init);
