class FilterManager:
    def prepare_filter(self, filters=None, sort_field='_id', sort_order='desc'):
        query = {}

        # Обробка фільтрів
        if filters:
            for key, value in filters.items():
                if ':' not in value:  # Check if the value contains a colon
                    continue  # Skip invalid entries or handle them as needed

                operator, filter_value = value.split(':', 1)

                if operator == 'ne':  # Не дорівнює
                    query[key] = {"$ne": filter_value}
                elif operator == 'gte':  # Більше або дорівнює
                    query[key] = {"$gte": filter_value}
                elif operator == 'lte':  # Менше або дорівнює
                    query[key] = {"$lte": filter_value}
                elif operator == 'in':  # У списку
                    query[key] = {"$in": filter_value.split(',')}  # Розділення по комі
                elif operator == 'eq':  # Дорівнює
                    query[key] = filter_value

        # Формуємо об'єкт для сортування
        sort_order_value = -1 if sort_order == 'desc' else 1
        sort_criteria = [(sort_field, sort_order_value)]

        return query, sort_criteria

    def get_filter_query(self, filters=None, sort_field='_id', sort_order='desc'):
        return self.prepare_filter(filters, sort_field, sort_order)
