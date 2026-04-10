import joblib
from pathlib import Path

# Get project root using relative path from this file
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"


class ModelLoader:
    _model = None
    _columns = None
    
    @classmethod
    def get_model(cls):
        if cls._model is None:
            model_path = ARTIFACTS_DIR / "model.pkl"
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Model not found at {model_path}. "
                    f"Please ensure ml/artifacts/model.pkl exists."
                )
            cls._model = joblib.load(model_path)
        return cls._model
    
    @classmethod
    def get_columns(cls):
        if cls._columns is None:
            columns_path = ARTIFACTS_DIR / "columns.pkl"
            if not columns_path.exists():
                raise FileNotFoundError(
                    f"Columns not found at {columns_path}. "
                    f"Please ensure ml/artifacts/columns.pkl exists."
                )
            cls._columns = joblib.load(columns_path)
        return cls._columns


# Module-level convenience functions
def get_model():
    return ModelLoader.get_model()


def get_columns():
    columns = ModelLoader.get_columns()
    model = get_model()
    if hasattr(model, 'n_features_in_'):
        return columns[:model.n_features_in_]
    return columns
