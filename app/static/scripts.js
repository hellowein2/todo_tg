function addTask() {
    const newTask = prompt('Введите новую задачу:');
    if (newTask) {
        fetch('http://127.0.0.1:8000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: newTask })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Задача добавлена:', data);
            // Добавьте логику для обновления DOM, если необходимо
        })
        .catch(error => {
            console.error('Ошибка при добавлении задачи:', error);
        });
    }
}

function deleteTask() {
    const taskName = prompt('Введите задачу, которую нужно удалить:');
    if (taskName) {
        fetch(`http://127.0.0.1:8000/tasks/${taskName}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            console.log('Задача удалена:', data);
            // Добавьте логику для удаления элемента из DOM, если необходимо
        })
        .catch(error => {
            console.error('Ошибка при удалении задачи:', error);
        });
    }
}
