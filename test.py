try:
    with open('output.json', 'w') as f:
        f.write('{"key": "value"}')
    print("File created successfully")
    input()
except PermissionError:
    print("Permission denied")
    input()
except Exception as e:
    print(f"An error occurred: {e}")
    input()