import sys
import os
import pytest

# Add the 'agents' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.security import FraudService, VelocityChecker, AnomalyDetector

def test_fraud_service():
    service = FraudService()
    result = service.get_risk_score({'amount': 500})
    assert 'risk_score' in result
    assert isinstance(result['risk_score'], float)

def test_velocity_checker():
    service = VelocityChecker()
    result = service.check_transaction_velocity('user123', {})
    assert 'velocity_exceeded' in result
    assert isinstance(result['velocity_exceeded'], bool)

def test_anomaly_detector():
    service = AnomalyDetector()
    result = service.detect_anomalies(['login', 'logout'])
    assert 'anomaly_detected' in result
    assert isinstance(result['anomaly_detected'], bool)
