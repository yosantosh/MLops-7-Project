# Copilot instructions for MLops-7-Project

These notes are written for an AI coding agent (Copilot/agents/assistants) to be immediately productive on this repository.
Keep edits small and explicit; reference affected files by path and run the pipeline via `demo.py` when validating changes.

## Big picture (what to know first) ✅
- Project is a lightweight MLOps pipeline (ETL → validation → transformation → training). The main orchestration is in:
  - `src/pipline/training_pipeline.py` (start_data_ingestion → start_data_validation → start_data_transformation; model training is present but commented out).
- Core components (each in `src/components/`):
  - `data_ingestion.py` — reads dataset from MongoDB and writes CSVs under `Artifacts/data_ingestion/`.
  - `data_validation.py` — basic schema/shape checks and writes a `report.yaml` under `Artifacts/data_validation/`.
  - `data_transformation.py` — builds a `sklearn` preprocessing `Pipeline`, saves preprocessor (`dill`) and NumPy `.npy` arrays under `Artifacts/data_transformation/`.
  - `model_trainer.py` — contains training code (RandomForest, metrics); not currently executed by pipeline (commented out).
- Artifacts are versioned under `Artifacts/` (constant names and file paths live in `src/constants/__init__.py` and `src/entity/config_entity.py`).

## Quick-start / developer workflows 🔧
- Install project (recommended):
  - pip: `pip install -r requirements.txt` then `pip install -e .` (project is packaged as `src`).
- Run the full pipeline locally:
  - Ensure MongoDB URI is exported: `export MONGODB_URL="<your-mongo-uri>"`
  - Run: `python demo.py` (this constructs `TrainPipeline` and calls `run_pipeline()`).
- Logs: `src/logger` configures a rotating file logger automatically on import. Check `logs/` for timestamps.
- Serialization:
  - Models and preprocessing objects are saved with `dill` via `src/utils/main_utils.py` (helpers: `save_object`, `load_object`).
  - Transformed data are saved/loaded with `np.save` / `np.load` helpers (`save_numpy_array_data`, `load_numpy_array_data`).

## Important environment variables & integration points ⚙️
- MongoDB: `MONGODB_URL` (key in `src/constants/__init__.py` as `MONGODB_URL_KEY`). The code will raise if the env var is unset (`src/configuration/mongo_db_connection.py`).
- Optional S3/Model push constants exist in `src/constants` (e.g., `AWS_ACCESS_KEY_ID_ENV_KEY`) though model pusher code is commented out.
- MLflow examples live in sibling folder `MLops-4-ML-Flow/` — useful references but not integrated into the pipeline in this project.

## Project conventions & patterns to follow 💡
- Use dataclasses for config and artifact objects (`src/entity/config_entity.py`, `src/entity/artifact_entity.py`).
- Centralized constants: `src/constants/__init__.py` — prefer new configuration keys there.
- Use `src.logger` (import `from src.logger import logging`) — importing it triggers logger configuration across modules.
- Error handling uses a custom wrapper from `src.exception.exceptions` — prefer raising that consistent wrapper.
- File I/O and serialization should reuse helpers in `src/utils/main_utils.py`.
- Keep pipeline steps idempotent: components write into `Artifacts/<component>/` subdirectories managed by config.

## Concrete code pointers & examples (for quick edits) 🔎
- To run the pipeline locally: `export MONGODB_URL='<uri>' && python demo.py` (demo imports `TrainPipeline` and calls `run_pipeline`).
- To add tests: add pytest tests under `tests/`, import components in isolation (e.g., construct `DataTransformation` using small DataFrame fixtures) and run `pytest`.
- To enable model training in the pipeline: uncomment ModelTrainer parts in `src/pipline/training_pipeline.py` and wire `ModelTrainer` to return `ModelTrainerArtifact`.
- To change model defaults: edit constants in `src/constants/__init__.py` (e.g., `MODEL_TRAINER_N_ESTIMATORS`) or use `ModelTrainerConfig` in `src/entity/config_entity.py`.

## Known gaps & safe assumptions ⚠️
- There are no automated tests in the repo — assume manual testing is required when modifying pipeline logic.
- `app.py` is empty; there's no production API entrypoint yet — avoid proposing API changes without the user's consent.
- Model pushing / evaluation / MLflow are partially present in separate folders or commented sections; treat them as reference or TODOs rather than existing integrations.

## When you open a PR 🧭
- Include a small demo script or unit test which exercises the changed behaviour (e.g., a minimal run of `DataTransformation` or `DataIngestion` with a mocked Mongo client).
- Confirm artifacts are written in `Artifacts/` and logs are produced in `logs/`.

---
If you'd like I can:
- Add a short `CONTRIBUTING.md` or test scaffolding (pytest + basic fixture) for component-level tests.
- Wire `ModelTrainer` back into the pipeline and add a smoke test that verifies an end-to-end run.

Please tell me which area you'd like improved or clarified. — GitHub Copilot
