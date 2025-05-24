from sqlalchemy.sql import and_
from sqlalchemy import select, delete
from src.infra.database.sql import Session

from src.ports.public import IUBaseRepoPort


class BaseRepo(IUBaseRepoPort):
    def __init__(self):
        self.session = Session
        self.model = None

    def find(self, **kwargs):
        with self.session() as session:
            return session.execute(
                select(self.model).filter_by(**kwargs)
            ).scalar()

    def find_all(
        self,
        page: int = None,
        limit: int = None,
        period: dict = None,
        **filters,
        ): #noqa: F821
        with self.session() as session:
            stmt = select(self.model)

            conditions = []

            for key, value in filters.items():
                if value is None or not hasattr(self.model, key):
                    continue

                if key in {'name', 'email'}:
                    conditions.append(
                        getattr(self.model, key).ilike(f'%{value}%')
                    )
                else:
                    conditions.append(getattr(self.model, key) == value)

            if period and isinstance(period, dict):
                start = period.get('start')
                end = period.get('end')
                if hasattr(self.model, 'created_at'):
                    if start:
                        conditions.append(
                            getattr(self.model, 'created_at') >= start
                        )
                    if end:
                        conditions.append(
                            getattr(self.model, 'created_at') <= end
                        )

            if conditions:
                stmt = stmt.where(and_(*conditions))

            if page is not None and limit is not None:
                offset = (page - 1) * limit
                stmt = stmt.offset(offset).limit(limit)

            return session.execute(stmt).scalars().all()

    def delete(self, **kwargs):
        already = self.find(**kwargs)

        if not already:
            raise Exception('user not found')

        with self.session() as session:
            try:
                session.execute(delete(self.model).filter_by(**kwargs))
                session.commit()
                return True
            except Exception as e:
                print(e)
                return False
