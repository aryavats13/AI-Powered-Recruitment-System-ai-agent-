from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db
from extractor import (
    extract_text,
    extract_email,
    extract_phone,
    extract_skills,
    extract_sections,
    extract_github_username
)
from github import get_github_stats

app = Flask(__name__)
CORS(app)

#resume
@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["file"]
    text = extract_text(file)

    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    sections = extract_sections(text)
    github_username = extract_github_username(file)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates (email, phone, skills, experience, projects, education, github_username)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        phone,
        ",".join(skills),
        sections["experience"],
        sections["projects"],
        sections["education"],
        github_username
    ))
    conn.commit()

    cid = cursor.lastrowid

    return jsonify({
        "candidate_id": cid,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience": sections["experience"],
        "projects": sections["projects"],
        "education": sections["education"],
        "github_username": github_username
    })

#candidate id
@app.route("/candidate/<int:cid>")
def get_candidate(cid):
    conn = get_db()
    row = conn.execute("SELECT * FROM candidates WHERE id=?", (cid,)).fetchone()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "id": row["id"],
        "email": row["email"],
        "phone": row["phone"],
        "skills": row["skills"].split(","),
        "experience": row["experience"],
        "projects": row["projects"],
        "education": row["education"],
        "github_username": row["github_username"]
    })

#git stats
@app.route("/github/<username>")
def github(username):
    return jsonify(get_github_stats(username))


if __name__ == "__main__":
    app.run(debug=True)
