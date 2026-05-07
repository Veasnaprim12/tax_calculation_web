import os
print('File modification time:', os.path.getmtime('template/about_tax.html'))

with open('template/about_tax.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('Contains HTML entities:', '&quot;' in content)
print('Contains proper quotes:', "'Khmer Moul'" in content)

# Show the first 200 characters
print('First 200 chars:')
print(repr(content[:200]))