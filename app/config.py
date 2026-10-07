"""
Application configuration for the Pharma Bottle Vision System.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Pharma Bottle Vision System"
    app_env: str = "development"
    log_level: str = "INFO"

    # MySQL Database
    database_url: str = (
        "mysql+pymysql://root:@127.0.0.1:3307/pharma_vision"
    )

    # Camera
    camera_ip: str = ""
    camera_port: int = 0
    camera_username: str = ""
    camera_password: str = ""

    # PLC
    plc_ip: str = ""
    plc_port: int = 502

    # AI Model
    model_path: str = str(PROJECT_ROOT / "models" / "detector.pt")

    # Storage
    evidence_path: str = str(PROJECT_ROOT / "evidence")
    log_path: str = str(PROJECT_ROOT / "logs")

    # Production target
    target_bottles_per_minute: int = 120
    target_bottle_interval_ms: int = 500

    # Inspection settings
    cap_inspection_enabled: bool = True
    fill_level_inspection_enabled: bool = True
    packaging_inspection_enabled: bool = True
    tamper_ring_inspection_enabled: bool = True
    ocr_enabled: bool = False

    # Confidence thresholds
    cap_confidence_threshold: float = 0.50
    label_confidence_threshold: float = 0.50
    tamper_confidence_threshold: float = 0.50
    packaging_confidence_threshold: float = 0.50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()