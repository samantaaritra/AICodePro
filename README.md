AICodePro 🚀
AI-Powered Code Optimization & Review Tool
📌 Overview
AICodePro is a machine learning–driven tool that analyzes GitHub Pull Requests (PRs) to provide insights on code quality, performance optimization, and maintainability.
It automates PR analysis, labeling, model training, and prediction — helping developers at scale (like Microsoft, Meta, Amazon, NVIDIA) improve code reviews efficiently.

✨ Features
🔎 Fetch & Clean PR Data from GitHub API
📊 Analyze PRs (open/closed, contributors, code changes, complexity)
🏷 Label PRs automatically (simple vs complex)
🤖 Train ML Model to learn from labeled PRs
🎯 Predict PR Outcomes for new/unseen PRs
📈 Generate Reports for maintainability & optimization insights

🛠 Tech Stack
Language: Python
ML Library: scikit-learn
Data Handling: JSON, pandas
API: GitHub REST API
Tools: Git, VS Code
Version Control: GitHub

Project Stucture (tentative)
AICodePro/
│
├── data/                  # Stores PR data & JSON files
│   ├── clean_prs.json
│   ├── pr_diffs.json
│   ├── labeled_prs.json
│   └── predicted_prs.json
│
├── models/                # Trained ML models
│   └── pr_model.pkl
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── fetch_prs.py
│   ├── analyze_prs.py
│   ├── fetch_diffs.py
│   ├── label_prs.py
│   ├── train_model.py
│   └── predict_prs.py
│
├── requirements.txt       # Dependencies
└── README.md

Future Enhancements
✅ Add deep learning models for advanced predictions
✅ Build Streamlit dashboard for visualization
✅ Integrate auto-comments on GitHub PRs
✅ Support for multiple languages (Python, Java, C++)

👨‍💻 Author
Aritra Samanta
📌 Pre-final Year Computer Science Student
