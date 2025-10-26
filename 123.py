from pathlib import Path

def process_python_files(directory="."):
    path = Path(directory)
    
    for file_path in path.rglob("*.py"):
        print(f"Обрабатываем файл: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                    f.write(line)

process_python_files()