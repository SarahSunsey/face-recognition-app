import datetime

def extract_date_time(filename):
  
  try:
    # Split the filename based on delimiters
    
    parts = filename.split("-")
    
    day=parts[0]
    month=parts[1]
    year=parts[2]
    hour=parts[3]
    minute=parts[4]
    print(day,month,year,hour,minute)
    return day,month,year,hour,minute
  except ValueError:
    return "Invalid filename format"  # Handle format errors

# Example usage
filename = "29-04-2024-14-00-AL24.mp4"

