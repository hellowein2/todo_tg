document.addEventListener("DOMContentLoaded", () => {
  if (!window.Telegram?.WebApp) {
    console.error("Telegram WebApp не найден");
    document.getElementById('dataContainer')?.innerText = 'Ошибка: Telegram WebApp не найден';
    return;
  }

  window.Telegram.WebApp.ready();
  const initData = window.Telegram.WebApp.initData;

  fetch('https://sosi-serega.ru/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ initData })
  })
.then(res => {
  if (!res.ok) throw new Error(`Ошибка ${res.status}`);
  return res.json();
})
  .then(data => {
    document.getElementById('dataContainer')?.innerText = data.someField || 'Данные отсутствуют';
    if (window.location.pathname !== '/') window.location.reload();
  })
  .catch(e => {
    console.error('Ошибка запроса:', e);
    document.getElementById('dataContainer')?.innerText = 'Ошибка загрузки данных';
  });
});
