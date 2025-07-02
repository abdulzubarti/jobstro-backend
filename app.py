from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "✅ Jobstro Resume Generator API is live!"

@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.json
    full_name = data.get("fullName")
    target_role = data.get("targetRole")
    skills = data.get("skills")
    user_type = data.get("userType")

    if not full_name or not target_role or not skills or not user_type:
        return jsonify({"error": "Missing required fields"}), 400

    prompt = f"Create an ATS-friendly resume for {full_name}, targeting the role of {target_role}, with skills: {skills}. User type: {user_type}."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        resume = response.choices[0].message.content.strip()
        return jsonify({"resume": resume})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
