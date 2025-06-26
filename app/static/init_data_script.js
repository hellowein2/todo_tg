document.addEventListener("DOMContentLoaded", function() {
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    console.log('Куки:', document.cookie); // Логируем все куки
    console.log('user_cookie:', getCookie('user_cookie')); // Логируем конкретную куки

    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();

        if (!getCookie('user_cookie')) {
            console.log('Куки нет, отправляем запрос', getCookie('user_cookie'));
            let initData = window.Telegram.WebApp.initData;

            fetch('https://serega-sosi.ru/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ initData: initData }),
                credentials: 'include'
            })
            .then(response => {
                console.log('Статус ответа:', response.status); // Логируем статус
                return response.json();
            })
            .then(data => {
                console.log('Ответ сервера:', data);

                    console.log('Перенаправляем на /');
                    window.location.href = "/";

            }).catch(error => {
                console.error('Ошибка запроса:', error);
            });
        } else {
            console.log('Кука user_cookie уже есть, запрос не нужен');
        }
    } else {
        console.error("Telegram WebApp не найден");
    }
});