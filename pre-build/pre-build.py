import os

folder = '/ignore'

if not os.path.isfile(folder):
    os.makedirs(folder, exist_ok=True)
