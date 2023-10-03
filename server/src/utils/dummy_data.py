from sqlalchemy import text
from fastapi_async_sqlalchemy import db

from src.models import Venue


async def create_dummy_data():
    venue1 = Venue(
        name="Rusty Bar",
        description="In rust we trust! Only BROgrammers allowed! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Rust Street 1",
        city="San Francisco"
    )
    venue2 = Venue(
        name="Bash Bar",
        description="Cool venue for cool people, YOLO! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Bash Street 1",
        city="San Francisco"
    )
    venue3 = Venue(
        name="Python Bar",
        description="Cool venue for cool people, Python is the best! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ",
        address="Python Street 1",
        city="San Francisco"
    )
    venue4 = Venue(
        name="Java Bar",
        description="A cup of Java for everyone! We have coffee too :D Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Java Street 1",
        city="San Francisco"
    )
    venue5 = Venue(
        name="C++ Bar",
        description="Oops, buffer overflow! Just kidding, we are safe :D Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Compiler Street 1",
        city="San Francisco"
    )
    venue6 = Venue(
        name="JavaScript Bar",
        description="Building another framework. Come back tomorrow for a new one! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Node Street 1",
        city="San Francisco"
    )
    venue7 = Venue(
        name="PHP Bar",
        description="We are dead but still alive! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="PHP Street 1",
        city="San Francisco"
    )
    venue8 = Venue(
        name="Ruby Bar",
        description="Found random gems in the street? Come here! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Ruby Street 1",
        city="San Francisco"
    )
    venue9 = Venue(
        name="Go Bar",
        description="We are fast and concurrent! Gofers are welcome! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Go Street 1",
        city="San Francisco"
    )
    venue10 = Venue(
        name="Assembly Bar",
        description="We are low level, but we are not low quality! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        address="Assembly Street 1",
        city="San Francisco"
    )

    async with db():
        # Clean up database
        await db.session.execute(text("DELETE FROM venues;"))

        # Add dummy data
        db.session.add_all(
            [venue1, venue2, venue3, venue4, venue5, venue6, venue7, venue8, venue9, venue10]
        )
        await db.session.commit()

