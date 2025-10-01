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
    } catch (err) {
        console.error("Ошибка запроса:", err);
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
        location.reload();
    }
}

async function deleteTask() {
    const task = prompt("Введите задачу для удаления:");
    if (!task) return;

    let resp = await fetch(`/tasks/${encodeURIComponent(task)}`, {
        method: "DELETE"
    });

    if (resp.ok) {
        location.reload();
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
