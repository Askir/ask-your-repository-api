from flask import current_app
from mamba import description, before, it
from expects import expect, equal
from doublex import Mock, ANY_ARG, method_returning
from doublex_expects import have_been_called
from application.controllers.artifacts_controller import ArtifactsController
from application.synonyms.synonyms import SynonymGenerator
import nltk
from textblob import Word

with description('all functions return correct value') as self:
    with before.each:
        self.synonym_generator = SynonymGenerator("1234")
        self.synset = []
    with it('get_synonyms returns original params if no synonyms found'):
        self.synonym_list = self.synonym_generator.get_synonyms()
        expect(self.synonym_list).to(equal("1234"))

with description('SynonymGenerator returns correct synonyms') as self:
    def strings_are_similar(self, syn_result, syn_response):
        result = syn_result.split().sort()
        response = syn_response.split().sort()
        return True if result == response else False

    with before.each:
        self.synonym_generator = SynonymGenerator("test")
        self.synonyms_result = "try_out study test verify"
    with it('synonym_list includes all synonyms for "test"'):
        self.synonyms= self.synonym_generator.get_synonyms()
        expect(self.strings_are_similar(self.synonyms_result, self.synonyms)).to(equal(True))
