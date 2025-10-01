async function verifyUser() {
    const initData = window.Telegram.WebApp.initData;

    if (!initData) {
        console.error("initData не найдено. Открой через Telegram WebApp!");
        return;
    }

    try {
        let resp = await fetch("/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ initData })
        });

        if (!resp.ok) {
            console.error("Ошибка верификации:", await resp.text());
            return;
        }

        console.log("Авторизация прошла успешно");
        await loadTasks(); // сразу загружаем список задач
    } catch (err) {
        console.error("Ошибка запроса:", err);
    }
}

// === Загрузка задач ===
async function loadTasks() {
    let resp = await fetch("/tasks");
    if (!resp.ok) {
        console.error("Ошибка загрузки задач");
        return;
    }

    let data = await resp.json();
    renderTasks(data.pending_tasks, data.completed_tasks);
}

function renderTasks(pending, completed) {
    const pendingList = document.querySelector(".task-category:nth-child(2) ul");
    const completedList = document.querySelector(".task-category:nth-child(1) ul");

    pendingList.innerHTML = "";
    completedList.innerHTML = "";

    if (completed.length > 0) {
        completed.forEach(task => {
            let li = document.createElement("li");
            li.className = "completed";
            li.textContent = task;
            completedList.appendChild(li);
        });
    } else {
        completedList.innerHTML = "<li class='pending'>Нет выполненных задач.</li>";
    }

    if (pending.length > 0) {
        pending.forEach(task => {
            let li = document.createElement("li");
            li.className = "pending";
            li.textContent = task;
            pendingList.appendChild(li);
        });
    } else {
        pendingList.innerHTML = "<li class='completed'>Нет невыполненных задач.</li>";
    }
}

// === Работа с задачами ===
async function addTask() {
    const task = prompt("Введите новую задачу:");
    if (!task) return;

    let resp = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task })
    });

    if (resp.ok) {
        await loadTasks();
    }
}

async function deleteTask() {
    const task = prompt("Введите задачу для удаления:");
    if (!task) return;

    let resp = await fetch(`/tasks/${encodeURIComponent(task)}`, {
        method: "DELETE"
    });

    if (resp.ok) {
        await loadTasks();
    }
}

function toggleComplete() {
    alert("Эта функция пока не реализована на сервере :)");
}

function remind() {
    alert("Здесь можно будет прикрутить напоминания через бота");
}

// Сначала пробуем авторизовать
verifyUser();
