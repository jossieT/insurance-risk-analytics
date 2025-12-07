def dvc_steps():
    """
    Returns the DVC steps as a string.
    """
    steps = """
    DVC Steps:
    1. Initialize DVC: dvc init
    2. Configure remote: dvc remote add -d myremote <storage_path>
    3. Add data: dvc add data/processed/cleaned_data.csv
    4. Commit DVC file: git add data/processed/cleaned_data.csv.dvc
    5. Commit changes: git commit -m "Add processed data"
    6. Push data: dvc push
    """
    return steps

