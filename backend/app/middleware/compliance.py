import json

from app.crud import get_profile_by_laundr_id
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from agents.security.fraud_service import FraudService
from agents.security.velocity_checker import VelocityChecker

FINANCIAL_PATHS = [
    "/api/v1/loads/send-load",
    "/api/v1/loads/request-load",
    "/api/v1/loads/swap-funds",
]


class ComplianceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.fraud_service = FraudService()
        self.velocity_checker = VelocityChecker()

    async def dispatch(self, request: Request, call_next):
        if request.url.path in FINANCIAL_PATHS:
            body = await request.body()
            transaction_details = json.loads(body) if body else {}

            sender_id = transaction_details.get("sender_id") or transaction_details.get(
                "source_id"
            )

            if not sender_id:
                # If we can't identify the user, we can't perform checks.
                # In a real-world scenario, we might want to block this.
                # For now, we will allow it to proceed and let the endpoint handle it.
                return await call_next(request)

            # 1. Check KYC status
            profile = await get_profile_by_laundr_id(sender_id)
            if not profile:
                # Let the endpoint handle the "profile not found" error
                return await call_next(request)

            if profile.kyc_status != "verified":
                return JSONResponse(
                    status_code=403, content={"detail": "KYC not verified"}
                )

            # 2. Perform risk analysis
            risk_score_result = self.fraud_service.get_risk_score(transaction_details)
            if risk_score_result.get("risk_score", 0) > 0.75:
                return JSONResponse(
                    status_code=403, content={"detail": "Transaction risk too high"}
                )

            velocity_check_result = self.velocity_checker.check_transaction_velocity(
                profile.laundr_id, transaction_details
            )
            if velocity_check_result.get("velocity_exceeded"):
                return JSONResponse(
                    status_code=403, content={"detail": "Transaction velocity exceeded"}
                )

        response = await call_next(request)
        return response
