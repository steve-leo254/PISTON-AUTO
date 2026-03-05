from dbservice import create_app, db, User, UserRole

app = create_app()

with app.app_context():
    print("=== ALL USERS IN DATABASE ===")
    users = User.query.all()
    
    if not users:
        print("❌ No users found in database!")
    else:
        for user in users:
            print(f"👤 Username: {user.username}")
            print(f"📧 Email: {user.email}")
            print(f"🏷️ Role: {user.role.value}")
            print(f"🆔 ID: {user.id}")
            print("-" * 40)
    
    print(f"\n📊 Total Users: {len(users)}")
    
    # Check specifically for admin
    admin_users = User.query.filter_by(role=UserRole.ADMIN).all()
    print(f"👑 Admin Users: {len(admin_users)}")
    
    if admin_users:
        for admin in admin_users:
            print(f"   📧 Admin Email: {admin.email}")
            print(f"   👤 Admin Username: {admin.username}")
