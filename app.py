import streamlit as st
import os

# Function to split the SQL file into smaller chunks
def split_sql_file(file_path, chunk_size=50 * 1024 * 1024):  # 50 MB in bytes
    try:
        with open(file_path, 'rb') as f:
            part_num = 1
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                part_file = f"{file_path}_part_{part_num}.sql"
                with open(part_file, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                st.success(f"Created: {part_file}")
                part_num += 1
        st.success("File splitting completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app
def main():
    st.title("SQL File Splitter")
    st.write("Upload a large SQL file, and it will be split into 50 MB chunks.")

    # File uploader
    uploaded_file = st.file_uploader("Upload your SQL file", type=["sql"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        file_path = os.path.join("/tmp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Button to process the file
        if st.button("Process File"):
            st.write("Splitting the file into 50 MB chunks...")
            split_sql_file(file_path)

            # Clean up the temporary file
            os.remove(file_path)
            st.write("Temporary file removed.")

# Run the app
if __name__ == "__main__":
    main()
