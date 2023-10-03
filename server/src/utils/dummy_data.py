from sqlalchemy import text
from fastapi_async_sqlalchemy import db

from src.models import Venue


async def create_dummy_data():
    venue1 = Venue(
        name="Rusty Bar",
        description="In rust we trust! Only BROgrammers allowed!",
        address="Rust Street 1",
        city="San Francisco"
    )
    venue2 = Venue(
        name="Bash Bar",
        description="Cool venue for cool people, YOLO!",
        address="Bash Street 1",
        city="San Francisco"
    )
    venue3 = Venue(
        name="Python Bar",
        description="Cool venue for cool people, Python is the best! ",
        address="Python Street 1",
        city="San Francisco"
    )
    venue4 = Venue(
        name="Java Bar",
        description="A cup of Java for everyone! We have coffee too :D",
        address="Java Street 1",
        city="San Francisco"
    )
    venue5 = Venue(
        name="C++ Bar",
        description="Oops, buffer overflow! Just kidding, we are safe :D",
        address="Compiler Street 1",
        city="San Francisco"
    )
    venue6 = Venue(
        name="JavaScript Bar",
        description="Building another framework. Come back tomorrow for a new one!",
        address="Node Street 1",
        city="San Francisco"
    )
    venue7 = Venue(
        name="PHP Bar",
        description="We are dead but still alive!",
        address="PHP Street 1",
        city="San Francisco"
    )
    venue8 = Venue(
        name="Ruby Bar",
        description="Found random gems in the street? Come here!",
        address="Ruby Street 1",
        city="San Francisco"
    )
    venue9 = Venue(
        name="Go Bar",
        description="We are fast and concurrent! Gofers are welcome!",
        address="Go Street 1",
        city="San Francisco"
    )
    venue10 = Venue(
        name="Assembly Bar",
        description="We are low level, but we are not low quality!",
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

