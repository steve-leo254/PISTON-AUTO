# Fix registration form
with open('Templates/register.html', 'r') as f:
    content = f.read()

# Fix the form tag to use Flask-WTF
content = content.replace(
    '<form id="registerForm">',
    '<form method="POST" action="{{ url_for(\'register\') }}">\n                                {{ form.hidden_tag() }}'
)

# Replace plain HTML inputs with Flask-WTF fields
content = content.replace(
    '<input type="text" class="form-control" id="firstName" placeholder="First Name" required>',
    '{{ form.username(class="form-control", placeholder="Username") }}'
)

content = content.replace(
    '<label for="firstName"><i class="fa fa-user me-2"></i>First Name</label>',
    '<label for="username"><i class="fa fa-user me-2"></i>Username</label>'
)

content = content.replace(
    '<input type="email" class="form-control" id="email" placeholder="Email Address" required>',
    '{{ form.email(class="form-control", placeholder="Email Address") }}'
)

content = content.replace(
    '<input type="password" class="form-control" id="password" placeholder="Password" required>',
    '{{ form.password(class="form-control", placeholder="Password") }}'
)

content = content.replace(
    '<input type="password" class="form-control" id="confirmPassword" placeholder="Confirm Password" required>',
    '{{ form.confirm_password(class="form-control", placeholder="Confirm Password") }}'
)

content = content.replace(
    '<button type="submit" class="btn btn-primary w-100 py-3">Register</button>',
    '{{ form.submit(class="btn btn-primary w-100 py-3") }}'
)

with open('Templates/register.html', 'w') as f:
    f.write(content)

print("Fixed registration form to use Flask-WTF!")
