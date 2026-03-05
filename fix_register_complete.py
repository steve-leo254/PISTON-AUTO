# Complete registration form fix
with open('Templates/register.html', 'r') as f:
    content = f.read()

# Fix remaining plain HTML inputs
content = content.replace(
    '<input type="text" class="form-control" id="lastName" placeholder="Last Name" required>',
    '{{ form.role(class="form-control") }}'
)

content = content.replace(
    '<label for="lastName"><i class="fa fa-user me-2"></i>Last Name</label>',
    '<label for="role"><i class="fa fa-user-tag me-2"></i>Role</label>'
)

content = content.replace(
    '<input type="tel" class="form-control" id="phone" placeholder="Phone Number" required>',
    '{{ form.confirm_password(class="form-control", placeholder="Confirm Password") }}'
)

content = content.replace(
    '<label for="phone"><i class="fa fa-phone me-2"></i>Phone Number</label>',
    '<label for="confirm_password"><i class="fa fa-lock me-2"></i>Confirm Password</label>'
)

# Add password field after email
content = content.replace(
    '                                </div>\n\n                                <div class="form-floating">',
    '                                </div>\n\n                                <div class="form-floating">\n                                    {{ form.password(class="form-control", placeholder="Password") }}\n                                    <label for="password"><i class="fa fa-lock me-2"></i>Password</label>\n                                </div>\n\n                                <div class="form-floating">'
)

with open('Templates/register.html', 'w') as f:
    f.write(content)

print("Completed registration form fix!")
