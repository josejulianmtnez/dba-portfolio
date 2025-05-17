import os
from PyPDF2 import PdfMerger

evidences_dir = "evidence"
output_dir = "partial_portfolio"
final_output_dir = "final_portfolio"

def merge_pdfs_in_folder(input_dir, output_name):
    path_folder = os.path.join(evidences_dir, input_dir)
    files_pdf = sorted([
        os.path.join(path_folder, f) for f in os.listdir(path_folder)
        if f.endswith('.pdf')
    ])

    if not files_pdf:
        print(f"No se encontraron archivos PDF en el directorio: {path_folder}.")
        return None
    
    output_path = os.path.join(output_dir, output_name)
    merger = PdfMerger()

    for pdf in files_pdf:
        merger.append(pdf)
    
    merger.write(output_path)
    merger.close()
    print(f"PDFs fusionados en: {output_path}")
    return output_path

def main():
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(final_output_dir, exist_ok=True)

    generated_partials = []

    result = merge_pdfs_in_folder("first_partial", "P1_Portafolio_MDLCJJ_8IDS1.pdf")
    if result:
        generated_partials.append(result)

    for folder, filename in [
        ("second_partial", "P2_Portafolio_MDLCJJ_8IDS1.pdf"),
        ("third_partial", "P3_Portafolio_MDLCJJ_8IDS1.pdf")
    ]:
        path = os.path.join(evidences_dir, folder)
        if os.path.exists(path):
            has_pdfs = any(f.endswith('.pdf') for f in os.listdir(path))
            if has_pdfs:
                result = merge_pdfs_in_folder(folder, filename)
                if result:
                    generated_partials.append(result)

    if generated_partials:
        final_path = os.path.join(final_output_dir, "Portafolio_MDLCJJ_8IDS1.pdf")
        merger = PdfMerger()
        for partial in generated_partials:
            merger.append(partial)
        merger.write(final_path)
        merger.close()
        print(f"\n🎉 Portafolio final generado exitosamente en: {final_path}")
    else:
        print("⚠ No se generaron los archivos del Parcial. Portafolio final no creado.")

if __name__ == "__main__":
    main()
