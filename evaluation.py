import os
import re

# Configuración: extensiones, exclusiones, etc.
JAVA_EXTENSION = ".java"
EXCLUDED_DIRS = {"build", "target", ".git", ".idea", "out", "test"}

def is_excluded(path):
    return any(excluded in path.split(os.sep) for excluded in EXCLUDED_DIRS)

def strip_comments(java_code):
    """
    Elimina comentarios de línea (//) y bloque (/* */) de código Java.
    """
    # Eliminar comentarios de bloque
    code_no_block_comments = re.sub(r"/\*.*?\*/", "", java_code, flags=re.DOTALL)
    # Eliminar comentarios de línea
    code_no_line_comments = re.sub(r"//.*", "", code_no_block_comments)
    return code_no_line_comments

def analyze_java_project(root_dir="."):
    num_files = 0
    num_classes = 0
    num_code_lines = 0

    for dirpath, _, filenames in os.walk(root_dir):
        if is_excluded(dirpath):
            continue

        for filename in filenames:
            if not filename.endswith(JAVA_EXTENSION):
                continue

            num_files += 1
            filepath = os.path.join(dirpath, filename)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    clean_code = strip_comments(content)

                    # Contar clases reales (usando regex simple)
                    class_matches = re.findall(r"(?m)^\s*(public\s+)?(abstract\s+)?(final\s+)?class\s+\w+", clean_code)
                    num_classes += len(class_matches)

                    # Contar líneas de código no vacías (después de eliminar comentarios)
                    lines = clean_code.splitlines()
                    num_code_lines += sum(1 for line in lines if line.strip())
            except Exception as e:
                print(f"Error leyendo {filepath}: {e}")

    return num_files, num_classes, num_code_lines


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cuenta ficheros, clases y líneas de código en un proyecto Java.")
    parser.add_argument("path", help="Ruta al proyecto Java")
    parser.add_argument("--exclude", nargs="*", help="Carpetas a excluir", default=[])
    args = parser.parse_args()

    if args.exclude:
        EXCLUDED_DIRS.update(args.exclude)

    files, classes, lines = analyze_java_project(args.path)

    print("\n📊 Estadísticas del proyecto Java")
    print(f"📁 Ficheros .java:     {files}")
    print(f"🏷️  Clases detectadas:  {classes}")
    print(f"📏 Líneas de código:   {lines}")
