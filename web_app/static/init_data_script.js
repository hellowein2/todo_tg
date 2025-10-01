document.addEventListener("DOMContentLoaded", function() {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        console.log('initData:', window.Telegram.WebApp.initData);

        function checkAndLoadData() {
            const initData = window.Telegram.WebApp.initData;
            fetch('https://sosi-serega.ru/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ initData }),
                credentials: 'include' // чтобы отправлять куки
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Ошибка верификации:', response.status);
                    localStorage.removeItem('user_verified');
                    throw new Error(`Ошибка верификации: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Верификация успешна:', data);
                localStorage.setItem('user_verified', 'true');
                // Перезагружаем страницу, чтобы куки применились и задачи загрузились
                window.location.reload();
            })
            .catch(error => {
                console.error('Ошибка запроса:', error);
                const dataContainer = document.getElementById('dataContainer');
                if (dataContainer) {
                    dataContainer.innerText = 'Ошибка загрузки данных';
                }
            });
        }

        if (!localStorage.getItem('user_verified')) {
            console.log('Флага нет, запускаем валидацию');
            checkAndLoadData();
        } else {
            console.log('Профиль проверен, загружаем задачи обычным способом');
            // Здесь лучше просто сделать fetch запрос на твой API, чтобы загрузить задачи,
            // куки уже есть, сервер их прочитает
            loadTasks();
        }

        // Пример функции загрузки задач (замени на свой код)
        function loadTasks() {
            fetch('/tasks', { credentials: 'include' })
            .then(res => res.json())
            .then(tasks => {
                const container = document.getElementById('dataContainer');
                if (container) {
                    container.innerText = JSON.stringify(tasks, null, 2);
                }
            })
            .catch(err => console.error('Ошибка загрузки задач:', err));
        }

    } else {
        console.error("Telegram WebApp не найден");
        const dataContainer = document.getElementById('dataContainer');
        if (dataContainer) {
            dataContainer.innerText = 'Ошибка: Telegram WebApp не найден';
        }
    }
});
