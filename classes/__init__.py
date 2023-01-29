__all__ = ['algorithms', 'GUI', 'representation']


from .algorithms import delete, generator, genetic, hillclimber, multiprocessor, mutate, simulatedannealing
from .GUI import generator_GUI, generator_test_live, generator_test, init_GUI, selector_GUI_execute, selector_GUI, visualize_example
from .representation import course, malus_calc, room, roster, student