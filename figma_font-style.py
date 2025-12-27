# import json
# import requests
# import re

# # --- Dart textStyle template ---
# template = '''  static final textStyle{size}c{color}{fontName}{fontWeight}=TextStyle( 
#   fontFamily: "{font}", 
#   fontFamilyFallback: const ['DMSans', 'Open Sans', 'Roboto', 'Noto Sans'], 
#   color: AppColors.c{color}, 
#   fontSize: {size}.sp, 
#   fontWeight: FontWeight.w{fontWeight}, 
# );'''

# # --- Figma API settings ---
# FIGMA_TOKEN = "figma token profile -settings-token-gen"
# FILE_KEY = "Figma url thake file key"

# headers = {
#     "X-Figma-Token": FIGMA_TOKEN
# }

# # --- Fetch Figma nodes ---
# def fetch_figma_nodes():
#     url = f"https://api.figma.com/v1/files/{FILE_KEY}"
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print("Failed to fetch Figma nodes:", response.text)
#         return {}
#     return response.json()

# # --- Convert Figma color RGBA to hex without # ---
# def rgba_to_hex(rgba):
#     r = round(rgba['r'] * 255)
#     g = round(rgba['g'] * 255)
#     b = round(rgba['b'] * 255)
#     a = round(rgba.get('a', 1) * 255)
#     return f"{r:02X}{g:02X}{b:02X}"
#  # # বাদ দেওয়া

# # --- Parse text style properties ---
# def parse_text_style(node):
#     try:
#         style = node['style']
#         fontFamily = style.get('fontFamily', 'Poppins')
#         fontWeight = style.get('fontWeight', 400)
#         fontSize = int(style.get('fontSize', 14))
#         fills = node.get('fills', [])
#         color = "00000000"
#         if fills:
#             solid_fill = next((f for f in fills if f['type']=="SOLID"), None)
#             if solid_fill:
#                 color = rgba_to_hex(solid_fill['color'])
#         return fontFamily, fontWeight, fontSize, color
#     except Exception as e:
#         return "Poppins", 400, 14, "00000000"

# # --- Generate Dart lines ---
# def generate_dart_from_nodes(nodes):
#     dart_lines = []
#     unique_lines = set()
    
#     def traverse(node):
#         if 'children' in node:
#             for child in node['children']:
#                 traverse(child)
#         if node.get('type') == "TEXT":
#             fontFamily, fontWeight, fontSize, color = parse_text_style(node)
#             fontName = re.sub(r'\W+', '', fontFamily)
#             line = template_google_fonts.format(
#                 size=fontSize,
#                 color=color,  # # থাকবে না
#                 fontName=fontName,
#                 fontWeight=fontWeight
#             )
#             if line not in unique_lines:
#                 unique_lines.add(line)
#                 dart_lines.append(line)
    
#     traverse(nodes['document'])
#     return dart_lines

# # --- Main ---
# figma_nodes = fetch_figma_nodes()
# dart_lines = generate_dart_from_nodes(figma_nodes)

# # --- Write to Dart file ---
# with open("lib/constants/text_font_style.dart", "w") as f:
#     for line in dart_lines:
#         f.write(line + "\n")
#         print(f"Added Figma textStyle: {line}")

# print("✅ text_font_style.dart generated with pure hex color (no #).")


import json
import requests
import re

# --- Dart textStyle template ---
template = '''  static final textStyle{size}c{color}{fontName}{fontWeight} = TextStyle(
    fontFamily: "{font}",
    fontFamilyFallback: const ['DMSans', 'Open Sans', 'Roboto', 'Noto Sans'],
    color: AppColors.c{color},
    fontSize: {size}.sp,
    fontWeight: FontWeight.w{fontWeight},
  );'''

# --- Figma API settings ---
FIGMA_TOKEN = "figma token profile -settings-token-gen"
FILE_KEY = "Figma url thake file key"

headers = {
    "X-Figma-Token": FIGMA_TOKEN
}

# --- Fetch Figma nodes ---
def fetch_figma_nodes():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch Figma nodes:", response.text)
        return {}
    print("✅ Successfully fetched Figma file data.")
    return response.json()

# --- Convert RGBA to hex (no #) ---
def rgba_to_hex(rgba):
    r = round(rgba['r'] * 255)
    g = round(rgba['g'] * 255)
    b = round(rgba['b'] * 255)
    return f"{r:02X}{g:02X}{b:02X}"

# --- Parse text style ---
def parse_text_style(node):
    try:
        style = node['style']
        fontFamily = style.get('fontFamily', 'Poppins')
        fontWeight = style.get('fontWeight', 400)
        fontSize = int(style.get('fontSize', 14))
        fills = node.get('fills', [])
        color = "000000"
        if fills:
            solid_fill = next((f for f in fills if f['type'] == "SOLID"), None)
            if solid_fill:
                color = rgba_to_hex(solid_fill['color'])
        return fontFamily, fontWeight, fontSize, color
    except Exception as e:
        print(f"⚠️ Error parsing node: {e}")
        return "Poppins", 400, 14, "000000"

# --- Generate Dart styles from Figma nodes ---
def generate_dart_from_nodes(nodes):
    dart_lines = []
    unique_lines = set()

    def traverse(node):
        if 'children' in node:
            for child in node['children']:
                traverse(child)
        if node.get('type') == "TEXT":
            fontFamily, fontWeight, fontSize, color = parse_text_style(node)
            fontName = re.sub(r'\W+', '', fontFamily)
            line = template.format(
                size=fontSize,
                color=color,
                fontName=fontName,
                fontWeight=fontWeight,
                font=fontFamily
            )
            if line not in unique_lines:
                unique_lines.add(line)
                dart_lines.append(line)

    traverse(nodes['document'])

    # Sort by size then weight for cleaner output
    dart_lines.sort(key=lambda l: (int(re.search(r"textStyle(\d+)", l).group(1)), l))
    return dart_lines

# --- Main execution ---
if __name__ == "__main__":
    figma_nodes = fetch_figma_nodes()
    if not figma_nodes:
        exit(1)

    dart_lines = generate_dart_from_nodes(figma_nodes)

    output_path = "lib/constants/text_font_style.dart"
    with open(output_path, "w") as f:
        for line in dart_lines:
            f.write(line + "\n")
            print(f"✅ Added textStyle: {line}")

    print(f"\n🎉 File successfully generated at: {output_path}")
