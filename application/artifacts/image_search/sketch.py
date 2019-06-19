"""Access to Sketches via Neo4J"""

from neomodel import StructuredNode, StringProperty, JSONProperty, RelationshipTo, RelationshipFrom, \
    cardinality

from application.model_mixins import DefaultPropertyMixin, DefaultHelperMixin


class Sketch(StructuredNode, DefaultPropertyMixin, DefaultHelperMixin):
    """The class that manages sketches"""

    file_url = StringProperty(required=True)
    features = JSONProperty()

    results = RelationshipTo("application.models.Result", "HAS", cardinality=cardinality.ZeroOrMore)
    intended_result = RelationshipFrom("application.models.Artifact", "DESCRIBES", cardinality=cardinality.ZeroOrOne)

    @property
    def sketch_url(self):
        return self.file_url

    @property
    def ordered_results(self):
        return list(map(lambda x: x.artifact.single(), self.results.order_by('distance')[:20]))

    @property
    def intended_artifact(self):
        return self.intended_result.single()
