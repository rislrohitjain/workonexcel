import os
import sys

def get_app_path():
    """ Returns the base path of the application, whether running as a script or .exe """
    if getattr(sys, 'frozen', False):
        # If the app is running as a bundle (.exe)
        return os.path.dirname(sys.executable)
    else:
        # If running in a normal Python environment
        return os.path.dirname(os.path.abspath(__file__))

def setup_folders(base_path):
    """ Creates the required folders if they don't exist """
    folders = ['logs', 'config', 'database']
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")

def main():
    # 1. Get the directory where the .exe or script is located
    app_path = get_app_path()
    
    # 2. Ensure folders exist on the client machine
    setup_folders(app_path)
    
    # --- YOUR ACTUAL EXCEL LOGIC STARTS HERE ---
    print("WorkOnExcelRohitJianPro is running...")
    # Example: writing a log
    log_file = os.path.join(app_path, "logs", "activity.log")
    with open(log_file, "a") as f:
        f.write("Application started successfully.\n")
    
    # Add your pandas/excel code here

if __name__ == "__main__":
    main()