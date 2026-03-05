# Clean up registration form completely
with open('Templates/register.html', 'r') as f:
    content = f.read()

# Find the form section and replace it with clean version
form_start = content.find('<form method="POST" action="{{ url_for(\'register\') }}">')
form_end = content.find('</form>', form_start) + 7

if form_start != -1 and form_end != -1:
    clean_form = '''                            <form method="POST" action="{{ url_for('register') }}">
                                {{ form.hidden_tag() }}
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-floating">
                                            {{ form.username(class="form-control", placeholder="Username") }}
                                            <label for="username"><i class="fa fa-user me-2"></i>Username</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-floating">
                                            {{ form.email(class="form-control", placeholder="Email Address") }}
                                            <label for="email"><i class="fa fa-envelope me-2"></i>Email Address</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-floating">
                                            {{ form.password(class="form-control", placeholder="Password") }}
                                            <label for="password"><i class="fa fa-lock me-2"></i>Password</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-floating">
                                            {{ form.confirm_password(class="form-control", placeholder="Confirm Password") }}
                                            <label for="confirm_password"><i class="fa fa-lock me-2"></i>Confirm Password</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="form-floating mb-3">
                                    {{ form.role(class="form-control") }}
                                    <label for="role"><i class="fa fa-user-tag me-2"></i>Role</label>
                                </div>

                                <div class="form-check mb-3">
                                    <input class="form-check-input" type="checkbox" id="terms" required>
                                    <label class="form-check-label" for="terms">
                                        I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
                                    </label>
                                </div>

                                <div class="form-check mb-3">
                                    <input class="form-check-input" type="checkbox" id="newsletter">
                                    <label class="form-check-label" for="newsletter">
                                        Send me service reminders and exclusive offers
                                    </label>
                                </div>

                                {{ form.submit(class="btn btn-primary w-100 py-3") }}
                            </form>'''
    
    # Replace the messy form with clean version
    new_content = content[:form_start] + clean_form + content[form_end:]
    
    with open('Templates/register.html', 'w') as f:
        f.write(new_content)
    
    print("Cleaned up registration form!")
else:
    print("Could not find form section to clean up.")
