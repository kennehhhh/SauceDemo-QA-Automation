from __future__ import annotations

import os

BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes", "on"}
TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", "12"))

USERS = {
    "standard_user": "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user": "secret_sauce",
    "performance_glitch_user": "secret_sauce",
    "error_user": "secret_sauce",
    "visual_user": "secret_sauce",
}
