import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

evidences_dir = "evidence"
partial_dirs = ["first_partial", "second_partial", "third_partial"]

def get_next_serial(folder_path):
    existing = [
        f for f in os.listdir(folder_path)
        if f.endswith('.pdf') and f[:2].isdigit()
    ]
    if not existing:
        return 1
    last_num = max(int(f[:2]) for f in existing)
    return last_num + 1

def rename_single_pdf(filepath):
    folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if filename[:2].isdigit():
        print(f"⏩ Ya tiene número: {filename}")
        return

    serial = get_next_serial(folder)
    new_name = f"{serial:02d}_{filename}"
    new_path = os.path.join(folder, new_name)

    time.sleep(1)

    try:
        os.rename(filepath, new_path)
        print(f"✅ Renombrado: {filename} → {new_name}")
    except Exception as e:
        print(f"⚠ Error al renombrar {filename}: {e}")

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            print(f"\n📥 PDF nuevo detectado: {event.src_path}")
            rename_single_pdf(event.src_path)

def main():
    observer = Observer()
    for folder in partial_dirs:
        path = os.path.join(evidences_dir, folder)
        os.makedirs(path, exist_ok=True)
        observer.schedule(PDFHandler(), path=path, recursive=False)
        print(f"👁️ Observando carpeta: {path}")

    observer.start()
    try:
        print("\n🌀 Esperando nuevos archivos... (Ctrl+C para detener)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Observador detenido.")
    observer.join()

if __name__ == "__main__":
    main()
