from pdf2image import convert_from_path

def convert_pdf_to_jpeg(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i+1}.jpeg", "JPEG")

# Example usage

path = "/Users/haritha/Desktop/OS Lab01/test/"
pdf_file = path+"E18118_Lab01.pdf"
output_folder = path

convert_pdf_to_jpeg(pdf_file, output_folder)