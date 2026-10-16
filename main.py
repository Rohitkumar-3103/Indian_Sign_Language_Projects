"""
Indian Sign Language (ISL) Recognition Platform - Main Launcher.
Alias entry point that launches the core Flask server in app.py.
"""
import runpy

if __name__ == "__main__":
    runpy.run_module("app", run_name="__main__")
