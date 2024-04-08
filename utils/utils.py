def validate_filters(filters):
    valid_filters = {}
    if 'year' in filters:
        try:
            valid_filters['year'] = int(filters['year'])
        except ValueError:
            raise ValueError("El filtro de 'year' debe ser un número entero.")
    if 'city' in filters:
        valid_filters['city'] = filters['city']
    if 'state' in filters:
        if filters['state'] not in ['pre_venta', 'en_venta', 'vendido']:
            raise ValueError("El filtro de 'state' es inválido.")
        valid_filters['state'] = filters['state']
    return valid_filters