Instruction

1. sudo apt-get update && sudo apt-get upgrade
2. mkdir /ignore
3. nano /ignore/api.py #API="insert_your_token"#
4. docker build -t my-python-app .
docker run -d --name my-python-container my-python-app
