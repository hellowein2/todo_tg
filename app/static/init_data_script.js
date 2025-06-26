document.addEventListener("DOMContentLoaded", function() {
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();

        if (!getCookie('user_cookie')) { // Запускаем только если куки нет
            let initData = window.Telegram.WebApp.initData;

            fetch('https://serega-sosi.ru/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ initData: initData }),
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Ответ сервера:', data);
                window.location.href = "/";
            }).catch(error => {
                console.error('Ошибка:', error);
            });
        } else {
            console.log('Кука user_cookie уже есть, запрос не нужен');
        }
    } else {
        console.error("Telegram WebApp не найден");
    }
});
