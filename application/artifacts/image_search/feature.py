"""Access to Sketches via Neo4J"""

from neomodel import StructuredNode, ArrayProperty, RelationshipFrom, \
    cardinality

from application.model_mixins import DefaultPropertyMixin, DefaultHelperMixin


class Feature(StructuredNode, DefaultPropertyMixin, DefaultHelperMixin):
    """The class that manages ImageFeatures"""

    features = ArrayProperty()
    artifact = RelationshipFrom("application.models.Artifact", "HAS_FEATURE", cardinality=cardinality.ZeroOrOne)