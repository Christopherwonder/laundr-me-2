from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json

from agents.security.fraud_service import FraudService
from agents.security.velocity_checker import VelocityChecker
from app.crud import get_profile_by_id

class ComplianceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.fraud_service = FraudService()
        self.velocity_checker = VelocityChecker()

    async def dispatch(self, request: Request, call_next):
        # We will assume that any request that is not a GET request is a financial transaction
        # for the purpose of this task.
        if request.method != "GET":
            print(f"Intercepted financial transaction: {request.method} {request.url.path}")

            path_parts = request.url.path.split('/')
            user_id = None
            if len(path_parts) > 4 and path_parts[3] == "profiles":
                try:
                    user_id = int(path_parts[4])
                except (ValueError, IndexError):
                    # Not a path with a user_id, so we can't do compliance checks.
                    # We will allow it to proceed, but in a real-world scenario we might want to deny it.
                    pass

            if user_id:
                # 1. Check KYC status
                try:
                    profile = await get_profile_by_id(user_id)
                    if profile.kyc_status != "verified":
                        return JSONResponse(status_code=403, content={"detail": "KYC not verified"})
                except HTTPException as e:
                    if e.status_code == 404:
                        # Profile not found, let it proceed to be handled by the endpoint
                        pass
                    else:
                        raise

                # 2. Perform risk analysis
                # We need to get the transaction details from the request body.
                body = await request.body()
                transaction_details = json.loads(body) if body else {}

                risk_score_result = self.fraud_service.get_risk_score(transaction_details)
                if risk_score_result.get("risk_score", 0) > 0.75:
                    return JSONResponse(status_code=403, content={"detail": "Transaction risk too high"})

                velocity_check_result = self.velocity_checker.check_transaction_velocity(str(user_id), transaction_details)
                if velocity_check_result.get("velocity_exceeded"):
                    return JSONResponse(status_code=403, content={"detail": "Transaction velocity exceeded"})

        response = await call_next(request)
        return response
