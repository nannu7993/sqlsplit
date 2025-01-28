import os
import streamlit as st
from pathlib import Path

def split_sql_file(file_path, output_dir, chunk_size_mb=50):
    """
    Splits a large SQL file into smaller files of specified size.

    :param file_path: Path to the large SQL file
    :param output_dir: Directory where split files will be saved
    :param chunk_size_mb: Size of each split file in MB
    """
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'rb') as infile:
        part_num = 1
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break

            output_file = os.path.join(output_dir, f"part_{part_num}.sql")
            with open(output_file, 'wb') as outfile:
                outfile.write(chunk)

            part_num += 1

    return output_dir

# Streamlit GUI setup
st.title("SQL File Splitter")
st.write("This app splits large SQL files into smaller files of 50 MB each.")

# File path input
uploaded_path = st.text_input("Enter the path to the SQL file on the server:")
if uploaded_path and Path(uploaded_path).is_file():
    st.success(f"File found: {uploaded_path}")
    
    # Process button
    if st.button("Process"):
        output_dir = Path("split_files")
        split_sql_file(uploaded_path, output_dir, chunk_size_mb=50)

        st.success(f"File split successfully into {len(list(output_dir.iterdir()))} parts.")

        # Display download links
        st.write("Download split files:")
        for split_file in output_dir.iterdir():
            with open(split_file, "rb") as f:
                st.download_button(
                    label=f"Download {split_file.name}",
                    data=f,
                    file_name=split_file.name
                )
else:
    st.warning("Please enter a valid file path.")
