def split_file(file_name, chunk_size=100 * 1024 * 1024):
    """Splits a large file into smaller chunks."""
    with open(file_name, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            with open(f'{file_name}_part_{chunk_number}', 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_number += 1

split_file('claim_prediction_model.pkl')
