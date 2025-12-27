import requests

# ===== CONFIGURATION =====
FIGMA_TOKEN = "figma token profile -settings-token-gen"
FILE_KEY = "Figma url thake file key"
OUTPUT_FILE = 'assets/colors/colors.xml'
# ==========================

headers = {
    "X-Figma-Token": FIGMA_TOKEN
}

def rgb_to_hex(r, g, b):
    """Convert Figma RGB (0–1) to 6-digit hex (no #)."""
    return "{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))

def parse_node(node, colors):
    """Recursively extract color fills."""
    if "fills" in node:
        for fill in node["fills"]:
            if fill.get("type") == "SOLID":
                color = fill["color"]
                hex_code = rgb_to_hex(color["r"], color["g"], color["b"])
                # Always 6 digits, prefixed with FF for full opacity
                modifyData = f'<color name="c{hex_code}">#FF{hex_code}</color>'
                colors.add(modifyData)

    # Recurse into children
    for child in node.get("children", []):
        parse_node(child, colors)

def main():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    print("🎨 Fetching colors from Figma...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch Figma file:", response.text)
        return

    data = response.json()
    colors = set()
    parse_node(data["document"], colors)

    # Read existing file to avoid duplicates
    existing_lines = set()
    try:
        with open(OUTPUT_FILE, 'r') as f:
            for line in f:
                existing_lines.add(line.strip())
    except FileNotFoundError:
        pass

    # Append only new colors
    with open(OUTPUT_FILE, 'a') as f:
        for color_line in sorted(colors):
            if color_line not in existing_lines:
                f.write(color_line + '\n')
                print(f"✅ Added new color: {color_line}")
            else:
                print(f"⚠️ Skipped (already exists): {color_line}")

    print("\n🎉 All Figma colors saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
