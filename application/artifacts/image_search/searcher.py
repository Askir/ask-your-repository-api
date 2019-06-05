from .eh_descriptor import EdgeHistogramDescriptor
from .hog_descriptor import HOGDescriptor
from .feature_extractor import FeatureExtractor

class Searcher():

    @classmethod
    def default(cls):
        descriptors = [
            HOGDescriptor()
            #EdgeHistogramDescriptor(4, 4)
            # ColorDescriptor([8, 12, 3])
        ]
        return Searcher(descriptors)

    def __init__(self, descriptors):
        self.descriptors = descriptors

    def search(self, query_image, artifacts):
        search_features = FeatureExtractor(self.descriptors).extract(query_image)
        results = []
        for artifact in artifacts:
            distance = 0
            for descriptor in self.descriptors:
                name = descriptor.name()
                distance += descriptor.distance(search_features[name],artifact.features[name])
            results.append({"artifact": artifact, "distance": distance})

        newlist = sorted(results, key=lambda k: k['distance'])
        for element in newlist:
            print(element['distance'])
        newlist = list(map(lambda x: x["artifact"], newlist))
        return newlist


