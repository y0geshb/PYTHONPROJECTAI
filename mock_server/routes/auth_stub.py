import email
import os
import re

from flask import Blueprint, request, jsonify

from utilities.response_loader import load_response

auth_bp = Blueprint("auth_bp", __name__)

# -----------------------------
# Mock valid credentials
# -----------------------------
VALID_EMAIL = "kajal.gupta11@gmail.com"
VALID_PASSWORD = "Password@123dd4"


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():

    body = request.json or {}

    email = body.get("email")
    password = body.get("password")
    captcha = body.get("captchaToken")
    
    print("\n========== LOGIN REQUEST ==========")
    print("FULL BODY =", body)
    print("EMAIL RECEIVED =", email)
    print("PASSWORD RECEIVED =", password)
    print("CAPTCHA RECEIVED =", captcha)
    print("EXPECTED EMAIL =", VALID_EMAIL)
    print("EXPECTED PASSWORD =", VALID_PASSWORD)
    print("===================================\n")

    # -----------------------------
    # Missing fields
    # -----------------------------
    if not email:
        return jsonify({
            "success": False,
            "message": {
                "en": "Email is required"
            }
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": {
                "en": "Password is required"
            }
        }), 400

    if not captcha:
        return jsonify({
            "success": False,
            "message": {
                "en": "Captcha token is required"
            }
        }), 400

    # -----------------------------
    # Invalid email format
    # -----------------------------
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(email_regex, email):

        return jsonify({
            "success": False,
            "message": {
                "en": "Invalid email format"
            }
        }), 400

    # -----------------------------
    # SQL injection attempt
    # -----------------------------
    if "'" in email or "=" in email:

        return jsonify({
            "success": False,
            "message": {
                "en": "Invalid input"
            }
        }), 400

    # -----------------------------
    # Unknown field injection
    # -----------------------------
    allowed_fields = {
        "email",
        "password",
        "captchaToken"
    }

    extra_fields = set(body.keys()) - allowed_fields

    if extra_fields:

        return jsonify({
            "success": False,
            "message": {
                "en": "Unknown fields not allowed"
            }
        }), 400

    # -----------------------------
    # Account locked
    # -----------------------------
    if email == "locked@test.com":

        response = load_response(
            os.path.join(
                "responses",
                "auth",
                "account_locked.json"
            )
        )

        return jsonify(response), 423

    # -----------------------------
    # Nonexistent email
    # -----------------------------
    if email == "notregistered_xyz@example.com":

        response = load_response(
            os.path.join(
                "responses",
                "auth",
                "email_not_found.json"
            )
        )

        return jsonify(response), 401

    # -----------------------------
    # Valid credentials check
    # -----------------------------
    if email != VALID_EMAIL or password != VALID_PASSWORD:

        response = load_response(
            os.path.join(
                "responses",
                "auth",
                "invalid_password.json"
            )
        )

        return jsonify(response), 401

    # -----------------------------
    # SUCCESS
    # -----------------------------
    response = load_response(
        os.path.join(
            "responses",
            "auth",
            "login_success.json"
        )
    )

    return jsonify(response), 200