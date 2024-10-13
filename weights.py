import json

weights_data = [
    [0.4, 0.6, 0],
    [0.6, 0.4, 0],
    [0.7, 0.3, 0],
    [0.3, 0.3, 0],
    [0.4, 0.4, 0]
]

with open('weights.json', 'w') as f:
    json.dump(weights_data, f)
