# Algorithm that calculates the present value of a stream of yearly cash flows given...
# 1. The discount rate (as a decimal, not a percent)
# 2. An array of cash flows, with the index of the cash flow being the associated year

# Note: This algorithm assumes that cash flows are paid at the end of the specified year

from typing import List, Tuple

def present_value(discount_rate: float, cash_flows: List[float]) -> Tuple[float, str]:
    present_value = 0.0

    if discount_rate == -1:
        return (0, 'Invalid discount rate, please choose a rate other than -1')

    for idx, cash_flow in enumerate(cash_flows):
        present_value += cash_flow / ((1 + discount_rate) ** idx)
    
    return (present_value, 'The present value of the given yearly cash flows at a ' 
            + str(round(discount_rate * 100, 2)) + '% discount rate is $' 
            + str(round(present_value, 2)))