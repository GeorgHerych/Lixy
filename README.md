# Lixy Headless + Clients

Цей репозиторій тепер містить Django-бекенд з REST API, а також стартові клієнти на React (web) та React Native (mobile).

## Запуск бекенду

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Запуск веб-клієнта (React)

```bash
cd web
npm install
npm run dev
```

За потреби можна вказати адресу бекенду у файлі `.env`:

```
VITE_API_URL=http://localhost:8000/api
```

## Запуск мобільного клієнта (React Native / Expo)

```bash
cd mobile
npm install
npx expo start
```

Для емулятора або фізичного пристрою встановіть змінну середовища `EXPO_PUBLIC_API_URL`, щоб Expo знала адресу сервера.

API сервера очікується за адресою `http://localhost:8000`.
