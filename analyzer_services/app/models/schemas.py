from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    # Constrain the user-supplied query to mitigate abuse / prompt-injection
    # payloads via excessively large inputs. 1-2000 chars is plenty for a
    # natural-language request targeting Oracle Cloud Readiness.
    query: str = Field(..., min_length=1, max_length=2000)

