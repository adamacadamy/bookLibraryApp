import os

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL")

EMAIL_REGISTRATION_MESSAGE_TEMPLATE = """" 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Regional Library Registration</title>
  <link href="https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap" rel="stylesheet">
  <style>
    body {
      background-color: #1f1f1f;
      font-family: Arial, sans-serif;
      color: white;
      margin: 0;
      padding: 0;
    }

    .header {
      background-color: #f4511e;
      padding: 10px 20px;
      font-family: 'Comic Neue', cursive;
      font-size: 20px;
      font-weight: bold;
      color: white;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      width: fit-content;
    }

    .container {
      background: #2a2a2a;
      max-width: 600px;
      margin: 50px auto;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
    }

    .content {
      line-height: 1.6;
      font-size: 16px;
    }

    .credentials {
      margin-top: 20px;
      margin-bottom: 20px;
    }

    .credentials strong {
      display: inline-block;
      width: 100px;
    }

    .footer {
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">Regional Library</div>
    <div class="content">
      <p>Dear &nbsp;<strong>{full_name}</strong>,</p>

      <p>We are pleased to inform you that you have been successfully registered with the Regional Library.</p>

      <div class="credentials">
        <p><strong>Username:</strong>{Username}</p>
        <p><strong>Password:</strong> {Password}</p>
      </div>

      <p>You can now log in to our library portal to browse books, reserve titles, access e-resources, and manage your account.</p>

      <p>If you have any questions or need assistance, feel free to contact our support team.</p>

      <p class="footer">Welcome aboard, and happy reading!</p>

      <p>Warm regards,<br>
      Regional Library Team</p>
    </div>
  </div>
</body>
</html>

"""
