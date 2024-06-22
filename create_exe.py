import os
import subprocess
import sys


def create_exe(script_name, output_name):
    """
    Создает .exe файл из Python скрипта с использованием PyInstaller.

    :param script_name: Имя исходного Python файла
    :param output_name: Желаемое имя выходного .exe файла
    """
    print(f"Начинаем создание .exe файла из {script_name}...")

    # Проверяем, установлен ли PyInstaller
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("PyInstaller не установлен. Устанавливаем...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Создаем команду для PyInstaller
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--name={output_name}",
        script_name
    ]

    # Запускаем PyInstaller
    try:
        subprocess.run(command, check=True)
        print(f"Создание .exe файла завершено успешно!")
        print(f"Вы можете найти {output_name}.exe в папке 'dist'")
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка при создании .exe файла: {e}")


if __name__ == "__main__":
    # Имя вашего исходного Python файла
    script_name = "code_counter.py"

    # Желаемое имя выходного .exe файла
    output_name = "CodeCounter"

    # Проверяем существование исходного файла
    if not os.path.exists(script_name):
        print(f"Ошибка: Файл {script_name} не найден.")
        sys.exit(1)

    create_exe(script_name, output_name)
