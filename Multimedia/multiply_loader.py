import requests
from pathlib import Path

# Абсолютный путь к папке для загрузок
DOWNLOAD_DIR = Path("/home/ss/PycharmProjects/VK_prod/Downloads")


async def multiply_loader(self, attachments_list, user_id, session_id, post, link):
    print("Начало загрузки файлов")
    print("Получены вложения:", attachments_list)

    # Создаем папку для загрузок (если не существует)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Файлы будут сохранены в: {DOWNLOAD_DIR}")

    for i, url in enumerate(attachments_list):
        try:
            # Формируем имя файла
            filename = f"downloaded_file_{i}_{user_id}_{session_id}.jpg"
            file_path = DOWNLOAD_DIR / filename

            print(f"Загрузка файла {i + 1} из {len(attachments_list)}...")

            # Загружаем файл с обработкой возможных ошибок
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Проверяем статус ответа

            # Сохраняем файл
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Фильтруем keep-alive chunks
                        f.write(chunk)

            print(f"Файл успешно сохранен: {file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке файла {url}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    print("Загрузка завершена")
    await self.multiply_correct_attachments(self, user_id, session_id, post, link)
    return True