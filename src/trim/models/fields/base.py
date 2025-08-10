
DEFAULT_NIL = True


def defaults(args, params, nil_sub=True, nil_key='nil', **kw):

    if nil_sub:
        # nil subtract, or substitution
        #  Nil. being blank+null - where nil=True
        if (nil_key in kw) or (nil_key in params):
            # Fetch the value without treating False as missing.
            val = kw.get(nil_key) if (nil_key in kw) else params.get(nil_key)

            if isinstance(val, bool):
                # if the given value is a single bool,
                # unpack and multiply into the count of
                # args for the blank_null func,
                val = [val] * 2
                kw.update(**blank_null(*val))

    for k, v in kw.items():
        if k == nil_key:
            continue
        params.setdefault(k, v)
    params.pop('nil', None)
    return params


def blank_null(b=True, n=True):
    return {'blank':b, 'null': n}
