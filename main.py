import numpy
import math

def with_probability(probability):
    """
    Returns True with the given probability.

    Parameters:
    - probability (float): A value between 0 and 1 representing the probability of returning True.

    Returns:
    - bool: True with the specified probability, False otherwise.
    """
    return numpy.around(numpy.random.uniform(0, 1), 2) < (1 - probability)


# Example usage:
probability_value = 1  # You can adjust this value as needed
trues = 0

for x in range(0, 100):
    result = with_probability(probability_value)
    if result:
        trues += 1


mu, sigma = 60, 30 # mean and standard deviation
type(numpy.uint32(0).item())  # <class 'int'>
type(numpy.int16(0).item())   # <class 'int'>

s = numpy.floor(numpy.random.normal(60, 30, 1).item()).astype(int).item()
print(type(s))
print("random repair time is ", s)