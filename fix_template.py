
import os

file_path = 'web/templates/web/cars_in_stock.html'

with open(file_path, 'r') as f:
    content = f.read()

# Replace the specific multi-line string with single line
# Adjusting for potential whitespace variations
import re
new_content = re.sub(r'intcomma\s*\n\s*}}', 'intcomma }}', content)

with open(file_path, 'w') as f:
    f.write(new_content)

print("File fixed.")
