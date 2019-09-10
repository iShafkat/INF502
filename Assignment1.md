
1. Draw a diagram of the commits and branches in repository.

    - Use `git branch` to list the branches in this repository.
    - Use `git checkout` to explore each branch.
    - Use `git log --decorate` to explore the structure of commits.

```
The screenshot below shows:
```
![image](https://github.com/iShafkat/INF502/blob/master/Docs/ans1.JPG)

2. Try `git log --graph --all` to see the commit tree. What do you see?
```
It shows all the latest commits to the branches.

```

3. Use `git diff BRANCH_NAME` to view the differences from a branch and the current branch.
   Summarize the difference from master to the other branch.

```
The green lines are in the current branch (master) whereas the red lines are in the other branch not in the current branch. 

```

4. Write a command sequence to merge the non-master branch into `master`

```
git merge BRANCH_NAME

```


5. Write a command (or sequence) to (i) create a new branch called `math` (from the `master`) 
and (ii) change to this branch

```
git branch math
git checkout math


```
   
6. Edit B.py adding the following source code below the content you have there
```
print 'I know math, look:'
print 2+2
```

7. Write a command (or sequence) to commit your changes
```


```

8. Change back to the `master` branch and change B.py adding the following source code (commit your change to `master`):
```
print 'hello world!'
```

9. Write a command sequence to merge the `math` branch into `master` and describe what happened
```


```
   
10. Write a set of commands to abort the merge
```


```
   
11. Now repeat item 9, but proceed with the manual merge (Editing B.py). All implemented methods are needed. Explain your procedure
```


```

12. Write a command (or set of commands) to proceed with the merge and make `master` branch up-to-date
```


```



Report your experience of making this submission, including the steps followed, commands used, and hurdles faced (within the file you created for the **Part 1**.
```


```
