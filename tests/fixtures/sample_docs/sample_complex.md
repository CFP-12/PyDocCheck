# Advanced Python Guide

## Data Processing with Pandas

First, import the library:

```python
import pandas as pd
import numpy as np
```

## Creating DataFrames

Here's how to create a simple dataframe:

```python
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 75000]
}

df = pd.DataFrame(data)
print(df)
```

## Some invalid code (this will fail)

```python
# This has a typo and should fail
df.columns()  # Should be df.columns (property, not method)
```

## Processing Data

Filtering and aggregation:

```python
df_filtered = df[df['age'] > 25]
avg_salary = df['salary'].mean()
print(f"Average salary: {avg_salary}")
```

## Comment-only code block

This should be filtered out:

```python
# Just a comment explaining something
# Nothing executable here
```
