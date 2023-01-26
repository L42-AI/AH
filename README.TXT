# swap worst student
when swapping worst student, we do not pick the student with the worst malus. 
instead, we select the top 5 students with the most malus and randomly pick one. 
this is because there could be a situation where the worst student cannot swap because there 
are no other tutorials. When this happens, the swap might keep on selecting that student
for many iterations.
