from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional
from datetime import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=100.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500, default=None)
    is_verified: bool = False

    @model_validator(mode="after")
    def VerifyAlienContact(self) -> "AlienContact":
        errors = []
        if self.contact_id[:2] != "AC":
            errors.append("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            errors.append("Physical contact requires verification")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            errors.append("Telepathic contact requires at least 3 "
                          "witnesses")
        if errors:
            raise ValueError("\n".join(errors))
        return self


def describeContact(alienContact: AlienContact):
    print("========================================")
    print(f"ID: {alienContact.contact_id}")
    print(f"Type: {alienContact.contact_type.value}")
    print(f"Location: {alienContact.location}")
    print(f"Signal: {alienContact.signal_strength}/10")
    print(f"Duration: {alienContact.duration_minutes} minutes")
    print(f"Witnesses: {alienContact.witness_count}")
    if alienContact.message_received:
        print(f"Message: '{alienContact.message_received}'")
    if alienContact.is_verified:
        print("This contact was verified by credible sources")
    print()
    print("========================================")


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    alienContact = AlienContact(contact_id="AC-2024-001",
                                timestamp=datetime.now(),
                                location="Area 51, Nevada",
                                contact_type=ContactType.RADIO,
                                signal_strength=8.5, duration_minutes=45,
                                witness_count=5,
                                message_received="Greetings from Zeta Reticuli"
                                )
    describeContact(alienContact)
    try:
        alienContact = AlienContact(contact_id="AD-2024-001",
                                    timestamp=datetime.now(),
                                    location="Area 51, Nevada",
                                    contact_type=ContactType.TELEPATHIC,
                                    signal_strength=8.5, duration_minutes=45,
                                    witness_count=2,
                                    message_received="Greetings from Zeta "
                                    "Reticuli"
                                    )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            message = error['msg']
            print(message.replace("Value error, ", ""))
