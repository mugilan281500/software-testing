from sqlalchemy.orm import Session
import datetime
from app.models import ApiTarget, TestCase, Finding

class ApiChangeDetectorService:
    @staticmethod
    def process_openapi_import(db: Session, title: str, version: str, endpoints: list) -> dict:
        existing_targets = db.query(ApiTarget).all()
        existing_map = {t.endpoint: t for t in existing_targets}

        new_endpoints = []
        modified_endpoints = []
        removed_endpoints = []
        affected_test_cases = []

        imported_paths = set()

        for ep in endpoints:
            path = ep.get("endpoint") or ep.get("path")
            method = ep.get("method", "GET").upper()
            description = ep.get("description", "")
            imported_paths.add(path)

            if path not in existing_map:
                # NEW Endpoint
                target = ApiTarget(
                    name=ep.get("name") or f"API {path}",
                    endpoint=path,
                    method=method,
                    description=description,
                    version=version,
                    risk_score=15.0,
                    risk_level="LOW",
                    security_score=100.0,
                    regression_priority="NORMAL"
                )
                db.add(target)
                new_endpoints.append({"endpoint": path, "method": method, "type": "NEW_ENDPOINT"})
            else:
                curr = existing_map[path]
                changes = []
                if curr.method != method:
                    changes.append(f"HTTP Method changed from {curr.method} to {method}")
                    curr.method = method
                if curr.version != version:
                    changes.append(f"Version bumped to {version}")
                    curr.version = version

                if changes:
                    modified_endpoints.append({"endpoint": path, "changes": changes})

                # Check if this API has past open security findings -> Auto assign CRITICAL regression priority
                past_findings = db.query(Finding).filter(
                    Finding.api_endpoint == path,
                    Finding.status.in_(["OPEN", "INVESTIGATING"])
                ).count()

                if past_findings > 0:
                    curr.regression_priority = "CRITICAL"
                    # Mark related test cases as CRITICAL priority
                    tcs = db.query(TestCase).filter(TestCase.endpoint == path).all()
                    for tc in tcs:
                        tc.status = "NEEDS_REGRESSION"
                        affected_test_cases.append(tc.test_id)

        # Check for removed endpoints
        for path, curr in existing_map.items():
            if path not in imported_paths:
                removed_endpoints.append({"endpoint": path, "method": curr.method, "type": "REMOVED_ENDPOINT"})

        db.commit()

        return {
            "title": title,
            "version": version,
            "total_imported": len(endpoints),
            "new_endpoints_count": len(new_endpoints),
            "modified_endpoints_count": len(modified_endpoints),
            "removed_endpoints_count": len(removed_endpoints),
            "new_endpoints": new_endpoints,
            "modified_endpoints": modified_endpoints,
            "removed_endpoints": removed_endpoints,
            "affected_test_cases": list(set(affected_test_cases))
        }
