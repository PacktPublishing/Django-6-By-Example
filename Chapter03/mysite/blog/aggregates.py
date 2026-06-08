from django.db.models import Aggregate


class StringAgg(Aggregate):
    function = "STRING_AGG"
    template = "%(function)s(%(expressions)s, %(delimiter)s %(order_by)s)"
    allow_order_by = True
    arity = 1

    def __init__(self, expression, delimiter=", ", **extra):
        super().__init__(expression, delimiter=f"'{delimiter}'", **extra)
