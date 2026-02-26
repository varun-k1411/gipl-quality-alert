from PIL import Image, ImageDraw, ImageFont
import os

# ======================
# DOCUMENT CONTROL
# ======================

COMPANY = "GABRIL INDUSTRIES PVT. LTD."
DOCUMENT_NO = "GIPL-QA-001"
REVISION_NO = "00"

FONT_PATH = "DejaVuSans.ttf"


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


# Schaeffler font hierarchy
title_font = load_font(64)
header_font = load_font(34)
label_font = load_font(28)
text_font = load_font(30)


# ======================
# GENERATOR
# ======================

def generate_alert(data, defect_path, ok_path=None):

    W, H = 1650, 1150

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    margin = 40

    # ======================
    # LOGO + COMPANY HEADER
    # ======================

    if os.path.exists("logo.png"):

        logo = Image.open("logo.png").resize((240, 80))
        img.paste(logo, (margin, margin))

    draw.text(
        (margin + 300, margin + 10),
        COMPANY,
        font=header_font,
        fill="black"
    )

    draw.text(
        (W//2 - 200, margin + 90),
        "QUALITY ALERT",
        font=title_font,
        fill="black"
    )

    # ======================
    # DOCUMENT CONTROL BAR
    # ======================

    y = margin + 180

    draw.rectangle(
        (margin, y, W-margin, y+80),
        outline="black",
        width=2
    )

    draw.text(
        (margin+15, y+10),
        f"Document No : {DOCUMENT_NO}",
        font=label_font,
        fill="black"
    )

    draw.text(
        (margin+15, y+45),
        f"Revision No : {REVISION_NO}",
        font=label_font,
        fill="black"
    )

    draw.text(
        (W//2-150, y+10),
        f"Issue Date : {data['date']}",
        font=label_font,
        fill="black"
    )

    draw.text(
        (W-450, y+10),
        f"NC No : {data['nc_no']}",
        font=label_font,
        fill="black"
    )

    draw.text(
        (W-450, y+45),
        f"Barcode No : {data['barcode_no']}",
        font=label_font,
        fill="black"
    )

    # ======================
    # TRACEABILITY GRID
    # ======================

    y += 100

    draw.rectangle(
        (margin, y, W-margin, y+320),
        outline="black",
        width=2
    )

    left_x = margin + 15
    right_x = W//2 + 50

    line_y = y + 15
    gap = 45

    left_fields = [

        ("Customer", data["customer"]),
        ("Supplier", COMPANY),
        ("Part No", data["part_no"]),
        ("Description", data["description"]),
        ("Size", data["size"]),
        ("Grade", data["grade"])

    ]

    right_fields = [

        ("Process Step", data["process"]),
        ("Machine No", data["machine"]),
        ("Operator", data["operator"]),
        ("Shift", data["shift"]),
        ("Defect", data["defect"]),
        ("Quantity", str(data["qty"]))

    ]

    for i in range(6):

        draw.text(
            (left_x, line_y),
            f"{left_fields[i][0]:15} : {left_fields[i][1]}",
            font=text_font,
            fill="black"
        )

        draw.text(
            (right_x, line_y),
            f"{right_fields[i][0]:15} : {right_fields[i][1]}",
            font=text_font,
            fill="black"
        )

        line_y += gap

    # ======================
    # IMAGE HEADERS
    # ======================

    y += 360

    box_h = 60

    draw.rectangle(
        (margin, y, W//2 - 10, y+box_h),
        fill=(220,0,0)
    )

    draw.rectangle(
        (W//2 + 10, y, W-margin, y+box_h),
        fill=(0,150,0)
    )

    draw.text(
        (margin + 260, y+12),
        "NOT OK",
        font=header_font,
        fill="white"
    )

    draw.text(
        (W//2 + 260, y+12),
        "OK",
        font=header_font,
        fill="white"
    )

    # ======================
    # IMAGE BOXES
    # ======================

    y += box_h + 10

    draw.rectangle(
        (margin, y, W//2 - 10, y+320),
        outline="black",
        width=2
    )

    draw.rectangle(
        (W//2 + 10, y, W-margin, y+320),
        outline="black",
        width=2
    )

    if defect_path and os.path.exists(defect_path):

        defect = Image.open(defect_path)
        defect.thumbnail((700, 300))

        img.paste(
            defect,
            (margin+40, y+10)
        )

    if ok_path and os.path.exists(ok_path):

        ok = Image.open(ok_path)
        ok.thumbnail((700, 300))

        img.paste(
            ok,
            (W//2 + 50, y+10)
        )

    # ======================
    # SIGNATURE SECTION
    # ======================

    y += 340

    draw.rectangle(
        (margin, y, W-margin, y+70),
        outline="black",
        width=2
    )

    draw.text(
        (margin+15, y+20),
        f"Prepared By : {data['prepared_by']}",
        font=label_font,
        fill="black"
    )


    draw.text(
        (W//2 + 200, y+20),
        "Approved By : Varun K",
        font=label_font,
        fill="black"
    )

    draw.text(
        (W-margin-280, y+20),
        f"Date : {data['date'].split(' ')[0]}",
        font=label_font,
        fill="black"
    )

    # ======================
    # SAVE
    # ======================

    os.makedirs("alerts", exist_ok=True)

    path = f"alerts/{data['nc_no']}.png"

    img.save(path)

    return path

