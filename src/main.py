import os

def keep_first_20_pdfs(data_path='data'):
    for role in os.listdir(data_path):
        role_path = os.path.join(data_path, role)
        if not os.path.isdir(role_path):
            continue

        # Get list of all .pdf files and sort lexicographically
        pdf_files = [f for f in os.listdir(role_path) if f.lower().endswith('.pdf')]
        pdf_files.sort()  # Lexicographic sort

        # Keep only the first 20
        to_delete = pdf_files[20:]

        for file in to_delete:
            file_path = os.path.join(role_path, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

if __name__ == '__main__':
    keep_first_20_pdfs()
