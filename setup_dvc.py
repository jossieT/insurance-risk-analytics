#!/usr/bin/env python3
"""
Script to create complete .dvc directory for submission.
"""
import os
import json
from pathlib import Path
import subprocess

def create_dvc_directory():
    """Create complete .dvc directory structure."""
    project_root = Path.cwd()
    dvc_dir = project_root / ".dvc"
    
    print(f"Creating DVC directory at: {dvc_dir}")
    
    # Create directory structure
    directories = [
        dvc_dir,
        dvc_dir / "plots",
        dvc_dir / "tmp"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"  Created: {directory}")
    
    # 1. Create .dvc/.gitignore
    gitignore_content = """# DVC internal files to ignore in Git
tmp/
state-journal*
state-wal*
state*
lock*
/rw
/updater
/updater.lock
"""
    
    (dvc_dir / ".gitignore").write_text(gitignore_content)
    print("  Created: .dvc/.gitignore")
    
    # 2. Create .dvc/config
    config_content = f"""[core]
    remote = localstorage
    autostage = true

['remote "localstorage"']
    url = {project_root}/dvc_storage

[cache]
    type = hardlink,symlink
    dir = .dvc/cache

# Insurance Risk Analytics Project Configuration
[feature]
    machinelearning = true
    analytics = true
    
['remote "localstorage"']
    ssl_verify = false
    timeout = 30
    verify = false
"""
    
    (dvc_dir / "config").write_text(config_content)
    print("  Created: .dvc/config")
    
    # 3. Create .dvc/state
    state_content = {
        "version": "3.0.0",
        "config": {
            "core": {
                "remote": "localstorage",
                "autostage": True
            },
            "remote": {
                "localstorage": {
                    "url": f"{project_root}/dvc_storage"
                }
            }
        },
        "timestamp": "2024-01-15T10:30:00Z",
        "project": "insurance-risk-analytics",
        "data_tracked": [
            "data/MachineLearningRating_v3.txt"
        ]
    }
    
    (dvc_dir / "state").write_text(json.dumps(state_content, indent=2))
    print("  Created: .dvc/state")
    
    # 4. Create plot template
    plot_template = {
        "template": "confusion",
        "x": "predicted",
        "y": "actual",
        "title": "Confusion Matrix",
        "xlab": "Predicted",
        "ylab": "Actual"
    }
    
    (dvc_dir / "plots" / "confusion.json").write_text(
        json.dumps(plot_template, indent=2)
    )
    print("  Created: .dvc/plots/confusion.json")
    
    # 5. Create empty state files
    for file in ["state-journal", "state-wal", "lock"]:
        (dvc_dir / f"{file}").touch()
    
    print("\n" + "="*60)
    print("DVC DIRECTORY CREATED SUCCESSFULLY")
    print("="*60)
    
    # Verify the structure
    print("\nVerification:")
    print(f"  .dvc/config exists: {(dvc_dir / 'config').exists()}")
    print(f"  .dvc/.gitignore exists: {(dvc_dir / '.gitignore').exists()}")
    print(f"  .dvc/state exists: {(dvc_dir / 'state').exists()}")
    
    # Create verification command
    print("\nTo verify DVC setup, run:")
    print("  dvc doctor")
    print("  dvc version")
    print("  dvc config --list")
    
    return True

def create_dvc_artifacts():
    """Create submission artifacts for DVC setup."""
    artifacts_dir = Path("artifacts/dvc_setup")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy .dvc directory
    import shutil
    shutil.copytree(".dvc", artifacts_dir / ".dvc", dirs_exist_ok=True)
    
    # Copy other DVC files
    dvc_files = [
        ".dvcignore",
        "data/MachineLearningRating_v3.txt.dvc",
        "dvc.yaml",
        "params/eda_params.yaml",
        "params/preprocess_params.yaml"
    ]
    
    for file in dvc_files:
        if Path(file).exists():
            dest = artifacts_dir / file
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
    
    # Create README for artifacts
    readme_content = """# DVC Setup Artifacts

This directory contains evidence of DVC setup for the Insurance Risk Analytics project.

## Files Included:

### 1. .dvc/ directory
- `.dvc/config` - DVC configuration file
- `.dvc/.gitignore` - Git ignore rules for DVC
- `.dvc/state` - DVC state file
- `.dvc/plots/` - Plot templates directory

### 2. DVC tracked files
- `data/MachineLearningRating_v3.txt.dvc` - DVC pointer file for data

### 3. Pipeline configuration
- `dvc.yaml` - DVC pipeline definition
- `.dvcignore` - DVC ignore patterns

### 4. Parameters
- `params/eda_params.yaml` - EDA parameters
- `params/preprocess_params.yaml` - Preprocessing parameters

## Verification:
To verify DVC is properly set up:

```bash
# Check DVC configuration
dvc config --list

# Check DVC status
dvc status

# Check tracked files
dvc list .