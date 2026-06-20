from dataclasses import dataclass, field


@dataclass
class Entity:
    type: str
    text: str
    start: int | None = None
    end: int | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "metadata": self.metadata,
        }