"""
Root entry-point for the Pharma Bottle Vision Inspection System.

Delegates to ``app.main.main`` so that the application logic stays
decoupled from the repository root.
"""

from app.main import main

if __name__ == "__main__":
    main()
