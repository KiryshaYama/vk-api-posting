# Публикация комиксов

Скрипт скачивает рандомную картинку и комментарий автора с сайта [xkcd.com](https://xkcd.com)

Постит данную картинку в группу [VK](https://vk.com/groups), удаляя файл картинки из папки после публикации
### Как установить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости

```sh
pip install -r requirements.txt
```

Запустите скрипт

```sh
python script.py
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `script.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 2 переменные:
- `ACCESS_TOKEN` — Токен Вконтакте
- `GROUP_ID` — ID группы Вконтакте
- `API_VERSION` — актуальная версия API Вконтакте

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).