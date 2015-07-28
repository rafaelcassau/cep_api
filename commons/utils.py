# -*- coding:utf-8 -*-


def model_to_dict(model_entity, exclude=[]):

    model_dict = {}

    for field in model_entity._fields:
        if field not in exclude:
            model_dict[field] = model_entity.__getitem__(field)

    return model_dict