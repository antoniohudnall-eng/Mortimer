# SMTP Configuration for PSDEPOT Marketing
# Update these values with your credentials

SMTP_CONFIG = {
    "sender": {
        "primary": "performancedepot@gmail.com",
        "backup": "mortimer@myl0nr0s.cloud"
    },
    "gmail": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,  # TLS
        "username": "performancedepot@gmail.com",
        # "password": "YOUR_APP_PASSWORD_HERE",  # <-- SET THIS
    },
    "myl0nr0s": {
        "smtp_server": "smtp.mailgun.org",  # or your provider
        "smtp_port": 587,
        "username": "mortimer@myl0nr0s.cloud",
        # "password": "YOUR_PASSWORD_HERE",  # <-- SET THIS
    }
}

# Choose which to use
ACTIVE_SENDER = "gmail"  # or "myl0nr0s"
DRY_RUN = True  # Set to False when ready to send
