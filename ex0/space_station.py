from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(max_length=200, default=None)


def describeStation(spaceStation: SpaceStation):
    print("========================================")
    print(f"ID: {spaceStation.station_id}")
    print(f"Name: {spaceStation.name}")
    print(f"Crew: {spaceStation.crew_size} people")
    print(f"Power: {spaceStation.power_level}%")
    print(f"Oxygen: {spaceStation.oxygen_level}%")
    if spaceStation.is_operational:
        print("Status: Operational")
    else:
        print("Status: Non-operational")
    if spaceStation.notes:
        print(f"Notes: {spaceStation.notes}")
    print()
    print("========================================")


if __name__ == "__main__":
    print("Space Station Data Validation")
    spaceStation = SpaceStation(station_id="ISS001",
                                name="International Space Station",
                                crew_size=6, power_level=85.5,
                                oxygen_level=92.3,
                                last_maintenance=datetime.now())
    describeStation(spaceStation)
    try:
        spaceStation = SpaceStation(station_id="ISS001",
                                    name="International Space Station",
                                    crew_size=25, power_level=85.5,
                                    oxygen_level=92.3,
                                    last_maintenance=datetime.now())
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            print(f"{field}: {message}")
