#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания версий задач без решений
Обрабатывает все файлы из md_src и создает версии только с задачами в папке tasks_only
"""

import os
import re

def process_file(input_path, output_path):
    """Обрабатывает один файл, удаляя секцию с решением"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем секцию с решением
    # Паттерн для поиска секции "## ✅ Решение" и всего что после неё
    solution_pattern = r'---\s*\n\s*## ✅ Решение.*$'
    
    # Удаляем секцию с решением
    processed_content = re.sub(solution_pattern, '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Убираем лишние пустые строки в конце
    processed_content = processed_content.rstrip() + '\n'
    
    # Записываем обработанный файл
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"✅ Обработан: {os.path.basename(input_path)}")

def main():
    """Основная функция"""
    
    # Пути к папкам
    source_dir = "md_src"
    target_dir = "tasks_only"
    
    # Проверяем существование исходной папки
    if not os.path.exists(source_dir):
        print(f"❌ Папка {source_dir} не найдена!")
        return
    
    # Создаем целевую папку если её нет
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"📁 Создана папка {target_dir}")
    
    # Получаем список всех .md файлов
    md_files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    
    if not md_files:
        print(f"❌ В папке {source_dir} не найдено .md файлов!")
        return
    
    print(f"🚀 Начинаем обработку {len(md_files)} файлов...")
    
    # Обрабатываем каждый файл
    for md_file in sorted(md_files):
        input_path = os.path.join(source_dir, md_file)
        output_path = os.path.join(target_dir, md_file)
        
        try:
            process_file(input_path, output_path)
        except Exception as e:
            print(f"❌ Ошибка при обработке {md_file}: {e}")
    
    print(f"\n🎉 Обработка завершена!")
    print(f"📁 Результаты сохранены в папке: {target_dir}")
    print(f"📊 Обработано файлов: {len(md_files)}")

if __name__ == "__main__":
    main()
