import pandas as pd

def value_contract(i_date, w_date, i_price, w_price, rate_volume, rate_cost, max_volume, storage_cost):
    # assume that dates in i_date and w_date are sorted in an increasing order
    # assume there are no days where both injection and withdrawal is done
    # convert dates to datetime format
    i_date = pd.to_datetime(i_date, format='%m/%d/%y')
    w_date = pd.to_datetime(w_date, format='%m/%d/%y')

    
    value, volume = 0, 0 
    i_idx, w_idx = 0, 0
    while i_idx < len(i_date) and w_idx < len(w_date):
        if i_date[i_idx] < w_date[w_idx]: # injection is done
            if volume + rate_volume <= max_volume:
                # subtract cost to purchase and inject gas from contract value
                value -= rate_volume * (i_price[i_idx] + rate_cost) 
                # update volume
                volume += rate_volume 
                print(f"Injection on {i_date[i_idx]}")

            else:
                print(f"Injection on {i_date[i_idx]} failed due to insufficient storage")

            i_idx += 1 # track next injection date

        else: # withdrawal is done
            if volume - rate_volume >= 0:
                # add earnings from sale of case and subtract cost of withdrawal from contract value
                value += rate_volume * (w_price[w_idx] - rate_cost)
                # update volume
                volume -= rate_volume 
                print(f"Withdrawal on {w_date[w_idx]}")

            else:
                print(f"Withdrawal on {i_date[i_idx]} failed due to insufficient product")

            w_idx += 1 # track next withdrawal date

    # inject on remaining dates
    while i_idx < len(i_date):
        if volume + rate_volume <= max_volume:
            # subtract cost to purchase and inject gas from contract value
            value -= rate_volume * (i_price[i_idx] + rate_cost) 
            # update volume           
            volume += rate_volume 
            print(f"Injection on {i_date[i_idx]}")
        else:
            print(f"Injection on {i_date[i_idx]} failed due to insufficient storage")
        i_idx += 1 # track next injection date

    # withdraw on remaing dates
    while w_idx < len(w_date):
        if volume - rate_volume >= 0:
                # add earnings from sale of case and subtract cost of withdrawal from contract value
                value += rate_volume * (w_price[w_idx] - rate_cost)
                # update volume
                volume -= rate_volume 
                print(f"Withdrawal on {w_date[w_idx]}")
        else:
            print(f"Withdrawal on {i_date[i_idx]} failed due to insufficient product")
        w_idx += 1 # track next withdrawal date

    # subtract monthly storage cost 
    # assume storage is held from first start date to last withdrawal date
    value -= storage_cost * ((w_date[-1] - i_date[0]).days)//30
    return value

if __name__ == "__main__":
    i_date = input("Enter injection date(s) (MM/DD/YY): ")
    w_date = input("Enter withdrawal date(s) (MM/DD/YY): ")
    i_price = input("Enter price on injection date(s): ")
    w_price = input("Enter price on withdrawal date(s): ")
    rate_volume = input("Enter rate for injection/withdrawal: ")
    rate_cost = input("Enter cost for injection/withdrawal: ")
    max_volume = input("Enter storage capacity: ")
    storage_cost = input("Enter storgae cost: ")
    
    i_date, w_date, i_price, w_price = eval(i_date), eval(w_date), eval(i_price), eval(w_price)
    val = value_contract(i_date, w_date, i_price, w_price, rate_volume, rate_cost, max_volume, storage_cost)
    print(f"The price of the contract is: {val}")
