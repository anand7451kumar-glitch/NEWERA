import os
import subprocess
while True:
    command = input("myshell> ")

    if command == "exit":
        break
    if command == "pwd":
        print(os.getcwd())
        continue

    if command == "ls":
        print("\n".join(os.listdir()))
        continue

    subprocess.run(command, shell=True)