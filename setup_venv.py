import os
import sys
import subprocess
import venv
from pathlib import Path

def main():
    """Create virtual environment and install dependencies."""
    venv_dir = Path("venv")
    requirements_file = Path("requirements.txt")
    
    print("[*] Setting up Python virtual environment for Samsung TV Controller")
    
    # Check if requirements.txt exists
    if not requirements_file.exists():
        print(f"[-] {requirements_file} not found!")
        sys.exit(1)
    
    # Create virtual environment
    if venv_dir.exists():
        print(f"[*] Virtual environment already exists at {venv_dir}")
    else:
        print(f"[*] Creating virtual environment at {venv_dir}...")
        try:
            venv.create(venv_dir, with_pip=True)
            print("[+] Virtual environment created successfully")
        except Exception as e:
            print(f"[-] Failed to create virtual environment: {e}")
            sys.exit(1)
    
    # Determine pip executable path
    if sys.platform == "win32":
        pip_executable = venv_dir / "Scripts" / "pip.exe"
        python_executable = venv_dir / "Scripts" / "python.exe"
    else:
        pip_executable = venv_dir / "bin" / "pip"
        python_executable = venv_dir / "bin" / "python"
    
    # Upgrade pip
    print("[*] Upgrading pip...")
    try:
        subprocess.run([str(pip_executable), "install", "--upgrade", "pip"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to upgrade pip: {e}")
        sys.exit(1)
    
    # Install requirements
    print("[*] Installing dependencies from requirements.txt...")
    try:
        subprocess.run([str(pip_executable), "install", "-r", str(requirements_file)], check=True)
        print("[+] Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to install dependencies: {e}")
        sys.exit(1)
    
    # Print activation instructions
    print("\n" + "="*60)
    print("[+] Setup complete! To activate the virtual environment:")
    print("="*60)
    if sys.platform == "win32":
        print(f"    {venv_dir}\\Scripts\\activate")
    else:
        print(f"    source {venv_dir}/bin/activate")
    print("="*60)
    print("\nThen you can run the scripts, for example:")
    print(f"    python send_command.py")
    print(f"    python tv_controller.py mute")
    print(f"    python test_secure.py")

if __name__ == "__main__":
    main()
