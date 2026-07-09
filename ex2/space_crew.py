from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def verifySpaceMission(self):
        errors = []
        if self.mission_id[0] != "M":
            errors.append("Mission ID must start with 'M'")
        if (Rank.COMMANDER or Rank.CAPTAIN) not in [crewMember.rank
                                                    for crewMember
                                                    in self.crew]:
            errors.append("Mission must have at least one "
                          "Commander or Captain")
        if (self.duration_days > 365 and
            len([crewMember for crewMember in self.crew
                if crewMember.years_experience >= 5]) / len(self.crew) < 0.5):
            errors.append("Long missions must have ")
        if (not all([crewMember.is_active for crewMember in self.crew])):
            errors.append("All crew must be active")
        if errors:
            raise ValueError("\n".join(errors))
        return self


def describeSpaceMission(spaceMission: SpaceMission):
    print("========================================")
    print(f"Mission: {spaceMission.mission_name}")
    print(f"ID: {spaceMission.mission_id}")
    print(f"Destination: {spaceMission.destination}")
    print(f"Duration: {spaceMission.duration_days} days")
    print(f"Budget: ${spaceMission.budget_millions}M")
    print(f"Crew size: {len(spaceMission.crew)}")
    print("Crew members:")
    for member in spaceMission.crew:
        print(f"- {member.name} ({member.rank}) - {member.specialization}")
    print()
    print("========================================")


if __name__ == "__main__":
    try:
        spaceMission = SpaceMission(
            mission_name="Mars Colony Establishment", mission_id="M2024_MARS",
            destination="Mars", duration_days=900, budget_millions=2500.0,
            launch_date=datetime.now(), crew=[
                CrewMember(member_id="123", name="Sarah Connor",
                           rank=Rank.COMMANDER, age=50,
                           specialization="Mission Command",
                           years_experience=10),
                CrewMember(member_id="124", name="John Smith",
                           rank=Rank.LIEUTENANT, age=40,
                           specialization="Navigation", years_experience=7),
                CrewMember(member_id="125", name="Alice Johnson",
                           rank=Rank.OFFICER, age=30,
                           specialization="Engineering", years_experience=4)
            ])
        describeSpaceMission(spaceMission)
        try:
            spaceMission = SpaceMission(
                mission_name="Mars Colony Establishment",
                mission_id="M2024_MARS", destination="Mars", duration_days=900,
                budget_millions=2500.0,
                launch_date=datetime.now(), crew=[
                    CrewMember(member_id="123", name="Sarah Connor",
                               rank=Rank.CADET, age=50,
                               specialization="Mission Command",
                               years_experience=10),
                    CrewMember(member_id="124", name="John Smith",
                               rank=Rank.LIEUTENANT, age=40,
                               specialization="Navigation",
                               years_experience=7),
                    CrewMember(member_id="125", name="Alice Johnson",
                               rank=Rank.OFFICER, age=30,
                               specialization="Engineering",
                               years_experience=4)
                ])
        except ValidationError as e:
            print("Expected validation error:")
            for error in e.errors():
                message = error['msg']
                print(message.replace("Value error, ", ""))
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            print(f"{field}: {message}")
