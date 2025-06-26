document.addEventListener("DOMContentLoaded", function() {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        console.log('initData:', window.Telegram.WebApp.initData);

        // Функция для проверки валидности куки и загрузки данных
        function checkAndLoadData() {
            const initData = window.Telegram.WebApp.initData;
            fetch('https://serega-sosi.ru/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                },
                body: JSON.stringify({ initData: initData }),
                credentials: 'include' // Отправляем user_cookie, если она есть
            })
            .then(response => {
                console.log('Статус ответа:', response.status);
                console.log('Response headers:', [...response.headers.entries()]);
                if (!response.ok) {
                    if (response.status === 401 || response.status === 403) {
                        // Куки недействительна, сбрасываем localStorage
                        console.log('Куки недействительна, сбрасываем user_verified');
                        localStorage.removeItem('user_verified');
                    }
                    throw new Error(`Сервер вернул ошибку: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Ответ сервера:', JSON.stringify(data, null, 2));
                // Устанавливаем флаг, если верификация прошла успешно
                localStorage.setItem('user_verified', 'true');
                // Обновляем интерфейс
                const dataContainer = document.getElementById('dataContainer');
                if (dataContainer && data.someField) { // Замените someField на нужное поле
                    dataContainer.innerText = data.someField;
                } else {
                    console.log('Данные отсутствуют или элемент UI не найден');
                    if (dataContainer) {
                        dataContainer.innerText = 'Данные отсутствуют';
                    }
                }
                // Проверяем перенаправление
                const rootPaths = ['/', '/index.html', '/index'];
                if (!rootPaths.includes(window.location.pathname)) {
                    console.log('Перенаправляем на /');
                    window.location.href = "/";
                } else {
                    console.log('Уже на главной странице, перенаправление не требуется');
                }
            })
            .catch(error => {
                console.error('Ошибка запроса:', error);
                const dataContainer = document.getElementById('dataContainer');
                if (dataContainer) {
                    dataContainer.innerText = 'Ошибка загрузки данных';
                }
            });
        }

        // Если флага нет, отправляем запрос
        if (!localStorage.getItem('user_verified')) {
            console.log('Флага нет, отправляем запрос');
            checkAndLoadData();
        } else {
            console.log('Флаг user_verified есть, проверяем валидность куки и загружаем данные');
            // Проверяем, действительна ли куки, и загружаем данные
            checkAndLoadData();
        }
    } else {
        console.error("Telegram WebApp не найден");
        const dataContainer = document.getElementById('dataContainer');
        if (dataContainer) {
            dataContainer.innerText = 'Ошибка: Telegram WebApp не найден';
        }
    }
});