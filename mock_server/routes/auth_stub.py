import os
import re

from flask import Blueprint, request, jsonify

from utilities.response_loader import load_response

auth_bp = Blueprint("auth_bp", __name__)

# -----------------------------
# Mock valid credentials – loaded from environment variables.
# Set MOCK_VALID_EMAIL and MOCK_VALID_PASSWORD in your .env file.
# These must NEVER be hardcoded in source code.
# -----------------------------
VALID_EMAIL = os.getenv("MOCK_VALID_EMAIL", "qa.mock.user@testdomain.com")
VALID_PASSWORD = os.getenv("MOCK_VALID_PASSWORD", "MockPass#0000")


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():

    body = request.json or {}

    email = body.get("email")
    password = body.get("password")
    captcha = body.get("captchaToken")
    
    print("\n========== LOGIN REQUEST ==========")
    print("EMAIL RECEIVED =", email)
    print("CAPTCHA RECEIVED =", captcha)
    # NOTE: Passwords are never logged
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