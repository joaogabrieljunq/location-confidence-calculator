# Tower Jumps Analysis and Confidence Calculator

This repository contains tools and scripts for analyzing and determining the confidence of mobile subscriber locations based on cell tower triangulation data. The project includes:

1. **Exploratory Analysis**: A Jupyter notebook to explore the dataset.
2. **Interactive Streamlit App**: A web app for uploading datasets and calculating confidence for specific intervals.
3. **Unit Tests**: A set of tests to ensure the robustness of the confidence calculation logic.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/joaogabrieljunq/location-confidence-calculator.git
   cd location-confidence-calculator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Unit Tests**:
   ```bash
   python app/test.py
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

5. **Test Demo**:
   [Click here to access the live demo](https://location-confidence-calculator-yhcie8emmbjyqjn977vruh.streamlit.app/)
