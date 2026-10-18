import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# استدعاء مفتاح OpenRouter من متغيرات البيئة بأمان تام
OPENROUTER_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#10B981">
<title>نظام السعرات الحرارية الذكي</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
--primary-color: #10B981;
--primary-hover: #059669;
--bg-color: #F3F4F6;
--card-bg: #FFFFFF;
--text-color: #1F2937;
--border-color: #E5E7EB;
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
}

.container {
width: 100%;
max-width: 500px;
background: var(--card-bg);
border-radius: 20px;
padding: 24px;
box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
height: fit-content;
position: relative;
}

.header {
text-align: center;
margin-bottom: 20px;
}

.header h2 {
font-size: 1.4rem;
color: #111827;
font-weight: 700;
}

.header p {
font-size: 0.85rem;
color: #6B7280;
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
background: #ECFDF5;
border: 1px solid #A7F3D0;
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
color: #047857;
font-weight: 600;
}

.tracker-item strong {
font-size: 1.1rem;
color: #065F46;
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
color: #374151;
white-space: nowrap;
}

.target-input-row input {
flex: 1;
padding: 6px 10px;
border: 1px solid #D1D5DB;
border-radius: 8px;
font-size: 0.85rem;
outline: none;
}

.tabs {
display: flex;
gap: 6px;
margin-bottom: 20px;
background: #E5E7EB;
padding: 4px;
border-radius: 12px;
}

.tab-btn {
flex: 1;
padding: 10px;
text-align: center;
background: transparent;
border: none;
border-radius: 8px;
font-weight: 600;
cursor: pointer;
font-size: 0.85rem;
color: #4B5563;
transition: all 0.2s;
}

.tab-btn.active {
background: white;
color: var(--primary-color);
box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.tab-content {
display: none;
}

.tab-content.active {
display: block;
}

.form-group {
margin-bottom: 12px;
}

.form-group label {
display: block;
margin-bottom: 4px;
font-size: 0.85rem;
font-weight: 600;
color: #374151;
}

.form-control {
width: 100%;
padding: 10px 12px;
border: 1px solid #D1D5DB;
border-radius: 10px;
font-size: 0.9rem;
outline: none;
background: #FAFAFA;
}

.form-control:focus {
border-color: var(--primary-color);
background: #FFFFFF;
}

.action-buttons {
display: flex;
gap: 12px;
margin-bottom: 12px;
}

.upload-card {
flex: 1;
border: 2px dashed #D1D5DB;
border-radius: 14px;
padding: 14px 8px;
text-align: center;
background: #FAFAFA;
cursor: pointer;
position: relative;
}

.upload-card:hover {
border-color: var(--primary-color);
background: #ECFDF5;
}

.upload-icon {
font-size: 26px;
margin-bottom: 4px;
display: block;
}

.upload-card span:not(.upload-icon) {
font-size: 0.8rem;
color: #4B5563;
font-weight: 600;
}

.file-input {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
opacity: 0;
cursor: pointer;
z-index: 10;
}

.file-name {
margin-top: 8px;
font-size: 0.8rem;
color: var(--primary-color);
font-weight: 600;
word-break: break-all;
text-align: center;
}

.btn-submit {
width: 100%;
background-color: var(--primary-color);
color: white;
border: none;
padding: 12px;
border-radius: 12px;
font-size: 0.95rem;
font-weight: 700;
cursor: pointer;
margin-top: 6px;
box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.btn-submit:hover {
background-color: var(--primary-hover);
}

.result-box {
margin-top: 20px;
padding-top: 16px;
border-top: 1px solid var(--border-color);
}

.result-box h3 {
font-size: 1.1rem;
margin-bottom: 10px;
color: #111827;
}

.markdown-content {
font-size: 0.9rem;
line-height: 1.6;
color: #374151;
white-space: normal;
word-break: break-word;
overflow-wrap: break-word;
}

.markdown-content h3 {
font-size: 1.05rem;
color: var(--primary-color);
margin-top: 12px;
margin-bottom: 6px;
}

.markdown-content ul {
padding-right: 20px;
margin-bottom: 10px;
}

.markdown-content blockquote {
background: #ECFDF5;
border-right: 4px solid var(--primary-color);
padding: 10px;
border-radius: 8px;
margin-top: 10px;
}
</style>
</head>
<body>

<div class="container">
<button id="install-btn">📲 تثبيت التطبيق على هاتفك</button>

<div class="header">
<h2>نظام السعرات الذكي 🥗</h2>
<p>حلل وجبتك واخصم سعراتها من رصيدك اليومي تلقائياً</p>
</div>

<div class="tabs">
<button type="button" class="tab-btn active" onclick="switchTab('meal')">📸 تحليل الوجبة</button>
<button type="button" class="tab-btn" onclick="switchTab('calculator')">📊 حاسبة الاحتياج</button>
</div>

<div id="meal-tab" class="tab-content active">
<div class="tracker-card">
<div class="target-input-row">
<label>الهدف اليومي:</label>
<input type="number" id="daily-target" value="2000" onchange="updateTrackerStorage()">
<button type="button" onclick="resetDay()" style="background:#EF4444; color:white; border:none; padding:5px 10px; border-radius:6px; font-size:0.75rem; cursor:pointer;">إعادة ضبط</button>
</div>
<div class="tracker-grid">
<div class="tracker-item">
<span>المستهلك</span>
<strong id="consumed-calories">0</strong>
</div>
<div class="tracker-item">
<span>المتبقي</span>
<strong id="remaining-calories">2000</strong>
</div>
</div>
</div>

<form method="post" enctype="multipart/form-data">
<input type="hidden" name="form_type" value="meal">
<div class="action-buttons">
<div class="upload-card">
<span class="upload-icon">📸</span>
<span>تصوير بالكاميرا</span>
<input type="file" name="camera_image" id="camera-input" class="file-input" accept="image/*" capture="environment" onchange="handleFileSelect(this, 'camera')">
</div>
<div class="upload-card">
<span class="upload-icon">📁</span>
<span>رفع من الجهاز</span>
<input type="file" name="device_image" id="device-input" class="file-input" accept="image/*" onchange="handleFileSelect(this, 'device')">
</div>
</div>
<div id="file-name" class="file-name"></div>
<button type="submit" class="btn-submit">تحليل الوجبة وخصم السعرات</button>
</form>
</div>

<div id="calculator-tab" class="tab-content">
<form method="post">
<input type="hidden" name="form_type" value="calculator">
<div class="form-group">
<label>الجنس</label>
<select name="gender" class="form-control" required>
<option value="male">ذكر</option>
<option value="female">أنثى</option>
</select>
</div>
<div class="form-group">
<label>الوزن (كغ)</label>
<input type="number" step="0.1" name="weight" class="form-control" placeholder="مثال: 75" required>
</div>
<div class="form-group">
<label>الطول (سم)</label>
<input type="number" name="height" class="form-control" placeholder="مثال: 175" required>
</div>
<div class="form-group">
<label>العمر (سنوات)</label>
<input type="number" name="age" class="form-control" placeholder="مثال: 25" required>
</div>
<div class="form-group">
<label>مستوى التدريب والنشاط اليومي</label>
<select name="activity" class="form-control" required>
<option value="1.2">قليل الحركة (لا توجد تمارين)</option>
<option value="1.375">نشاط خفيف (تمرين 1-3 أيام أسبوعياً)</option>
<option value="1.55">نشاط متوسط (تمرين 3-5 أيام أسبوعياً)</option>
<option value="1.725">نشاط عالي (تمرين 6-7 أيام أسبوعياً)</option>
<option value="1.9">نشاط عالي جداً (تمارين شاقة يومياً)</option>
</select>
</div>
<div class="form-group">
<label>الهدف</label>
<select name="goal" class="form-control" required>
<option value="lose">تخفيف الوزن (حرق الدهون)</option>
<option value="maintain">ثبات الوزن</option>
<option value="gain">زيادة الوزن (بناء عضلات)</option>
</select>
</div>
<button type="submit" class="btn-submit">حساب السعرات اليومية</button>
</form>
</div>

{% if result %}
<div class="result-box">
<h3>النتيجة 📊</h3>
<div id="result-content" class="markdown-content"></div>
</div>

<script>
const rawText = {{ result|tojson }};
document.getElementById('result-content').innerHTML = marked.parse(rawText);

if ("{{ active_tab }}" === "calculator") {
switchTab('calculator');
}
</script>
{% endif %}
</div>

<script>
document.addEventListener("DOMContentLoaded", () => {
loadTrackerState();
});

{% if extracted_calories and extracted_calories > 0 %}
let storedConsumed = parseInt(localStorage.getItem('daily_consumed')) || 0;
let lastProcessed = sessionStorage.getItem('last_processed_cals');
let currentResponseMarker = "{{ result[:30] if result else '' }}";

if (lastProcessed !== currentResponseMarker) {
storedConsumed += {{ extracted_calories }};
localStorage.setItem('daily_consumed', storedConsumed);
sessionStorage.setItem('last_processed_cals', currentResponseMarker);
}
{% endif %}

function loadTrackerState() {
const savedTarget = localStorage.getItem('daily_target');
const savedConsumed = localStorage.getItem('daily_consumed');

if (savedTarget) document.getElementById('daily-target').value = savedTarget;
window.consumedCalories = savedConsumed ? parseInt(savedConsumed) : 0;

updateDisplay();
}

function updateTrackerStorage() {
const target = parseInt(document.getElementById('daily-target').value) || 2000;
localStorage.setItem('daily_target', target);
updateDisplay();
}

function updateDisplay() {
const target = parseInt(document.getElementById('daily-target').value) || 2000;
const remaining = target - window.consumedCalories;

document.getElementById('consumed-calories').innerText = window.consumedCalories;
document.getElementById('remaining-calories').innerText = remaining;
}

function resetDay() {
window.consumedCalories = 0;
localStorage.setItem('daily_consumed', 0);
updateDisplay();
alert("تم إعادة ضبط السعرات اليومية بنجاح.");
}

function switchTab(tabName) {
document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
if (tabName === 'meal') {
document.querySelectorAll('.tab-btn')[0].classList.add('active');
document.getElementById('meal-tab').classList.add('active');
} else {
document.querySelectorAll('.tab-btn')[1].classList.add('active');
document.getElementById('calculator-tab').classList.add('active');
}
}

function handleFileSelect(input, source) {
const fileNameDiv = document.getElementById('file-name');
const cameraInput = document.getElementById('camera-input');
const deviceInput = document.getElementById('device-input');

if (input.files && input.files[0]) {
if (source === 'camera') {
deviceInput.value = "";
} else {
cameraInput.value = "";
}
fileNameDiv.innerText = "تم اختيار الصورة: " + input.files[0].name;
}
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    active_tab = "meal"
    extracted_calories = 0

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "meal":
            active_tab = "meal"
            file = None
            if "camera_image" in request.files and request.files["camera_image"].filename != "":
                file = request.files["camera_image"]
            elif "device_image" in request.files and request.files["device_image"].filename != "":
                file = request.files["device_image"]

            if file and file.filename != "":
                try:
                    import base64
                    image_bytes = file.read()
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    mime_type = file.content_type or "image/jpeg"
                    image_url = f"data:{mime_type};base64,{encoded_image}"

                    headers = {
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "google/gemini-2.5-flash",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "أنت خبير تغذية. قم بتحليل هذه الصورة وتقديم اسم الوجبة، واكتب سطرًا بهذا الشكل تمامًا: 'السعرات الحرارية: [الرقم]' متبوعًا بـ 'سعرة حرارية'، ثم اذكر العناصر الغذائية (بروتين، كارب، دهون) وأية ملاحظات مفيدة باللغة العربية."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": image_url
                                        }
                                    }
                                ]
                            }
                        ]
                    }

                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    
                    res_data = response.json()
                    
                    if response.status_code == 200:
                        result = res_data['choices'][0]['message']['content']
                    else:
                        result = f"خطأ من OpenRouter: {res_data.get('error', {}).get('message', 'Unknown error')}"

                    match = re.search(r'السعرات\sالحرارية[:\s](\d+)', result)
                    if not match:
                        match = re.search(r'(\d+)\s*سعرة', result)

                    if match:
                        extracted_calories = int(match.group(1))

                except Exception as e:
                    result = f"حدث خطأ أثناء التحليل: {e}"
            else:
                result = "الرجاء اختيار صورة أو التقاطها أولاً."

        elif form_type == "calculator":
            active_tab = "calculator"
            try:
                gender = request.form.get("gender")
                weight = float(request.form.get("weight"))
                height = float(request.form.get("height"))
                age = int(request.form.get("age"))
                activity = float(request.form.get("activity"))
                goal = request.form.get("goal")

                if gender == "male":
                    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
                else:
                    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

                tdee = bmr * activity

                if goal == "lose":
                    target = tdee - 400
                    goal_desc = "تخفيف الوزن (عجز 400 سعرة حرارية يومياً)"
                elif goal == "gain":
                    target = tdee + 400
                    goal_desc = "زيادة الوزن وبناء العضلات (فائض 400 سعرة حرارية يومياً)"
                else:
                    target = tdee
                    goal_desc = "ثبات الوزن"

                result = f"""### تقرير السعرات اليومية 📊
• معدل الأيض الأساسي (BMR): {round(bmr)} سعرة حرارية
• السعرات لحفظ الوزن (TDEE): {round(tdee)} سعرة حرارية
• الهدف: {goal_desc}
• السعرات المستهدفة يومياً:{round(target)} سعرة حرارية

ملاحظة غذائية: يمكنك نقل رقم السعرات المستهدفة إلى حقل الهدف اليومي في تاب تحليل الوجبات لمتابعة سعراتك وخصم وجباتك أولاً بأول!"""
            except Exception as e:
                result = f"حدث خطأ أثناء الحساب: {e}"

    return render_template_string(HTML_PAGE, result=result, active_tab=active_tab, extracted_calories=extracted_calories)

@app.route('/sw.js')
def service_worker():
    sw_code = """
    self.addEventListener('install', (e) => {
    console.log('Service Worker: Installed');
    });
    self.addEventListener('fetch', (e) => {
    });
    """
    return sw_code, 200, {'Content-Type': 'application/javascript'}

@app.route('/manifest.json')
def manifest():
    return {
        "name": "نظام السعرات الحرارية الذكي",
        "short_name": "السعرات",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#10B981",
        "description": "تطبيق ذكي لتحليل السعرات الحرارية وحساب الاحتياج اليومي",
        "icons": [
            {
                "src": "https://via.placeholder.com/512",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

