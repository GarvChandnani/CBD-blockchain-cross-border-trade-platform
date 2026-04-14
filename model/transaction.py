import time

class Transaction:
    def __init__(self, shipment_id, exporter, importer, carrier, amount, status="Registered", timestamp=None):
        self.shipment_id = shipment_id
        self.exporter = exporter
        self.importer = importer
        self.carrier = carrier
        self.amount = amount
        self.status = status
        self.timestamp = timestamp or time.time()
        self.payment_released = False

    def to_dict(self):
        return {
            "shipment_id": self.shipment_id,
            "exporter": self.exporter,
            "importer": self.importer,
            "carrier": self.carrier,
            "amount": self.amount,
            "status": self.status,
            "timestamp": self.timestamp,
            "payment_released": self.payment_released
        }
