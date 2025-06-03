document.addEventListener("DOMContentLoaded", function() {
    if (window.Telegram && window.Telegram.WebApp) {
        // Инициализация Web App
        window.Telegram.WebApp.ready();

        // Получаем initData (строка параметров)
        let initData = window.Telegram.WebApp.initData;

        // Отправляем initData на бек
        fetch('https://serega-sosi.ru/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ initData: initData }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Ответ сервера:', data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    } else {
        console.error("Telegram WebApp не найден");
    }
});
