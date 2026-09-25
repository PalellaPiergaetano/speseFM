"""Converte il foglio spese in un CSV normalizzato, usando solo il venv del progetto."""

from __future__ import annotations

import csv
import posixpath
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def shared_strings(book: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in book.namelist():
        return []
    root = ElementTree.fromstring(book.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.findall(".//x:t", NS)) for item in root.findall("x:si", NS)]


def worksheet_targets(book: zipfile.ZipFile) -> dict[str, bytes]:
    relations = ElementTree.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    relation_map = {
        relation.attrib["Id"]: posixpath.normpath(posixpath.join("xl", relation.attrib["Target"].lstrip("/")))
        for relation in relations
        if relation.attrib.get("Type", "").endswith("/worksheet")
    }
    workbook = ElementTree.fromstring(book.read("xl/workbook.xml"))
    targets = {}
    for sheet in workbook.findall("x:sheets/x:sheet", NS):
        relation_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = relation_map.get(relation_id or "")
        if target in book.namelist():
            targets[sheet.attrib["name"]] = book.read(target)
    return targets


def export(source: Path, destination: Path) -> int:
    with zipfile.ZipFile(source) as book:
        strings = shared_strings(book)
        rows_out: list[dict[str, str]] = []
        for sheet_name, sheet_bytes in worksheet_targets(book).items():
            if sheet_name.strip().lower() == "template":
                continue
            root = ElementTree.fromstring(sheet_bytes)
            for row in root.findall(".//x:row", NS):
                cells = row.findall("x:c", NS)
                values = []
                for cell in cells:
                    value = cell.findtext("x:v", default="", namespaces=NS)
                    if cell.attrib.get("t") == "s" and value:
                        value = strings[int(value)]
                    values.append(value)
                if any(values):
                    rows_out.append({"mese": sheet_name, "riga": str(row.attrib["r"]), "valori": " | ".join(values)})
    with destination.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["mese", "riga", "valori"])
        writer.writeheader()
        writer.writerows(rows_out)
    return len(rows_out)


if __name__ == "__main__":
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "Foglio spese.xlsx")
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "tools/spese_importate.csv")
    print(f"Esportate {export(input_path, output_path)} righe in {output_path}")