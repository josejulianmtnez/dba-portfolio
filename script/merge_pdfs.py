import os
from PyPDF2 import PdfMerger

evidences_dir = "evidences"
output_dir = "final_portfolio"

def merge_pdfs_in_folder(input_dir, output_name):
    path_folder = os.path.join(evidences_dir, input_dir)
    files_pdf = sorted([
        os.path.join(path_folder, f) for f in os.listdir(path_folder)
        if f.endswith('.pdf')
    ])

    if not files_pdf:
        print(f"No se encontraron archivos PDF en el directorio: {path_folder}.")
        return
    
    output_path = os.path.join(output_dir, output_name)
    merger = PdfMerger()

    for pdf in files_pdf:
        merger.append(pdf)
    
    merger.write(output_path)
    merger.close()
    print(f"PDFs fusionados en: {output_path}")

def main():
    os.makedirs(output_dir, exist_ok=True)
    
    merge_pdfs_in_folder("first_partial", "first_complete_partial.pdf")
    merge_pdfs_in_folder("second_partial", "second_complete_partial.pdf")
    merge_pdfs_in_folder("third_partial", "third_complete_partial.pdf")

    merger = PdfMerger()
    merger.append(os.path.join(output_dir, "first_complete_partial.pdf"))
    merger.append(os.path.join(output_dir, "second_complete_partial.pdf"))
    merger.append(os.path.join(output_dir, "third_complete_partial.pdf"))
    merger.close()

    print("✔ Portafolio final generado.")

if __name__ == "__main__":
    main()
