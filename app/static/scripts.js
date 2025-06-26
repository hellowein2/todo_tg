function addTaskToDOM(task, category) {
    const ulSelector = category === 'completed_tasks' ? '.task-category:nth-of-type(1) ul' : '.task-category:nth-of-type(2) ul';
    const ul = document.querySelector(ulSelector);

    if (!ul) {
        console.error(`Ошибка: элемент списка ${ulSelector} не найден.`);
        return;
    }

    const listItem = document.createElement('li');
    listItem.className = category === 'completed_tasks' ? 'completed' : 'pending';
    listItem.textContent = task;

    ul.appendChild(listItem);
}

function addTask() {
    const newTask = prompt('Введите новую задачу:');
    if (newTask) {
        fetch('https://serega-sosi.ru/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: newTask })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Задача добавлена:', data);
            // Добавляем новую задачу в "невыполненные задачи"
            addTaskToDOM(newTask, 'pending_tasks');
        })
        .catch(error => {
            console.error('Ошибка при добавлении задачи:', error);
        });
    }
}

function deleteTask() {
    const taskName = prompt('Введите задачу, которую нужно удалить:');
    if (taskName) {
        fetch(`http://localhost:8000/tasks/${encodeURIComponent(taskName)}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            console.log('Задача удалена:', data);
            // Удаляем задачу из DOM
            removeTaskFromDOM(taskName);
        })
        .catch(error => {
            console.error('Ошибка при удалении задачи:', error);
        });
    }
}

function removeTaskFromDOM(taskName) {
    const taskListItems = document.querySelectorAll('.task-list ul li');
    taskListItems.forEach(item => {
        if (item.textContent === taskName) {
            item.remove();
        }
    });
}
