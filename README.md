# Python-documents

# Proxy Management System (Backend)

Веб-сервис для управления доверенностями и справочниками. Архитектура: Routes -> Controllers -> Services -> Repositories.

## Стек

- **Язык:** Python 3.x
- **Фреймворк:** Flask, Flask-CORS
- **БД:** MongoDB (PyMongo)
- **Тестирование:** Postman

## Запуск

1. Установить зависимости:
   ```
   pip install flask pymongo flask-cors
   ```
2. Запустить сервер:
   ```
   python main.py
   ```
3. Сервер доступен по адресу: http://127.0.0.1:5000

# Document Flow System (Frontend)

SPA для управления доверенностями. Vue 3 + Vuex + Vue Router + Axios.

## Стек

- **Framework:** Vue.js 3
- **State:** Vuex 4
- **Routing:** Vue Router 4
- **HTTP:** Axios
- **UI:** Bootstrap 5

## Архитектура

- `views/` — страницы приложения
- `components/` — переиспользуемые UI-элементы
- `store/` — централизованное состояние (actions, mutations, getters)
- `router/` — конфигурация маршрутов

## Запуск

1. Установить зависимости:
   ```bash
   npm install
   ```

# document-flow-app

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
