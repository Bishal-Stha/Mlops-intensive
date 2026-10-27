from flask import Flask, request, render_template_string

app = Flask(__name__)

# Inline HTML template with an input form and greeting display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Greeting App</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
            background-color: #f4f4f9;
        }
        .card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            width: 320px;
        }
        input[type="text"] {
            width: 80%;
            padding: 0.5rem;
            margin: 1rem 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 0.5rem 1.2rem;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1d4ed8;
        }
        .greeting {
            margin-top: 1.5rem;
            font-size: 1.25rem;
            color: #16a34a;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Enter Your Name</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="e.g. Bishal" required autofocus>
            <br>
            <button type="submit">Submit</button>
        </form>

        {% if name %}
            <div class="greeting">Hello, {{ name }}!</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    name = None
    if request.method == "POST":
        name = request.form.get("username", "").strip()
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == "__main__":
    # host="0.0.0.0" ensures it will work both locally and inside Docker
    app.run(host="0.0.0.0", port=5000, debug=True)