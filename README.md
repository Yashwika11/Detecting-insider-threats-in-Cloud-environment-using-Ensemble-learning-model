# Detecting-insider-threats-in-Cloud-environment-using-Ensemble-learning-model
**Overview**
Cloud environments face a growing threat from insiders — employees or privileged users who misuse legitimate access to compromise sensitive data. According to the 2022 Cloud Security Report, insider attacks account for ~35% of all cloud data breaches globally.
This project proposes an Ensemble Learning Model combining Random Forest, AdaBoost, and CatBoost classifiers to detect insider threats in real-time with high accuracy, replacing reactive, manual security approaches with a proactive, automated solution.

 **Dataset**
CERT Insider Threat Dataset — features include login times, USB activity, file transfers, after-hours access, user roles, and resource usage. Labels: 0 = Normal, 1 = Insider Attack.

**Project Structure**
insider-threat-detection/
│
├── Dataset/
│   ├── CERT_dataset.csv          # Training dataset
│   └── test_data.csv             # Test dataset for prediction
│
├── main.py                       # Main application with GUI
├── requirements.txt              # Python dependencies
└── README.md

**Tech Stack**
Python 3.7.6 · Tkinter · Scikit-learn · CatBoost · Pandas · Matplotlib · Seaborn

**Setup**
bashgit clone https://github.com/your-username/insider-threat-detection.git
cd insider-threat-detection
pip install pandas numpy scikit-learn catboost matplotlib seaborn
python main.py

**How to Use**
Upload CERT Database → load dataset
Preprocess & Split Dataset → clean + 80/20 split
Random Forest / AdaBoost / Proposed Ensemble Model → train & evaluate
Performance Evaluation Graph → compare models
Predict Attack from Test Data → run inference

**Results**
Model              | Accuracy | Precision | Recall | F1
------------------------------------------------------------
Random Forest      |95.96%    | 97.01%    | 94.44% | 95.52%
AdaBoost           |95.96%    | 97.01%    |94.44%  |95.52%
CatBoost (Proposed)|98.99%    | 99.22%    |98.61%  |98.90%

