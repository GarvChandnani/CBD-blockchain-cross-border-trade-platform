from flask import Flask, request, jsonify, render_template
import sys
import os

# Add the root directory to path so we can import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.blockchain import Blockchain
from model.transaction import Transaction
from model.smart_contract import SmartContract

app = Flask(__name__, 
            template_folder='../view/templates', 
            static_folder='../view/static')

# Initialize Blockchain
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_shipment', methods=['POST'])
def create_shipment():
    data = request.json
    try:
        new_tx = Transaction(
            shipment_id=data['shipment_id'],
            exporter=data['exporter'],
            importer=data['importer'],
            carrier=data['carrier'],
            amount=data['amount'],
            status="Created"
        )
        blockchain.add_transaction(new_tx)
        return jsonify({"message": "Shipment created and added to blockchain.", "status": "success"}), 201
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 400

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    shipment_id = data['shipment_id']
    new_status = data['status']
    
    # Get latest state to maintain data
    latest = blockchain.get_latest_shipment_state(shipment_id)
    if not latest:
        return jsonify({"message": "Shipment not found", "status": "error"}), 404
    
    # Create new transaction with updated status
    update_tx = Transaction(
        shipment_id=shipment_id,
        exporter=latest['exporter'] if isinstance(latest, dict) else latest.exporter,
        importer=latest['importer'] if isinstance(latest, dict) else latest.importer,
        carrier=latest['carrier'] if isinstance(latest, dict) else latest.carrier,
        amount=latest['amount'] if isinstance(latest, dict) else latest.amount,
        status=new_status,
        timestamp=None
    )
    
    blockchain.add_transaction(update_tx)
    
    # Check Smart Contract if status is Delivered
    contract_triggered = False
    contract_msg = ""
    if new_status == "Delivered":
        triggered, msg = SmartContract.validate_and_execute(blockchain, shipment_id)
        if triggered:
            contract_triggered = True
            contract_msg = msg
            # Add the payment release transaction
            # Note: In real logic, validate_and_execute might return the transaction object
            latest_after_delivery = blockchain.get_latest_shipment_state(shipment_id)
            payment_tx = Transaction(
                shipment_id=shipment_id,
                exporter=latest_after_delivery['exporter'] if isinstance(latest_after_delivery, dict) else latest_after_delivery.exporter,
                importer=latest_after_delivery['importer'] if isinstance(latest_after_delivery, dict) else latest_after_delivery.importer,
                carrier=latest_after_delivery['carrier'] if isinstance(latest_after_delivery, dict) else latest_after_delivery.carrier,
                amount=latest_after_delivery['amount'] if isinstance(latest_after_delivery, dict) else latest_after_delivery.amount,
                status="Delivered",
                timestamp=None
            )
            payment_tx.payment_released = True
            blockchain.add_transaction(payment_tx)

    return jsonify({
        "message": f"Status updated to {new_status}.",
        "contract_executed": contract_triggered,
        "contract_message": contract_msg,
        "status": "success"
    }), 200

@app.route('/track_shipment/<shipment_id>', methods=['GET'])
def track_shipment(shipment_id):
    history = blockchain.get_shipment_history(shipment_id)
    # Convert history items to dicts if they aren't already
    clean_history = [h if isinstance(h, dict) else h.to_dict() for h in history]
    return jsonify({"history": clean_history, "status": "success"}), 200

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.to_dict())
    return jsonify({
        "length": len(chain_data),
        "chain": chain_data,
        "is_valid": blockchain.is_chain_valid()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
