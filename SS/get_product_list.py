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

from datetime import datetime

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


def add_stock(productid):
    spirits = session.query(Spirits).filter(Spirits.product_id == productid).first()
    stock = Stock(spirit=spirits)
    return stock


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


def get_all_spirits():
    """Get all Spirits' product ids and product names

    Returns:
        [list]: [list of tuples of all product ids and product names]
    """

    all_spirits = session.query(Spirits.product_id, Spirits.product_name).all()

    # product_ids = [value for value, in all_spirits]

    return all_spirits


def get_all_spirits_and_stock():
    all_spirit_stocks = session.query(Spirits).join(Stock, Spirits.stock).all()

    # empty list
    temp_list = []

    for row in all_spirit_stocks:
        tup1 = (row.product_id, row.stock.stock_level)
        temp_list.append(tup1)

    return temp_list


def update_stock(stockinfo):
    """Updates stock information from a filtered list of product ids

    Args:
        stockinfo ([type]): [description]
    """
    # get list of product ids from stockinfo list of dictionaries
    res = [sub["product_id"] for sub in stockinfo]

    # filtered stocks
    spirit_stocks = (
        session.query(Stock)
        .join(Spirits, Stock.spirit)
        .filter(Spirits.product_id.in_(res))
        .all()
    )

    # update filtered stocks with information from stockinfo
    for stock_filtered in spirit_stocks:

        spiritid = stock_filtered.spirit_id
        productid = (
            session.query(Spirits).filter(Spirits.id == spiritid).one().product_id
        )
        # productid = stock_filtered.product_id
        res = [sub for sub in stockinfo if sub["product_id"] == productid]

        stock_filtered.in_stock = res[0]["in_stock"]
        stock_filtered.city = res[0]["city"]
        stock_filtered.store_address = res[0]["store_address"]
        stock_filtered.store_phone_number = res[0]["store_phone_number"]
        stock_filtered.store_id = res[0]["store_id"]
        stock_filtered.stock_level = res[0]["stock_level"]
        stock_filtered.last_updated = get_date_time()


def get_all_spirits_by_user(discord_ids):
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


def get_date_time():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


# # testing module
# specific_spirit = session.query(Spirits).filter(Spirits.product_id == 203517).all()
# all_spirits = session.query(Spirits).all()

# print("\n### All spirits:")
# for spirit in specific_spirit:
#     print(f"{spirit.product_id} was released on {spirit.product_name}")
# print("")


def try_commmit():
    try:
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()


def main_loop():
    try:
        # user1 = User(discord_id=135951952814145537, user_name="bRIKO")
        # user2 = User(discord_id=748731267381592106, user_name="beardedeng")

        # user_to_spirit(discord_ids="135951952814145537", product_ids=203517)
        # user_to_spirit(discord_ids="135951952814145537", product_ids=99510)
        # user_to_spirit(discord_ids="135951952814145537", product_ids=60321)

        # get_all_spirits(discord_ids="135951952814145537")

        # session.add(add_spirit("Talisker 15-Year-Old Single Malt Scotch Whisky", 13506))

        # get_all_spirits()

        # elems_list = [
        #     {
        #         "city": "Mississauga",
        #         "in_stock": "Yes",
        #         "product_id": 203517,
        #         "product_name": "Glenfiddich 14 Year ...el Reserve",
        #         "stock_level": "61",
        #         "store_address": "25 Hillcrest Avenue",
        #         "store_id": "715841812",
        #         "store_phone_number": "(905) 279-6837",
        #     },
        #     {
        #         "city": "Richmond hill",
        #         "in_stock": "Yes",
        #         "product_id": 56294,
        #         "product_name": "Four Roses Small Batch Bourbon",
        #         "stock_level": "42",
        #         "store_address": "12300 Yonge Street",
        #         "store_id": "715841851",
        #         "store_phone_number": "(905) 773-5275",
        #     },
        # ]

        # update_stock(elems_list)

        get_all_spirits_and_stock()

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