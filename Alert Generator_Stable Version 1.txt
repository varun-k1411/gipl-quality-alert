from PIL import Image, ImageDraw, ImageFont
import os

COMPANY = "GABRIL INDUSTRIES PVT. LTD."
DOCUMENT_NO = "GIPL-QA-001"
REVISION_NO = "00"

FONT_PATH = "arial.ttf"

title_font = ImageFont.truetype(FONT_PATH, 48)
header_font = ImageFont.truetype(FONT_PATH, 28)
text_font = ImageFont.truetype(FONT_PATH, 24)


def generate_alert(data, defect_path, ok_path=None):

    W, H = 1600, 1100

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # ======================
    # HEADER
    # ======================

    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").resize((200, 70))
        img.paste(logo, (50, 30))

    draw.text((300, 30), COMPANY, font=header_font, fill="black")

    draw.text((550, 80), "QUALITY ALERT", font=title_font, fill="black")

    # ======================
    # DOCUMENT CONTROL BOX
    # ======================

    draw.rectangle((50, 160, 1550, 230), outline="black", width=2)

    draw.text((70, 170),
              f"Document No : {DOCUMENT_NO}",
              font=text_font, fill="black")

    draw.text((70, 200),
              f"Revision No : {REVISION_NO}",
              font=text_font, fill="black")

    draw.text((600, 170),
              f"Issue Date : {data['date']}",
              font=text_font, fill="black")

    draw.text((1000, 170),
              f"NC No : {data['nc_no']}",
              font=text_font, fill="black")

    draw.text((1000, 200),
              f"Barcode No : {data['barcode_no']}",
              font=text_font, fill="black")

    # ======================
    # TRACEABILITY BOX
    # ======================

    draw.rectangle((50, 260, 1550, 600), outline="black", width=2)

    left_x = 70
    right_x = 820

    y = 280
    spacing = 35

    left_fields = [

        ("Customer", data["customer"]),
        ("Supplier", COMPANY),
        ("Part No", data["part_no"]),
        ("Description", data["description"]),
        ("Size", data["size"]),
        ("Grade", data["grade"])

    ]

    right_fields = [

        ("Process Stage", data["process"]),
        ("Machine No", data["machine"]),
        ("Operator", data["operator"]),
        ("Shift", data["shift"]),
        ("Defect", data["defect"]),
        ("Qty", str(data["qty"]))

    ]

    max_rows = max(len(left_fields), len(right_fields))

    for i in range(max_rows):

        if i < len(left_fields):

            draw.text(
                (left_x, y),
                f"{left_fields[i][0]:15} : {left_fields[i][1]}",
                font=text_font,
                fill="black"
            )

        if i < len(right_fields):

            draw.text(
                (right_x, y),
                f"{right_fields[i][0]:15} : {right_fields[i][1]}",
                font=text_font,
                fill="black"
            )

        y += spacing

    # ======================
    # IMAGE HEADERS
    # ======================

    draw.rectangle((50, 620, 775, 670), fill="red")

    draw.text((330, 630),
              "NOT OK",
              font=header_font,
              fill="white")

    draw.rectangle((825, 620, 1550, 670), fill="green")

    draw.text((1120, 630),
              "OK",
              font=header_font,
              fill="white")

    # ======================
    # IMAGE BOXES
    # ======================

    draw.rectangle((50, 680, 775, 1020), outline="black", width=2)

    draw.rectangle((825, 680, 1550, 1020), outline="black", width=2)

    if defect_path and os.path.exists(defect_path):

        defect_img = Image.open(defect_path)

        defect_img.thumbnail((700, 320))

        img.paste(defect_img, (70, 700))

    if ok_path and os.path.exists(ok_path):

        ok_img = Image.open(ok_path)

        ok_img.thumbnail((700, 320))

        img.paste(ok_img, (845, 700))

    # ======================
    # SIGNATURE SECTION
    # ======================

    draw.rectangle((50, 1040, 1550, 1090), outline="black", width=2)

    draw.text((70, 1050),
              f"Prepared By : {data['prepared_by']}",
              font=text_font,
              fill="black")

    draw.text((500, 1050),
              "Verified By : ____________________",
              font=text_font,
              fill="black")

    draw.text((900, 1050),
              "Approved By : Varun K",
              font=text_font,
              fill="black")

    draw.text((1200, 1050),
              f"Date : {data['date'].split(' ')[0]}",
              font=text_font,
              fill="black")

    # ======================
    # SAVE
    # ======================

    os.makedirs("alerts", exist_ok=True)

    alert_path = f"alerts/{data['nc_no']}.png"

    img.save(alert_path)

    return alert_path