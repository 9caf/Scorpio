import json
import datetime
import dateutil.parser
import decimal

CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'decimal': decimal.Decimal,
}


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, (decimal.Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super().default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


def main():
    data = {
        "hello": "world",
        "thing": datetime.datetime.now(),
        "other": decimal.Decimal(0)
    }
    thing = json.dumps(data, cls=MyJSONEncoder)

    print(json.loads(thing, object_hook=object_hook))

if __name__ == '__main__':
    main()
