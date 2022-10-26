import spacy


class LocationDetector:
    def __init__(self):
        print('Initializing.')
        self.model = spacy.load('en_core_web_md')

    def predict(self, X, feature_names):
        print(f'Received request with input X: {X}')
        
        text_features = self.model(str(X[0]))
        print(f'Model returned text: {text_features.text}')
        
        entities = text_features.ents
        print(f'Model detected entities: {entities}')

        locations = [
            entity.text for entity in entities
            if entity.label_ in ['GPE', 'LOC']
        ]
        print(f'Detected locations: {locations}')
        return locations
