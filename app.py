import os
import re
from flask import Flask, request, render_template_string
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#000000">
<title>نظام السعرات الحرارية الذكي</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
--primary-color: #10B981;
--primary-hover: #059669;
--bg-color: #000000;
--card-bg: rgba(17, 24, 39, 0.92);
--text-color: #F9FAFB;
--border-color: #374151;
--cement-color: #6B7280;
}

* {
box-sizing: border-box;
margin: 0;
padding: 0;
font-family: 'Cairo', sans-serif;
}

body {
background-color: var(--bg-color);
color: var(--text-color);
display: flex;
justify-content: center;
padding: 20px 12px;
min-height: 100vh;
background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=1000&auto=format&fit=crop');
background-size: cover;
background-position: center;
background-attachment: fixed;
}

.container {
width: 100%;
max-width: 500px;
background: var(--card-bg);
border-radius: 20px;
padding: 24px;
box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
height: fit-content;
position: relative;
border: 1px solid var(--border-color);
backdrop-filter: blur(8px);
}

.header {
text-align: center;
margin-bottom: 20px;
}

.header h2 {
font-size: 1.4rem;
color: #FFFFFF;
font-weight: 700;
}

.header p {
font-size: 0.85rem;
color: #9CA3AF;
margin-top: 4px;
}

#install-btn {
display: none;
width: 100%;
background-color: #3B82F6;
color: white;
border: none;
padding: 10px;
border-radius: 12px;
font-size: 0.9rem;
font-weight: 700;
cursor: pointer;
margin-bottom: 16px;
box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.tracker-card {
background: rgba(31, 41, 55, 0.8);
border: 1px solid var(--border-color);
border-radius: 14px;
padding: 14px;
margin-bottom: 16px;
text-align: center;
}

.tracker-grid {
display: flex;
justify-content: space-around;
margin-top: 8px;
}

.tracker-item span {
display: block;
font-size: 0.75rem;
color: #9CA3AF;
font-weight: 600;
}

.tracker-item strong {
font-size: 1.1rem;
color: #34D399;
}

.target-input-row {
display: flex;
gap: 8px;
margin-bottom: 12px;
align-items: center;
}

.target-input-row label {
font-size: 0.8rem;
font-weight: 600;
color: #D1D5DB;
white-space: nowrap;
}

.target-input-row input {
flex: 1;
padding: 6px 10px;
background: #1F2937;
border: 1px solid var(--border-color);
color: #FFFFFF;
border-radius: 8px;
font-size: 0.85rem;
outline: none;
}

.tabs {
display: flex;
gap: 4px;
margin-bottom: 20px;
background: var(--cement-color);
padding: 4px;
border-radius: 12px;
}

.tab {
flex: 1;
padding: 8px;
text-align: center;
background: var(--cement-color);
border: none;
border-radius: 8px;
font-size: 0.8rem;
font-weight: 600;
color: #FFFFFF;
cursor: pointer;
transition: 0.2s;
}

.tab.active {
background: #374151;
color: #FFFFFF;
box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.upload-box {
border: 2px dashed var(--border-color);
border-radius: 14px;
padding: 20px;
text-align: center;
background: rgba(17, 24, 39, 0.5);
cursor: pointer;
margin-bottom: 16px;
}

.upload-box span {
font-size: 0.85rem;
color: #9CA3AF;
display: block;
margin-top: 8px;
}

.action-btn {
width: 100%;
background-color: var(--primary-color);
color: white;
border: none;
padding: 12px;
border-radius: 12px;
font-size: 0.95rem;
font-weight: 700;
cursor: pointer;
transition: background 0.2s;
box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.action-btn:hover {
background-color: var(--primary-hover);
}

.result-section {
margin-top: 20px;
background: rgba(31, 41, 55, 0.8);
border: 1px solid var(--border-color);
padding: 16px;
border-radius: 14px;
font-size: 0.9rem;
line-height: 1.6;
color: #E5E7EB;
}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h2>نظام السعرات الذكي 🥗</h2>
<p>حلل وجبتك واخصم سعراتها من رصيدك اليومي تلقائياً</p>
</div>

<div class="tabs">
<button class="tab active">تحليل الوجبة 📷</button>
<button class="tab">تحليل الجسم 🚶‍♂️</button>
<button class="tab">حاسبة الاحتياج 📊</button>
</div>

<div class="tracker-card">
<div class="target-input-row">
<label>الهدف اليومي:</label>
<input type="number" id="target-calories" value="2779">
</div>
<div class="tracker-grid">
<div class="tracker-item">
<span>المستهلك</span>
<strong>0</strong>
</div>
<div class="tracker-item">
<span>المتبقي</span>
<strong>2779</strong>
</div>
</div>
</div>

<div class="upload-box">
<span>📁 رفع من الجهاز أو 📷 تصوير بالكاميرا</span>
</div>

<button class="action-btn">تحليل الوجبة وخصم السعرات</button>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

