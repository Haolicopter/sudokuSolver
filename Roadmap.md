Plan A:
Scan each cell:
1. Check square completeness
2. Check row completeness
3. Check col completeness
4. Generate all possible combos, fliter by violations. If one left, we have a solution for this cell

Scan each number:
For example, in one sqaure there are three spots for number 2.
But if two of the spots' row or col already have 2 in other squares,
then that leave only one possible spot for number 2

Plan B: DFS
Make a decision tree