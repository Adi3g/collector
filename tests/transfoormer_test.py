from collector.core.transformer import DataTransformer

def test_transformer():
    transformations = [
        {
            'target': 'unified_data',
            'source': 'raw_data',
            'rules': [
                {'field': 'amount', 'type': 'float', 'default': 0.0},
                {'field': 'sale_date', 'type': 'string', 'rename': 'date'},
            ]
        }
    ]
    transformer = DataTransformer(transformations)
    data = [{'amount': '100.50', 'sale_date': '2023-09-17'}]
    transformed_data = transformer.transform(data)
    assert transformed_data[0]['amount'] == 100.50
    assert transformed_data[0]['date'] == '2023-09-17'
