# SentinelEye - Behavioral Anomaly Detection for Insider Threat Monitoring

SentinelEye is a modular, unsupervised machine learning system designed to monitor user behavior and detect potential insider threats or anomalous activity on a workstation. It observes file system events, keystroke dynamics, mouse movement patterns, and network IP changes to build a baseline of "normal" behavior and alert on deviations.

---

## 🧠 Approach & Methodology

SentinelEye operates in two distinct phases managed by `Main.py`:

1. **Learning Period (Default: 7 Days)**
   - **Train.py** runs periodically to process raw logs and train/update ML models (Isolation Forest, One-Class SVM, Autoencoder).
   - **Monitor.py** runs continuously to collect data using **high-frequency** monitoring scripts.
   - *Goal:* Establish a statistical baseline of normal user behavior.

2. **Monitoring Period (Post-Learning)**
   - **Train.py** continues to run periodically for **incremental learning** (updating the model with new, normal data).
   - **Monitor_S.py** switches to **stable/low-frequency** monitoring scripts to reduce system overhead while maintaining vigilance.
   - *Goal:* Detect anomalies in real-time against the established baseline.

---

## 🛠️ Features

- **File Access Monitoring:** Tracks file creations, modifications, and deletions.
- **Keystroke Dynamics:** Analyzes typing rhythm, press duration, and key intervals.
- **Mouse Dynamics:** Tracks cursor position, speed, clicks, and scroll events.
- **Network Monitoring:** Logs changes in IP configuration.
- **Unsupervised Learning:** Does not require labeled "malicious" data; it learns what "normal" looks like.
- **Low Footprint:** Automatically throttles monitoring frequency after the initial learning phase to save resources.
- **Graceful Termination:** Uses `ESC` key listeners for clean shutdown of all subprocesses and threads.

---

## 📁 Project Structure

```
SentinelEye/
│
├── config.json                 # Auto-generated on first run (tracks start date & frequencies)
├── Main.py                     # Orchestrator: Manages learning/monitoring phases & threads
├── Train.py                    # ML Pipeline: Processes logs and updates models
├── Monitor.py                  # High-frequency data collection (Learning Phase)
├── Monitor_S.py                # Low-frequency data collection (Stable Phase)
├── Test.py                     # Inference test script for sample data
│
├── Records/                    # Generated data storage
│   ├── file_access_log/
│   │   └── trained/            # Processed data moved here after training
│   ├── key_log/
│   │   └── trained/
│   ├── mouse_data_log/
│   │   └── trained/
│   └── ip_change_log/
│
├── Models/                     # Serialized ML models
│   ├── file_access_log/
│   ├── key_log/
│   └── mouse_data_log/
│
├── Monitoring/                 # High-frequency sensor scripts (Learning Phase)
│   ├── FI_R.py                 # File Interface Recorder
│   ├── KI_R.py                 # Keyboard Interface Recorder
│   ├── MI_R.py                 # Mouse Interface Recorder
│   └── IPI_R.py                # IP Interface Recorder
│
├── Monitoring_Stable/          # Low-frequency sensor scripts (Stable Phase)
│   ├── FI_R_S.py
│   ├── KI_R_S.py
│   ├── MI_R_S.py
│   └── IPI_R_S.py
│
├── Model_Handler/              # Prediction interface
│   └── handler.py
│
└── Training/                   # ML algorithm implementations
    ├── training_isolation_forest.py
    ├── training_one_class_svm.py
    └── training_autoencoder.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `pynput` (for keyboard/mouse hooks and global hotkeys)
- `pandas`, `numpy`, `scikit-learn` (for data processing and ML models)
- `tensorflow` or `torch` (for Autoencoder model)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/SentinelEye.git
   cd SentinelEye
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Missing Modules**
   > *Note: This repository contains the orchestration logic. You must implement or place the missing sensor modules in `Monitoring/`, `Monitoring_Stable/`, and the training algorithms in `Training/`.*

### Running the System

1. **Start the Orchestrator**
   ```bash
   python Main.py
   ```
   On the first run, `config.json` will be created with the current timestamp. The system will enter the **Learning Period**.

2. **Stopping the System**
   Press the `ESC` key at any time. The system will gracefully terminate all monitoring subprocesses and save the current state.

3. **Testing Predictions**
   Once models are trained, test the inference pipeline:
   ```bash
   python Test.py
   ```

---

## ⚙️ Configuration (`config.json`)

| Key | Description |
|-----|-------------|
| `initiated_date` | Auto-generated timestamp marking the start of the learning period. |
| `learning_period_days` | Duration (in days) to run high-frequency monitoring before switching to stable mode. |
| `train_frequency` | How often (in seconds) `Train.py` is executed to retrain/update models. |
| `monitor_frequency` | How long each monitoring script runs before restarting (restarts help clear memory buffers). |

---

## ⚠️ Ethical and Legal Disclaimer

**SentinelEye is intended for authorized security monitoring and research purposes only.**

This tool captures keystrokes and mouse movements. **You must obtain explicit, written consent from the user of the device before running this software.** Unauthorized use of this tool to monitor individuals without their knowledge is illegal in many jurisdictions and a violation of privacy. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

## 🤝 Contributing

Contributions to improve the ML models, add new sensor types, or optimize performance are welcome. Please ensure any sensors added are designed to minimize system impact and respect user privacy boundaries.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
