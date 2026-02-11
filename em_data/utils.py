from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_next_promotion(employee):
    # Get the latest promotion
    latest_promotion = employee.promotions.order_by('-promotion_date').first()
    
    if latest_promotion:
        to_rank_id = latest_promotion.to_rank_id
        promotion_date = latest_promotion.promotion_date
    else:
        to_rank_id = employee.rank.id if employee.rank else None
        promotion_date = employee.date_of_appointment # Fallback if no promotions recorded
    
    next_promotion_date = None
    
    if not promotion_date and not latest_promotion:
        return None

    # Logic from tarkyat/views.py
    if to_rank_id in [2, 3, 4, 5, 6]:
        next_promotion_date = promotion_date + relativedelta(years=6)
    elif to_rank_id == 1:
        next_promotion_date = None
    elif to_rank_id == 10:
        next_promotion_date = promotion_date + relativedelta(years=4)
    elif to_rank_id in [8, 9]:
        next_promotion_date = promotion_date + relativedelta(years=5)
    elif to_rank_id == 7:
        next_promotion_date = None
    elif to_rank_id in [19, 20, 21, 22]:
        next_promotion_date = promotion_date + relativedelta(years=4)
    elif to_rank_id in [24, 25, 26, 27, 28]:
        next_promotion_date = promotion_date + relativedelta(years=6)
    elif to_rank_id == 23:
        next_promotion_date = None
    else:
        next_promotion_date = None
    
    # Adjust to June 1 or Dec 1
    if next_promotion_date:
        year = next_promotion_date.year
        month = next_promotion_date.month
        day = next_promotion_date.day
        
        june_1 = date(year, 6, 1)
        december_1 = date(year, 12, 1)
        
        if not (month == 6 and day == 1) and not (month == 12 and day == 1):
            if next_promotion_date < june_1:
                next_promotion_date = june_1
            elif june_1 <= next_promotion_date < december_1:
                next_promotion_date = december_1
            else:
                next_promotion_date = date(year + 1, 6, 1)
                
    return next_promotion_date
