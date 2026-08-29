import fitz
import os
import json

pdf_path = "sample.pdf"
output_folder = "extracted_images"

os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)

metadata = []

for page_number, page in enumerate(doc, start=1):

    images = page.get_images(full=True)

    for image_number, image in enumerate(images, start=1):

        xref = image[0]

        image_data = doc.extract_image(xref)

        image_bytes = image_data["image"]
        image_ext = image_data["ext"]

        image_id = f"page_{page_number}_image_{image_number}"

        filename = f"{image_id}.{image_ext}"
        output_path = os.path.join(output_folder, filename)

        with open(output_path, "wb") as file:
            file.write(image_bytes)

        metadata.append({
            "image_id": image_id,
            "page_number": page_number,
            "image_path": output_path
        })

        print(f"Extracted: {filename}")

doc.close()

with open("metadata.json", "w") as file:
    json.dump(metadata, file, indent=4)

print("Image extraction completed!")
print("Metadata created!")