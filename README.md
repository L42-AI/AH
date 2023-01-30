# AH
Algoritmes en Heuristieken

Introduction

This program creates a university schedule by scheduling courses that consist of lectures, tutorials, and practicals into specific rooms and time slots.
These Rooms can have a specific capacity of how many students they can hold.
We have a costfunction/maluspoints, that we are trying to minimize. The maluspoints are defined like this: 
Each student that would not fit the capacity of a room the class it is scheduled in is plus 1 maluspoint.
If a student has one gaphour it is counted as 1 extra point, two gaphours as 3 and 3 gaphours is not allowed. 
So we chose to give 3 gaphours a high value, so that it will always be minimized. We chose 10.
There is also one Room with an evening timeslot. If that is used it costs plus 5 maluspoints.

Approach

We minimize the maluspoints by using a hillclimber algorithm, a version of annealing and a version of a greedy algorithm. In this version of annealing it is not used at the start of the hillclimber,
but rather at the end. So when it seems, that we have diverged annealing is started and we try to walk down to a better optimum, then the local optimum we just were.
The hillclimber consists of 4 possible changes to the roster. They all are called an equal amount of times each generation.
The first method swaps one class with another class or one class with a room and timeslot that is still available. 
The second method swaps classes with the highest capacity points and swaps it with a random other room.
The third method takes a random student, calculates the day with the highest gap maluspoints and swaps with another student from another room or simply goes into another practical or tutorial group.
The fourth method takes a random student, calculates the day with the highes double hour maluspoints and again swaps with another student or goes into different class group.
This is repeated up until the program cant find an improvement on the schedule for 30 iterations in a row.

Reproducibility of Results

In order to reproduce the data and get a good Schedule...
