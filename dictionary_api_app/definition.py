import pandas


class Definition:
    '''
    Definition page, allow us to get definitions of the term
    '''

    def __init__(self, term):
        self.term = term

    def get(self):
        df = pandas.read_csv('data/data.csv')
        definition = tuple(df.loc[df['word'] == self.term]['definition'])
        if definition:
            return definition
        else:
            return f'No definition for the mentioned word, please try again'
