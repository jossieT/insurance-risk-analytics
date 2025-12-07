"""
DVC (Data Version Control) setup and configuration module.
"""
import subprocess
import os
import shutil
from pathlib import Path
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DVCSetup:
    """Class to handle DVC setup and configuration."""
    
    def __init__(self, project_root: str = ".."):
        """
        Initialize DVC setup.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.dvc_dir = self.project_root / ".dvc"
        
    def initialize_dvc(self):
        """
        Initialize DVC in the project directory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Initializing DVC...")
            result = subprocess.run(
                ["dvc", "init", "--no-scm"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("DVC initialized successfully!")
                
                # Initialize Git if not already
                if not (self.project_root / ".git").exists():
                    subprocess.run(["git", "init"], cwd=self.project_root)
                    logger.info("Git initialized for DVC")
                
                return True
            else:
                logger.error(f"DVC initialization failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("DVC not installed. Install with: pip install dvc")
            return False
    
    def setup_local_remote(self, storage_path: str = "dvc_storage"):
        """
        Set up local remote storage for DVC.
        
        Args:
            storage_path: Path for local storage
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create storage directory
            storage_dir = self.project_root / storage_path
            storage_dir.mkdir(exist_ok=True)
            logger.info(f"Created storage directory: {storage_dir}")
            
            # Add local remote
            result = subprocess.run(
                ["dvc", "remote", "add", "-d", "localstorage", str(storage_dir)],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Local remote storage configured successfully!")
                
                # Configure default remote
                config_result = subprocess.run(
                    ["dvc", "remote", "default", "localstorage"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                
                # Create .dvcignore file
                self.create_dvcignore()
                
                return True
            else:
                logger.error(f"Failed to configure remote: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting up local remote: {str(e)}")
            return False
    
    def create_dvcignore(self):
        """Create .dvcignore file."""
        dvcignore_content = """# Ignore patterns for DVC
*.pyc
__pycache__/
.ipynb_checkpoints/
.DS_Store
Thumbs.db
*.log
logs/
reports/temp/
models/temp/
"""
        
        dvcignore_path = self.project_root / ".dvcignore"
        with open(dvcignore_path, 'w') as f:
            f.write(dvcignore_content)
        
        logger.info(f"Created .dvcignore at {dvcignore_path}")
    
    def add_data_to_dvc(self, data_path: str):
        """
        Add data file to DVC tracking.
        
        Args:
            data_path: Path to data file relative to project root
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            full_path = self.project_root / data_path
            
            if not full_path.exists():
                logger.error(f"Data file not found: {full_path}")
                return False
            
            logger.info(f"Adding {data_path} to DVC tracking...")
            
            # Add file to DVC
            result = subprocess.run(
                ["dvc", "add", data_path],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Successfully added {data_path} to DVC")
                
                # Git add the .dvc file
                dvc_file = f"{data_path}.dvc"
                subprocess.run(["git", "add", dvc_file], cwd=self.project_root)
                logger.info(f"Added {dvc_file} to Git staging")
                
                return True
            else:
                logger.error(f"Failed to add data to DVC: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding data to DVC: {str(e)}")
            return False
    
    def commit_changes(self, message: str = "Update data via DVC"):
        """
        Commit DVC changes to Git.
        
        Args:
            message: Commit message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add .dvc directory to Git
            subprocess.run(["git", "add", ".dvc"], cwd=self.project_root)
            
            # Commit changes
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Committed changes: {message}")
                return True
            else:
                logger.warning(f"Commit may have failed or nothing to commit: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error committing changes: {str(e)}")
            return False
    
    def push_to_remote(self):
        """
        Push data to DVC remote storage.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Pushing data to DVC remote storage...")
            
            result = subprocess.run(
                ["dvc", "push"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Data successfully pushed to remote storage!")
                return True
            else:
                logger.error(f"Failed to push data: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error pushing to remote: {str(e)}")
            return False
    
    def create_dvc_pipeline(self):
        """
        Create a DVC pipeline configuration for reproducible workflows.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pipeline_config = {
                'stages': {
                    'load_data': {
                        'cmd': 'python src/pipeline/load_data.py',
                        'deps': [
                            'src/pipeline/load_data.py',
                            'data/raw/MachineLearningRating_v3.txt'
                        ],
                        'outs': [
                            'data/processed/cleaned_data.csv',
                            'data/processed/data_info.json'
                        ],
                        'metrics': ['reports/load_metrics.json'],
                        'plots': ['reports/data_summary.html']
                    },
                    'eda': {
                        'cmd': 'python src/pipeline/eda_pipeline.py',
                        'deps': [
                            'src/pipeline/eda_pipeline.py',
                            'data/processed/cleaned_data.csv'
                        ],
                        'outs': [
                            'reports/eda_report.html',
                            'reports/figures/'
                        ],
                        'metrics': ['reports/eda_metrics.json'],
                        'params': ['params/eda_params.yaml']
                    },
                    'preprocess': {
                        'cmd': 'python src/pipeline/preprocess.py',
                        'deps': [
                            'src/pipeline/preprocess.py',
                            'data/processed/cleaned_data.csv',
                            'params/preprocess_params.yaml'
                        ],
                        'outs': [
                            'data/processed/train.csv',
                            'data/processed/test.csv',
                            'models/preprocessor.pkl'
                        ]
                    }
                }
            }
            
            pipeline_file = self.project_root / "dvc.yaml"
            with open(pipeline_file, 'w') as f:
                yaml.dump(pipeline_config, f, default_flow_style=False)
            
            logger.info(f"Created DVC pipeline configuration at {pipeline_file}")
            
            # Create params directory and files
            params_dir = self.project_root / "params"
            params_dir.mkdir(exist_ok=True)
            
            # Create sample parameter files
            eda_params = {
                'visualization': {
                    'figsize': [12, 8],
                    'dpi': 100,
                    'color_palette': 'husl'
                },
                'analysis': {
                    'outlier_threshold': 3.0,
                    'correlation_threshold': 0.7
                }
            }
            
            eda_params_file = params_dir / "eda_params.yaml"
            with open(eda_params_file, 'w') as f:
                yaml.dump(eda_params, f, default_flow_style=False)
            
            preprocess_params = {
                'split': {
                    'test_size': 0.2,
                    'random_state': 42
                },
                'encoding': {
                    'method': 'onehot',
                    'max_categories': 20
                },
                'imputation': {
                    'strategy': 'median'
                }
            }
            
            preprocess_params_file = params_dir / "preprocess_params.yaml"
            with open(preprocess_params_file, 'w') as f:
                yaml.dump(preprocess_params, f, default_flow_style=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating DVC pipeline: {str(e)}")
            return False
    
    def verify_dvc_setup(self):
        """
        Verify DVC setup and print status.
        
        Returns:
            dict: Dictionary with verification results
        """
        verification = {
            'dvc_installed': False,
            'dvc_initialized': False,
            'remote_configured': False,
            'data_tracked': False,
            'git_integrated': False
        }
        
        try:
            # Check if DVC is installed
            result = subprocess.run(
                ["dvc", "--version"],
                capture_output=True,
                text=True
            )
            verification['dvc_installed'] = result.returncode == 0
            
            # Check if DVC is initialized
            dvc_config = self.dvc_dir / "config"
            verification['dvc_initialized'] = dvc_config.exists()
            
            # Check remote configuration
            if verification['dvc_initialized']:
                with open(dvc_config, 'r') as f:
                    config_content = f.read()
                    verification['remote_configured'] = 'remote "localstorage"' in config_content
            
            # Check if data is tracked
            dvc_files = list(self.project_root.glob("*.dvc"))
            verification['data_tracked'] = len(dvc_files) > 0
            
            # Check Git integration
            git_dir = self.project_root / ".git"
            verification['git_integrated'] = git_dir.exists()
            
            return verification
            
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return verification