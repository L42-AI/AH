# AH
Algoritmes en Heuristieken
8
## Introduction

This program creates a university schedule by scheduling courses that consist of lectures, tutorials, and practicals into specific rooms and timeslots.
These rooms have a specific capacity of how many students they can hold.
We have a cost function, that calculates maluspoints, which we are trying to minimize. The maluspoints are defined by the following criteria: 
- The number of students attending a seminar exceeding the capacity of a room (1 malus point per student).
- Gaphours. If a student has 1 gaphour it is counted as 1 malus point, 2 gaphours as 3 malus points and finally, three gaphours is not allowed. 
- We choose to give 3 gaphours a high value, so that it will always be minimized to 0. We chose 10. Therefore, the initial startup is not a 'correct' solution
- An evening slot (15:00 - 17:00). If any student has this time slot, it counts as 5 malus points.

## Approach
The goal is to minimize the maluspoints. We have a total of 3 algorithms that try to do this. These algorithms could be used seperately, but often times, a combination is most effective. We start our experiment by creating a schedule randomly. This means that students could have multiple seminars at the same time and lectures where over a hundred students want to attend can get scheduled in a room that fits 20.
This is why we created our Greedy Algorithm. Greedy can lower the initial startup malus points. This results in less computing power needed when trying to minimize the cost function with our hillclimbers. When running our experiments, Greedy was turned off. This was to rigurously test the effectiveness of our hillclimbers. Also, some experiments were written in later stages of our development process, therefore, to ensure a high degree of camparabiliy, we turned off greedy in our later experiment.
After our initialisation, we want to lower the malus points. For this we originally created 4 variations of hillclimbers, with the following functionality:
The first two hillclimbers swap classes as a whole, meaning that they relocate the class, with their assigned students to a new class moment, or timeslot.
- HC_TimeSlotSwapRandom swaps 2 randomly chosen classes, which could be lectures, tutorials or practicals.
- HC_TimeSlotSwapCapacity selected a class based on the capacity malus count. It than picks another course to swap the timeslot of this class with. The second course was choosen randomly, to avoid the swaps following the greedy principle. By incorporating some degree of randomness we can explore different, and therefore more states in the complete statespace.

The other two hill climbers swap the assigned groups a student is enrolled in
- HC_SwapBadTimeslots_GapHour pickes the student with the most malus points based on gap hours. Then it looked at their 'worst day', the day that causes the most mals. This could for example be a day where he/she started at 9 and had one final siminar at 5 o'clocks, which results in 3 gap hours. This Hillclimber would then pick one of the two seminar types, tutorial or practical, and try to change the group a student is enrolled in, for example from tutorial 1, to tutorial 3. A student cannot change lecture group, since all students enrolled in a course go to the same lecture.
- HC_SwapBadTimeslots_DoubleHour is identical to HC_SwapBadTimeslots_GapHour but instead of selecting the 'worst day' by looking at gap hours, it looks at double hours.

When a new schedule is created by the Hillclimbers, it is normally only accepted when it results in a lower malus score. When Simulated Annealing is turned on, it generates a probabilty and an acceptance rate based of a Temperature that follows a cooling scheme. Without going into many technical details, it is neccesarily to explain that our Simulated Annealing mostly gets activated when the Hillclimbers are converging to a malus score (=cannot improve) and not at the beginning of the experiment. When that happens, there is a possibility that the program accepts a worse schedule in order to escape a local optimum.

Besides a Hillclimber and a Simulated Annealing algorithm, we run a Genetic Algorithm. Since we have 4 types of Hillclimbers, we start of by sending 4 identical schedules to each Hillclimber 2 times. This results in 32 new schedules. These schedules get paired with another schedule and the schedule with the *highest* malus score is thrown out. These 'rounds' continue untill there are 4 schedules left. These 4 schedules get placed into each Hillclimber twice again. This process is called Genetic because it 'selects' from its population 4 schedules that show good improvement but do not have to be the best 4, allowing the algorithm to explore other options too. 

Reproducibility of Results

We have ran 5 experiments. For each experiment we turned of any initialisation heuristics. The heuristics we have are: 
- Capacity: Courses can only schedule their lectures in the largest rooms, preventing capacity points generated by placing 80 students in the smallest room.
- Popular: Courses that have a large number of students enrolled get assigned to timeslots first
- Popular own day: The 5 most popular courses get their lectures on their own day. The idea behind this is that when a large number of students follow the same courses, scheduling them at the same time or on the same day with gap hours might result in more gap hours
- Busy students: This heuristic flags courses that have students enrolled that follow 5 or more courses. Those courses get their seminars assigned first


 We have created a histogram to show at what scores our program start without heuristics:
![Baseline_random](https://user-images.githubusercontent.com/70103333/216134905-075f9c04-8ce7-46a5-a77f-3de860574029.png)



https://user-images.githubusercontent.com/70103333/216144973-43452cca-0214-4be6-902e-663a8043669b.mp4




## Usage

To run our application, you first install the required libraries:

- Activate the ProgLab environment
- pip install customtkinter
- 




