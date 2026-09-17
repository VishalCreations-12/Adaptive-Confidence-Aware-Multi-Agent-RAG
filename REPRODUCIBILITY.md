# REPRODUCIBILITY & VERIFICATION GUIDE

## 1. Environment Setup
- Python 3.10+ installed
- Command to install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Running Automated Unit Tests
To verify all unit tests (13 test cases):
```bash
pytest tests/
```
Or double-click `run_tests.bat`.

## 3. Running Master Automated Research Experiments
To execute the five-way baseline comparison, ablation study, statistical tests, and generate research graphics:
```bash
python scripts/run_full_experiments.py
```
Or double-click `run_experiments.bat`.

Outputs generated:
- `data/results/five_way_results.csv`
- `data/results/summary_metrics.json`
- `data/results/ablation_results.json`
- `data/results/statistical_results.json`
- `data/results/plots/` (5 PNG plot graphics)

## 4. Launching Interactive Streamlit Application
To launch the interactive research web dashboard:
```bash
streamlit run app.py
```
Or double-click `run_app.bat`.

App will open in default browser at `http://localhost:8501`.
