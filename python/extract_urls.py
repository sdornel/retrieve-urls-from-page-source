from flask import Flask, request, render_template_string
import re
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Page URL Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; }
        input[type="text"] { width: 100%; padding: 0.5em; margin-bottom: 1em; }
        .url-list { margin-top: 1em; }
    </style>
</head>
<body>
    <h1>🔗 Web Page URL Extractor</h1>
    <p>Enter a website URL to extract all links from the page source.</p>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter Website URL" value="{{ url or '' }}" required>
        <button type="submit">Extract URLs</button>
    </form>
    {% if urls is not none %}
        {% if urls %}
            <div class="url-list">
                <h3>✅ Found {{ urls|length }} URLs:</h3>
                <ul>
                    {% for link in urls %}
                        <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
                    {% endfor %}
                </ul>
            </div>
        {% else %}
            <p><strong>⚠️ No URLs found.</strong></p>
        {% endif %}
    {% elif error %}
        <p><strong>⚠️ {{ error }}</strong></p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    url = None
    urls = None
    error = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if url.startswith("www"):
            url = "https://" + url
        elif not url.startswith("http"):
            url = "https://www." + url

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            urls = sorted(set(re.findall(r'https?://[^\s"\'<>]+', response.text)))
        except requests.exceptions.RequestException as e:
            error = f"Error fetching URL. Details: {e}"

    return render_template_string(HTML_TEMPLATE, url=url, urls=urls, error=error)

if __name__ == "__main__":
    app.run(debug=False)
