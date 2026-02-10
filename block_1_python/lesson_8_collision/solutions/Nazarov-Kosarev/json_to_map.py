"""Конвертирует map.json (cells, cols, rows) в map.txt для main.py."""
import json
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(dir_path, "map.json")
txt_path = os.path.join(dir_path, "map.txt")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cols = data["cols"]
rows = data["rows"]
filled = set(tuple(cell) for cell in data["cells"])  # (c, r) = (x, y)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(f"{cols} {rows}\n")
    for r in range(rows):
        line = "".join("1" if (c, r) in filled else "0" for c in range(cols))
        f.write(line + "\n")

print("map.txt OK:", cols, "x", rows, "cells:", len(filled))
