# forms.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class PersonForm:
    name: str
    generation: int
    parent_id: Optional[int]
