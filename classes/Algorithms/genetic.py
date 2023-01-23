import random

class GeneticAlgorithm():
    def __init__(self, population, mutation_rate):
        self.population = population
        self.mutation_rate = mutation_rate
        self.best = None
        self.best_malus = float('inf')
    
    def evolve(self):
        new_population = []
        for i in range(len(self.population)):
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        self.population = new_population
        
    def select_parent(self):
        """
        Select a parent from the population using tournament selection.
        """
        selected = random.sample(self.population, 2)
        return min(selected, key=lambda x: x.malus_count)

    def crossover(self, parent1, parent2):
        """
        Perform crossover on the parents to create a child.
        """
        child = Roster(parent1.rooms_list, parent1.student_list, parent1.course_list, parent1.CAPACITY)
        child.schedule = {**parent1.schedule, **parent2.schedule}
        return child
    
    def mutate(self, child):
        """
        Apply mutation to the child according to the mutation rate.
        """
        for course_name, course_schedule in child.schedule.items():
            for class_name, class_data in course_schedule.items():
                if random.uniform(0, 1) < self.mutation_rate:
                    child = hillclimber(child)
                    break
        return child
    
    def run(self, n_generations):
        """
        Run the genetic algorithm for n_generations.
        """
        for i in range(n_generations):
            self.evolve()
            for individual in self.population:
                if individual.malus_count < self.best_malus:
                    self.best = individual
                    self.best_malus = individual.malus_count
