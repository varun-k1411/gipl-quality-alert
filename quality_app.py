import streamlit as st
import pandas as pd
import os
from datetime import datetime
from alert_generator import generate_alert

SUPPLIER = "GABRIL INDUSTRIES PVT. LTD."
DB_FILE = "nc_database.csv"

# Load masters
part_master = pd.read_csv("part_master.csv")
process_sheet = pd.read_csv("process_sheet.csv")
operator_master = pd.read_csv("operator_master.csv")
machine_master = pd.read_csv("machine_master.csv")
shift_master = pd.read_csv("shift_master.csv")
customer_master = pd.read_csv("customer_master.csv")

# Database columns (ADDED Barcode No, Prepared By)
columns = [
    "NC No",
    "Barcode No",
    "Date",
    "Customer",
    "Part No",
    "Description",
    "Size",
    "Grade",
    "Process",
    "Machine",
    "Operator",
    "Shift",
    "Qty",
    "Defect",
    "Prepared By",
    "Defect Image",
    "OK Image",
    "Alert Image"
]

# Ensure DB exists
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=columns).to_csv(DB_FILE, index=False)

db = pd.read_csv(DB_FILE)

# NC number generator (unchanged)
def generate_nc():

    year = datetime.now().year

    if len(db) == 0:
        return f"NC-{year}-0001"

    year_db = db[db["NC No"].str.contains(str(year), na=False)]

    if len(year_db) == 0:
        return f"NC-{year}-0001"

    last = year_db.iloc[-1]["NC No"]

    num = int(last.split("-")[2])

    return f"NC-{year}-{num+1:04d}"


st.title("GIPL Quality Alert System")

# Form
customer = st.selectbox("Customer", customer_master.iloc[:, 0])

part_no = st.selectbox("Part No", part_master["part_no"])

part_row = part_master[part_master["part_no"] == part_no].iloc[0]

description = part_row["part_description"]
if pd.isna(description):
    description = "—"
else:
    description = str(description)

size = str(part_row["size"])
grade = str(part_row["grade"])

st.write(f"Description: {description}")
st.write(f"Size: {size}")
st.write(f"Grade: {grade}")

process_list = process_sheet[
    process_sheet["part_no"] == part_no
]["process_name"]

process = st.selectbox("Process Stage", process_list)

machine = st.selectbox("Machine No", machine_master.iloc[:, 0])

operator = st.selectbox("Operator", operator_master.iloc[:, 0])

shift = st.selectbox("Shift", shift_master.iloc[:, 0])

qty = st.number_input("Quantity", min_value=1)

# NEW FIELD: BARCODE ENTRY
barcode_no = st.text_input(
    "Barcode No (Manual Entry)",
    placeholder="Enter Barcode"
)

# NEW FIELD: PREPARED BY
prepared_by = st.selectbox(
    "Prepared By (Inspector)",
    operator_master.iloc[:, 0],
    key="prepared_by"
)

defect = st.text_input("Defect Description")

defect_uploaded = st.file_uploader("Upload NOT OK Image")

ok_uploaded = st.file_uploader("Upload OK Image (Optional)")


if st.button("Generate Quality Alert"):

    if defect_uploaded is None:
        st.error("Upload NOT OK image")
        st.stop()

    if barcode_no.strip() == "":
        st.error("Enter Barcode No")
        st.stop()

    nc_no = generate_nc()

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    os.makedirs("defect_images", exist_ok=True)
    os.makedirs("ok_images", exist_ok=True)

    defect_path = f"defect_images/{nc_no}.jpg"

    with open(defect_path, "wb") as f:
        f.write(defect_uploaded.getbuffer())

    ok_path = None

    if ok_uploaded is not None:

        ok_path = f"ok_images/{nc_no}.jpg"

        with open(ok_path, "wb") as f:
            f.write(ok_uploaded.getbuffer())

    # UPDATED DATA DICTIONARY (Barcode added)
    data = {

        "nc_no": nc_no,
        "barcode_no": barcode_no,
        "date": date,
        "customer": customer,
        "part_no": part_no,
        "description": description,
        "size": size,
        "grade": grade,
        "process": process,
        "machine": machine,
        "operator": operator,
        "shift": shift,
        "qty": qty,
        "defect": defect,
        "prepared_by": prepared_by

    }

    alert_path = generate_alert(data, defect_path, ok_path)

    new_row = {

        "NC No": nc_no,
        "Barcode No": barcode_no,
        "Date": date,
        "Customer": customer,
        "Part No": part_no,
        "Description": description,
        "Size": size,
        "Grade": grade,
        "Process": process,
        "Machine": machine,
        "Operator": operator,
        "Shift": shift,
        "Qty": qty,
        "Defect": defect,
        "Prepared By": prepared_by,
        "Defect Image": defect_path,
        "OK Image": ok_path,
        "Alert Image": alert_path

    }

    db2 = pd.concat([db, pd.DataFrame([new_row])], ignore_index=True)

    db2.to_csv(DB_FILE, index=False)

    st.success(f"Quality Alert Generated: {nc_no}")

    st.image(alert_path)

    with open(alert_path, "rb") as f:

        st.download_button(
            "Download Alert",
            f,
            file_name=f"{nc_no}.png"

        )
