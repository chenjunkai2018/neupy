import numpy as np

from neuralpy.algorithms import Instar
from neuralpy.layers import StepLayer, OutputLayer

from base import BaseTestCase


input_data = np.array([
    [0, 1, -1, -1],
    [1, 1, -1, -1],
])


class HebbRuleTestCase(BaseTestCase):
    def setUp(self):
        super(HebbRuleTestCase, self).setUp()
        kwargs = {
            'weight': np.array([
                [3],
                [0],
                [0],
                [0],
            ]),
            'function_coef': {
                'lower_value': 0,
                'upper_value': 1,
            }
        }
        self.conn = StepLayer(4, **kwargs) > OutputLayer(1)

    def test_learning_process(self):
        hn = Instar(
            self.conn,
            n_unconditioned=1,
            step=1,
        )

        hn.train(input_data, epochs=10)

        self.assertEqual(hn.predict(np.array([[0, 1, -1, -1]]))[0, 0], 1)
        self.assertTrue(np.all(
            hn.input_layer.weight == np.array([
                [3],
                [1],
                [-1],
                [-1],
            ])
        ))