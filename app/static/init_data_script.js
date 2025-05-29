document.addEventListener("DOMContentLoaded", function() {
    if (window.Telegram && window.Telegram.WebApp) {
        // Инициализация вашего Web App
        window.Telegram.WebApp.ready();

        // Получение initData
        const initData = window.Telegram.WebApp.initData;

        // Выполнение запроса к серверу
        fetch('https://sosi-serega.ru/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ initData })
        })
        .then(response => response.json())
        .then(data => {
            console.log('User ID:', data.user_id);
            alert('Ваш User ID: ' + data.user_id);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при получении User ID');
        });
    } else {
        console.error("соси");
    }
});