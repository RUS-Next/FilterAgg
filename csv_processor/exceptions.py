class InvalidOperatorError(Exception):
    """Invalid filter operator"""
    pass

class InvalidAggregateError(Exception):
    """Invalid aggregate operation"""
    pass

class InvalidColumnError(Exception):
    """Invalid column"""
    pass