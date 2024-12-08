# Security Policy

## Supported Versions

We actively maintain and support the following versions of this project:

| Version   | Supported          |
| --------- | ------------------ |
| 1.x.x     | ✅ Fully supported |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do not disclose publicly**: Avoid posting details about the vulnerability in public forums or repositories.
2. **Contact the maintainers**:
   - Open a private issue in the repository if supported.
3. **Provide details**:
   - Affected version(s) of the project.
   - Steps to reproduce the vulnerability.
   - Impact of the vulnerability (e.g., data leakage, code execution, etc.).
   - Any possible fixes or suggestions.

---

## Security Best Practices for Deploying on Streamlit

To ensure the security of your deployed Streamlit application:

1. **Protect sensitive data**:
   - Use environment variables to store API keys, database credentials, or other sensitive information.
   - Avoid hardcoding credentials in your codebase.
   - Add a `.streamlit/secrets.toml` file to securely store sensitive data (if using Streamlit Cloud).

2. **Restrict access**:
   - Use authentication mechanisms (e.g., OAuth, Basic Authentication) to control access to the application.
   - Streamlit Cloud offers built-in options to limit access to authenticated users.

3. **Validate inputs**:
   - Validate and sanitize all user inputs to prevent injection attacks (e.g., SQL injection, command injection).
   - Use libraries like `pydantic` or `marshmallow` for input validation.

4. **Use HTTPS**:
   - Ensure your application is served over HTTPS, especially when deployed in production.
   - If deploying on Streamlit Cloud, HTTPS is provided by default.

5. **Keep dependencies updated**:
   - Regularly update Python dependencies listed in `requirements.txt` or `pyproject.toml`.
   - Use tools like `pip-audit` or `safety` to identify and fix vulnerabilities in dependencies.

6. **Monitor logs**:
   - Enable logging in your application to monitor for unusual activity.
   - Avoid logging sensitive information such as passwords or tokens.

---

## Resources for Maintaining Security

- [Streamlit Security Best Practices](https://docs.streamlit.io/)
- [Python Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)
- [CVE Database](https://cve.mitre.org/)

---
