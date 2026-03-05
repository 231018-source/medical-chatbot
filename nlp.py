from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

patterns = {

    "SymptomCheck": re.compile(r"(لدي|عندي|أشعر|أعاني).*(صداع|ألم|سعال|دوخة|حلق)"),

    "MedicationAdvice": re.compile(r"(دواء|الجرعة|باراسيتامول|ماذا آخذ|ما العلاج)"),

    "FeverConcern": re.compile(r"(حرارتي|حرارة|درجة).*(3[8-9]|4[0-1])"),

    "DoctorVisit": re.compile(r"(متى أزور الطبيب|هل حالتي خطيرة|هل أحتاج فحص|أحتاج طبيب)"),

    "DiseaseInfo": re.compile(r"(ما أعراض|أخبرني عن|ما أسباب|معلومات عن).*(الإنفلونزا|السكري|الربو)"),

    "Emergency": re.compile(r"(لا أستطيع التنفس|ألم شديد في الصدر|نزيف حاد)")
}

responses = {

    "SymptomCheck": "قد تكون هذه أعراض مرض بسيط، لكن إذا استمرت لفترة طويلة يفضل زيارة الطبيب.",

    "MedicationAdvice": "يفضل استشارة طبيب أو صيدلي قبل أخذ أي دواء لمعرفة الجرعة المناسبة.",

    "FeverConcern": "إذا كانت الحرارة أعلى من 38.5 ينصح بالراحة وشرب السوائل واستخدام خافض حرارة.",

    "DoctorVisit": "إذا كانت الأعراض شديدة أو استمرت أكثر من يومين فمن الأفضل زيارة الطبيب.",

    "DiseaseInfo": "يمكنني إعطاؤك معلومات عامة عن هذا المرض، لكن التشخيص يجب أن يكون من الطبيب.",

    "Emergency": "هذه حالة طارئة! يرجى التوجه إلى أقرب مستشفى فوراً.",

    "Unknown": "عذراً، لم أفهم السؤال جيداً. هل يمكنك توضيحه؟"
}


def detect_intent(user_input):

    for intent, pattern in patterns.items():

        if pattern.search(user_input):

            return intent

    return "Unknown"


def get_bot_reply(user_input):

    intent = detect_intent(user_input)

    return responses.get(intent, responses["Unknown"])


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"]

    reply = get_bot_reply(user_message)

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(debug=True)