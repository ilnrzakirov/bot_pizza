import sqlalchemy

from db.db import Product, Groups, Modification
from settings import session_maker
from sqlalchemy import select


async def get_product_by_group_id(group: Groups, session_in=None) -> list[Product]:
    if session_in:
        session = session_in
    else:
        session = session_maker()
    query = sqlalchemy.select(Product).where(Product.group == group.id)
    product_list = []
    products = await session.execute(query)
    for product in products:
        product_list.append(product[0])
    if session_in is None:
        await session.close()
    return product_list


async def get_product_by_iiko_id(iiko_id: str, session_in=None):
    if session_in:
        session = session_in
    else:
        session = session_maker()
    query = sqlalchemy.select(Product).where(Product.product_id == iiko_id)
    product = await session.execute(query)
    instance = product.scalars().first()
    if session_in is None:
        await session.close()
    if not instance:
        return None
    return instance


async def delete_all_products():
    session = session_maker()
    query = sqlalchemy.delete(Product)
    await session.execute(query)
    await session.commit()
    await session.close()


async def delete_product_by_id(id_in):
    session = session_maker()
    query = sqlalchemy.delete(Product).where(Product.product_id == id_in)
    await session.execute(query)
    await session.commit()
    await session.close()


async def delete_all_mod():
    session = session_maker()
    query = sqlalchemy.delete(Modification)
    await session.execute(query)
    await session.commit()
    await session.close()


async def get_mod_by_id(id_in, session_in=None):
    if session_in:
        session = session_in
    else:
        session = session_maker()
    query = sqlalchemy.select(Modification).where(Modification.mod_id == id_in)
    mod = await session.execute(query)
    if session_in is None:
        await session.close()
    return mod.scalar()


async def get_product_by_id(id_in, session_in=None):
    if session_in:
        session = session_in
    else:
        session = session_maker()
    query = sqlalchemy.select(Product).where(Product.product_id == id_in)
    product = await session.execute(query)
    if session_in is None:
        await session.close()
    return product.scalar()
