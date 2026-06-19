import json
import os

def build():
    with open("data.json") as f:
        items = json.load(f)

    lines = ["<html><body>", "<h1>Lista mea de carti</h1>", "<ul>"]
    for item in items:
        lines.append(f"  <li><strong>{item['title']}</strong>: {item['description']}</li>")
    lines.append("</ul></body></html>")

    os.makedirs("site", exist_ok=True)
    with open("site/index.html", "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    build()
