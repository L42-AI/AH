def save_results(info):
    iter, dict_pair = info
    with open('data/HCresults.csv', mode='a') as f:

        string = f'{iter},{list(dict_pair.keys())[0]},{list(dict_pair.values())[0]}'
        print(string)
        f.write(f'\n{string}')

info = (1, {'HC3': 299})
save_results(info)