<<<<<<< HEAD
from pydantic import BaseModel


class DetectionResult(BaseModel):
    format: str  # JSON, Syslog, CEF, LEEF, Key=Value, CSV, XML, Plaintext
    confidence: float
    reason: str
=======
from pydantic import BaseModel


class DetectionResult(BaseModel):
    format: str  # JSON, Syslog, CEF, LEEF, Key=Value, CSV, XML, Plaintext
    confidence: float
    reason: str
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
