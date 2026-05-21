"""Sample data for Lab 4 — run: poetry run seed-db"""

import asyncio
from decimal import Decimal

from sqlalchemy import select

from app.core.password import hash_password
from app.db.session import AsyncSessionLocal
from app.models import Category, Order, OrderItem, Post, Product, User, UserProfile

# --- Sample records (referenced in lab documentation) ---
SAMPLE_USERS = [
    {
        "username": "marine",
        "email": "marine@houshou.pirate",
        "password": "ahoy12345",
        "full_name": "Houshou Marine",
    },
    {
        "username": "crew_mate",
        "email": "crew@houshou.pirate",
        "password": "treasure99",
        "full_name": "Pirate Crew Mate",
    },
    {
        "username": "shopper",
        "email": "shopper@example.com",
        "password": "shopper123",
        "full_name": "Treasure Shopper",
    },
]

SAMPLE_PROFILES = [
    {"bio": "Captain of the Houshou Pirates. Ahoy!", "country": "Japan"},
    {"bio": "Treasure hunter in training.", "country": "International"},
    {"bio": "Collects pirate merch and music.", "country": "USA"},
]

SAMPLE_CATEGORIES = [
    {"name": "Merchandise", "description": "Official-style pirate goods"},
    {"name": "Music", "description": "Albums and digital singles"},
    {"name": "Treasure", "description": "Rare collectibles"},
    {"name": "Apparel", "description": "Clothing and accessories"},
]

SAMPLE_PRODUCTS = [
    {
        "name": "Captain's Hat",
        "description": "Classic pirate hat",
        "price": Decimal("29.99"),
        "stock": 50,
        "category_index": 0,
    },
    {
        "name": "Ahoy!! Single (Digital)",
        "description": "First original song",
        "price": Decimal("1.99"),
        "stock": 999,
        "category_index": 1,
    },
    {
        "name": "Treasure Chest Mini",
        "description": "Decorative chest",
        "price": Decimal("49.00"),
        "stock": 20,
        "category_index": 2,
    },
    {
        "name": "Pirate Coat",
        "description": "Captain's coat replica",
        "price": Decimal("89.99"),
        "stock": 15,
        "category_index": 3,
    },
    {
        "name": "Unison (Digital)",
        "description": "Second original single",
        "price": Decimal("1.99"),
        "stock": 500,
        "category_index": 1,
    },
]

SAMPLE_POSTS = [
    {"title": "Set sail!", "content": "Welcome aboard the Houshou Pirates.", "owner_index": 0},
    {"title": "New treasure found", "content": "Check the shop for new goods.", "owner_index": 0},
]


async def seed_database() -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(User).limit(1))
        if existing.scalar_one_or_none() is not None:
            print("Database already seeded — skipping.")
            return

        users: list[User] = []
        for data in SAMPLE_USERS:
            user = User(
                username=data["username"],
                email=data["email"],
                hashed_password=hash_password(data["password"]),
                full_name=data["full_name"],
                is_active=True,
            )
            db.add(user)
            users.append(user)
        await db.flush()

        for user, profile_data in zip(users, SAMPLE_PROFILES, strict=True):
            db.add(UserProfile(user_id=user.id, **profile_data))

        categories: list[Category] = []
        for data in SAMPLE_CATEGORIES:
            category = Category(**data)
            db.add(category)
            categories.append(category)
        await db.flush()

        products: list[Product] = []
        for data in SAMPLE_PRODUCTS:
            product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                stock=data["stock"],
                category_id=categories[data["category_index"]].id,
            )
            db.add(product)
            products.append(product)
        await db.flush()

        for data in SAMPLE_POSTS:
            db.add(
                Post(
                    title=data["title"],
                    content=data["content"],
                    owner_id=users[data["owner_index"]].id,
                )
            )

        order = Order(user_id=users[0].id, status="paid", total_amount=Decimal("31.98"))
        db.add(order)
        await db.flush()

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=products[0].id,
                quantity=1,
                unit_price=products[0].price,
            )
        )
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=products[1].id,
                quantity=1,
                unit_price=products[1].price,
            )
        )

        await db.commit()
        print("Database seeded successfully.")


def run() -> None:
    asyncio.run(seed_database())


if __name__ == "__main__":
    run()
