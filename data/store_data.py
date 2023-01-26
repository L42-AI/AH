import pandas as pd

def store_improvements(list1, list2, list3, list4):
    """This function takes in 3 lists, converts them into a dataframe and then stores it as a csv."""
    df = pd.DataFrame(list(zip(list1, list2, list3, list4)),
                        columns = ['Swap Lecture', 'Swap Student', 'Swap Gaphour', 'Swap Doubleclasses'])

    df.to_csv('data/generation-improvements.csv', index=False)