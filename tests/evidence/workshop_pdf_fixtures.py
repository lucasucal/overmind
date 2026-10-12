import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NumberObject,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def scan(number):
    image = Image.new("RGB", (1200, 420), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=36)
    for index, text in enumerate(
        [
            f"Service handbook page {number}",
            "Returns are accepted for thirty days.",
            "Standard delivery takes three days.",
            "Keep the original receipt for each order.",
        ]
    ):
        draw.text((50, 50 + index * 75), text, fill="black", font=font)
    return image


def document(path, pages, kind="native", marker="Document"):
    pdf = Canvas(str(path), pagesize=(612, 792), invariant=True)
    for number in range(1, pages + 1):
        if kind == "native" or (kind == "mixed" and number % 3 != 2):
            pdf.setFont("Helvetica", 14)
            pdf.drawString(60, 720, f"{marker} page {number:04d}")
            pdf.drawString(60, 690, "Invoice total: 1234.56 USD")
        if kind == "scanned" or (kind == "mixed" and number % 3 != 1):
            with scan(number) as raster:
                pdf.drawImage(ImageReader(raster), 36, 480, width=540, height=189)
        pdf.showPage()
    pdf.save()


def uncompressed_scans(path, pages):
    writer = PdfWriter()
    for number in range(1, pages + 1):
        page = writer.add_blank_page(width=612, height=792)
        with scan(number) as original, original.resize((1800, 2400)) as raster:
            image = DecodedStreamObject()
            image.set_data(raster.tobytes())
        image.update(
            {
                NameObject("/Type"): NameObject("/XObject"),
                NameObject("/Subtype"): NameObject("/Image"),
                NameObject("/Width"): NumberObject(1800),
                NameObject("/Height"): NumberObject(2400),
                NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
                NameObject("/BitsPerComponent"): NumberObject(8),
            }
        )
        page[NameObject("/Resources")] = DictionaryObject(
            {
                NameObject("/XObject"): DictionaryObject(
                    {NameObject("/Scan"): writer._add_object(image)}
                )
            }
        )
        content = DecodedStreamObject()
        content.set_data(b"q 540 0 0 189 36 480 cm /Scan Do Q")
        page[NameObject("/Contents")] = writer._add_object(content)
    writer.write(path)


def rotated_native(path):
    document(path, 4, marker="Rotated evidence")
    reader = PdfReader(str(path))
    writer = PdfWriter()
    for page, rotation in zip(reader.pages, (0, 90, 180, 270), strict=True):
        writer.add_page(page)
        writer.pages[-1].rotate(rotation)
    buffer = BytesIO()
    writer.write(buffer)
    path.write_bytes(buffer.getvalue())


def messy_report(path):
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Q3 warehouse exception log", styles["Title"]),
        Paragraph("Messy report page 0001", styles["Normal"]),
        Paragraph(
            "Returns window is thirty days from delivery. Do not rebin without a second scan.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Table(
            [
                ["SKU", "Qty", "Unit", "Line"],
                ["SKU-4419", "3", "12.50", "37.50"],
                ["SKU-8821", "1", "200.00", "200.00"],
                ["SKU-0094", "12", "0.99", "11.88"],
            ],
            colWidths=[120, 60, 80, 80],
        ),
        Spacer(1, 0.25 * inch),
        Table(
            [
                [
                    Paragraph(
                        "Aisle B7 is closed on bank holidays. Overflow sits on the north mezzanine.",
                        styles["BodyText"],
                    ),
                    Paragraph(
                        "Cycle count 8841 disagreed with WMS by four units on 12 March.",
                        styles["BodyText"],
                    ),
                ]
            ],
            colWidths=[240, 240],
        ),
        PageBreak(),
        Paragraph("Messy report page 0002", styles["Normal"]),
        Paragraph(
            "Handwritten pick notes on this page are out of scope. Typed footer: HOLD-ZONE-C.",
            styles["BodyText"],
        ),
    ]
    story[4].setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    SimpleDocTemplate(str(path), pagesize=(612, 792)).build(story)


def mixed_blank(path, pages=6, blank=(3, 6)):
    pdf = Canvas(str(path), pagesize=(612, 792), invariant=True)
    for number in range(1, pages + 1):
        if number not in blank:
            pdf.setFont("Helvetica", 14)
            pdf.drawString(60, 720, f"Mixed blank evidence page {number:04d}")
            pdf.drawString(60, 690, "Invoice total: 1234.56 USD")
        pdf.showPage()
    pdf.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    fixtures = []

    def record(name, pages, kind, expected="idle", marker=None, **extra):
        path = args.directory / name
        fixtures.append(
            {
                "filename": name,
                "pages": pages,
                "kind": kind,
                "expected": expected,
                "marker": marker,
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                **extra,
            }
        )

    for pages in (1, 10, 100, 500, 2000, 2001):
        name = f"native-{pages}.pdf"
        document(args.directory / name, pages, marker="Native evidence")
        record(name, pages, "native", "error" if pages > 2000 else "idle", "Native evidence")
    for pages in (1, 25):
        name = f"scanned-{pages}.pdf"
        document(args.directory / name, pages, "scanned")
        record(name, pages, "scanned")
    document(args.directory / "mixed-30.pdf", 30, "mixed", "Mixed evidence")
    record("mixed-30.pdf", 30, "mixed")
    rotated_native(args.directory / "rotated-native.pdf")
    record("rotated-native.pdf", 4, "rotated", marker="Rotated evidence")
    mixed_blank(args.directory / "mixed-blank-pages.pdf")
    record(
        "mixed-blank-pages.pdf",
        6,
        "mixed-blank",
        marker="Mixed blank evidence",
        blank_pages=[3, 6],
    )
    messy_report(args.directory / "messy-report.pdf")
    record(
        "messy-report.pdf",
        2,
        "report",
        marker="Messy report",
        phrases=[
            "Q3 warehouse exception log",
            "Returns window is thirty days from delivery",
            "SKU-4419",
            "SKU-8821",
            "Aisle B7 is closed on bank holidays",
            "Cycle count 8841",
            "HOLD-ZONE-C",
        ],
    )
    for pages, name, expected in (
        (3, "large-scanned.pdf", "idle"),
        (8, "near-byte-limit.pdf", "idle"),
        (9, "over-byte-limit.pdf", "error"),
    ):
        uncompressed_scans(args.directory / name, pages)
        record(name, pages, "scanned", expected)
    writer = PdfWriter()
    writer.append(PdfReader(args.directory / "native-1.pdf"))
    writer.encrypt("fixture-password")
    writer.write(args.directory / "encrypted.pdf")
    record("encrypted.pdf", 1, "encrypted", "error")
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(args.directory / "blank.pdf")
    record("blank.pdf", 1, "blank", "error")
    (args.directory / "corrupt.pdf").write_bytes(b"%PDF-1.7\ninvalid fixture\n%%EOF\n")
    record("corrupt.pdf", None, "corrupt", "error")
    for number in range(25):
        name = f"batch-{number:02d}.pdf"
        marker = f"Batch document {number:02d}"
        document(args.directory / name, 1, marker=marker)
        record(name, 1, "batch", marker=marker)
    (args.directory / "manifest.json").write_text(json.dumps(fixtures, indent=2) + "\n")
    print(json.dumps({"fixtures": len(fixtures), "bytes": sum(f["bytes"] for f in fixtures)}))


if __name__ == "__main__":
    main()
