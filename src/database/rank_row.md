# SQL Ranking Functions: ROW_NUMBER(), RANK(), and DENSE_RANK()

## Overview

SQL provides three primary window functions for ranking rows, each with distinct behaviors when handling ties (rows with identical values):

1. **ROW_NUMBER()** - Assigns a unique sequential integer to each row
2. **RANK()** - Assigns the same rank to ties, but skips subsequent ranks
3. **DENSE_RANK()** - Assigns the same rank to ties, but doesn't skip ranks

## Example Dataset

To illustrate the differences, consider this employees table with salary data:

```
| employee_id | name      | salary |
|-------------|-----------|--------|
| 1           | Alice     | 85000  |
| 2           | Bob       | 75000  |
| 3           | Charlie   | 75000  |
| 4           | David     | 70000  |
| 5           | Eve       | 65000  |
| 6           | Frank     | 65000  |
| 7           | Grace     | 60000  |
```

## ROW_NUMBER()

Assigns a unique, sequential number to each row, regardless of ties.

```sql
SELECT 
    employee_id, 
    name, 
    salary, 
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;
```

Result:
```
| employee_id | name      | salary | row_num |
|-------------|-----------|--------|---------|
| 1           | Alice     | 85000  | 1       |
| 2           | Bob       | 75000  | 2       |
| 3           | Charlie   | 75000  | 3       |
| 4           | David     | 70000  | 4       |
| 5           | Eve       | 65000  | 5       |
| 6           | Frank     | 65000  | 6       |
| 7           | Grace     | 60000  | 7       |
```

**Key characteristics**:
- Every row gets a unique number
- Numbers are sequential without gaps
- For tied salaries (Bob/Charlie and Eve/Frank), the order is deterministic only with a complete ORDER BY clause
- Useful when you need exactly N rows regardless of ties

## RANK()

Assigns the same rank to ties and skips the next rank(s).

```sql
SELECT 
    employee_id, 
    name, 
    salary, 
    RANK() OVER (ORDER BY salary DESC) as rank_num
FROM employees;
```

Result:
```
| employee_id | name      | salary | rank_num |
|-------------|-----------|--------|----------|
| 1           | Alice     | 85000  | 1        |
| 2           | Bob       | 75000  | 2        |
| 3           | Charlie   | 75000  | 2        |
| 4           | David     | 70000  | 4        |
| 5           | Eve       | 65000  | 5        |
| 6           | Frank     | 65000  | 5        |
| 7           | Grace     | 60000  | 7        |
```

**Key characteristics**:
- Tied values receive the same rank
- The next rank after ties skips numbers based on the number of ties
- Bob and Charlie both get rank 2, then the next rank is 4 (skipping 3)
- Eve and Frank both get rank 5, and the next rank is 7 (skipping 6)
- Similar to "Olympic ranking" (1st, 2nd, 2nd, 4th)

## DENSE_RANK()

Assigns the same rank to ties but doesn't skip any ranks.

```sql
SELECT 
    employee_id, 
    name, 
    salary, 
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_num
FROM employees;
```

Result:
```
| employee_id | name      | salary | dense_rank_num |
|-------------|-----------|--------|----------------|
| 1           | Alice     | 85000  | 1              |
| 2           | Bob       | 75000  | 2              |
| 3           | Charlie   | 75000  | 2              |
| 4           | David     | 70000  | 3              |
| 5           | Eve       | 65000  | 4              |
| 6           | Frank     | 65000  | 4              |
| 7           | Grace     | 60000  | 5              |
```

**Key characteristics**:
- Tied values receive the same rank
- The next rank after ties is always the next consecutive integer
- Bob and Charlie both get rank 2, then the next rank is 3 (no skipping)
- Eve and Frank both get rank 4, and the next rank is 5 (no skipping)
- Useful for finding top N distinct values (e.g., top 3 salary levels)

## Side-by-Side Comparison

```sql
SELECT 
    employee_id, 
    name, 
    salary, 
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank_num,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_num
FROM employees;
```

Result:
```
| employee_id | name      | salary | row_num | rank_num | dense_rank_num |
|-------------|-----------|--------|---------|----------|----------------|
| 1           | Alice     | 85000  | 1       | 1        | 1              |
| 2           | Bob       | 75000  | 2       | 2        | 2              |
| 3           | Charlie   | 75000  | 3       | 2        | 2              |
| 4           | David     | 70000  | 4       | 4        | 3              |
| 5           | Eve       | 65000  | 5       | 5        | 4              |
| 6           | Frank     | 65000  | 6       | 5        | 4              |
| 7           | Grace     | 60000  | 7       | 7        | 5              |
```

## Common Use Cases

### ROW_NUMBER()
- Pagination (get records 11-20)
- Removing duplicates (keeping only the first occurrence)
- Getting exactly N rows regardless of ties
- Assigning a unique identifier to each row

```sql
-- Getting the top 3 highest paid employees, regardless of ties
SELECT * FROM (
    SELECT 
        employee_id, 
        name, 
        salary, 
        ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
    FROM employees
) ranked
WHERE row_num <= 3;
```

### RANK()
- Traditional competition ranking ("Olympic ranking")
- When you want to see gaps that represent the number of tied rows
- When the strict "first, second, third" terminology matters

```sql
-- Find employees with the top 3 salary ranks (may return more than 3 employees due to ties)
SELECT * FROM (
    SELECT 
        employee_id, 
        name, 
        salary, 
        RANK() OVER (ORDER BY salary DESC) as rank_num
    FROM employees
) ranked
WHERE rank_num <= 3;
```

### DENSE_RANK()
- Finding the top N distinct values (e.g., top 3 salary levels)
- When you want consecutive ranks without gaps
- When ties should share the same rank but not affect subsequent ranks

```sql
-- Find employees with the top 3 salary levels (may return more than 3 employees due to ties)
SELECT * FROM (
    SELECT 
        employee_id, 
        name, 
        salary, 
        DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_num
    FROM employees
) ranked
WHERE dense_rank_num <= 3;
```

## Partitioning

All three ranking functions can be partitioned, which resets the ranking for each partition:

```sql
SELECT 
    employee_id, 
    name,
    department,
    salary, 
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_salary_rank
FROM employees;
```

This would provide the salary ranking within each department separately.

## Performance Considerations

- Performance is generally similar for all three functions
- All three functions require an ORDER BY clause
- For large datasets, ensure appropriate indexing on the columns used in the ORDER BY clause
- Window functions are calculated after WHERE clauses but before ORDER BY, LIMIT, and OFFSET in the query execution

## Summary

| Function | Ties Handling | Gaps | Common Uses |
|----------|---------------|------|------------|
| ROW_NUMBER() | Unique numbers for all rows | No gaps | Pagination, exact counts, removing duplicates |
| RANK() | Same rank for ties | Gaps after ties | Traditional competition ranking, showing distance between ranks |
| DENSE_RANK() | Same rank for ties | No gaps | Finding distinct value rankings, consecutive numbering |

Understanding these subtle differences is essential for correctly applying these functions to various data analysis requirements.