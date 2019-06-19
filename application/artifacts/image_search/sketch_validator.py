from webargs import fields

def create_args():
    """Defines and validates params for create"""
    return {
        "sketch": fields.String(required=True),
        "intended_image": fields.UUID()
    }

def modify_args():
    """Defines and validates params for update"""
    return {
        "sketch_id": fields.UUID(location='view_args'),
        "intended_image": fields.UUID()
    }

def search_args():
    """Defines and validates params for searching"""
    return {
        "sketch_id": fields.UUID(location='view_args')
    }