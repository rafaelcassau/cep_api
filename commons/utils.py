# -*- coding:utf-8 -*-


def model_to_dict(model_entity, exclude=[]):

    model_dict = {}

    for field in model_entity._fields:
        if field not in exclude:
            model_dict[field] = model_entity.__getitem__(field)

    return model_dict


def convert_query_set_to_list_dict(queryset, exclude=[]):

    queryset_list = [model_to_dict(obj, exclude) for obj in queryset]

    return queryset_list