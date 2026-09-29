from grawlix.book import PdfInParts
from .output_format import OutputFormat, Update
from io import BytesIO
from pypdf import PdfWriter
from zipfile import ZipFile

class Pdf(OutputFormat):
    extension = "pdf"
    input_types = [PdfInParts]

    async def download(self, book: Book, location: str, update: Update) -> None:
        if isinstance(book.data, PdfInParts):
            await self._download_pdf_in_parts(book.data, book.metadata, location, update)
        else:
            raise UnsupportedOutputFormat

    async def _download_pdf_in_parts(self, data: EpubInParts, metadata: Metadata, location: str, update: Update) -> None:
        files = data.files
        file_count = len(files)
        progress = 1/(file_count)
        output = PdfWriter()

        for file in files:
            content = await self._download_file(file)
            with ZipFile(BytesIO(content), "r") as zipfile:
                for filename in zipfile.namelist():
                    if not filename.endswith(".pdf"):
                        continue
                    with zipfile.open(filename, "r") as pdf:
                        output.append(pdf)
            if update:
                update(progress)

        output.write(location)
        output.close()
        exit()
