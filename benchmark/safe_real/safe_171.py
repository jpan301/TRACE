# source: RedashSafe / redash/utils/query_order.py
# function: sort_query

def sort_query(query, *args, **kwargs):
    """
    Applies an sql ORDER BY for given query. This function can be easily used
    with user-defined sorting.
    The examples use the following model definition:
    ::
        import sqlalchemy as sa
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy_utils import sort_query
        engine = create_engine(
            'sqlite:///'
        )
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()
        class Category(Base):
            __tablename__ = 'category'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
        class Article(Base):
            __tablename__ = 'article'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            category_id = sa.Column(sa.Integer, sa.ForeignKey(Category.id))
            category = sa.orm.relationship(
                Category, primaryjoin=category_id == Category.id
            )
    1. Applying simple ascending sort
    ::
        query = session.query(Article)
        query = sort_query(query, 'name')
    2. Applying descending sort
    ::
        query = sort_query(query, '-name')
    3. Applying sort to custom calculated label
    ::
        query = session.query(
            Category, sa.func.count(Article.id).label('articles')
        )
        query = sort_query(query, 'articles')
    4. Applying sort to joined table column
    ::
        query = session.query(Article).join(Article.category)
        query = sort_query(query, 'category-name')
    :param query:
        query to be modified
    :param sort:
        string that defines the label or column to sort the query by
    :param silent:
        Whether or not to raise exceptions if unknown sort column
        is passed. By default this is `True` indicating that no errors should
        be raised for unknown columns.
    """
    return QuerySorter(**kwargs)(query, *args)