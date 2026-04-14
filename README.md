# GlobalChain | Blockchain Logistics System

A decentralized application (DApp) for cross-border trade management, built using MVC architecture and featuring a custom blockchain with smart contract automation.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask

### Installation
1. Install dependencies:
   ```bash
   pip install flask
   ```

2. Run the application:
   ```bash
   python controller/app.py
   ```

3. Access the dashboard:
   Open `http://127.0.0.1:5000` in your browser.

## 🏗️ Architecture

- **Model**: Custom blockchain implementation in `model/`.
  - `block.py`: SHA-256 hashing and PoW mining logic.
  - `blockchain.py`: Chain management and transaction handling.
  - `smart_contract.py`: Automated payment release logic.
- **Controller**: Flask API endpoints in `controller/app.py`.
- **View**: Glassmorphism UI in `view/`.

## 🔄 Workflow Demo

1. **Create Shipment**: Initialize trade between an Exporter and Importer.
2. **Update Status**: Carrier updates shipment location (e.g., In Transit, Customs).
3. **Smart Contract Automation**: Once status is set to **Delivered**, the Smart Contract automatically triggers a "Payment Released" transaction on the blockchain.
4. **Transparency**: View the full immutable audit trail in the Blockchain Ledger and Live Tracking sections.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Blockchain**: SHA-256, Proof-of-Work
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript (Fetch API)
- **Icons**: Phosphor Icons
- **Fonts**: Outfit (Google Fonts)
