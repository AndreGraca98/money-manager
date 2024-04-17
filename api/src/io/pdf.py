from pathlib import Path

import PIL.Image
import pypdfium2 as pdfium


def convert_pdf_to_images(pdf_path: Path | str) -> list[Path]:
    """Convert a PDF file to a series of images.
    The images are saved in a folder `images` in the same folder as the PDF file,
    in JPEG format with a quality of 95. Images are saved with the format `00.jpg`,
    `01.jpg`, etc.
    Returns a list of paths to the saved images.
    """
    pdf_path = Path(pdf_path).resolve()
    out_folder = pdf_path.parent / "images"
    out_folder.mkdir(parents=True, exist_ok=True)

    pdf = pdfium.PdfDocument(str(pdf_path))
    img_paths: list[Path] = []
    for i, page in enumerate(pdf):
        # scale=5 for better quality picture
        img: PIL.Image.Image = page.render(scale=5).to_pil()
        # Image saved in format: /tmp/mm/abc/images/00.jpg
        img_path = out_folder / f"{i:02}.jpg"
        img.save(img_path, format="JPEG", subsampling=0, quality=95)
        img_paths.append(img_path)
    return img_paths
