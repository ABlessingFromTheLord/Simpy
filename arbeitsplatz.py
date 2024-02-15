import math


def amount_of_runs(orders):

    for i in range(len(orders)):
        if orders[i] == 0:
            continue
        else:
            match i:
                case 0:
                    orders[0] = orders[0] / 17
                case 1:
            orders[0] = orders[0] / 17
                case 2:
                case 3:

            to_return = [ob / 17, ut / 11, ht / 49, rg / 97]

    for i in range(len(to_return)):
        if to_return[i] < 1:
            to_return[i] = 1
        else:
            to_return[i] = math.ceil(to_return[i])

    return to_return


print(amount_of_runs(20, 20, 20, 20))
print(amount_of_runs(100, 100, 100, 100))
print(amount_of_runs(1, 1, 1, 1))
print(amount_of_runs(0, 0, 0, 0))
print(amount_of_runs(53, 53, 53, 53))
print(amount_of_runs(30, 30, 30, 30))
