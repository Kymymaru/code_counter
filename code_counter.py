import os
import tkinter as tk
from tkinter import filedialog, ttk
from collections import defaultdict


def count_lines_chars_and_get_hierarchy(directory, file_stats=None):
    """
    Рекурсивно обходит директорию, подсчитывая строки кода, символы и формируя иерархию файлов.

    :param directory: Путь к директории для анализа
    :param file_stats: Словарь для хранения статистики каждого файла
    :return: Кортеж (иерархия файлов, общее количество строк, общее количество символов)
    """
    if file_stats is None:
        file_stats = defaultdict(lambda: {"lines": 0, "chars": 0})

    total_lines = 0
    total_chars = 0
    excluded_dirs = {'.git', '.idea', '__pycache__'}
    excluded_files = {'example.py'}
    hierarchy = []

    for item in sorted(os.listdir(directory)):
        path = os.path.join(directory, item)

        if os.path.isdir(path):
            if item not in excluded_dirs:
                sub_hierarchy, sub_lines, sub_chars = count_lines_chars_and_get_hierarchy(path, file_stats)
                hierarchy.append((item, sub_hierarchy))
                total_lines += sub_lines
                total_chars += sub_chars
        elif os.path.isfile(path):
            if item.endswith('.py') and item not in excluded_files:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len([line for line in content.splitlines() if line.strip()])
                    chars = len(content)
                hierarchy.append((item, (lines, chars)))
                total_lines += lines
                total_chars += chars
                file_stats[path] = {"lines": lines, "chars": chars}
            elif item not in excluded_files:
                hierarchy.append((item, (0, 0)))

    return hierarchy, total_lines, total_chars


class ProjectAnalyzer(tk.Tk):
    """
    Главный класс приложения для анализа структуры проекта и подсчета строк кода и символов.
    """

    def __init__(self):
        """
        Инициализация главного окна приложения и его компонентов.
        """
        super().__init__()
        self.title("Анализатор проекта")
        self.geometry("1000x600")

        self.button = tk.Button(self, text="Выбрать директорию", command=self.select_directory)
        self.button.pack(pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tree_frame = ttk.Frame(self.notebook)
        self.files_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tree_frame, text="Структура проекта")
        self.notebook.add(self.files_frame, text="Список файлов")

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(expand=True, fill='both')

        self.files_tree = ttk.Treeview(self.files_frame, columns=("File", "Lines", "Chars"), show="headings")
        self.files_tree.heading("File", text="Файл")
        self.files_tree.heading("Lines", text="Строки")
        self.files_tree.heading("Chars", text="Символы")
        self.files_tree.column("File", width=600)
        self.files_tree.column("Lines", width=100, anchor="e")
        self.files_tree.column("Chars", width=100, anchor="e")
        self.files_tree.pack(expand=True, fill='both')

        self.total_label = tk.Label(self, text="")
        self.total_label.pack(pady=10)

    def select_directory(self):
        """
        Обработчик нажатия кнопки "Выбрать директорию".
        Открывает диалог выбора директории и запускает анализ проекта.
        """
        directory = filedialog.askdirectory()
        if directory:
            file_stats = defaultdict(lambda: {"lines": 0, "chars": 0})
            hierarchy, total_lines, total_chars = count_lines_chars_and_get_hierarchy(directory, file_stats)
            self.update_tree(hierarchy)
            self.update_files_list(file_stats)
            self.total_label.config(text=f"Общее количество строк кода: {total_lines}, символов: {total_chars}")

    def update_tree(self, hierarchy, parent=""):
        """
        Обновляет дерево структуры проекта.

        :param hierarchy: Иерархия файлов и папок проекта
        :param parent: Родительский элемент в дереве (для рекурсивного вызова)
        """
        self.tree.delete(*self.tree.get_children())
        self.add_to_tree(hierarchy, parent)

    def add_to_tree(self, items, parent):
        """
        Рекурсивно добавляет элементы в дерево структуры проекта.

        :param items: Список элементов для добавления
        :param parent: Родительский элемент в дереве
        """
        for item in items:
            if isinstance(item[1], list):
                folder = self.tree.insert(parent, 'end', text=f"📁 {item[0]}")
                self.add_to_tree(item[1], folder)
            else:
                icon = "📄" if item[1][0] == 0 else "🐍"
                info = f" ({item[1][0]} строк, {item[1][1]} символов)" if item[1][0] > 0 else ""
                self.tree.insert(parent, 'end', text=f"{icon} {item[0]}{info}")

    def update_files_list(self, file_stats):
        """
        Обновляет список файлов, отсортированный по количеству строк кода.

        :param file_stats: Словарь со статистикой для каждого файла
        """
        self.files_tree.delete(*self.files_tree.get_children())
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1]['lines'], reverse=True)
        for path, stats in sorted_files:
            self.files_tree.insert("", "end", values=(path, stats['lines'], stats['chars']))


if __name__ == "__main__":
    app = ProjectAnalyzer()
    app.mainloop()