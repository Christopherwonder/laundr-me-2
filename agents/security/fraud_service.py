from .utils.logging import log_audit


class FraudService:
    def get_risk_score(self, transaction_details: dict) -> dict:
        """
        Calculates a risk score for a given transaction.

        Args:
            transaction_details: A dictionary containing details of the transaction.
                                 Example: {'amount': 100.00, 'user_id': 'user123'}

        Returns:
            A dictionary containing the risk score.
        """
        log_audit(f"Calculating risk score for transaction: {transaction_details}")

        # Mock implementation: simple rule-based logic
        if transaction_details.get("amount", 0) > 1000:
            risk_score = 0.8
        else:
            risk_score = 0.1

        log_audit(f"Risk score calculated: {risk_score}")
        return {"risk_score": risk_score}
