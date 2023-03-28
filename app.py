import streamlit as st
import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('inspection_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inspection_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 part_id INTEGER, part_type TEXT, visual TEXT, comment TEXT);''') 
    
    c.execute('''CREATE TABLE IF NOT EXISTS parts
                 (part_id INTEGER PRIMARY KEY,
                 pre_filled_info TEXT, dropdown_options TEXT);''')
           
    conn.commit()
    conn.close()


init_db()

def add_part(part_id, pre_filled_info, dropdown_options):
    conn = sqlite3.connect('inspection_data.db')
    c = conn.cursor()
    # Check if part ID already exists
    c.execute("SELECT * FROM parts WHERE part_id=?", (part_id,))
    existing_part = c.fetchone()

    if not existing_part:
        c.execute("INSERT INTO parts (part_id, pre_filled_info, dropdown_options) VALUES (?, ?, ?)",
                  (part_id, pre_filled_info, dropdown_options))
        conn.commit()
        print(f"Part ID {part_id} added successfully.")
    else:
        print(f"Part ID {part_id} already exists. No changes made.")
    conn.commit()
    conn.close()
    
add_part(1000,"Insert MH","good,scratches,burst")
add_part(2000,"Insert FH","good,big,small")
add_part(3000,"Special part", "good,rough,dirty")

def fetch_part_info(part_id):
    conn = sqlite3.connect('inspection_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM parts WHERE part_id=?", (part_id,))
    part_info = c.fetchone()
    conn.close()
    return part_info


st.title("Inspection Registration")

part_id = st.text_input("Part ID", value = '')

#point_a = st.text_input("Point 1")
if part_id != '':
    part_info = fetch_part_info(int(part_id))

    if part_info:
        pre_filled_info = part_info[1]
        dropdown_options = part_info[2].split(',')  # Assuming dropdown options are stored as comma-separated values in the database
        point_a = st.empty().text_input("Part type", value=pre_filled_info)
        point_b = st.empty().selectbox('Visual', options = dropdown_options)

        
    else:
        st.write("Invalid Part ID")
        point_a = None
        point_b = None

    point_c = st.text_input("Comments")
    

    if st.button("Submit"):
        conn = sqlite3.connect('inspection_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO inspection_data (part_id, part_type, visual, comment)
                    VALUES (?, ?, ?, ?);''', (part_id, point_a, point_b, point_c))
        conn.commit()
        conn.close()
        st.success("Inspection data submitted successfully")
        
    def fetch_data():
        conn = sqlite3.connect('inspection_data.db')
        df = pd.read_sql_query("SELECT * FROM inspection_data", conn)
        conn.close()
        return df

    st.title("Inspection Data")

    data = fetch_data()

    if not data.empty:
        st.write(data)
    else:
        st.write("No inspection data available")

