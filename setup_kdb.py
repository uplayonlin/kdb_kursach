import os
import zipfile
import shutil

# Конфигурация
kdb_zip_file = "/home/user/l64.zip"  # Путь к файлу l64.zip
kdb_license_file = "/home/user/kc.lic" # Путь к файлу kc.lic
kdb_install_dir = "/home/user/kdb"      # Директория для установки KDB+ (ИЗМЕНЕНО)
bashrc_file = os.path.expanduser("~/.bashrc")

def deploy_kdb():
    """Разворачивает KDB+."""

    # 1. Создание директории установки (если её нет)
    if not os.path.exists(kdb_install_dir):
        print(f"Создание директории: {kdb_install_dir}")
        os.makedirs(kdb_install_dir, exist_ok=True)  # Создать, если не существует

    # 2. Распаковка zip-файла (ИСПРАВЛЕНО)
    print(f"Распаковка {kdb_zip_file} в {kdb_install_dir}")
    try:
        with zipfile.ZipFile(kdb_zip_file, 'r') as zip_ref:
            # Получаем список файлов и папок внутри zip-архива
            members = zip_ref.namelist()
            # Проверяем, есть ли подкаталог верхнего уровня
            if len(members) > 0 and members[0].endswith('/'):
                # Если есть, то считаем, что нужно распаковать файлы в корневую директорию
                zip_ref.extractall(kdb_install_dir)
            else:
                # Если нет, то распаковываем в подкаталог
                zip_ref.extractall(kdb_install_dir)

    except zipfile.BadZipFile:
        print("Ошибка: Некорректный ZIP-файл.")
        return False

    # 3. Копирование лицензионного файла
    print(f"Копирование {kdb_license_file} в {kdb_install_dir}")
    try:
        shutil.copy(kdb_license_file, kdb_install_dir)
    except FileNotFoundError:
        print("Ошибка: Файл лицензии не найден.")
        return False

    # 4.  Добавление переменных окружения в .bashrc (или .zshrc)
    qhome_line = f"export QHOME={kdb_install_dir}"
    path_line = "export PATH=$PATH:$QHOME"

    # Проверяем, есть ли уже эти строки в файле
    with open(bashrc_file, "r") as f:
        bashrc_content = f.read()

    if qhome_line not in bashrc_content:
        print(f"Добавление QHOME в {bashrc_file}")
        with open(bashrc_file, "a") as f:
            f.write(f"\n{qhome_line}\n")
    else:
        print(f"QHOME уже определен в {bashrc_file}")

    if path_line not in bashrc_content:
        print(f"Добавление PATH в {bashrc_file}")
        with open(bashrc_file, "a") as f:
            f.write(f"{path_line}\n")
    else:
        print(f"PATH уже содержит $QHOME в {bashrc_file}")

    # 5. Установка прав на выполнение (ИСПРАВЛЕНО)

    # Поиск файла 'q' в поддиректории 'l64'
    q_executable = os.path.join(kdb_install_dir, "l64", "q")

    if os.path.exists(q_executable):
        print(f"Установка прав на выполнение для {q_executable}")
        try:
            os.chmod(q_executable, 0o755)  # rwxr-xr-x
        except OSError as e:
            print(f"Ошибка при установке прав на выполнение: {e}")
            return False
    else:
        print(f"Файл {q_executable} не найден.")
        return False


    print("KDB+ успешно развернут.")
    return True

if __name__ == "__main__":
    if deploy_kdb():
        print("Пожалуйста, выполните `source ~/.bashrc` или `source ~/.zshrc` для применения изменений переменных окружения.")
    else:
        print("Развертывание KDB+ завершилось с ошибками.")
