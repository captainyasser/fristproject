from datetime import timedelta
from .models import Attendance

def validate_attendance(employee, attendance_map, start_date, num_days):
    """
    Validates attendance for a single employee based on 7 rules.
    attendance_map: dict { date_obj: attendance_obj } containing history relative to check period.
    Returns: list of error dicts with 'date' and 'message'.
    """
    errors = []
    
    # Define codes based on rules
    REST_CODES = ['راحة', 'ر بديلة'] # Rule 3 specific
    PATROL_CODES = ['دورية'] # Rule 4 - Patrol codes
    MISSION_CODES = ['مأمورية', 'مأمورية خ', 'فرقة', 'انتداب', 'خاصه', 'مرضي', 'ج وضع'] # Rule 4 triggers
    ABSENCE_CODES = ['غياب']
    EMERGENCY_CODES = ['طارئة']
    SHIFT_CODES = ['نوبتجي']
    DAILY_CODES = ['يومي']
    ALLOWED_AFTER_ABSENCE = SHIFT_CODES + DAILY_CODES + ABSENCE_CODES # Rule 5: Shift, Daily, or Absence
    ALLOWED_AFTER_EMERGENCY = EMERGENCY_CODES + DAILY_CODES + SHIFT_CODES + ABSENCE_CODES # Rule 6: Emergency, Daily, Shift, or Absence

    
    date_list = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # State tracking for cumulative error reporting
    max_consecutive_rest = 0
    max_consecutive_rest_date = None
    
    for current_date in date_list:
        if current_date not in attendance_map:
            continue
            
        current_att = attendance_map[current_date]
        state = current_att.state
        
        # Get previous dates logic
        prev_date = current_date - timedelta(days=1)
        prev_att = attendance_map.get(prev_date)
        prev_state = prev_att.state if prev_att else '_'
        
        # Rule 1: No more than 2 consecutive Emergency (max 2)
        # Check if today is Emergency, yesterday was Emergency, and day before was Emergency
        if state in EMERGENCY_CODES:
            if prev_state in EMERGENCY_CODES:
                before_prev_date = current_date - timedelta(days=2)
                before_prev_att = attendance_map.get(before_prev_date)
                before_prev_state = before_prev_att.state if before_prev_att else '_'
                if before_prev_state in EMERGENCY_CODES:
                    errors.append({
                        'date': current_date,
                        'message': "لا يجوز أكثر من يومين طارئة متتالية"
                    })

        # Rule 2: No Rest/Alt Rest after Patrol ('دورية') or Emergency
        if state in REST_CODES:
            if prev_state in PATROL_CODES + EMERGENCY_CODES:
                errors.append({
                    'date': current_date,
                    'message': "لا يجوز راحة بعد دورية أو طارئة"
                })

        # Rule 3: No more than 4 days Rest (Rest + Alt Rest)
        if state in REST_CODES:
            consecutive_rest = 1
            # Look back
            check_date = prev_date
            while True:
                existing_att = attendance_map.get(check_date)
                if existing_att and existing_att.state in REST_CODES:
                    consecutive_rest += 1
                    check_date -= timedelta(days=1)
                else:
                    break
            
            if consecutive_rest > 4:
                # Update global max for this period
                if consecutive_rest > max_consecutive_rest:
                    max_consecutive_rest = consecutive_rest
                    max_consecutive_rest_date = current_date
                    max_consecutive_rest_date = current_date

        # Rule 4: No Patrol after Mission/Delegation/Special/Sick
        if state in PATROL_CODES:
            if prev_state in MISSION_CODES:
                errors.append({
                    'date': current_date,
                    'message': "لا يجوز دورية بعد فرقة/انتداب/خاصة/مرضي"
                })
 

        # Rule 5: After Absence, only Shift or 'Two Days'(Daily) allowed
        if prev_state in ABSENCE_CODES:
            if state not in ALLOWED_AFTER_ABSENCE:
                errors.append({
                    'date': current_date,
                    'message': "لا يجوز بعد الغياب إلا حضور"
                })

        # Rule 6: Emergency followed only by Emergency (max 2), Daily, or Attendance(Shift)
        if prev_state in EMERGENCY_CODES and state not in ALLOWED_AFTER_EMERGENCY:
            errors.append({
                'date': current_date,
                'message': "الطارئة لا يعقبها إلا حضور أو غياب"
            })

        # Rule 7: If operation is Daily, Friday cannot be Rest if worked < 4 Daily days in week (Sat-Thu)
        # Check if today is Friday
        if current_date.weekday() == 4: # Friday is 4 in Python? 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
            # Wait, standard Python weekday: Mon=0, Sun=6.
            # So Friday=4.
            # User phrase: "Week from Saturday to Sunday".
            # Standard week for "Daily" operation usually ends on Friday (Rest).
            # Work days: Sat, Sun, Mon, Tue, Wed, Thu.
            # We need to count 'Daily' states in these 6 days.
            
            if employee.operation == 'يومي' and state in ['راحة']: # Assuming Friday Rest is marked as 'راحة'
                # Count daily days from previous Saturday up to Thursday
                # Start of week (Saturday) relative to this Friday
                # Friday is index 4. Saturday (start of week) is prev Ind 5 (6 days ago).
                week_start_sat = current_date - timedelta(days=6)
                dw_count = 0
                for d in range(6): # 0 to 5 (Sat to Thu)
                    d_date = week_start_sat + timedelta(days=d)
                    d_att = attendance_map.get(d_date)
                    if d_att and d_att.state in DAILY_CODES:
                        dw_count += 1
                
                if dw_count < 4:
                    errors.append({
                        'date': current_date,
                        'message': f"لا يجوز راحة الجمعة (العمل اليومي أقل من 4 أيام هذا الأسبوع)"
                    })

    # Post loop: Add max violation for rest
    if max_consecutive_rest > 4 and max_consecutive_rest_date:
        errors.append({
            'date': max_consecutive_rest_date,
            'message': f"لا يجوز أكثر من 4 أيام راحة متتالية (العدد الحالي: {max_consecutive_rest})"
        })

    return errors


def check_operation_compliance(employee, attendance_map, start_date, num_days):
    """
    Checks if attendance state matches the expected state based on employee operation.
    Returns: list of error dicts with 'date' and 'message'.
    """
    errors = []
    
    # Define rules
    # Operation 'السبت'
    op_sat_rules = {
        5: 'نوبتجي', 6: 'نوبتجي', 0: 'نوبتجي',
        1: 'يومي',
        2: 'راحة', 3: 'راحة', 4: 'راحة'
    }
    # Operation 'الأحد'
    op_sun_rules = {
        6: 'نوبتجي', 0: 'نوبتجي', 1: 'نوبتجي',
        2: 'يومي',
        3: 'راحة', 4: 'راحة', 5: 'راحة'
    }
    # Operation 'الاثنين'
    op_mon_rules = {
        0: 'نوبتجي', 1: 'نوبتجي', 2: 'نوبتجي',
        3: 'يومي',
        4: 'راحة', 5: 'راحة', 6: 'راحة'
    }
    # Operation 'الثلاثاء'
    op_tue_rules = {
        1: 'نوبتجي', 2: 'نوبتجي', 3: 'نوبتجي',
        4: 'يومي',
        5: 'راحة', 6: 'راحة', 0: 'راحة'
    }
    # Operation 'الأربعاء'
    op_wed_rules = {
        2: 'نوبتجي', 3: 'نوبتجي', 4: 'نوبتجي',
        5: 'يومي',
        6: 'راحة', 0: 'راحة', 1: 'راحة'
    }
    # Operation 'الخميس'
    op_thu_rules = {
        3: 'نوبتجي', 4: 'نوبتجي', 5: 'نوبتجي',
        6: 'يومي',
        0: 'راحة', 1: 'راحة', 2: 'راحة'
    }
    # Operation 'الجمعة'
    op_fri_rules = {
        4: 'نوبتجي', 5: 'نوبتجي', 6: 'نوبتجي',
        0: 'يومي',
        1: 'راحة', 2: 'راحة', 3: 'راحة'
    }
    
    rules_map = {
        'السبت': op_sat_rules,
        'الأحد': op_sun_rules,
        'الاثنين': op_mon_rules,
        'الثلاثاء': op_tue_rules,
        'الأربعاء': op_wed_rules,
        'الخميس': op_thu_rules,
        'الجمعة': op_fri_rules,
        'انتداب': 'انتداب',
        'خاصه': 'خاصه',
        'ج وضع': 'ج وضع',
        'قرار66': 'قرار66',
        'مرضي': 'مرضي',
    }
    
    date_list = [start_date + timedelta(days=i) for i in range(num_days)]
    
    rule = rules_map.get(employee.operation)
    if not rule:
        return [] # No rule for this operation
        
    for current_date in date_list:
        if current_date not in attendance_map:
            continue
            
        current_att = attendance_map[current_date]
        actual_state = current_att.state
        
        day_of_week = current_date.weekday()
        expected_state = None
        
        if isinstance(rule, dict):
            expected_state = rule.get(day_of_week)
        elif isinstance(rule, str):
            expected_state = rule
            
        if not expected_state:
            continue
            
        if actual_state != expected_state:
            # Special case: 'قرار66' and 'مرضي' are treated as equivalent (Sick)
            is_sick_equivalent_expected = expected_state in ['قرار66', 'مرضي']
            is_sick_equivalent_actual = actual_state in ['قرار66', 'مرضي']
            
            if is_sick_equivalent_expected and is_sick_equivalent_actual:
                continue # Treated as valid match
                
            errors.append({
                'date': current_date,
                'message': f"({expected_state})"
            })
            
    return errors
