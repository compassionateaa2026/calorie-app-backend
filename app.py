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
<meta name="theme-color" content="#78350F">
<title>نظام السعرات الحرارية الذكي</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
--primary-color: #78350F;
--primary-hover: #451A03;
--bg-color: #000000;
--card-bg: rgba(15, 15, 15, 0.88);
--text-color: #F3F4F6;
--border-color: #4B5563;
}

* {
box-sizing: border-box;
margin: 0;
padding: 0;
font-family: 'Cairo', sans-serif;
}

body {
background-color: var(--bg-color);
/* تعديل الطبقة الشفافة ورابط الصورة لضمان ظهور تفاصيل العضلات بوضوح */
background-image: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url('https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
background-size: cover;
background-position: center top;
background-repeat: no-repeat;
background-attachment: fixed;
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
border: 1px solid #374151;
border-radius: 20px;
padding: 24px;
box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7);
height: fit-content;
position: relative;
backdrop-filter: blur(3px);
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
background-color: #78350F;
color: white;
border: none;
padding: 10px;
border-radius: 12px;
font-size: 0.9rem;
font-weight: 700;
cursor: pointer;
margin-bottom: 16px;
box-shadow: 0 4px 12px rgba(120, 53, 15, 0.3);
}

.tracker-card {
background: rgba(31, 41, 55, 0.7);
border: 1px solid #4B5563;
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
color: #E5E7EB;
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
color: #9CA3AF;
white-space: nowrap;
}

.target-input-row input {
flex: 1;
padding: 6px 10px;
background: #1F2937;
color: #FFFFFF;
border: 1px solid #4B5563;
border-radius: 8px;
font-size: 0.85rem;
outline: none;
}

.tabs {
display: flex;
gap: 4px;
margin-bottom: 20px;
background: #1F2937;
padding: 4px;
border-radius: 12px;
border: 1px solid #374151;
}

.tab-btn {
flex: 1;
padding: 8px;
text-align: center;
background: transparent;
border: none;
border-radius: 8px;
font-weight: 600;
cursor: pointer;
font-size: 0.75rem;
color: #9CA3AF;
transition: all 0.2s;
}

.tab-btn.active {
background: #374151;
color: #FFFFFF;
box-shadow: 0 2px 5px rgba(0,0,0,0.3);
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
color: #9CA3AF;
}

.form-control {
width: 100%;
padding: 10px 12px;
border: 1px solid #4B5563;
border-radius: 10px;
font-size: 0.9rem;
outline: none;
background: #1F2937;
color: #FFFFFF;
}

.form-control:focus {
border-color: var(--primary-color);
background: #111827;
}

.action-buttons {
display: flex;
gap: 12px;
margin-bottom: 12px;
}

.upload-card {
flex: 1;
border: 2px dashed #4B5563;
border-radius: 14px;
padding: 14px 8px;
text-align: center;
background: rgba(31, 41, 55, 0.4);
cursor: pointer;
position: relative;
}

.upload-card:hover {
border-color: var(--primary-color);
background: rgba(120, 53, 15, 0.2);
}

.upload-icon {
font-size: 26px;
margin-bottom: 4px;
display: block;
}

.upload-card span:not(.upload-icon) {
font-size: 0.8rem;
color: #9CA3AF;
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
box-shadow: 0 4px 12px rgba(120, 53, 15, 0.4);
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
color: #FFFFFF;
}

.markdown-content {
font-size: 0.9rem;
line-height: 1.6;
color: #D1D5DB;
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
background: rgba(120, 53, 15, 0.2);
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
<p>حلل وجبتك واخصم سعراتها أو حلل نسبة دهون جسمك بدقة</p>
</div>

<div class="tabs">
<button type="button" class="tab-btn active" onclick="switchTab('meal')">📸 تحليل الوجبة</button>
<button type="button" class="tab-btn" onclick="switchTab('body')">💪 تحليل الجسم</button>
<button type="button" class="tab-btn" onclick="switchTab('calculator')">📊 حاسبة الاحتياج</button>
</div>

<!-- تاب تحليل الوجبة -->
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
<input type="file" name="camera_image" id="meal-camera-input" class="file-input" accept="image/*" capture="environment" onchange="handleFileSelect(this, 'meal-file-name')">
</div>
<div class="upload-card">
<span class="upload-icon">📁</span>
<span>رفع من الجهاز</span>
<input type="file" name="device_image" id="meal-device-input" class="file-input" accept="image/*" onchange="handleFileSelect(this, 'meal-file-name')">
</div>
</div>
<div id="meal-file-name" class="file-name"></div>
<button type="submit" class="btn-submit">تحليل الوجبة وخصم السعرات</button>
</form>
</div>

<!-- تاب تحليل الجسم -->
<div id="body-tab" class="tab-content">
<form method="post" enctype="multipart/form-data">
<input type="hidden" name="form_type" value="body">
<div class="action-buttons">
<div class="upload-card">
<span class="upload-icon">📸</span>
<span>تصوير بالكاميرا</span>
<input type="file" name="body_camera_image" id="body-camera-input" class="file-input" accept="image/*" capture="environment" onchange="handleFileSelect(this, 'body-file-name')">
</div>
<div class="upload-card">
<span class="upload-icon">📁</span>
<span>رفع من الجهاز</span>
<input type="file" name="body_device_image" id="body-device-input" class="file-input" accept="image/*" onchange="handleFileSelect(this, 'body-file-name')">
</div>
</div>
<div id="body-file-name" class="file-name"></div>
<button type="submit" class="btn-submit">تحليل نسبة دهون الجسم</button>
</form>
</div>

<!-- تاب حاسبة الاحتياج -->
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

const activeTab = "{{ active_tab }}";
if (activeTab === "calculator") {
switchTab('calculator');
} else if (activeTab === "body") {
switchTab('body');
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
let currentResponseMarker = "{{ result[:30] }}";

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
} else if (tabName === 'body') {
document.querySelectorAll('.tab-btn')[1].classList.add('active');
document.getElementById('body-tab').classList.add('active');
} else {
document.querySelectorAll('.tab-btn')[2].classList.add('active');
document.getElementById('calculator-tab').classList.add('active');
}
}

function handleFileSelect(input, targetNameId) {
const fileNameDiv = document.getElementById(targetNameId);
if (input.files && input.files[0]) {
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
                    image_bytes = file.read()
                    mime_type = file.content_type or "image/jpeg"

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            {
                                "inline_data": {
                                    "data": image_bytes,
                                    "mime_type": mime_type
                                }
                            },
                            "أنت خبير تغذية. قم بتحليل هذه الصورة وتقديم اسم الوجبة، واكتب سطرًا بهذا الشكل تمامًا: 'السعرات الحرارية: [الرقم]' متبوعًا بـ 'سعرة حرارية'، ثم اذكر العناصر الغذائية (بروتين، كارب، دهون) وأية ملاحظات مفيدة باللغة العربية."
                        ]
                    )
                    result = response.text

                    match = re.search(r'السعرات\sالحرارية[:\s](\d+)', result)
                    if not match:
                        match = re.search(r'(\d+)\s*سعرة', result)

                    if match:
                        extracted_calories = int(match.group(1))

                except Exception as e:
                    result = f"حدث خطأ أثناء التحليل: {e}"
            else:
                result = "الرجاء اختيار صورة أو التقاطها أولاً."

        elif form_type == "body":
            active_tab = "body"
            file = None
            if "body_camera_image" in request.files and request.files["body_camera_image"].filename != "":
                file = request.files["body_camera_image"]
            elif "body_device_image" in request.files and request.files["body_device_image"].filename != "":
                file = request.files["body_device_image"]

            if file and file.filename != "":
                try:
                    image_bytes = file.read()
                    mime_type = file.content_type or "image/jpeg"

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[
                            {
                                "inline_data": {
                                    "data": image_bytes,
                                    "mime_type": mime_type
                                }
                            },
                            "أنت خبير لياقة بدنية واختصاصي قياس تكوين الجسم. قم بتحليل هذه الصورة لتقدير نسبة دهون الجسم (Body Fat Percentage) تقريبياً، وتقدير الكتلة العضلية، وقدم نصائح رياضية وغذاء مناسبة للوصول إلى جسم مثالي باللغة العربية."
                        ]
                    )
                    result = response.text
                except Exception as e:
                    result = f"حدث خطأ أثناء تحليل الجسم: {e}"
            else:
                result = "الرجاء اختيار أو التقاط صورة للجسم أولاً."

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
• السعرات المستهدفة يومياً: {round(target)} سعرة حرارية

ملاحظة غذائية: يمكنك نقل رقم السعرات المستهدفة إلى حقل الهدف اليومي لمتابعة سعراتك أولاً بأول!"""
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
        "background_color": "#000000",
        "theme_color": "#78350F",
        "description": "تطبيق ذكي لتحليل السعرات الحرارية وحساب الاحتياج وتحليل نسبة الدهون",
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
