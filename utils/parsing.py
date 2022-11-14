def parsing_json(file):
    groups = ('id', 'name')
    groups = [{key: value for key, value in x.items() if key in groups} for x in file.get('groups')]
    groups_name = ['Пицца', 'Роллы', 'Суши',
                   'Запеченные роллы Пицца Хаус',
                   'Жаренные роллы Пицца Хаус',
                   'Классические роллы Пицца Хаус',
                   'Сливочные роллы Пицца Хаус',
                   'Фирменные роллы Пицца Хаус',
                   'Паста', 'Десерты', 'Напитки',
                   'Салаты', 'Закуски', 'Комбо']
    groups = [x for x in groups if x.get('name') in groups_name]
    groups_ids = [x.get('id') for x in groups]
    productCategories = ('id', 'name')
    productCategories = [{key: value for key, value in x.items() if key in productCategories} for x in
                         file.get('productCategories')]
    products_dish = []
    products_modifier = []
    dish = (
        'id', 'groupId', 'productCategoryId', 'name', 'sizePrice', 'weight',
        'groupModifiers', 'imageLinks', 'description', 'parentGroup'
    )
    modifier = ('id', 'groupId', 'productCategoryId', 'name', 'sizePrices', 'weight', 'parentGroup')
    products = file.get('products')
    for x in products:
        if x.get('type') == 'Dish':
            if x.get('parentGroup') in groups_ids:
                tmp = {}
                for key, value in x.items():
                    if key in dish:
                        if key == 'sizePrices':
                            tmp[key] = value[0].get('price').get('currentPrice')
                        elif key == 'imageLinks':
                            try:
                                tmp[key] = value[0]
                            except IndexError:
                                tmp[key] = ''
                        elif key == 'groupModifiers':
                            groupModifiers = []
                            for val in value:
                                tmp_group = {}
                                tmp_group['id'] = val.get('id')
                                childModifiers = []
                                for val_mod in val.get('childModifiers'):
                                    tmp_child = {}
                                    tmp_child['id'] = val_mod.get('id')
                                    childModifiers.append(tmp_child)
                                tmp_group['childModifiers'] = childModifiers
                                groupModifiers.append(tmp_group)
                            tmp[key] = groupModifiers
                        else:
                            tmp[key] = value
                products_dish.append(tmp)
        elif x.get('type') == 'Modifier':
            tmp = {}
            for key, value in x.items():
                if key in modifier:
                    if key == 'sizePrices':
                        tmp[key] = value[0].get('price').get('currentPrice')
                    else:
                        tmp[key] = value
            products_modifier.append(tmp)
    json_obj = {'groups': groups, 'productCategories': productCategories, 'products_dish': products_dish,
                'products_modifier': products_modifier}
    return json_obj
