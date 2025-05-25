from fastapi import HTTPException

from sqlalchemy.sql import and_, or_
from sqlalchemy import select, delete, func, update
from src.infra.database.sql import Session

from src.ports.public import IUBaseRepoPort


class BaseRepo(IUBaseRepoPort):
    def __init__(self):
        self.session = Session
        self.model = None
        self.public = None

    def find(self, **kwargs):
        with self.session() as session:
            response = session.execute(
                select(self.model).filter_by(**kwargs)
            ).scalar()
            if response:
                return self.public.model_validate(response)
            return None

    def find_all(
        self,
        page: int = None,
        limit: int = None,
        period: dict = None,
        **filters,
    ):  # noqa
        with self.session() as session:
            stmt = select(self.model)
            conditions = []

            # Verifica se email e document estão nos filtros para aplicar OR
            email_value = filters.get('email')
            document_value = filters.get('document')

            barcode = filters.get('barcode')
            name = filters.get('name')

            if email_value and document_value:
                # Se ambos email e document estão presentes, usa OR
                email_condition = getattr(self.model, 'email').ilike(
                    f'%{email_value}%'
                )
                document_condition = (
                    getattr(self.model, 'document') == document_value
                )
                conditions.append(or_(email_condition, document_condition))

                # Remove email e document dos filters para não processar novamente
                remaining_filters = {
                    k: v
                    for k, v in filters.items()
                    if k not in ['email', 'document']
                }
            elif barcode and name:
                duplicate_check_stmt = select(self.model).filter(
                    or_(
                        getattr(self.model, 'barcode') == barcode,
                        getattr(self.model, 'name').ilike(f'{name}'),
                    )
                )

                duplicate_result = (
                    session.execute(duplicate_check_stmt).scalars().all()
                )
                if duplicate_result:
                    raise HTTPException(
                        status_code=409,
                        detail='Another item with the same barcode or name already exists',
                    )
            elif barcode:
                duplicate_check_stmt = select(self.model).filter(
                    or_(getattr(self.model, 'barcode') == barcode)
                )

                duplicate_result = (
                    session.execute(duplicate_check_stmt).scalars().all()
                )
                if duplicate_result:
                    raise HTTPException(
                        status_code=409,
                        detail='Another item with the same barcode or name already exists',
                    )

            remaining_filters = filters

            # Aplica os demais filtros baseados nos parâmetros passados
            for key, value in remaining_filters.items():
                if value is None or not hasattr(self.model, key):
                    continue
                if key == 'name':
                    conditions.append(
                        getattr(self.model, key).ilike(f'%{value}%')
                    )
                elif key == 'email':
                    conditions.append(
                        getattr(self.model, key).ilike(f'%{value}%')
                    )
                elif key == 'document':
                    conditions.append(getattr(self.model, key) == value)
                else:
                    conditions.append(getattr(self.model, key) == value)

            # Aplica filtros de período (caso passado)
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

            # Aplica as condições de filtro
            if conditions:
                stmt = stmt.where(and_(*conditions))

            # Total de registros (para saber quantos itens existem no banco)
            total_stmt = select(func.count()).select_from(self.model)
            if conditions:
                total_stmt = total_stmt.where(and_(*conditions))
            total_count = session.execute(
                total_stmt
            ).scalar()  # Conta o número total de registros

            # Adiciona paginação
            if page is not None and limit is not None:
                offset = (page - 1) * limit
                stmt = stmt.offset(offset).limit(limit)

            results = [
                self.public.model_validate(x)
                for x in session.execute(stmt).scalars().all()
            ]

            return {
                'total': total_count,
                'page': page,
                'limit': limit,
                'results': results,
            }

    def update(self, id: int, data):
        already = self.find(id=id)
        if not already:
            raise HTTPException(
                status_code=409, detail='email or document already exists'
            )

        # filtranto apenas campos que não são nulos
        data = {k: v for k, v in data.dict().items() if v is not None}

        # se não tiver email ou document, não precisa fazer a verificação
        if 'email' in data or 'document' in data:
            cop = data.copy()

            # removendo campos não unique para verificar se já existe
            for key in data:
                if key in ['email', 'document']:
                    cop.pop(key)

            already = self.find_all(**data)
            results = already.get('results')

            # caso tenha apenas um resultado, verifica se é o mesmo id e retorna
            # caso contrário, já é um erro
            # caso tenha mais de um resultado, já é um erro
            if len(results) == 1 and results[0].id != id or len(results) > 1:
                raise HTTPException(
                    status_code=409, detail='email or document already exists'
                )

        with self.session() as session:
            session.execute(
                update(self.model).values(**data).where(self.model.id == id)
            )
            session.commit()
        return self.find(id=id)

    def delete(self, **kwargs):
        already = self.find(**kwargs)

        if not already:
            raise Exception('user not found')

        with self.session() as session:
            try:
                session.execute(delete(self.model).filter_by(**kwargs))
                session.commit()
                return already
            except Exception as e:
                print(e)
                return False
