from neomodel import StructuredNode, FloatProperty, RelationshipTo, RelationshipFrom, cardinality

from application.model_mixins import DefaultPropertyMixin, DefaultHelperMixin


class Result(StructuredNode, DefaultPropertyMixin, DefaultHelperMixin):
    distance = FloatProperty(required=True)

    sketch = RelationshipFrom("application.models.Sketch", "HAS", cardinality=cardinality.One)
    artifact = RelationshipTo("application.models.Artifact", "RESULTS" , cardinality=cardinality.One)
