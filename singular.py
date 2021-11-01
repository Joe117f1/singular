import pandas as pd

FILENAME = '\Python\singular\Exercise.xlsx'


def create_list(filterd_list):
    new_list = []
    for i, val in enumerate(filterd_list):
        new_list.append({'idx': i, 'value': val})
    return new_list


def get_valid_numbers(element):
    if not element:
        return False
    string = str(element)
    el = string.lower()
    for x in '!@#$%^&*()abcdefghijklmnopqrstuvwxyz':
        el = el.replace(x, '')
    return float(el) if el else False


def get_column_total(file, coulumn):
    data_column = file[coulumn]
    list_of_values = [get_valid_numbers(
        el) for el in data_column if get_valid_numbers(el)]
    # mean_cost = sum(cost_list[:-1]) / (len(cost_list)-1)
    value_sum = sum(list_of_values[:-1])
    value_indices = create_list(list_of_values)

    return {
        'total': value_sum,
        'proccessed_list': value_indices
    }


def get_single_date_column(file, coulumn):
    date_column = file[coulumn]
    date_list = [cell for cell in date_column]
    list_build_helper = []

    for el in date_list:
        if type(el) == str:
            if el[0] == '0' or el[0] == '1' or el[0] == '2':
                list_build_helper.append(el)

    dates_indexed_list = create_list(list_build_helper)
    return dates_indexed_list


def get_curr_month_dates(date_list):
    dates = []
    curr_date = ''
    for d in date_list:
        if d['value'] == curr_date:
            continue
        else:
            curr_date = d['value']
            dates.append(d['value'])
    return dates


def get_totals_per_date(totals, date_list):
    totals_per_date = []

    dates = get_curr_month_dates(date_list)
    for date in dates:
        values_per_date = []
        desired_date_list = [d for d in date_list if d['value'] == date]

        for d in desired_date_list:
            idx = d['idx']
            val = totals[idx]['value']
            values_per_date.append(val)

        total_per_date = (sum(values_per_date))
        date_dict = {'date': date, 'total': total_per_date}
        totals_per_date.append(date_dict)
    return totals_per_date


def analyze_file(filename):
    file_content = pd.read_excel(filename)
    # print(file_content.head())
    costs_dict = get_column_total(file_content, 'Unnamed: 4')
    costs_list = costs_dict['proccessed_list']
    installs_dict = get_column_total(file_content, 'Unnamed: 5')
    installs_list = installs_dict['proccessed_list']

    dates = get_single_date_column(file_content, 'Monthly Report')

    cost_per_date = get_totals_per_date(costs_list, dates)
    installs_per_date = get_totals_per_date(installs_list, dates)

    print('TOTAL COST: ', cost_per_date)
    print('-'*50)
    print('TOTAL INSTALLS: ', installs_per_date)


analyze_file(FILENAME)
