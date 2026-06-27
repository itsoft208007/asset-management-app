import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Asset Management", layout="wide")

# Simple Login
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "user": {
        "password": "user123",
        "role": "user"
    }
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Asset Management Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if (
            username in USERS and
            USERS[username]["password"] == password
        ):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]

            st.rerun()

    

        else:
            st.error("Invalid Username or Password")
    
    st.stop()

if os.path.exists("Images.png"):
    st.sidebar.image("Images.png", use_container_width=True)

if "username" in st.session_state:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# ==========================
# SIDEBAR MENU
# ==========================
with st.sidebar.expander("⚙️ Assets", expanded=True):

    if st.session_state.get("role") == "admin":

        menu = st.radio(
            "",
            [
                "📋 List of Assets",
                "➕ Add New Asset",
                "📤 Import Data",
                "📥 Export Data"
            ]
        )

    else:

        menu = st.radio(
            "",
            [
                "📋 List of Assets",
                "📥 Export Data"
            ]
        )

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.title("💻 Asset Management App")

columns = [
    "FA_No",
    "Description",
    "Serial_No_",
    "Responsible_Employee",
    "Employee_Code",
    "Asset_Type",
    "Fa_Type",
    "Fa_Status",
    "Status",
    "Keyboard",
    "Mouse",
    "Headphone",
    "Laptop_Stand",
    "Vendor",
    "Invoice_No_"
]

# File name for permanent storage
FILE_NAME = "asset_data.xlsx"

# ==========================
# IMPORT DATA
# ==========================
if menu == "📤 Import Data":

    st.subheader("📤 Import Data")

    uploaded_file = st.file_uploader(
        "Upload Excel or CSV File",
        type=["xlsx", "csv"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):
            import_df = pd.read_csv(uploaded_file)

        else:
            import_df = pd.read_excel(uploaded_file)

        # Remove extra spaces from column names
        import_df.columns = import_df.columns.str.strip()

        # Check missing columns
        missing_cols = set(columns) - set(import_df.columns)

        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
            st.stop()

        st.session_state.df = pd.concat(
            [st.session_state.df, import_df],
            ignore_index=True
        )

        st.session_state.df.to_excel(
            FILE_NAME,
            index=False
        )

        st.success(
            f"✅ {len(import_df)} records imported successfully"
        )

# Load existing data if file exists
if "df" not in st.session_state:

    try:
        if os.path.exists(FILE_NAME):

            st.session_state.df = pd.read_excel(FILE_NAME)

        else:

            st.warning("Excel file not found. New file will be created.")

            st.session_state.df = pd.DataFrame(columns=columns)

    except Exception as e:

        st.error(f"Error loading file: {e}")

        st.session_state.df = pd.DataFrame(columns=columns)

# ==========================
# ADD NEW ASSET
# ==========================
if menu == "➕ Add New Asset":

    st.subheader("➕ Add New Asset")

    with st.form("add_asset_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            fa_no = st.text_input("FA No")
            description = st.text_input("Description")
            serial_no = st.text_input("Serial No")
            employee = st.text_input("Responsible Employee")

        with col2:
            emp_code = st.text_input("Employee Code")
            
            asset_type = st.selectbox(
                "Asset Type",
                [
                    "Camera",
                    "Desktop",
                    "Firewalls (UTM)",
                    "Routers & Switches",
                    "IP PBX & IP Desk Phones",
                    "Laptop",
                    "Mac Book",
                    "Printer",
                    "Servers & Storage",
                    "Software",
                    "TVs and Monitors",
                    "Video Conferencing Devices",
                    "Workstation"
                ]
            )
            fa_type = st.selectbox(
                "FA Type",
                [
                    "Inuse",
                    "Not in use"
                ]
            )
            fa_status = st.selectbox(
                "FA Status",
                [
                    "Corporate Office",
                    "Shyam Nagar",
                    "Delhi Office",
                    "Gurugram Office",
                    "ROOMA",
                    "Aadhunik Sarh",
                    "Magnus Malwan",
                    "Malwan",
                    "MRO",
                    "ARP Sarh"
                ]
            )
            
            keyboard = st.selectbox("Keyboard", ["Yes", "No"])
            
            status = st.selectbox(
                "Asset Status",
                [
                    "Available",
                    "Checked Out",
                    "Scrap"
                ]
            )

        with col3:
            mouse = st.selectbox("Mouse", ["Yes", "No"])
            headphone = st.selectbox("Headphone", ["Yes", "No"])
            laptop_stand = st.selectbox("Laptop Stand", ["Yes", "No"])
            vendor = st.text_input("Vendor")
            invoice_no = st.text_input("Invoice No")

        submit = st.form_submit_button("➕ Add Asset")

        if submit:

            new_row = {
                "FA_No": fa_no,
                "Description": description,
                "Serial_No_": serial_no,
                "Responsible_Employee": employee,
                "Employee_Code": emp_code,
                "Asset_Type": asset_type,
                "Fa_Type": fa_type,
                "Fa_Status": fa_status,
                "Status": status,
                "Keyboard": keyboard,
                "Mouse": mouse,
                "Headphone": headphone,
                "Laptop_Stand": laptop_stand,
                "Vendor": vendor,
                "Invoice_No_": invoice_no
            }

            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True
            )

            st.session_state.df.to_excel(FILE_NAME, index=False)

            st.success("✅ Asset Added Successfully")

if menu == "📋 List of Assets" and not st.session_state.edit_mode:

    required_cols = [
        "FA_No",
        "Fa_Type",
        "Asset_Type",
        "Fa_Status"
    ]

    missing = [
        col for col in required_cols
        if col not in st.session_state.df.columns
    ]

    if missing:
        st.error(f"Missing columns in Excel: {missing}")
        st.write(st.session_state.df.columns.tolist())
        st.stop()

    # ==========================
    # DASHBOARD CARDS
    # ==========================

    total_assets = len(st.session_state.df)

    in_use = len(
        st.session_state.df[
            st.session_state.df["Fa_Type"] == "Inuse"
        ]
    )

    not_in_use = len(
        st.session_state.df[
            st.session_state.df["Fa_Type"] == "Not in use"
        ]
    )

    laptops = len(
        st.session_state.df[
            st.session_state.df["Asset_Type"] == "Laptop"
        ]
    )

    desktops = len(
        st.session_state.df[
            st.session_state.df["Asset_Type"] == "Desktop"
        ]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("💻 Total Assets", total_assets)
    col2.metric("✅ In Use", in_use)
    col3.metric("❌ Not In Use", not_in_use)
    col4.metric("🖥️ Laptops", laptops)
    col5.metric("🖥️ Desktops", desktops)

    st.divider()

    df_show = st.session_state.df.copy()

    if "Sno_" in df_show.columns:
        df_show = df_show.drop(columns=["Sno_"])

    st.subheader("🔍 Search Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        fa_no_search = st.text_input("FA No")
        employee_search = st.text_input("Responsible Employee")

    with col2:
        serial_search = st.text_input("Serial No")

        status_search = st.selectbox(
            "Location (FA Status)",
            ["All"] + sorted(
                df_show["Fa_Status"]
                 .dropna()
                 .unique()
                 .tolist()
            )
        )

    with col3:
        fa_type_search = st.selectbox(
            "FA Type",
            ["All", "Inuse", "Not in use"]
        )

    # Apply Filters

    if fa_no_search:
        df_show = df_show[
            df_show["FA_No"].astype(str).str.contains(
            fa_no_search,
            case=False,
            na=False
        )
    ]

    if employee_search:
        df_show = df_show[
            df_show["Responsible_Employee"]
            .astype(str)
            .str.contains(
                employee_search,
                case=False,
                na=False
            )
        ]

    if serial_search:
        df_show = df_show[
            df_show["Serial_No_"].astype(str).str.contains(
                serial_search,
                case=False,
                na=False
            )
        ]
    
    # YEH NAYA CODE ADD KARO
    if status_search != "All":
        df_show = df_show[
            df_show["Fa_Status"] == status_search
        ]

    if fa_type_search != "All":
        df_show = df_show[
            df_show["Fa_Type"] == fa_type_search
        ]

    # Add Delete Column if not exists
    if "Delete" not in df_show.columns:
        df_show["Delete"] = False

    edited_df = st.data_editor(
        df_show,
        use_container_width=True,
        hide_index=True
    )

    fa_list = df_show["FA_No"].dropna().astype(str).tolist()

    selected_fa = st.selectbox(
        "✏️ Select Asset To Edit",
        fa_list
    )

    if st.button("✏️ Edit Selected Asset"):
        st.session_state.selected_fa = selected_fa
        st.session_state.edit_mode = True
        st.rerun()

    if st.button("💾 Save Changes"):

        final_df = edited_df.drop(
            columns=["Delete"],
            errors="ignore"
        )

        # Jo filtered dataframe dikh raha hai usko main dataframe me merge karo
        for i, idx in enumerate(df_show.index):
            st.session_state.df.loc[idx] = final_df.iloc[i]

        st.session_state.df.to_excel(
            FILE_NAME,
            index=False
        )

        st.success("✅ Changes Saved Successfully")

        st.rerun()

        st.session_state.edit_mode = False

        st.rerun()

    # Delete selected rows
    if st.session_state.role == "admin":
    
        # Delete button
        if st.button("🗑 Delete Selected Rows"):
            st.session_state.show_delete_confirm = True

        # Confirmation box
        if st.session_state.get("show_delete_confirm", False):

            st.warning("⚠️ Are you sure you want to delete selected rows?")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Yes, Delete"):

                    st.session_state.df = edited_df[
                        edited_df["Delete"] == False
                    ].drop(columns=["Delete"])

                    st.session_state.df.to_excel(
                        FILE_NAME,
                        index=False
                    )

                    st.session_state.show_delete_confirm = False

                    st.success("✅ Selected rows deleted successfully")
                    st.rerun()

            with col2:
                if st.button("❌ Cancel"):

                    st.session_state.show_delete_confirm = False
                    st.rerun()

# ==========================
# EDIT PAGE
# ==========================

if st.session_state.edit_mode:

    st.subheader("✏️ Edit Asset")

    filtered_row = st.session_state.df[
        st.session_state.df["FA_No"] ==
        st.session_state.get("selected_fa", "")
    ]

    if filtered_row.empty:
        st.error("❌ Selected Asset Not Found")

        if st.button("⬅️ Back To Asset List"):
            st.session_state.edit_mode = False
            st.rerun()

        st.stop()

    row = filtered_row.iloc[0]

    description = st.text_input(
        "Description",
        row["Description"]
    )

    serial_no = st.text_input(
        "Serial No",
        row["Serial_No_"]
    )

    status = st.selectbox(
        "Status",
        ["Available", "Checked Out", "Scrap"],
        index=[
            "Available",
            "Checked Out",
            "Scrap"
        ].index(
            row["Status"]
            if pd.notna(row["Status"])
            else "Available"
        )
    )

    if st.button("💾 Update Asset"):

        idx = st.session_state.df[
            st.session_state.df["FA_No"] ==
            st.session_state.selected_fa
        ].index[0]

        st.session_state.df.at[idx, "Description"] = description
        st.session_state.df.at[idx, "Serial_No_"] = serial_no
        st.session_state.df.at[idx, "Status"] = status

        st.session_state.df.to_excel(
            FILE_NAME,
            index=False
        )

        st.success("✅ Asset Updated Successfully")

    if st.button("⬅️ Back To Asset List"):
        st.session_state.edit_mode = False
        st.rerun()

# ==========================
# EXPORT DATA
# ==========================
if menu == "📥 Export Data":

    st.subheader("📥 Export Data")

    csv = st.session_state.df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="asset_data.csv",
        mime="text/csv"
    )

    excel_file = "export_asset_data.xlsx"

    st.session_state.df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="📥 Download Excel",
            data=f,
            file_name="asset_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )