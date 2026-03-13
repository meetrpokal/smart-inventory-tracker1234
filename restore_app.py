import re
import os
import json

with open('app.py', 'r') as f:
    text = f.read()

# 1. Imports
text = text.replace(
    "from flask import Flask, render_template, request, jsonify, send_file\nimport json",
    "from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for\nfrom werkzeug.security import generate_password_hash, check_password_hash\nfrom functools import wraps\nimport json"
)

# 2. Secret Key
text = text.replace(
    "app = Flask(__name__)\n\n# Setup MongoDB Connection",
    "app = Flask(__name__)\napp.secret_key = 'super_secret_inventory_key_123'\n\n# Setup MongoDB Connection"
)

# 3. Storage Functions
# I will define new load/save functions that support multiuser.
new_storage_code = """# Temporary storage for inventory data (Local Fallback)
INVENTORY_FILE = 'inventory_data.json'
USERS_FILE = 'users.json'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            if request.path.startswith('/api/') or request.path in ['/get_inventory', '/check_expiry', '/export_csv'] or request.path.startswith('/check_low_stock'):
                return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_users():
    if collection is not None:
        try:
            doc = collection.find_one({"_id": "users_list"})
            if doc:
                return doc.get("users", {})
        except Exception as e:
            pass
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        pass
    return {}

def save_users(users_data):
    if collection is not None:
        try:
            collection.update_one({"_id": "users_list"}, {"$set": {"users": users_data}}, upsert=True)
            return
        except Exception as e:
            pass
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f)
    except Exception as e:
        pass

def load_inventory(username):
    if collection is not None:
        try:
            doc = collection.find_one({"_id": f"inventory_{username}"})
            if doc:
                doc.pop('_id', None)
                return doc
        except Exception as e:
            print(f"Error reading from MongoDB: {e}")
            
    try:
        if os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, 'r') as f:
                all_data = json.load(f)
                
                if 'stock' in all_data:
                    old_data = all_data.copy()
                    all_data = {'default_admin': old_data}
                    with open(INVENTORY_FILE, 'w') as fw:
                        json.dump(all_data, fw)
                        
                return all_data.get(username, {"stock": {}, "expiry": []})
    except Exception as e:
        print(f"Error reading local JSON: {e}")
        
    return {"stock": {}, "expiry": []}

def save_inventory(username, data):
    if collection is not None:
        try:
            collection.update_one({"_id": f"inventory_{username}"}, {"$set": data}, upsert=True)
            return
        except Exception as e:
            print(f"Error writing to MongoDB: {e}")
    
    try:
        all_data = {}
        if os.path.exists(INVENTORY_FILE):
            try:
                with open(INVENTORY_FILE, 'r') as f:
                    all_data = json.load(f)
                    if 'stock' in all_data:
                        old_data = all_data.copy()
                        all_data = {'default_admin': old_data}
            except:
                pass
                
        all_data[username] = data
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(all_data, f)
    except Exception as e:
        print(f"Error writing local JSON: {e}")"""

# We need to find the range of original storage functions.
# Currently they are lines 24-46 approx.
# Let's replace the whole section from INVENTORY_FILE to the end of save_inventory.

pattern = re.compile(r"INVENTORY_FILE = 'inventory_data.json'.*?with open\(INVENTORY_FILE, 'w'\) as f:.*?json.dump\(data, f\)", re.DOTALL)
text = pattern.sub(new_storage_code, text)

# 4. Auth Routes
old_index = """@app.route('/')
def index():
    return render_template('index.html')"""

new_index = """@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        users = load_users()
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    users = load_users()
    if username in users:
        return jsonify({'status': 'error', 'message': 'Organization ID already exists'})
        
    users[username] = {
        'password': generate_password_hash(password)
    }
    save_users(users)
    session['username'] = username
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))"""

text = text.replace(old_index, new_index)

# 5. Patching functions with @login_required and username
endpoints = [
    'add_stock', 'remove_stock', 'get_inventory', 'check_expiry', 'export_csv', 'find_path'
]

for ep in endpoints:
    text = text.replace(f"@app.route('/{ep}'", f"@login_required\n@app.route('/{ep}'")
    # Actually wait, the order should be route then login_required
    text = text.replace(f"@login_required\n@app.route('/{ep}'", f"@app.route('/{ep}'\n@login_required")
    
    # Now find the def line and inject username
    text = text.replace(f"def {ep}():", f"def {ep}():\n    username = session['username']")

# Special case for parameterized route
text = text.replace("@app.route('/check_low_stock/<int:threshold>')", "@app.route('/check_low_stock/<int:threshold>')\n@login_required")
text = text.replace("def check_low_stock(threshold):", "def check_low_stock(threshold):\n    username = session['username']")

# Replace data = load_inventory() and save_inventory(data)
text = text.replace("data = load_inventory()", "data = load_inventory(username)")
text = text.replace("save_inventory(data)", "save_inventory(username, data)")

# 6. Apply the 'Expired(quantity)' fix
text = text.replace(
    "status = 'Expired' if item['expiry'] <= today else 'Valid'",
    "status = f\"Expired({item['quantity']})\" if item['expiry'] <= today else 'Valid'"
)

with open('app.py', 'w') as f:
    f.write(text)

print("Patching complete.")
