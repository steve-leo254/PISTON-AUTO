# Fix login.html syntax error
with open('Templates/login.html', 'r') as f:
    content = f.read()

# Fix the extra closing brace
content = content.replace('{{ url_for(\'login\') }}}', '{{ url_for(\'login\') }}')

with open('Templates/login.html', 'w') as f:
    f.write(content)

print("Fixed login.html syntax error!")
