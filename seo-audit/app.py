from flask import Flask, request, render_template_string
import audit  # importujemy nasz skrypt

app = Flask(__name__)

TEMPLATE = """
<form method="POST">
  <input type="text" name="url" placeholder="Podaj URL" style="width:300px;">
  <button type="submit">Analizuj</button>
</form>
{% if report %}
<h2>Raport SEO</h2>
<pre>{{ report }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    if request.method == "POST":
        url = request.form["url"]
        html = audit.fetch_html(url)
        if html:
            data = audit.extract_seo_data(html)
            report = audit.ai_analysis(data, url)
    return render_template_string(TEMPLATE, report=report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
