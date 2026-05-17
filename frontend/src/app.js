const state = {
  apiBase: localStorage.getItem("victory.apiBase") || "/api",
  token: localStorage.getItem("victory.accessToken") || "",
  refreshToken: localStorage.getItem("victory.refreshToken") || "",
  selectedOrganizationId: Number(localStorage.getItem("victory.organizationId")) || null,
  selectedProjectId: Number(localStorage.getItem("victory.projectId")) || null,
  selectedBoardId: Number(localStorage.getItem("victory.boardId")) || null,
  selectedTaskId: null,
  aiSummary: null,
  draggedTaskId: null,
  authMode: "login",
  currentPage: ["tasks", "boards", "projects", "organizations"].includes(localStorage.getItem("victory.page"))
    ? localStorage.getItem("victory.page")
    : "tasks",
  userEmail: localStorage.getItem("victory.userEmail") || "",
  projectSearch: "",
  projectsCollapsed: false,
  currentUser: null,
  isRefreshing: false,
  refreshSubscribers: [],
  data: {
    users: [],
    organizations: [],
    projects: [],
    boards: [],
    columns: [],
    tasks: [],
    comments: [],
    activities: []
  }
};

const endpoints = {
  users: "/identity/users/",
  organizations: "/organizations/",
  projects: "/projects/",
  boards: "/boards/",
  columns: "/columns/",
  tasks: "/tasks/",
  comments: "/comments/",
  activities: "/activities/"
};

const els = {
  navItems: document.querySelectorAll(".nav-item"),
  pagePanels: document.querySelectorAll("[data-page-panel]"),
  navProjectSearch: document.querySelector("#navProjectSearch"),
  navProjectList: document.querySelector("#navProjectList"),
  globalSearchResults: document.querySelector("#globalSearchResults"),
  openNavProjectDialog: document.querySelector("#openNavProjectDialog"),
  navProjectDialog: document.querySelector("#navProjectDialog"),
  navProjectForm: document.querySelector("#navProjectForm"),
  navProjectOrgSelect: document.querySelector("#navProjectOrgSelect"),
  cancelNavProjectButton: document.querySelector("#cancelNavProjectButton"),
  projectsCollapseButton: document.querySelector("#projectsCollapseButton"),
  organizationForm: document.querySelector("#organizationForm"),
  organizationInsights: document.querySelector("#organizationInsights"),
  organizationList: document.querySelector("#organizationList"),
  projectManagementForm: document.querySelector("#projectManagementForm"),
  projectInsights: document.querySelector("#projectInsights"),
  projectOrgSelect: document.querySelector("#projectOrgSelect"),
  projectList: document.querySelector("#projectList"),
  boardManagementForm: document.querySelector("#boardManagementForm"),
  boardInsights: document.querySelector("#boardInsights"),
  boardProjectSelect: document.querySelector("#boardProjectSelect"),
  boardList: document.querySelector("#boardList"),
  organizationSelect: document.querySelector("#organizationSelect"),
  projectSelect: document.querySelector("#projectSelect"),
  boardSelect: document.querySelector("#boardSelect"),
  contextForm: document.querySelector("#contextForm"),
  authEmail: document.querySelector("#authEmail"),
  authPassword: document.querySelector("#authPassword"),
  authName: document.querySelector("#authName"),
  authNameField: document.querySelector("#authNameField"),
  authForm: document.querySelector("#authForm"),
  authLoginTab: document.querySelector("#authLoginTab"),
  authRegisterTab: document.querySelector("#authRegisterTab"),
  loginButton: document.querySelector("#loginButton"),
  registerButton: document.querySelector("#registerButton"),
  logoutButton: document.querySelector("#logoutButton"),
  profileForm: document.querySelector("#profileForm"),
  profileName: document.querySelector("#profileName"),
  profileEmail: document.querySelector("#profileEmail"),
  profilePassword: document.querySelector("#profilePassword"),
  saveProfileButton: document.querySelector("#saveProfileButton"),
  accountAvatar: document.querySelector("#accountAvatar"),
  accountTitle: document.querySelector("#accountTitle"),
  accountSubtitle: document.querySelector("#accountSubtitle"),
  profileStats: document.querySelector("#profileStats"),
  accountSnapshot: document.querySelector("#accountSnapshot"),
  tokenState: document.querySelector("#tokenState"),
  authMessage: document.querySelector("#authMessage"),
  profileButton: document.querySelector("#profileButton"),
  profileLabel: document.querySelector("#profileLabel"),
  profileCompany: document.querySelector("#profileCompany"),
  authView: document.querySelector("#authView"),
  closeAuthButton: document.querySelector("#closeAuthButton"),
  newColumnButton: document.querySelector("#newColumnButton"),
  newTaskButton: document.querySelector("#newTaskButton"),
  boardTitle: document.querySelector("#boardTitle"),
  taskOverview: document.querySelector("#taskOverview"),
  emptyState: document.querySelector("#emptyState"),
  kanbanBoard: document.querySelector("#kanbanBoard"),
  overlay: document.querySelector("#overlay"),
  taskDrawer: document.querySelector("#taskDrawer"),
  drawerTitle: document.querySelector("#drawerTitle"),
  closeDrawerButton: document.querySelector("#closeDrawerButton"),
  taskForm: document.querySelector("#taskForm"),
  deleteTaskButton: document.querySelector("#deleteTaskButton"),
  catchupButton: document.querySelector("#catchupButton"),
  taskExtra: document.querySelector("#taskExtra"),
  aiSummaryPanel: document.querySelector("#aiSummaryPanel"),
  columnDialog: document.querySelector("#columnDialog"),
  columnForm: document.querySelector("#columnForm"),
  cancelColumnButton: document.querySelector("#cancelColumnButton")
};

function setStatus() {}

function log() {}

function apiUrl(path) {
  return `${state.apiBase.replace(/\/$/, "")}${path}`;
}

function requestHeaders(hasBody = false, useRefreshToken = false) {
  const headers = {};
  if (hasBody) headers["content-type"] = "application/json";
  const token = useRefreshToken ? state.refreshToken : state.token;
  if (token) headers.authorization = `Bearer ${token}`;
  return headers;
}

async function request(path, options = {}) {
  const method = options.method || "GET";
  setStatus("Запрос...");

  try {
    const response = await fetch(apiUrl(path), {
      ...options,
      headers: {
        ...requestHeaders(options.body !== undefined),
        ...(options.headers || {})
      }
    });

    if (response.status === 401 && !path.includes("/login") && !path.includes("/register") && !path.includes("/refresh")) {
      if (state.refreshToken) {
        try {
          const newToken = await refreshToken();
          return await request(path, options);
        } catch (refreshError) {
          logout();
          openAuthView();
          throw new Error("Сессия истекла. Войдите заново.");
        }
      } else {
        logout();
        openAuthView();
        throw new Error("Требуется авторизация.");
      }
    }

    const text = await response.text();
    const payload = text ? parseJson(text) : null;
    log(`${method} ${path} -> ${response.status}`, payload);

    if (!response.ok) {
      setStatus(`Ошибка ${response.status}`, true);
      throw new Error(formatApiError(payload, text, response.status));
    }

    setStatus("Готово");
    return payload;
  } catch (error) {
    setStatus("Ошибка сети", true);
    throw error;
  }
}

async function refreshToken() {
  if (state.isRefreshing) {
    return new Promise((resolve, reject) => {
      state.refreshSubscribers.push({ resolve, reject });
    });
  }

  state.isRefreshing = true;
  try {
    const data = await fetch(apiUrl("/refresh"), {
      method: "POST",
      headers: requestHeaders(false, true)
    });

    if (!data.ok) throw new Error("Refresh failed");

    const tokenInfo = await data.json();
    state.token = tokenInfo.access_token;
    localStorage.setItem("victory.accessToken", state.token);
    
    state.refreshSubscribers.forEach((s) => s.resolve(state.token));
    state.refreshSubscribers = [];
    return state.token;
  } catch (error) {
    state.refreshSubscribers.forEach((s) => s.reject(error));
    state.refreshSubscribers = [];
    throw error;
  } finally {
    state.isRefreshing = false;
  }
}

function formatApiError(payload, text, status) {
  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => `${item.loc?.join(".") || "field"}: ${item.msg}`)
      .join("\n");
  }

  if (payload?.detail) return String(payload.detail);
  if (typeof payload === "string") return payload;
  return text || `HTTP ${status}`;
}

function parseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function loadAll() {
  const keys = Object.keys(endpoints);
  const results = await Promise.allSettled(
    keys.map(async (key) => {
      state.data[key] = await request(endpoints[key]);
    })
  );

  const failed = results.filter((result) => result.status === "rejected");
  if (failed.length) {
    setStatus(`Ошибок загрузки: ${failed.length}`, true);
  }

  reconcileSelection();
  reconcileCurrentUser();
  render();
}

function reconcileCurrentUser() {
  state.currentUser = state.userEmail
    ? state.data.users.find((user) => user.email === state.userEmail) || null
    : null;
}

function reconcileSelection() {
  state.selectedOrganizationId = pickExisting(
    state.selectedOrganizationId,
    state.data.organizations
  );

  const availableProjects = state.data.projects.filter(
    (project) => !state.selectedOrganizationId || project.organization_id === state.selectedOrganizationId
  );
  state.selectedProjectId = pickExisting(state.selectedProjectId, availableProjects);

  const availableBoards = state.data.boards.filter(
    (board) => !state.selectedProjectId || board.project_id === state.selectedProjectId
  );
  state.selectedBoardId = pickExisting(state.selectedBoardId, availableBoards);

  persistSelection();
}

function pickExisting(currentId, items) {
  if (items.some((item) => item.id === currentId)) return currentId;
  return items[0]?.id ?? null;
}

function persistSelection() {
  persistNumber("victory.organizationId", state.selectedOrganizationId);
  persistNumber("victory.projectId", state.selectedProjectId);
  persistNumber("victory.boardId", state.selectedBoardId);
}

function persistNumber(key, value) {
  if (value) {
    localStorage.setItem(key, String(value));
  } else {
    localStorage.removeItem(key);
  }
}

function currentOrganization() {
  return state.data.organizations.find((item) => item.id === state.selectedOrganizationId) || null;
}

function currentProject() {
  return state.data.projects.find((item) => item.id === state.selectedProjectId) || null;
}

function currentBoard() {
  return state.data.boards.find((item) => item.id === state.selectedBoardId) || null;
}

function boardColumns() {
  return state.data.columns
    .filter((column) => column.board_id === state.selectedBoardId)
    .sort((a, b) => a.position - b.position || a.id - b.id);
}

function boardTasks() {
  const columnIds = new Set(boardColumns().map((column) => column.id));
  return state.data.tasks.filter((task) => columnIds.has(task.column_id));
}

function selectedTask() {
  return state.data.tasks.find((task) => task.id === state.selectedTaskId) || null;
}

function currentUser() {
  if (state.currentUser) return state.currentUser;
  if (!state.userEmail) return null;
  return state.data.users.find((user) => user.email === state.userEmail) || null;
}

function render() {
  renderPage();
  renderTokenState();
  renderAccountView();
  renderSelectors();
  renderNavProjects();
  renderGlobalSearchResults();
  renderManagementPages();
  renderHeader();
  renderBoard();
  renderDrawer();
}

function renderSelectors() {
  fillSelect(els.organizationSelect, state.data.organizations, state.selectedOrganizationId, "Нет организаций");
  fillSelect(els.projectOrgSelect, state.data.organizations, state.selectedOrganizationId, "Нет организаций");

  const projects = state.data.projects.filter(
    (project) => !state.selectedOrganizationId || project.organization_id === state.selectedOrganizationId
  );
  fillSelect(els.projectSelect, projects, state.selectedProjectId, "Нет проектов");
  fillSelect(els.boardProjectSelect, state.data.projects, state.selectedProjectId, "Нет проектов");
  fillSelect(els.navProjectOrgSelect, state.data.organizations, state.selectedOrganizationId, "Нет организаций");

  const boards = state.data.boards.filter(
    (board) => !state.selectedProjectId || board.project_id === state.selectedProjectId
  );
  fillSelect(els.boardSelect, boards, state.selectedBoardId, "Нет досок");
}

function fillSelect(select, items, selectedId, emptyText) {
  select.innerHTML = "";
  if (!items.length) {
    select.append(new Option(emptyText, ""));
    select.disabled = true;
    return;
  }

  select.disabled = false;
  for (const item of items) {
    const option = new Option(item.name, String(item.id));
    option.selected = item.id === selectedId;
    select.append(option);
  }
}

function renderHeader() {
  const board = currentBoard();

  els.boardTitle.textContent = board?.name || "Создайте доску";
  els.newColumnButton.disabled = !board;
  els.newTaskButton.disabled = !board || !boardColumns().length;
}

function renderPage() {
  els.pagePanels.forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.pagePanel === state.currentPage);
  });
  els.navItems.forEach((item) => {
    item.classList.toggle("active", item.dataset.page === state.currentPage);
  });
}

function renderNavProjects() {
  const query = state.projectSearch.trim().toLowerCase();
  const projects = state.data.projects
    .slice(0, 12);

  els.navProjectList.classList.toggle("collapsed", state.projectsCollapsed);
  els.projectsCollapseButton.textContent = state.projectsCollapsed ? "⌄" : "⌃";
  els.projectsCollapseButton.setAttribute("aria-expanded", String(!state.projectsCollapsed));

  if (state.projectsCollapsed) return;

  els.navProjectList.innerHTML = projects.length
    ? projects.map((project, index) => navProjectItem(project, index)).join("")
    : `<p class="nav-project-empty">Проектов пока нет</p>`;
}

function renderGlobalSearchResults() {
  const query = state.projectSearch.trim().toLowerCase();
  if (!query) {
    els.globalSearchResults.classList.remove("visible");
    els.globalSearchResults.innerHTML = "";
    return;
  }

  const results = searchEverything(query).slice(0, 10);
  els.globalSearchResults.classList.add("visible");
  els.globalSearchResults.innerHTML = results.length
    ? results.map(searchResultItem).join("")
    : `<p class="search-empty">Ничего не найдено</p>`;
}

function searchEverything(query) {
  const organizations = state.data.organizations
    .filter((item) => matchesSearch(item.name, query) || matchesSearch(item.slug, query))
    .map((item) => ({
      type: "organization",
      id: item.id,
      title: item.name,
      meta: "Организация",
      action: `organization:${item.id}`
    }));

  const projects = state.data.projects
    .filter((item) => matchesSearch(item.name, query) || matchesSearch(item.description, query))
    .map((item) => ({
      type: "project",
      id: item.id,
      title: item.name,
      meta: "Проект",
      action: `project:${item.id}`
    }));

  const boards = state.data.boards
    .filter((item) => matchesSearch(item.name, query))
    .map((item) => ({
      type: "board",
      id: item.id,
      title: item.name,
      meta: "Доска",
      action: `board:${item.id}`
    }));

  const tasks = state.data.tasks
    .filter((item) => matchesSearch(item.title, query) || matchesSearch(item.description, query))
    .map((item) => ({
      type: "task",
      id: item.id,
      title: item.title,
      meta: `Задача · ${columnName(item.column_id)}`,
      action: `task:${item.id}`
    }));

  return [...organizations, ...projects, ...boards, ...tasks];
}

function matchesSearch(value, query) {
  return String(value || "").toLowerCase().includes(query);
}

function searchResultItem(result) {
  return `
    <button type="button" class="search-result-item" data-search-action="${result.action}">
      <span class="search-type ${result.type}">${escapeHtml(result.type.charAt(0).toUpperCase())}</span>
      <span>
        <strong>${escapeHtml(result.title)}</strong>
        <small>${escapeHtml(result.meta)}</small>
      </span>
    </button>
  `;
}

function navProjectItem(project, index) {
  const organization = state.data.organizations.find((item) => item.id === project.organization_id);
  const colors = ["green", "orange", "blue", "pink", "purple"];
  const color = colors[index % colors.length];

  return `
    <button type="button" class="nav-project-item ${project.id === state.selectedProjectId ? "active" : ""}" data-project-nav="${project.id}">
      <span class="project-dot ${color}">${escapeHtml(project.name.charAt(0).toUpperCase())}</span>
      <span>
        <strong>${escapeHtml(project.name)}</strong>
        <small>${escapeHtml(organization?.name || "Без организации")}</small>
      </span>
    </button>
  `;
}

function setPage(page) {
  state.currentPage = page;
  localStorage.setItem("victory.page", page);
  renderPage();
}

function renderManagementPages() {
  renderOrganizations();
  renderProjects();
  renderBoards();
  renderManagementInsights();
  renderTaskOverview();
}

function renderOrganizations() {
  els.organizationList.innerHTML = state.data.organizations.length
    ? state.data.organizations.map((organization) => resourceCard({
        title: organization.name,
        meta: `Код: ${organization.slug}`,
        isActive: organization.id === state.selectedOrganizationId,
        stats: [
          `${state.data.projects.filter((project) => project.organization_id === organization.id).length} проектов`,
          `${state.data.boards.filter((board) => {
            const project = state.data.projects.find((item) => item.id === board.project_id);
            return project?.organization_id === organization.id;
          }).length} досок`
        ],
        actions: [
          actionButton("Выбрать", `select-organization:${organization.id}`),
          actionButton("Изменить", `edit-organization:${organization.id}`, "secondary"),
          actionButton("Удалить", `delete-organization:${organization.id}`, "danger")
        ]
      })).join("")
    : emptyResource("Организаций пока нет.");
}

function renderProjects() {
  els.projectList.innerHTML = state.data.projects.length
    ? state.data.projects.map((project) => {
        const organization = state.data.organizations.find((item) => item.id === project.organization_id);
        const projectBoards = state.data.boards.filter((board) => board.project_id === project.id);
        const projectBoardIds = new Set(projectBoards.map((board) => board.id));
        const projectTasks = state.data.tasks.filter((task) => projectBoardIds.has(task.board_id));
        return resourceCard({
          title: project.name,
          meta: `${organization?.name || `organization #${project.organization_id}`} · ${project.description || "без описания"}`,
          isActive: project.id === state.selectedProjectId,
          stats: [`${projectBoards.length} досок`, `${projectTasks.length} задач`],
          details: projectOverviewDetails(projectBoards, projectTasks),
          actions: [
            actionButton("Выбрать", `select-project:${project.id}`),
            actionButton("Изменить", `edit-project:${project.id}`, "secondary"),
            actionButton("Удалить", `delete-project:${project.id}`, "danger")
          ]
        });
      }).join("")
    : emptyResource("Проектов пока нет.");
}

function renderBoards() {
  els.boardList.innerHTML = state.data.boards.length
    ? state.data.boards.map((board) => {
        const project = state.data.projects.find((item) => item.id === board.project_id);
        const columnsCount = state.data.columns.filter((column) => column.board_id === board.id).length;
        const boardTasksList = state.data.tasks.filter((task) => task.board_id === board.id);
        return resourceCard({
          title: board.name,
          meta: `${project?.name || `project #${board.project_id}`} · ${columnsCount} колонок`,
          isActive: board.id === state.selectedBoardId,
          stats: [`${boardTasksList.length} задач`, board.id === state.selectedBoardId ? "выбрана" : "готова"],
          details: boardOverviewDetails(board.id, boardTasksList),
          actions: [
            actionButton("Открыть kanban", `open-board:${board.id}`),
            actionButton("Изменить", `edit-board:${board.id}`, "secondary"),
            actionButton("Удалить", `delete-board:${board.id}`, "danger")
          ]
        });
      }).join("")
    : emptyResource("Досок пока нет.");
}

function projectOverviewDetails(boards, tasks) {
  const boardItems = boards.slice(0, 3).map((board) => `<li>${escapeHtml(board.name)}</li>`).join("");
  const taskItems = tasks.slice(0, 4).map((task) => `<li>${escapeHtml(task.title)}</li>`).join("");

  return `
    <div class="resource-details">
      <div>
        <span>Доски</span>
        <ul>${boardItems || "<li>Пока нет досок</li>"}</ul>
      </div>
      <div>
        <span>Задачи</span>
        <ul>${taskItems || "<li>Пока нет задач</li>"}</ul>
      </div>
    </div>
  `;
}

function boardOverviewDetails(boardId, tasks) {
  const columns = state.data.columns.filter((column) => column.board_id === boardId).sort((a, b) => a.position - b.position);
  const columnItems = columns.slice(0, 4).map((column) => `<li>${escapeHtml(column.name)}</li>`).join("");
  const taskItems = tasks.slice(0, 4).map((task) => `<li>${escapeHtml(task.title)}</li>`).join("");

  return `
    <div class="resource-details">
      <div>
        <span>Колонки</span>
        <ul>${columnItems || "<li>Пока нет колонок</li>"}</ul>
      </div>
      <div>
        <span>Задачи</span>
        <ul>${taskItems || "<li>Пока нет задач</li>"}</ul>
      </div>
    </div>
  `;
}

function resourceCard({ title, meta, isActive, stats = [], details = "", actions }) {
  return `
    <article class="resource-card ${isActive ? "active" : ""}">
      <div>
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(meta)}</p>
      </div>
      ${stats.length ? `<div class="resource-stats">${stats.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>` : ""}
      ${details}
      <div class="resource-actions">
        ${actions.join("")}
      </div>
    </article>
  `;
}

function actionButton(label, action, variant = "") {
  return `<button type="button" class="${variant}" data-resource-action="${action}">${escapeHtml(label)}</button>`;
}

function emptyResource(text) {
  return `<div class="empty-resource">${escapeHtml(text)}</div>`;
}

function renderManagementInsights() {
  const selectedOrgProjects = state.data.projects.filter((project) => project.organization_id === state.selectedOrganizationId);
  const selectedProjectBoards = state.data.boards.filter((board) => board.project_id === state.selectedProjectId);
  const selectedBoardTasks = state.data.tasks.filter((task) => task.board_id === state.selectedBoardId);

  els.organizationInsights.innerHTML = insightGrid([
    ["Организаций", state.data.organizations.length],
    ["Проектов внутри", selectedOrgProjects.length],
    ["Следующий шаг", selectedOrgProjects.length ? "выбрать проект" : "создать проект"]
  ]);

  els.projectInsights.innerHTML = insightGrid([
    ["Проектов", state.data.projects.length],
    ["Досок в выбранном", selectedProjectBoards.length],
    ["Следующий шаг", selectedProjectBoards.length ? "открыть доску" : "создать доску"]
  ]);

  els.boardInsights.innerHTML = insightGrid([
    ["Досок", state.data.boards.length],
    ["Колонок", boardColumns().length],
    ["Задач", selectedBoardTasks.length]
  ]);
}

function insightGrid(items) {
  return items.map(([label, value]) => `
    <article>
      <strong>${escapeHtml(String(value))}</strong>
      <span>${escapeHtml(label)}</span>
    </article>
  `).join("");
}

function renderTaskOverview() {
  const board = currentBoard();
  const tasks = boardTasks();
  const columns = boardColumns();
  const active = tasks.filter((task) => task.status !== "done").length;
  const urgent = tasks.filter((task) => task.priority >= 4).length;

  els.taskOverview.innerHTML = `
    <article>
      <span>Текущая доска</span>
      <strong>${escapeHtml(board?.name || "Доска не выбрана")}</strong>
      <p>${escapeHtml(currentProject()?.name || "Выберите проект и доску, чтобы собрать рабочий kanban.")}</p>
    </article>
    <article>
      <span>Процесс</span>
      <strong>${columns.length} колонок</strong>
      <p>${columns.length ? columns.map((column) => column.name).slice(0, 4).join(" · ") : "Создайте Backlog, In progress и Done."}</p>
    </article>
    <article>
      <span>Нагрузка</span>
      <strong>${active} активных</strong>
      <p>${urgent ? `${urgent} задач высокого приоритета` : "Критичных задач нет."}</p>
    </article>
  `;
}

function renderAccountView() {
  const user = currentUser();
  const isSignedIn = Boolean(state.token);
  const displayName = user?.full_name || state.userEmail || "Пользователь";
  const initial = (displayName || "U").trim().charAt(0).toUpperCase();

  els.accountAvatar.textContent = initial;
  els.accountTitle.textContent = isSignedIn ? displayName : "Личный кабинет";
  els.accountSubtitle.textContent = isSignedIn
    ? `${user?.email || state.userEmail} · workspace overview`
    : "Войди, чтобы управлять профилем и рабочим контекстом.";

  els.authForm.classList.toggle("hidden", isSignedIn);
  els.profileForm.classList.toggle("hidden", !isSignedIn);

  if (isSignedIn) {
    els.profileName.value = user?.full_name || "";
    els.profileEmail.value = user?.email || state.userEmail || "";
  }

  const tasks = state.data.tasks;
  const activeTasks = tasks.filter((task) => task.status !== "done").length;
  const assignedTasks = user
    ? tasks.filter((task) => task.assignee_id === user.id || task.creator_id === user.id).length
    : tasks.filter((task) => task.assignee_id || task.creator_id).length;

  els.profileStats.innerHTML = [
    accountStat("Организации", state.data.organizations.length),
    accountStat("Проекты", state.data.projects.length),
    accountStat("Доски", state.data.boards.length),
    accountStat("Активные задачи", activeTasks)
  ].join("");

  els.accountSnapshot.innerHTML = `
    <div>
      <span>Текущая доска</span>
      <strong>${escapeHtml(currentBoard()?.name || "не выбрана")}</strong>
    </div>
    <div>
      <span>Связанные задачи</span>
      <strong>${assignedTasks}</strong>
    </div>
  `;
}

function accountStat(label, value) {
  return `
    <article>
      <strong>${value}</strong>
      <span>${escapeHtml(label)}</span>
    </article>
  `;
}

function renderBoard() {
  const board = currentBoard();
  const columns = boardColumns();
  const tasks = boardTasks();

  els.emptyState.innerHTML = "";
  els.emptyState.classList.remove("visible");
  els.kanbanBoard.innerHTML = "";

  if (!board) {
    showEmptyState(
      "Нужен рабочий контекст",
      "Создайте организацию, проект и доску в левом сайдбаре. После этого тут появится kanban."
    );
    return;
  }

  if (!columns.length) {
    showEmptyState(
      "На доске пока нет колонок",
      "Создайте первую колонку: Backlog, In progress или Done. После этого можно будет добавлять задачи."
    );
    return;
  }

  for (const column of columns) {
    const columnTasks = tasks.filter((task) => task.column_id === column.id);
    const section = document.createElement("section");
    section.className = "kanban-column";
    section.dataset.columnId = String(column.id);

    const header = document.createElement("header");
    header.innerHTML = `
      <div>
        <h3>${escapeHtml(column.name)}</h3>
        <p>${column.wip_limit ? `WIP ${columnTasks.length}/${column.wip_limit}` : `${columnTasks.length} задач`}</p>
      </div>
      <div class="column-actions">
        <button type="button" class="ghost small" data-column-action="add">+</button>
        <button type="button" class="ghost small" data-column-action="edit">···</button>
      </div>
    `;
    header.querySelector('[data-column-action="add"]').addEventListener("click", () => openTaskDrawer({ columnId: column.id }));
    header.querySelector('[data-column-action="edit"]').addEventListener("click", () => editColumn(column.id));
    section.append(header);

    const list = document.createElement("div");
    list.className = "task-list";
    list.dataset.columnId = String(column.id);
    list.addEventListener("dragover", handleTaskDragOver);
    list.addEventListener("dragleave", handleTaskDragLeave);
    list.addEventListener("drop", handleTaskDrop);

    if (!columnTasks.length) {
      const empty = document.createElement("div");
      empty.className = "column-empty";
      empty.textContent = "Пусто";
      list.append(empty);
    }

    for (const task of columnTasks) {
      list.append(renderTaskCard(task));
    }

    section.append(list);
    els.kanbanBoard.append(section);
  }
}

async function editColumn(columnId) {
  const column = state.data.columns.find((item) => item.id === columnId);
  if (!column) return;

  const action = prompt("Колонка: rename / delete", "rename");
  if (!action) return;

  if (action === "delete") {
    if (!confirm(`Удалить колонку "${column.name}"?`)) return;
    await request(`/columns/${columnId}`, { method: "DELETE" });
    await Promise.all([loadOnly("columns"), loadOnly("tasks")]);
    render();
    return;
  }

  const name = prompt("Название колонки", column.name);
  if (!name) return;
  const position = Number(prompt("Позиция", String(column.position ?? 0)) || column.position || 0);
  const wipLimitInput = prompt("WIP limit пусто = без лимита", column.wip_limit ?? "");
  const wip_limit = wipLimitInput ? Number(wipLimitInput) : null;

  await request(`/columns/${columnId}`, {
    method: "PATCH",
    body: JSON.stringify({ name, position, wip_limit })
  });
  await loadOnly("columns");
  render();
}

function showEmptyState(title, text) {
  els.emptyState.classList.add("visible");
  els.emptyState.innerHTML = `
    <h3>${escapeHtml(title)}</h3>
    <p>${escapeHtml(text)}</p>
  `;
}

function renderTaskCard(task) {
  const card = document.createElement("article");
  card.className = "task-card";
  card.draggable = true;
  card.dataset.taskId = String(task.id);
  card.dataset.columnId = String(task.column_id);
  const commentsCount = state.data.comments.filter((comment) => comment.task_id === task.id).length;
  const activityCount = state.data.activities.filter((activity) => activity.task_id === task.id).length;
  card.innerHTML = `
    <div class="task-card-head">
      <strong>${escapeHtml(task.title)}</strong>
      <span class="${priorityClass(task.priority)}">P${task.priority}</span>
    </div>
    <p>${escapeHtml(task.description || "Без описания")}</p>
    <div class="task-card-meta">
      <span>Автор: ${escapeHtml(formatActor(task.creator_id))}</span>
      ${task.assignee_id ? `<span>Исполнитель: ${escapeHtml(formatActor(task.assignee_id))}</span>` : "<span>Не назначена</span>"}
      <span>${commentsCount} комм.</span>
      <span>${activityCount} акт.</span>
    </div>
  `;
  card.addEventListener("dragstart", (event) => handleTaskDragStart(event, task));
  card.addEventListener("dragend", handleTaskDragEnd);
  card.addEventListener("click", () => openTaskDrawer({ taskId: task.id }));
  return card;
}

function handleTaskDragStart(event, task) {
  state.draggedTaskId = task.id;
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData("text/plain", String(task.id));
  event.currentTarget.classList.add("dragging");
}

function handleTaskDragEnd(event) {
  state.draggedTaskId = null;
  event.currentTarget.classList.remove("dragging");
  document.querySelectorAll(".task-list.drag-over").forEach((list) => {
    list.classList.remove("drag-over");
  });
}

function handleTaskDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
  event.currentTarget.classList.add("drag-over");
}

function handleTaskDragLeave(event) {
  if (!event.currentTarget.contains(event.relatedTarget)) {
    event.currentTarget.classList.remove("drag-over");
  }
}

async function handleTaskDrop(event) {
  event.preventDefault();
  event.currentTarget.classList.remove("drag-over");

  const taskId = Number(event.dataTransfer.getData("text/plain") || state.draggedTaskId);
  const newColumnId = Number(event.currentTarget.dataset.columnId);
  const task = state.data.tasks.find((item) => item.id === taskId);

  if (!task || !newColumnId || task.column_id === newColumnId) return;

  try {
    await moveTask(task, newColumnId);
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function moveTask(task, newColumnId) {
  await request(`/tasks/${task.id}/move`, {
    method: "POST",
    body: JSON.stringify({
      new_column_id: newColumnId,
      user_id: state.currentUser?.id || task.assignee_id || task.creator_id || 1
    })
  });

  await Promise.all([loadOnly("tasks"), loadOnly("activities")]);
  render();
}

function renderDrawer() {
  const task = selectedTask();
  const isOpen = els.taskDrawer.classList.contains("open");
  if (!isOpen) return;

  fillTaskColumnSelect();
  fillTaskUserSelects();
  renderTaskExtra(task);
  renderAiSummary();
}

function openTaskDrawer({ taskId = null, columnId = null } = {}) {
  state.selectedTaskId = taskId;
  state.aiSummary = null;
  const task = selectedTask();
  els.taskDrawer.classList.add("open");
  els.overlay.classList.add("visible");
  els.taskDrawer.setAttribute("aria-hidden", "false");
  els.drawerTitle.textContent = task ? task.title : "Новая задача";
  els.deleteTaskButton.hidden = !task;
  els.catchupButton.hidden = !task;
  fillTaskForm(task, columnId);
  renderTaskExtra(task);
  renderAiSummary();
}

function closeTaskDrawer() {
  state.selectedTaskId = null;
  state.aiSummary = null;
  els.taskDrawer.classList.remove("open");
  els.overlay.classList.remove("visible");
  els.taskDrawer.setAttribute("aria-hidden", "true");
  els.taskForm.reset();
  renderAiSummary();
}

function fillTaskForm(task, columnId) {
  const form = els.taskForm;
  form.elements.id.value = task?.id || "";
  form.elements.title.value = task?.title || "";
  form.elements.description.value = task?.description || "";
  form.elements.priority.value = String(task?.priority || 1);
  
  fillTaskUserSelects();
  form.elements.creator_id.value = String(task?.creator_id || state.currentUser?.id || 1);
  form.elements.assignee_id.value = task?.assignee_id ? String(task.assignee_id) : "";
  form.elements.metadata_json.value = task?.metadata_json
    ? JSON.stringify(task.metadata_json, null, 2)
    : "";

  fillTaskColumnSelect();
  form.elements.column_id.value = String(task?.column_id || columnId || boardColumns()[0]?.id || "");
}

function fillTaskColumnSelect() {
  const select = els.taskForm.elements.column_id;
  const columns = boardColumns();
  select.innerHTML = "";

  for (const column of columns) {
    select.append(new Option(column.name, String(column.id)));
  }
}

function fillTaskUserSelects() {
  const creatorSelect = els.taskForm.elements.creator_id;
  const assigneeSelect = els.taskForm.elements.assignee_id;
  
  const currentCreatorValue = creatorSelect.value;
  const currentAssigneeValue = assigneeSelect.value;

  creatorSelect.innerHTML = "";
  assigneeSelect.innerHTML = '<option value="">не назначен</option>';

  for (const user of state.data.users) {
    const label = user.full_name ? `${user.full_name} (${user.email})` : user.email;
    creatorSelect.append(new Option(label, String(user.id)));
    assigneeSelect.append(new Option(label, String(user.id)));
  }

  if (currentCreatorValue) creatorSelect.value = currentCreatorValue;
  if (currentAssigneeValue) assigneeSelect.value = currentAssigneeValue;
}

function renderTaskExtra(task) {
  if (!task) {
    els.taskExtra.innerHTML = `
      <section class="task-section hint-section">
        <div class="section-label">Черновик</div>
        <h3>Новая задача</h3>
        <p class="muted">Создание задачи сразу отправит POST /tasks/ и обновит доску.</p>
      </section>
    `;
    return;
  }

  const comments = state.data.comments.filter((comment) => comment.task_id === task.id);
  const activities = state.data.activities.filter((activity) => activity.task_id === task.id);

  els.taskExtra.innerHTML = `
    <section class="task-section comments-section">
      <div class="section-headline">
        <div class="section-label">Обсуждение</div>
        <h3>Комментарии</h3>
      </div>
      <form id="commentForm" class="comment-form">
        <textarea name="content" placeholder="Добавить комментарий"></textarea>
        <div class="form-row">
          <select name="user_id">
            ${state.data.users.map(u => `<option value="${u.id}" ${u.id === state.currentUser?.id ? 'selected' : ''}>${escapeHtml(u.full_name || u.email)}</option>`).join('')}
          </select>
          <button type="submit">Отправить</button>
        </div>
      </form>
      <div class="comment-list">
        ${comments.length ? comments.map(renderComment).join("") : '<p class="muted">Комментариев пока нет.</p>'}
      </div>
    </section>

    <section class="task-section activity-section">
      <div class="section-headline">
        <div class="section-label">История</div>
        <h3>Что происходило с задачей</h3>
      </div>
      <form id="activityForm" class="comment-form">
        <input name="activity_type" type="text" placeholder="status_changed" />
        <div class="form-row">
          <input name="old_value" type="text" placeholder="Было" />
          <input name="new_value" type="text" placeholder="Стало" />
        </div>
        <div class="form-row">
          <select name="user_id">
            ${state.data.users.map(u => `<option value="${u.id}" ${u.id === state.currentUser?.id ? 'selected' : ''}>${escapeHtml(u.full_name || u.email)}</option>`).join('')}
          </select>
          <button type="submit">Записать</button>
        </div>
      </form>
      <div class="activity-list">
        ${activities.length ? activities.map(renderActivity).join("") : '<p class="muted">Активности пока нет.</p>'}
      </div>
    </section>

    <details class="task-section raw-section">
      <summary>
        <span>Технические данные задачи</span>
      </summary>
      <pre>${escapeHtml(JSON.stringify(task, null, 2))}</pre>
    </details>
  `;

  document.querySelector("#commentForm").addEventListener("submit", submitComment);
  document.querySelector("#activityForm").addEventListener("submit", submitActivity);
}

function renderComment(comment) {
  return `
    <article class="note-card">
      <p>${escapeHtml(comment.content)}</p>
      <span>${escapeHtml(formatActor(comment.user_id))}${comment.created_at ? ` · ${escapeHtml(formatDate(comment.created_at))}` : ""}</span>
    </article>
  `;
}

function renderActivity(activity) {
  const log = describeActivity(activity);
  return `
    <article class="note-card activity-log-card">
      <p>${escapeHtml(log.title)}</p>
      <span>${escapeHtml(log.meta)}</span>
    </article>
  `;
}

function describeActivity(activity) {
  const actor = formatActor(activity.user_id);
  const when = activity.created_at ? formatDate(activity.created_at) : "";
  const meta = [actor, when].filter(Boolean).join(" · ");
  const oldValue = activity.old_value;
  const newValue = activity.new_value;

  const descriptions = {
    created: () => `Задача создана${newValue ? ` (#${newValue})` : ""}`,
    moved: () => `Перенесена из «${columnName(oldValue)}» в «${columnName(newValue)}»`,
    title_changed: () => `Название изменено: «${oldValue || "без названия"}» → «${newValue || "без названия"}»`,
    description_changed: () => "Описание задачи обновлено",
    priority_changed: () => `Приоритет изменен: ${priorityLabel(oldValue)} → ${priorityLabel(newValue)}`,
    assigned: () => `Исполнитель изменен: ${formatNullableUser(oldValue)} → ${formatNullableUser(newValue)}`,
    metadata_updated: () => "Метаданные задачи обновлены",
    status_change: () => `Статус изменен: ${oldValue || "-"} → ${newValue || "-"}`
  };

  const title = descriptions[activity.activity_type]?.() || humanizeActivityType(activity.activity_type, oldValue, newValue);
  return { title, meta: meta || "Системное событие" };
}

function columnName(value) {
  const id = Number(value);
  const column = state.data.columns.find((item) => item.id === id);
  return column?.name || (value ? `колонка #${value}` : "неизвестная колонка");
}

function priorityLabel(value) {
  if (!value) return "не задан";
  return `P${value}`;
}

function formatNullableUser(value) {
  return value ? formatActor(value) : "не назначен";
}

function formatActor(userId) {
  const id = Number(userId);
  const user = state.data.users.find((u) => u.id === id);
  if (user) {
    return user.full_name || user.email;
  }
  return userId ? `Пользователь #${userId}` : "Система";
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString("ru-RU", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function humanizeActivityType(type, oldValue, newValue) {
  const readableType = String(type || "Событие").replaceAll("_", " ");
  if (oldValue || newValue) {
    return `${readableType}: ${oldValue || "-"} → ${newValue || "-"}`;
  }
  return readableType;
}

async function submitTask(event) {
  event.preventDefault();
  const formData = new FormData(els.taskForm);
  const taskId = formData.get("id");

  try {
    const payload = normalizeTaskPayload(formData, Boolean(taskId));
    await request(taskId ? `/tasks/${taskId}` : "/tasks/", {
      method: taskId ? "PATCH" : "POST",
      body: JSON.stringify(payload)
    });

    await reloadBoardData();
    closeTaskDrawer();
    render();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

function normalizeTaskPayload(formData, isUpdate) {
  const payload = {
    title: requiredString(formData, "title"),
    description: optionalString(formData, "description"),
    priority: Number(formData.get("priority") || 1),
    column_id: Number(formData.get("column_id")),
    assignee_id: optionalNumber(formData, "assignee_id"),
    metadata_json: optionalJson(formData, "metadata_json")
  };

  if (!isUpdate) {
    payload.creator_id = Number(formData.get("creator_id") || state.currentUser?.id || 1);
  }

  return pruneEmpty(payload);
}

async function submitComment(event) {
  event.preventDefault();
  const task = selectedTask();
  if (!task) return;

  try {
    const formData = new FormData(event.currentTarget);
    const content = requiredString(formData, "content");
    const userId = Number(formData.get("user_id") || state.currentUser?.id || 1);

    await request("/comments/", {
      method: "POST",
      body: JSON.stringify({ content, task_id: task.id, user_id: userId })
    });
    await loadOnly("comments");
    renderTaskExtra(task);
    renderBoard();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitActivity(event) {
  event.preventDefault();
  const task = selectedTask();
  if (!task) return;

  try {
    const formData = new FormData(event.currentTarget);
    const payload = {
      activity_type: requiredString(formData, "activity_type"),
      old_value: optionalString(formData, "old_value"),
      new_value: optionalString(formData, "new_value"),
      task_id: task.id,
      user_id: Number(formData.get("user_id") || state.currentUser?.id || 1)
    };

    await request("/activities/", {
      method: "POST",
      body: JSON.stringify(payload)
    });
    await loadOnly("activities");
    renderTaskExtra(task);
    renderBoard();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitColumn(event) {
  event.preventDefault();
  const board = currentBoard();
  if (!board) return;

  try {
    const formData = new FormData(els.columnForm);
    const payload = pruneEmpty({
      name: requiredString(formData, "name"),
      position: Number(formData.get("position") || 0),
      wip_limit: optionalNumber(formData, "wip_limit"),
      board_id: board.id
    });

    await request("/columns/", {
      method: "POST",
      body: JSON.stringify(payload)
    });
    els.columnDialog.close();
    els.columnForm.reset();
    await loadOnly("columns");
    render();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitContext(event) {
  event.preventDefault();
  if (!els.contextForm) return;

  try {
    const formData = new FormData(els.contextForm);
    const organizationName = requiredString(formData, "organizationName");
    const organizationSlug = requiredString(formData, "organizationSlug");
    const projectName = requiredString(formData, "projectName");
    const boardName = requiredString(formData, "boardName");

    const organization = await request("/organizations/", {
      method: "POST",
      body: JSON.stringify({ name: organizationName, slug: organizationSlug })
    });
    const project = await request("/projects/", {
      method: "POST",
      body: JSON.stringify({
        name: projectName,
        description: "Создано из frontend skeleton",
        organization_id: organization.id
      })
    });
    const board = await request("/boards/", {
      method: "POST",
      body: JSON.stringify({ name: boardName, project_id: project.id })
    });

    state.selectedOrganizationId = organization.id;
    state.selectedProjectId = project.id;
    state.selectedBoardId = board.id;
    els.contextForm.reset();
    await loadAll();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitOrganization(event) {
  event.preventDefault();
  const formData = new FormData(els.organizationForm);

  try {
    const organization = await request("/organizations/", {
      method: "POST",
      body: JSON.stringify({
        name: requiredString(formData, "name"),
        slug: requiredString(formData, "slug")
      })
    });

    state.selectedOrganizationId = organization.id;
    els.organizationForm.reset();
    await loadAll();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitProjectManagement(event) {
  event.preventDefault();
  await createProjectFromForm(els.projectManagementForm, () => {
    els.projectManagementForm.reset();
  });
}

async function submitNavProject(event) {
  event.preventDefault();
  await createProjectFromForm(els.navProjectForm, () => {
    els.navProjectForm.reset();
    els.navProjectDialog.close();
  });
}

async function createProjectFromForm(form, onSuccess) {
  const formData = new FormData(form);

  try {
    const project = await request("/projects/", {
      method: "POST",
      body: JSON.stringify({
        name: requiredString(formData, "name"),
        description: optionalString(formData, "description"),
        organization_id: Number(formData.get("organization_id"))
      })
    });

    state.selectedOrganizationId = project.organization_id;
    state.selectedProjectId = project.id;
    onSuccess?.();
    await loadAll();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function submitBoardManagement(event) {
  event.preventDefault();
  const formData = new FormData(els.boardManagementForm);

  try {
    const board = await request("/boards/", {
      method: "POST",
      body: JSON.stringify({
        name: requiredString(formData, "name"),
        project_id: Number(formData.get("project_id"))
      })
    });

    const project = state.data.projects.find((item) => item.id === board.project_id);
    state.selectedOrganizationId = project?.organization_id || state.selectedOrganizationId;
    state.selectedProjectId = board.project_id;
    state.selectedBoardId = board.id;
    els.boardManagementForm.reset();
    await loadAll();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function handleResourceAction(event) {
  const button = event.target.closest("[data-resource-action]");
  if (!button) return;

  const [action, rawId] = button.dataset.resourceAction.split(":");
  const id = Number(rawId);

  try {
    if (action === "select-organization") selectOrganization(id);
    if (action === "select-project") selectProject(id);
    if (action === "open-board") openBoard(id);
    if (action === "edit-organization") await editOrganization(id);
    if (action === "edit-project") await editProject(id);
    if (action === "edit-board") await editBoard(id);
    if (action === "delete-organization") await deleteResource("organizations", id);
    if (action === "delete-project") await deleteResource("projects", id);
    if (action === "delete-board") await deleteResource("boards", id);
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

function selectOrganization(id) {
  state.selectedOrganizationId = id;
  state.selectedProjectId = null;
  state.selectedBoardId = null;
  reconcileSelection();
  setPage("projects");
  render();
}

function selectProject(id) {
  const project = state.data.projects.find((item) => item.id === id);
  state.selectedOrganizationId = project?.organization_id || state.selectedOrganizationId;
  state.selectedProjectId = id;
  state.selectedBoardId = null;
  reconcileSelection();
  setPage("boards");
  render();
}

function openProjectFromNav(id) {
  const project = state.data.projects.find((item) => item.id === id);
  if (!project) return;

  state.selectedOrganizationId = project.organization_id;
  state.selectedProjectId = id;
  state.selectedBoardId = state.data.boards.find((board) => board.project_id === id)?.id || null;
  persistSelection();
  setPage(state.selectedBoardId ? "tasks" : "boards");
  render();
}

function handleSearchAction(action) {
  const [type, rawId] = action.split(":");
  const id = Number(rawId);

  if (type === "organization") {
    selectOrganization(id);
  }
  if (type === "project") {
    openProjectFromNav(id);
  }
  if (type === "board") {
    openBoard(id);
  }
  if (type === "task") {
    const task = state.data.tasks.find((item) => item.id === id);
    const board = task ? state.data.boards.find((item) => item.id === task.board_id) : null;
    if (board) openBoard(board.id);
    openTaskDrawer(task);
  }

  state.projectSearch = "";
  els.navProjectSearch.value = "";
  renderGlobalSearchResults();
}

function applyTemplate(template) {
  const projectTemplates = {
    ads: {
      name: "Запуск рекламной кампании",
      description: "Подготовка креативов, медиаплана, посадочной страницы и контроля первых результатов."
    },
    site: {
      name: "Лендинг для клиента",
      description: "Дизайн, текст, разработка, аналитика и запуск клиентской посадочной страницы."
    },
    support: {
      name: "Ежемесячная поддержка",
      description: "Поток задач по сопровождению, правкам, контенту и регулярной отчётности."
    }
  };

  const boardTemplates = {
    delivery: "Production delivery",
    design: "Design pipeline",
    content: "Content calendar"
  };

  const [scope, key] = template.split(":");
  if (scope === "project" && projectTemplates[key]) {
    els.projectManagementForm.elements.name.value = projectTemplates[key].name;
    els.projectManagementForm.elements.description.value = projectTemplates[key].description;
  }
  if (scope === "board" && boardTemplates[key]) {
    els.boardManagementForm.elements.name.value = boardTemplates[key];
  }
}

function openBoard(id) {
  const board = state.data.boards.find((item) => item.id === id);
  const project = state.data.projects.find((item) => item.id === board?.project_id);
  state.selectedOrganizationId = project?.organization_id || state.selectedOrganizationId;
  state.selectedProjectId = board?.project_id || state.selectedProjectId;
  state.selectedBoardId = id;
  persistSelection();
  setPage("tasks");
  render();
}

async function editOrganization(id) {
  const organization = state.data.organizations.find((item) => item.id === id);
  if (!organization) return;
  const name = prompt("Название организации", organization.name);
  if (!name) return;
  const slug = prompt("Slug организации", organization.slug);
  if (!slug) return;
  await request(`/organizations/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name, slug })
  });
  await loadAll();
}

async function editProject(id) {
  const project = state.data.projects.find((item) => item.id === id);
  if (!project) return;
  const name = prompt("Название проекта", project.name);
  if (!name) return;
  const description = prompt("Описание проекта", project.description || "") || null;
  await request(`/projects/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name, description })
  });
  await loadAll();
}

async function editBoard(id) {
  const board = state.data.boards.find((item) => item.id === id);
  if (!board) return;
  const name = prompt("Название доски", board.name);
  if (!name) return;
  await request(`/boards/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name })
  });
  await loadAll();
}

async function deleteResource(resource, id) {
  if (!confirm("Удалить выбранный элемент?")) return;
  await request(`${endpoints[resource]}${id}`, { method: "DELETE" });
  await loadAll();
}

async function deleteSelectedTask() {
  const task = selectedTask();
  if (!task || !confirm(`Удалить задачу "${task.title}"?`)) return;

  try {
    await request(`/tasks/${task.id}`, { method: "DELETE" });
    await reloadBoardData();
    closeTaskDrawer();
    render();
  } catch (error) {
    alert(error instanceof Error ? error.message : String(error));
  }
}

async function getCatchUp() {
  const task = selectedTask();
  if (!task) return;

  try {
    state.aiSummary = { status: "loading" };
    renderAiSummary();
    const payload = await request(`/ai/task/${task.id}/catchup`, { method: "POST" });
    state.aiSummary = { status: "ready", payload };
    renderAiSummary();
  } catch (error) {
    state.aiSummary = { status: "error", message: error instanceof Error ? error.message : String(error) };
    renderAiSummary();
    alert(error instanceof Error ? error.message : String(error));
  }
}

function renderAiSummary() {
  if (!els.aiSummaryPanel) return;
  els.taskDrawer.classList.toggle("ai-open", Boolean(state.aiSummary));

  if (!state.aiSummary) {
    els.aiSummaryPanel.className = "ai-summary-panel";
    els.aiSummaryPanel.innerHTML = "";
    return;
  }

  els.aiSummaryPanel.className = "ai-summary-panel visible";

  if (state.aiSummary.status === "loading") {
    els.aiSummaryPanel.innerHTML = `
      <div class="ai-loading">
        <span class="ai-orb"></span>
        <h3>AI анализирует задачу</h3>
        <p>Собираю контекст задачи и комментарии.</p>
      </div>
    `;
    return;
  }

  if (state.aiSummary.status === "error") {
    els.aiSummaryPanel.innerHTML = `
      <div class="ai-error">
        <h3>AI Catch Up не сработал</h3>
        <p>${escapeHtml(state.aiSummary.message)}</p>
      </div>
    `;
    return;
  }

  const payload = state.aiSummary.payload;
  els.aiSummaryPanel.innerHTML = `
    <div class="ai-panel-head">
      <span class="ai-badge">AI Catch Up</span>
      <h3>Краткая сводка</h3>
    </div>

    <section class="ai-section">
      <h4>Суть</h4>
      <p>${escapeHtml(payload.summary || "Нет summary в ответе.")}</p>
    </section>

    <section class="ai-section">
      <h4>Блокеры</h4>
      ${renderAiList(payload.blockers, "Блокеров не найдено.")}
    </section>

    <section class="ai-section">
      <h4>Следующие шаги</h4>
      ${renderAiList(payload.next_steps, "Следующие шаги не вернулись.")}
    </section>
  `;
}

function renderAiList(items, emptyText) {
  if (!Array.isArray(items) || !items.length) {
    return `<p class="ai-muted">${escapeHtml(emptyText)}</p>`;
  }

  return `
    <ol class="ai-list">
      ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
    </ol>
  `;
}

async function login(mode) {
  const email = els.authEmail.value.trim();
  const password = els.authPassword.value;
  const fullName = els.authName.value.trim();

  if (!email || !password) {
    showAuthMessage("Заполни email и пароль.", true);
    return;
  }

  if (password.length < 8) {
    showAuthMessage("Пароль должен быть минимум 8 символов.", true);
    return;
  }

  if (mode === "register" && !fullName) {
    showAuthMessage("Для регистрации укажи имя.", true);
    return;
  }

  const payload = mode === "register"
    ? { email, password, full_name: fullName || null, is_active: true, is_superuser: false }
    : { email, password };

  try {
    setAuthBusy(true);
    showAuthMessage(mode === "register" ? "Регистрируем пользователя..." : "Проверяем логин...");
    const tokenInfo = await request(mode === "register" ? "/register" : "/login", {
      method: "POST",
      body: JSON.stringify(payload)
    });

	    state.token = tokenInfo.access_token;
	    state.refreshToken = tokenInfo.refresh_token || "";
	    state.userEmail = email;
	    localStorage.setItem("victory.accessToken", state.token);
	    localStorage.setItem("victory.refreshToken", state.refreshToken);
	    localStorage.setItem("victory.userEmail", email);
	    await loadCurrentUser();
	    renderTokenState();
	    renderAccountView();
	    showAuthMessage(mode === "register" ? "Регистрация успешна. Профиль открыт." : "Вход выполнен. Профиль открыт.");
	  } catch (error) {
	    showAuthMessage(error instanceof Error ? translateAuthError(error.message) : String(error), true);
	  } finally {
	    setAuthBusy(false);
	  }
}

async function loadCurrentUser() {
  state.data.users = await request(endpoints.users);
  reconcileCurrentUser();
}

async function submitProfile(event) {
  event.preventDefault();
  const user = currentUser();

  if (!user) {
    showAuthMessage("Не удалось найти пользователя для текущего email. Выйди и войди заново.", true);
    return;
  }

  const email = els.profileEmail.value.trim();
  const fullName = els.profileName.value.trim();
  const password = els.profilePassword.value;

  if (!email) {
    showAuthMessage("Email не может быть пустым.", true);
    return;
  }

  if (password && password.length < 8) {
    showAuthMessage("Новый пароль должен быть минимум 8 символов.", true);
    return;
  }

  const payload = pruneEmpty({
    email,
    full_name: fullName || null,
    password: password || null
  });

  try {
    setAuthBusy(true);
    showAuthMessage("Сохраняем профиль...");
    const updatedUser = await request(`/identity/users/${user.id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });

    state.currentUser = updatedUser;
    state.userEmail = updatedUser.email;
    state.data.users = state.data.users.map((item) => item.id === updatedUser.id ? updatedUser : item);
    localStorage.setItem("victory.userEmail", updatedUser.email);
    els.profilePassword.value = "";
    renderTokenState();
    renderAccountView();
    showAuthMessage("Профиль обновлен.");
  } catch (error) {
    showAuthMessage(error instanceof Error ? translateAuthError(error.message) : String(error), true);
  } finally {
    setAuthBusy(false);
  }
}

async function loadOnly(key) {
  state.data[key] = await request(endpoints[key]);
}

async function reloadBoardData() {
  await Promise.all(["tasks", "comments", "activities", "columns"].map(loadOnly));
}

function requiredString(formData, key) {
  const value = String(formData.get(key) || "").trim();
  if (!value) {
    throw new Error(`Заполните поле: ${key}`);
  }
  return value;
}

function optionalString(formData, key) {
  const value = String(formData.get(key) || "").trim();
  return value || null;
}

function optionalNumber(formData, key) {
  const value = String(formData.get(key) || "").trim();
  return value ? Number(value) : null;
}

function optionalJson(formData, key) {
  const value = String(formData.get(key) || "").trim();
  return value ? JSON.parse(value) : null;
}

function pruneEmpty(payload) {
  return Object.fromEntries(
    Object.entries(payload).filter(([, value]) => value !== null && value !== undefined && value !== "")
  );
}

function renderTokenState() {
  const user = currentUser();
  const label = user?.full_name || user?.email || state.userEmail || "пользователь";

  els.tokenState.textContent = state.token
    ? `Выполнен вход: ${label}`
    : "Токен не задан";

  if (els.profileLabel) {
    els.profileLabel.textContent = state.token ? label : "Войти";
  }
  if (els.profileCompany) {
    els.profileCompany.textContent = currentOrganization()?.name || "Victory workspace";
  }

  els.logoutButton.hidden = !state.token;
}

function openAuthView() {
  els.authView.classList.add("visible");
  els.authView.setAttribute("aria-hidden", "false");
}

function closeAuthView() {
  els.authView.classList.remove("visible");
  els.authView.setAttribute("aria-hidden", "true");
}

function logout() {
  state.token = "";
  state.refreshToken = "";
  state.userEmail = "";
  state.currentUser = null;
  localStorage.removeItem("victory.accessToken");
  localStorage.removeItem("victory.refreshToken");
  localStorage.removeItem("victory.userEmail");
  renderTokenState();
  renderAccountView();
  showAuthMessage("Вы вышли из аккаунта.");
}


function handleNavClick(event) {
  const item = event.currentTarget;
  const action = item.dataset.navAction;
  const page = item.dataset.page;

  if (action === "profile") {
    setActiveNavItem(item);
    openAuthView();
    return;
  }

  if (page) setPage(page);
}

function setActiveNavItem(activeItem) {
  els.navItems.forEach((item) => {
    item.classList.toggle("active", item === activeItem);
  });
}

function setAuthMode(mode) {
  state.authMode = mode;
  const isRegister = mode === "register";
  els.authLoginTab.classList.toggle("active", !isRegister);
  els.authRegisterTab.classList.toggle("active", isRegister);
  els.authNameField.classList.toggle("hidden", !isRegister);
  els.loginButton.classList.toggle("hidden", isRegister);
  els.registerButton.classList.toggle("hidden", !isRegister);
  els.authPassword.autocomplete = isRegister ? "new-password" : "current-password";
  showAuthMessage("");
}

function showAuthMessage(message, isError = false) {
  els.authMessage.textContent = message;
  els.authMessage.classList.toggle("error", isError);
}

function setAuthBusy(isBusy) {
  els.loginButton.disabled = isBusy;
  els.registerButton.disabled = isBusy;
  els.logoutButton.disabled = isBusy;
  els.saveProfileButton.disabled = isBusy;
}

function translateAuthError(message) {
  if (message.includes("already exists")) return "Пользователь с таким email уже существует.";
  if (message.includes("invalid username or password")) return "Неверный email или пароль.";
  return message;
}

function priorityClass(priority) {
  if (priority >= 4) return "priority high";
  if (priority >= 2) return "priority medium";
  return "priority";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

els.organizationSelect.addEventListener("change", () => {
  state.selectedOrganizationId = Number(els.organizationSelect.value) || null;
  state.selectedProjectId = null;
  state.selectedBoardId = null;
  reconcileSelection();
  render();
});

els.projectSelect.addEventListener("change", () => {
  state.selectedProjectId = Number(els.projectSelect.value) || null;
  state.selectedBoardId = null;
  reconcileSelection();
  render();
});

els.boardSelect.addEventListener("change", () => {
  state.selectedBoardId = Number(els.boardSelect.value) || null;
  persistSelection();
  render();
});

els.navProjectSearch.addEventListener("input", () => {
  state.projectSearch = els.navProjectSearch.value;
  renderNavProjects();
  renderGlobalSearchResults();
});
els.projectsCollapseButton.addEventListener("click", () => {
  state.projectsCollapsed = !state.projectsCollapsed;
  renderNavProjects();
});
els.navProjectList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-project-nav]");
  if (!button) return;
  openProjectFromNav(Number(button.dataset.projectNav));
});
els.globalSearchResults.addEventListener("click", (event) => {
  const button = event.target.closest("[data-search-action]");
  if (!button) return;
  handleSearchAction(button.dataset.searchAction);
});
els.openNavProjectDialog.addEventListener("click", () => {
  els.navProjectDialog.showModal();
});
els.navProjectForm.addEventListener("submit", submitNavProject);
els.cancelNavProjectButton.addEventListener("click", () => els.navProjectDialog.close());
els.navItems.forEach((item) => item.addEventListener("click", handleNavClick));
els.organizationForm.addEventListener("submit", submitOrganization);
els.projectManagementForm.addEventListener("submit", submitProjectManagement);
els.boardManagementForm.addEventListener("submit", submitBoardManagement);
els.organizationList.addEventListener("click", handleResourceAction);
els.projectList.addEventListener("click", handleResourceAction);
els.boardList.addEventListener("click", handleResourceAction);
document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-template]");
  if (!button) return;
  applyTemplate(button.dataset.template);
});
els.profileButton.addEventListener("click", openAuthView);
els.closeAuthButton.addEventListener("click", closeAuthView);
els.logoutButton.addEventListener("click", logout);
els.authForm.addEventListener("submit", (event) => {
  event.preventDefault();
  login(state.authMode);
});
els.profileForm.addEventListener("submit", submitProfile);
els.authLoginTab.addEventListener("click", () => setAuthMode("login"));
els.authRegisterTab.addEventListener("click", () => setAuthMode("register"));
els.newTaskButton.addEventListener("click", () => openTaskDrawer());
els.newColumnButton.addEventListener("click", () => els.columnDialog.showModal());
els.closeDrawerButton.addEventListener("click", closeTaskDrawer);
els.overlay.addEventListener("click", closeTaskDrawer);
els.taskForm.addEventListener("submit", submitTask);
els.deleteTaskButton.addEventListener("click", deleteSelectedTask);
els.catchupButton.addEventListener("click", getCatchUp);
els.columnForm.addEventListener("submit", submitColumn);
els.cancelColumnButton.addEventListener("click", () => els.columnDialog.close());
if (els.contextForm) {
  els.contextForm.addEventListener("submit", submitContext);
}
els.loginButton.addEventListener("click", () => login("login"));
els.registerButton.addEventListener("click", () => login("register"));

setAuthMode("login");
render();
loadAll();
