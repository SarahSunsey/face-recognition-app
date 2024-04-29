import os
latest_index =0
for filename in os.listdir("images"):
    # Check if the filename is a number
    try:
      number = int(filename.split(".")[0])  # Extract number before extension
      if number > latest_index:
        latest_index = number
    except ValueError:
      pass  # Ignore non-numeric filenames

print( latest_index )