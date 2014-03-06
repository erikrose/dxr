from pyelasticsearch import ElasticSearch, ElasticHttpNotFoundError

ES_HOSTS = ['http://127.0.0.1:9200']
INDEX = 'test_dxr'
FILE = 'file'
LINE = 'line'


def test_es():
    es = ElasticSearch(ES_HOSTS)
    try:
        es.delete_index(INDEX)
    except ElasticHttpNotFoundError:
        pass
    es.create_index(INDEX, settings={
        'mappings': {
            LINE: {
                '_parent': {"type": FILE}
            }
        }})
    es.bulk_index(INDEX, FILE, [
            {
                'id': 1,
                'path': 'first',
            },
            {
                'id': 2,
                'path': 'second',
            }
        ])
    es.bulk_index(INDEX, LINE, [
            {
                'id': 1,
                '_parent': 1,
                'number': 1,
                'text': 'One fish',
            },
            {
                'id': 2,
                '_parent': 1,
                'number': 2,
                'text': 'Two fish',
            },
            {
                'id': 3,
                '_parent': 2,
                'number': 1,
                'text': 'Red fish',
            },
            {
                'id': 4,
                '_parent': 2,
                'number': 2,
                'text': 'Red bull',
            }
        ])
