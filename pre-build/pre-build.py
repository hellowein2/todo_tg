import os

folder = '/ignore'

file_path = os.path.join(folder, 'data.db')

if not os.path.isfile(folder):
    os.makedirs(folder, exist_ok=True)
