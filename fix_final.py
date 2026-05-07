with open('template/about_tax.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all HTML entities
content = content.replace('&quot;{% static &quot;images/tax_image.png&quot; %}&quot;', "{% static 'images/tax_image.png' %}")
content = content.replace('&quot;Khmer Moul&quot;', "'Khmer Moul'")

with open('template/about_tax.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed all HTML entities')