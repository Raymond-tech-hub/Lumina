# student_decision_engine.py

import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

class StudentDecisionEngine:
    """
    Engine for personalized student decisions:
    - Pass/Fail prediction
    - Learning Path decision
    """

    def __init__(self):
        self.pass_model = None
        self.path_model = None
        self.path_encoder = None

    # ----------------------
    # Training methods
    # ----------------------
    def train_pass_model(self):
        """Train Pass/Fail model using built-in data with pandas DataFrame"""

        data_dict = {
            "study_hours": [2, 4, 6, 8, 10, 1, 3, 7, 9, 5],
            "attendance":  [60, 65, 70, 80, 90, 50, 55, 85, 95, 75],
            "result":      [0, 0, 1, 1, 1, 0, 0, 1, 1, 1]
        }

        df = pd.DataFrame(data_dict)
        X_pass = df[["study_hours", "attendance"]]
        y_pass = df["result"]

        self.pass_model = DecisionTreeClassifier()
        self.pass_model.fit(X_pass, y_pass)
        print("Pass/Fail model trained using pandas DataFrame!")

    def encode_csv_features(self, input_file="database/student_path_data.csv",
                        output_file="database/student_path_data_numeric.csv"):
        """
        Convert categorical/string features in the CSV to numeric values using 0..n encoding.
        Saves a new CSV with numeric features suitable for training.
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"{input_file} not found!")

        df = pd.read_csv(input_file)

        encoders = {}  # Store LabelEncoders for each column
        numeric_df = pd.DataFrame()

        # Loop through all columns
        for col in df.columns:
            if df[col].dtype == object:
                # Encode string categorical to numeric
                le = LabelEncoder()
                numeric_df[col] = le.fit_transform(df[col].astype(str))
                encoders[col] = le
            else:
                # Keep numeric columns as-is
                numeric_df[col] = df[col]

        # Save numeric CSV
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        numeric_df.to_csv(output_file, index=False)
        print(f"CSV features encoded and saved to {output_file}")

        return numeric_df, encoders
    def train_path_model(self, path_file="database/student_path_data_numeric.csv"):
        """Train Learning Path model using numeric CSV dataset"""

        if not os.path.exists(path_file):
            raise FileNotFoundError(f"{path_file} not found!")

        df = pd.read_csv(path_file)
        X_path = df.drop(columns=["learning_path"])
        y_path = df["learning_path"]

        # Force numeric just in case
        X_path = X_path.apply(pd.to_numeric, errors='raise')

        self.path_encoder = LabelEncoder()
        y_enc = self.path_encoder.fit_transform(y_path)

        self.path_model = DecisionTreeClassifier()
        self.path_model.fit(X_path, y_enc)
        print(f"Learning Path model trained using CSV data ({len(df)} rows)!")

    def train_all(self):
        """Train both Pass/Fail and Learning Path models"""

        print("Training Pass/Fail model...")
        self.train_pass_model()

        print("Encoding CSV and training Learning Path model...")
        self.encode_csv_features(
            input_file="database/student_path_data.csv",
            output_file="database/student_path_data_numeric.csv"
        )
        self.train_path_model(path_file="database/student_path_data_numeric.csv")
        print("All models trained successfully!")

    # ----------------------
    # Load/Save methods
    # ----------------------
    def save_pass_model(self, path="models/pass_model.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.pass_model, path)
        print(f"Pass/Fail model saved to {path}")

    def save_path_model(self, model_path="models/path_model.pkl", encoder_path="models/path_encoder.pkl"):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
        joblib.dump(self.path_model, model_path)
        joblib.dump(self.path_encoder, encoder_path)
        print(f"Path model saved to {model_path} and encoder to {encoder_path}")

    def load_pass_model(self, path="models/pass_model.pkl"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found!")
        self.pass_model = joblib.load(path)
        print("Pass/Fail model loaded!")

    def load_path_model(self, model_path="models/path_model.pkl", encoder_path="models/path_encoder.pkl"):
        if not os.path.exists(model_path) or not os.path.exists(encoder_path):
            raise FileNotFoundError("Path model or encoder not found!")
        self.path_model = joblib.load(model_path)
        self.path_encoder = joblib.load(encoder_path)
        print("Learning Path model loaded!")

    # ----------------------
    # Prediction methods
    # ----------------------
    def predict_pass(self, study_hours, attendance):
        if self.pass_model is None:
            raise ValueError("Pass/Fail model not trained or loaded!")
        will_pass = self.pass_model.predict([[study_hours, attendance]])[0]
        return "Pass" if will_pass == 1 else "Fail"

    def select_path(self, query_features):
        if self.path_model is None or self.path_encoder is None:
            raise ValueError("Learning Path model not trained or loaded!")
        path_enc = self.path_model.predict([query_features])[0]
        return self.path_encoder.inverse_transform([path_enc])[0]


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(abspath))
    print("Working directory set to:", os.getcwd())

    engine = StudentDecisionEngine()

    # Encode CSV and train all models
    engine.train_all()

    # Predict pass/fail
    pass_result = engine.predict_pass(7, 80)
    print("Pass result:", pass_result)

    # Example query for learning path (numeric features)
    query_features = [1, 0, 1, 0, 1, 0, 0, 1, 0, 1]  # adjust to your dataset
    path_result = engine.select_path(query_features)
    print("Learning path:", path_result)