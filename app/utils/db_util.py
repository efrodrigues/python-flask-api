from sqlalchemy import func
from sqlalchemy.sql import text


class ModelHelper(object):
    query = None
    model_class = None

    def get_model_class(self):
        return self.model_class


class DynamicFilter(ModelHelper):
    def __init__(self, model_class, filters, query=None, session=None):
        self.query = query
        self.model_class = model_class
        self.filters = filters
        self.session = session

    def get_query(self):
        if not self.query:
            self.query = self.session.query(self.model_class)
        return self.query

    def filter_query(self, query, filters):
        if query is None:
            query = self.get_query()
        model_class = self.get_model_class()

        if filters:
            query_filters = []
            sort_filters = []
            for key in filters.keys():
                value = filters[key]
                if key == "limit":
                    limit = value
                    continue
                if key == "offset":
                    offset = value
                    continue

                column = getattr(model_class, key)
                if "list" in value:
                    build_filter_list(column, value["list"], query_filters)

                if "order_by" in value:
                    order_by = value["order_by"].upper()
                    sort_filters.append(
                        column.asc() if order_by == "ASC" else column.desc()
                    )

        limit_offset = make_limit_offset(offset, limit)
        return_list = (
            self.session.query(model_class)
            .filter(*query_filters)
            .order_by(*sort_filters)
            .slice(limit_offset["offset"], limit_offset["limit"])
            .all()
        )
        total = (
            self.session.query(func.count(model_class.Id))
            .filter(*query_filters)
            .scalar()
        )

        result = {
            "list": return_list,
            "total": total,
            "limit": limit,
            "offset": offset,
        }
        self.session.flush()
        self.session.close()
        return result

    def find_filters(self, query, filters, filter_by_like=True):
        if query is None:
            query = self.get_query()
        model_class = self.get_model_class()

        query_filters = []
        if "filtered_by" in filters:
            for key in filters["filtered_by"]:
                column = (
                    getattr(model_class, key)
                    if "name" != key
                    else getattr(model_class, "id")
                )
                filter = filters["filtered_by"][key]
                if isinstance(filter, list):
                    filter_ids = []
                    for f in filter:
                        if "start" in f["id"]:
                            build_filter_between(
                                column,
                                f["id"]["start"],
                                f["id"]["end"],
                                query_filters,
                            )
                        else:
                            filter_ids.append(f["id"])
                    build_filter_list(column, filter_ids, query_filters)

        if "field_like" in filters and filter_by_like:
            column = getattr(model_class, filters["field_target"])
            query_filters.append(
                column.ilike("%{}%".format(filters["field_like"]))
            )

        if len(query_filters) > 0:
            query = query.filter(*query_filters)

        return_list = (
            self.session.query(model_class).filter(*query_filters).all()
        )
        return return_list


def build_filter_list(column, filter_list, query_filters):
    if len(filter_list) > 1:
        query_filters.append(column.in_(filter_list))
    elif len(filter_list) == 1:
        query_filters.append(column == filter_list[0])


def build_filter_between(column, start, end, query_filters):
    query_filters.append(column.between(start, end))


def dynamic_filtered_search(model_class, filters, session):
    dynamic_search_query = DynamicFilter(
        model_class=model_class, filters=filters, query=None, session=session
    )

    if "limit" not in filters:
        filters["limit"] = 10
    if "offset" not in filters:
        filters["offset"] = 0

    return dynamic_search_query.filter_query(query=None, filters=filters)


def make_limit_offset(start, stop):
    return {"offset": start * stop, "limit": stop * start + stop}


def find_by_id(entity_class, entity_id, session):
    return session.query(entity_class).filter_by(id=entity_id).first()


def find_by_filters(model_class, filters, session, filter_by_like=True):
    dynamic_search_query = DynamicFilter(
        model_class=model_class, filters=filters, query=None, session=session
    )

    return dynamic_search_query.find_filters(
        query=None, filters=filters, filter_by_like=filter_by_like
    )


def find_sql_server_version(connection):
    q = text("SELECT @@VERSION")
    return connection.execute(q).fetchone()
