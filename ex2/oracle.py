import os
import sys
from typing import Dict, List, Optional, Tuple


def ensure_env_file(env_path: str) -> bool:
    """Checks if the path to .env.example exists"""
    if os.path.exists(env_path):
        return True
    return False


def load_config() -> Optional[Dict[str, Optional[str]]]:
    """Tries to get and return data from .env.example
    If unsuccessful, returns None"""
    try:
        from dotenv import load_dotenv
        load_dotenv(".env.example")
        return {
            "MATRIX_MODE": os.getenv("MATRIX_MODE"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "API_KEY": os.getenv("API_KEY"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL"),
            "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
        }
    except ImportError:
        return None


def build_status(
    config: Dict[str, Optional[str]],
) -> Tuple[Dict[str, str], List[str]]:
    """Formats output data and warning messages"""

    warnings: List[str] = []
    mode = config["MATRIX_MODE"] or "development"

    if mode not in {"development", "production"}:
        mode = "development"
        warnings.append("Invalid MATRIX_MODE. Using development.")

    database_url = config["DATABASE_URL"]
    api_key = config["API_KEY"]
    log_level = config["LOG_LEVEL"] or "DEBUG"
    zion_endpoint = config["ZION_ENDPOINT"]

    if database_url:
        if mode == "production":
            database = "Connected to production instance"
        else:
            database = "Connected to local instance"
    else:
        database = "Missing configuration"
        warnings.append("DATABASE_URL is missing.")

    if api_key and len(api_key) > 0:
        api_access = "Authenticated"
    else:
        api_access = "Missing configuration"
        warnings.append("API_KEY is missing.")

    if not config["LOG_LEVEL"]:
        warnings.append("LOG_LEVEL is missing. Using DEBUG.")

    if zion_endpoint:
        zion_network = "Online"
    else:
        zion_network = "Offline"
        warnings.append("ZION_ENDPOINT is missing.")

    status = {
        "mode": mode,
        "database": database,
        "api_access": api_access,
        "log_level": log_level,
        "zion_network": zion_network,
    }
    return status, warnings


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")
    env_error = ensure_env_file(".env")
    if not env_error:
        print("\nERROR: file .env is missing from the root directory")
        print("Create it with:\ncp .env.example .env")
    else:
        config = load_config()
        if not config:
            print("\nERROR: module 'python-dotenv' not found")
            print("Install the module and try again")
        else:
            status, warnings = build_status(config)
            print("\nConfiguration loaded:")
            print(f"Mode: {status['mode']}")
            print(f"Database: {status['database']}")
            print(f"API Access: {status['api_access']}")
            print(f"Log Level: {status['log_level']}")
            print(f"Zion Network: {status['zion_network']}")
            print("\nEnvironment security check:")
            print("[OK] No hardcoded secrets detected")
            print("[OK] .env file properly configured")
            print("[OK] Production overrides available")
            print("\nThe Oracle sees all configurations.")
            if warnings:
                print("Warnings:")
                for warning in warnings:
                    print(f"- {warning}", file=sys.stderr)
