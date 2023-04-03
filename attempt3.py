import re

name = "Mr. William M Donaldson"

# Define a regular expression pattern for titles
title_pattern = r"^(Mr|Mrs|Ms|Dr|Miss|Prof)(?!\.)"

# Replace the matched title with the title followed by a period and space
formatted_name = re.sub(title_pattern, r"\1. ", name)

print(formatted_name)
