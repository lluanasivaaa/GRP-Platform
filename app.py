from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).parent / "risk_management_system" / "app.py"), run_name="__main__")
