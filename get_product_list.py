from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    or_,
    and_,
    not_,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "postgresql://pythonTest:postgres@localhost:5432/lcbo_stock", echo=False
)  # alternatives 'sqlite:///:memory:' or sqlite:///pytest.db'


Base = declarative_base()

association_table_spirit_user = Table(
    "association_spirit_user",
    Base.metadata,
    Column("spirit_id", Integer, ForeignKey("spirit.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(50), unique=True)
    user_name = Column(String(50))
    spirits = relationship(
        "Spirits", secondary=association_table_spirit_user, back_populates="users"
    )


class Spirits(Base):
    __tablename__ = "spirit"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(250))
    product_id = Column(Integer, unique=True)
    stock = relationship("Stock", uselist=False, back_populates="spirit")
    users = relationship(
        "User", secondary=association_table_spirit_user, back_populates="spirits"
    )


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    in_stock = Column(String(50))
    city = Column(String(50))
    store_address = Column(String(50))
    store_phone_number = Column(String(50))
    store_id = Column(Integer)
    stock_level = Column(Integer)
    last_updated = Column(String(50))

    spirit_id = Column(Integer, ForeignKey("spirit.id"))
    spirit = relationship("Spirits", back_populates="stock")


Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


def add_spirit(name, productid):
    return Spirits(product_name=name, product_id=productid)


def add_user(user_id, user_name=None):
    return User(discord_id=user_id, user_name=user_name)


def user_to_spirit(discord_ids, product_ids):
    # check if product_id in tracked entries, if not, tells user to add it
    if session.query(Spirits).filter(Spirits.product_id == product_ids).count() == 0:
        new_spirit = add_spirit(name="", productid=product_ids)
        session.add(new_spirit)
        print(f"Added Spirit: {product_ids}!")

    # check's if user is in User table, if not, adds him
    if session.query(User).filter(User.discord_id == discord_ids).count() == 0:
        new_user = add_user(user_id=discord_ids)
        session.add(new_user)
        print(f"Added User: {discord_ids}!")

    # query for spirit
    spirit_to_add = (
        session.query(Spirits).filter(Spirits.product_id == product_ids).first()
    )

    # query for user
    user_to_add = session.query(User).filter(User.discord_id == discord_ids).first()

    # add user to spirit if user not already associated with spirit
    if user_to_add not in spirit_to_add.users:
        spirit_to_add.users += [user_to_add]
        print(f"Product ID: {product_ids} added to User: {discord_ids}!")
    else:
        print(f"User is already tracking product.")
    spirit_to_add.users


def get_all_spirits(discord_ids):
    all_spirits = (
        session.query(Spirits)
        .join(User, Spirits.users)
        .filter(User.discord_id == discord_ids)
        .all()
    )

    print(f"### {discord_ids} spirits:")
    for spirit in all_spirits:
        print(f"{spirit.product_name}")
    print("")


def add_spirits_already_defined():
    # spirit1 = add_spirit("Glenfiddich 14 Year Old Bourbon Barrel Reserve", 203517)
    # spirit2 = add_spirit("Four Roses Small Batch Bourbon", 56294)
    # spirit3 = add_spirit("Hibiki Harmony", 61344)
    # spirit4 = add_spirit("Eagle Rare 10 Year Old Kentucky Straight Bourbon", 65616)
    # spirit5 = add_spirit("Caribou Crossing Single Barrel Canadian Whisky", 99510)
    # spirit6 = add_spirit("Blanton's Original Bourbon", 56284)
    # spirit7 = add_spirit(
    #     "Blanton's Single Barrel Special Reserve Kentucky Straight Bourbon", 64174
    # )
    # spirit8 = add_spirit("Clynelish 14 Year Old Single Malt Scotch Whisky", 105003)
    # spirit9 = add_spirit("Michter's US-1 Single Barrel Rye Whiskey", 59906)
    # spirit10 = add_spirit("W. L. Weller 12-Year-Old Kentucky Straight Bourbon", 56807)
    # spirit11 = add_spirit("W.L. Weller Special Reserve Bourbon", 59181)
    # spirit12 = add_spirit("Alberta Premium Cask Strength Rye (2019)", 299017)
    # spirit13 = add_spirit("Elijah Craig Barrel Proof", 115515)
    # spirit14 = add_spirit("Redbreast 12 Year Old Cask Strength Irish Whiskey", 60321)

    # session.add_all(
    #     [
    #         spirit1,
    #         spirit2,
    #         spirit3,
    #         spirit4,
    #         spirit5,
    #         spirit6,
    #         spirit7,
    #         spirit8,
    #         spirit9,
    #         spirit10,
    #         spirit11,
    #         spirit12,
    #         spirit13,
    #         user1,
    #         user2,
    #     ]
    # )

    pass


# # testing module
# specific_spirit = session.query(Spirits).filter(Spirits.product_id == 203517).all()
# all_spirits = session.query(Spirits).all()

# print("\n### All spirits:")
# for spirit in specific_spirit:
#     print(f"{spirit.product_id} was released on {spirit.product_name}")
# print("")


def main_loop():
    try:
        # user1 = User(discord_id=135951952814145537, user_name="bRIKO")
        # user2 = User(discord_id=748731267381592106, user_name="beardedeng")

        # user_to_spirit(discord_ids="135951952814145537", product_ids=203517)
        # user_to_spirit(discord_ids="135951952814145537", product_ids=99510)
        # user_to_spirit(discord_ids="135951952814145537", product_ids=60321)

        # get_all_spirits(discord_ids="135951952814145537")

        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main_loop()


# def print_out():

#     # Get data in order
#     students = session.query(Student).order_by(Student.name)

#     for student in students:
#         print(student.name, student.age, student.grade)

#     students = session.query(Student).filter(
#         or_(Student.name == "Ralph", Student.name == "Sam")
#     )


# def update_data():
#     # Update data

#     student = session.query(Student).filter(Student.name == "Sam").first()
#     student.name = "Sloth"
#     session.commit()


# def delete_data():
#     # Delete Data
#     student = session.query(Student).filter(Student.name == "Sloth").first()
#     session.delete(student)
#     session.commit()