# 🛡️ AI-Powered Brute Force Attack Detection System

An enterprise-style Machine Learning Intrusion Detection Platform designed to detect, analyze, and mitigate brute force login attacks using behavioral analysis, adaptive risk scoring, and real-time monitoring.

---

📌 Project Overview

This system combines:

- Machine Learning-based attack detection
- Behavioral rate limiting
- Sliding time window analysis
- IP reputation tracking
- Temporary ban logic
- Blacklist management
- SOC-style monitoring dashboard
- Dockerized microservice architecture
- CI/CD automation via GitHub Actions

The platform simulates a real-world intrusion detection system (IDS) used in modern cybersecurity infrastructures.

---

🧠 Core Features

 🔍 Machine Learning Detection
- Random Forest classifier
- Feature-based behavioral analysis
- Risk scoring engine
- Model evaluation (confusion matrix + metrics)

 🚨 Adaptive Threat Detection
- Sliding time-window attack monitoring
- Rate limiting per IP
- Brute force campaign detection
- Multi-factor risk scoring

 🛑 IP Reputation & Mitigation
- Automatic temporary bans
- Persistent blacklist storage
- Attack count tracking
- Request aggregation per IP

 📊 SOC Dashboard (Streamlit)
- Real-time metrics
- Threat level indicator
- Attack distribution chart
- IP activity overview
- Blacklisted IP tracking

 🐳 DevOps & Deployment
- Fully Dockerized services
- Docker Compose orchestration
- GitHub Actions CI/CD pipeline
- Production-ready structure
- Ready for cloud deployment (Render / Railway)

---

 🏗️ System Architecture


Client Login Request
↓
FastAPI Backend (ML Engine)
↓
Risk Scoring + Behavioral Analysis
↓
IP Tracking + Rate Limiting
↓
Temporary Ban / Blacklist
↓
Security Data Storage (JSON)
↓
SOC Dashboard (Streamlit)


---

 🛠️ Tech Stack

**Backend**
- Python
- FastAPI
- Scikit-learn
- Pandas
- Joblib

**Dashboard**
- Streamlit

**Security Logic**
- Sliding window detection
- Rate limiting engine
- IP reputation system

**DevOps**
- Docker
- Docker Compose
- GitHub Actions

---

 📁 Project Structure


brute-force-ml-detection/
│
├── api/  FastAPI backend
├── dashboard/  Streamlit SOC dashboard
├── model/  Trained ML model + metrics
├── security/  IP tracking + blacklist storage
├── src/  Training + monitoring scripts
├── nginx/  Reverse proxy config (optional)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


---

 ⚙️ Local Development Setup

 1️⃣ Clone Repository

```bash
git clone https://github.com/Perera1325/brute-force-ml-detection.git
cd brute-force-ml-detection
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Train Model
cd src
python data_generator.py
python train_model.py
4️⃣ Run API
cd ../api
uvicorn main:app --reload

Access Swagger:

http://127.0.0.1:8000/docs
5️⃣ Run Dashboard
cd ../dashboard
streamlit run app.py
🐳 Run With Docker
docker-compose up --build

API:

http://localhost:8000/docs

Dashboard:

http://localhost:8501
📈 Machine Learning Model

Model Type:

Random Forest Classifier

Features Used:

Failed login attempts

Time between attempts

Login success ratio

IP request frequency

Evaluation:

Accuracy score

Confusion matrix

Feature importance analysis

🔐 Security Logic Explained
Sliding Time Window

Tracks login attempts within a defined time window (60 seconds).

Rate Limiting

Detects abnormal request frequency.

Risk Score Formula

Combines:

ML probability

Request rate

Failure ratio

Temporary Ban System

IP is temporarily blocked when:

Excessive attack attempts

High request rate threshold exceeded

🚀 Deployment

This project is designed to be deployed using:

Render (Docker-based deployment)

Railway

AWS ECS

DigitalOcean App Platform

SSL is automatically handled by modern cloud platforms.

📊 Future Improvements

Isolation Forest anomaly detection

JWT authentication layer

Role-based access control (RBAC)

Persistent database (PostgreSQL)

Prometheus monitoring

Kubernetes deployment

Geo-IP visualization

👨‍💻 Author

Vinod Perera
Computer Science & Electrical/Electronic Engineering Undergraduate
Cybersecurity & AI Systems Enthusiast

GitHub: https://github.com/Perera1325

📜 License

This project is developed for educational and research purposes.
