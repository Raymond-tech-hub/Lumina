import os
import json
import matplotlib.pyplot as plt
import numpy as np


class StudentData:
    def __init__(self, folder, json_path):
        self.folder = folder
        self.json_path = json_path
        self.subjects = []
        self.data = {}
        self.exams = []

    def load_data(self, data_file):
        if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
            try:
                with open(data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"Loaded {data_file} successfully")
                    return data
            except Exception as e:
                print(f"Error loading json file {data_file}: {e}")
        else:
            print(f"{data_file} not found")

    def get_data(self):
        exam_data = self.load_data(self.json_path)

        self.data["Exams"] = exam_data["Exams"]

        for subject in exam_data["Subjects"]:
            self.subjects.append(subject)
            self.data[subject] = exam_data[subject]

        print(self.data)

    def plot_graph(self):
        exam_count = self.data["Exams"]
        self.exams = list(range(1, exam_count + 1))

        for subject in self.subjects:
            plt.figure()

            scores = np.array(self.data[subject])

            plt.plot(self.exams, scores, marker="o")
            plt.xlabel("Exam")
            plt.ylabel("Score")
            plt.title(subject)
            plt.grid(True)

            plt.savefig(
                f"{self.folder}/{subject}.png",
                dpi=300,
                bbox_inches="tight"
            )
            plt.close()

            print(f"Created {subject}.png")
            print("Scores:", scores)
            print("Shape:", scores.shape)
            print("Dimensions:", scores.ndim)

    def build(self):
        self.get_data()
        self.plot_graph()


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print("Working directory set to:", os.getcwd())

    folder = "001"
    json_path = os.path.join(folder, "exam_data.json")

    sd = StudentData(folder=folder, json_path=json_path)
    sd.build()
