# Introduction
This is a library for simulate probability theory problems specialy conditional probability. It is also useful to create custom single or joint distribution with specific PMF or PDF to get probability table and genearte data based on probability function.

## How to install?
`pip install pprobs`

## Probability Simulator 
It simulates probability theory problems specialy conditional probability.

### Example 1
We want to get some infromation by defining some events.

- `P(A) = 0.3`
- `P(B) = 0.2`
- `P(A^B) = 0.1`
- `A and B are dependent`
- `P(A+B) = ? , P(A|B) = ?`

```python
from pprobs.simulation import Simulator

space = Simulator()

space.add_event('A', 0.3)
space.add_event('B', 0.2)
space.add_event('A^B', 0.1)

prob_1 = space.get_prob('A+B') # A+B means union of A and B
prob_2 = space.get_prob('A|B')

print(prob_1, prob_2) # 0.4  0.5
```

### Example 2
In a group of 100 sports car buyers, 40 bought alarm systems, 30 purchased bucket seats, and 20 purchased an alarm system and bucket seats. If a car buyer chosen at random bought an alarm system, what is the probability they also bought bucket seats?

By [Statisticshowto](https://www.statisticshowto.com/probability-and-statistics/statistics-definitions/conditional-probability-definition-examples/)

- `P(SEAT) = 0.3`
- `P(ALARM) = 0.4`
- `P(SEAT ^ ALARM) = 0.2`
- `P(SEAT | ALARAM) = ?`

```python
from pprobs.simulation import Simulator

space = Simulator()

space.add_event('SEAT', 0.3).add_event('ALARM', 0.4) # We can also add events sequentially in a line (chaining) 
space.add_event('SEAT^ALARM', 0.2) # A^B means intersection of A & B

print(space.get_prob('SEAT|ALARM')) # 0.5
```

### Example 3
Totaly 1% of people have a certain genetic defect.90% of tests for the gene detect the defect (true positives).
9.6% of the tests are false positives.
If a person gets a positive test result, what are the odds they actually have the genetic defect?

By [Statisticshowto](https://www.statisticshowto.com/probability-and-statistics/probability-main-index/bayes-theorem-problems/#:~:text=Bayes'%20Theorem%20Example%20%231&text=A%20could%20mean%20the%20event,the%20clinic's%20patients%20are%20alcoholics.)


- `P(GEN_DEF) = 0.01`
- `P(POSITIVE|GEN_DEF) = 0.9`
- `P(POSITIVE|GEN_DEF!) = 0.096`
- `P(GEN_DEF|POSITIVE) = ?`

```python
space = Simulator()

space.add_event('GEN_DEF', 0.01)
space.add_event('POSITIVE|GEN_DEF', 0.9) # A|B means A given B
space.add_event('POSITIVE|GEN_DEF!', 0.096) # A! means complement of A

print(space.get_prob('GEN_DEF|POSITIVE')) # 0.0865
```

### Example 4
Bob has an important meeting tomorrow and he has to reach office on time in morning. His general mode of transport is by car and on a regular day (no car trouble) the probability that he will reach on time is 0.3. The probability that he might have car trouble is 0.2. If the car runs into trouble he will have to take a train and only 2 trains out of the available 10 trains will get him to office on time.

By [Hackerearth](https://www.hackerearth.com/practice/machine-learning/prerequisites-of-machine-learning/bayes-rules-conditional-probability-chain-rule/tutorial/)


- `P(ON_TIME|CAR_OK) = 0.3`
- `P(ON_TIME|CAR_OK!) = 2/10 => Go by train`
- `P(CAR_OK!) = 0.2`
- `P(ON_TIME) = ? `


```python
space = Simulator()

space.add_event('ON_TIME|CAR_OK', 0.3)
space.add_event('ON_TIME|CAR_OK!', 2/10)
space.add_event('CAR_OK!', 0.2)

prob = space.get_prob('ON_TIME') # Probability of ON_TIME

print(prob) # 0.28
```

## Distribution Simulator 
It is useful to create custom single or joint distribution with specific PMF or PDF to get probability table and genearte data based on probability function.

### Example 1
Suppose that we have a discrete random varible with specific PMF. We want to genearte many data based on this variable. As you see in the second example 1 has the largest probability and duplicates more and 4 has the smallest probability and duplicates less. 

```python
from pprobs.distribution import Discrete

# First 
def pmf(x):
    return 1 / 6

dist = Discrete(pmf, [1, 2, 3, 4, 5, 6]) # The second is the sample space of our PMF

print(dist.generate(15)) # [4, 3, 1, 6, 5, 3, 5, 3, 5, 4, 2, 5, 6, 1, 6]


# Second
def pmf(x):
    return 1 / x

dist = Discrete(pmf, [1, 2, 3, 4])
print(dist.generate(15)) # [1, 2, 1, 1, 1, 4, 3, 1, 1, 3, 2, 4, 1, 2, 2]

```

### Example 2
Suppose that we have a continuous random varible with specific PDF.

```python
from pprobs.distribution import Continuous

def pdf(x):
  if x > 1:
    return x / x ** 2
  return 0

dist = Continuous(pdf, [1, 6]) # The second is the sample interval of our PDF

print(dist.generate(15)) # [2.206896551724138, 4.103448275862069, ..., 5.655172413793104, 6.0]

```

### Example 3
Suppose that we have a Continuous Joint varible with specific PDF.

```python
from pprobs.distribution import Joint

def pdf(x, y):
  if x > 1:
    return 1 / (x * y)
  return 0

dist = Joint(pdf, [1, 6], [3, 10]) # The second and third are the intervals of our PDF

print(dist.probability_table(force=20)) # if force gets more, many number will generate
```
#### Output: 
| X/Y   | x=3.0 | X=3.7 | ... | X=10  |
|-------|-------|-------|-----|-------|
| X=1.0 | 0.000 | 0.000 | ... | 0.000 |
| ...   | ...   | ...   | ... | ...   |
| X=6.0 | 0.055 | 0.044 | ... | 0.016 |


```python
print(dist.get_prob(3.5, 3.5)) # 0.081 is P(X=3.5, Y=3.5)
print(dist.get_prob([1, 6], 4)) # 0.041 is P(Y=4) because X includes its whole domain
print(dist.get_prob(2.1, [1, 4])) # 0.206 is P(X=2.1, Y in [1, 4])
```

### Example 4
Suppose that we have a Discrete Joint varible with specific PMF.

```python
from pprobs.distribution import Joint

def pmf(x, y):
  if x > 1:
    return 1 / (x * y)
  return 0

dist = Joint(pmf, range(1, 6), range(6, 10)) # The second and third are the sample space of our PMF

print(dist.probability_table()) 
```
#### Output: 

| X/Y   | Y=6  | Y=7 | Y=8  |  Y=9  |
|-------|-------|-------|-----|-------|              
|X=1 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
|X=2 | 0.083333 | 0.071429 | 0.062500 | 0.055556 |
|X=3 | 0.055556 | 0.047619 | 0.041667 | 0.037037 |
|X=4 | 0.041667 | 0.035714 | 0.031250 | 0.027778 |
|X=5 | 0.033333 | 0.028571 | 0.025000 | 0.022222 |

```python
print(dist.get_prob(2, range(6, 10))) # 0.272 is P(X=2)
print(dist.get_prob(2, 6)) # 0.083 is P(X=2, Y=6)
```




