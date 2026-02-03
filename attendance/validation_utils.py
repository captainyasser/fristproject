from datetime import timedelta
from .models import Attendance

def validate_attendance(employee, attendance_map, start_date, num_days):
    """
    Validates attendance for a single employee based on 7 rules.
    attendance_map: dict { date_obj: attendance_obj } containing history relative to check period.
    Returns: list of error strings.
    """
    errors = set()
    
    # Define codes based on rules
    REST_CODES = ['راحة', 'ر بديلة'] # Rule 3 specific
    VACATION_CODES = ['راحة', 'ر بديلة', 'عطلة', 'منحة', 'اجازه'] # Rule 4 - assuming comprehensive list
    MISSION_CODES = ['مأمورية', 'مأمورية خ', 'فرقة', 'انتداب', 'خاصه', 'مرضي', 'ج وضع'] # Rule 4 triggers (plus Absence handled separately) - Adding 'خاصه', 'مرضي'
    ABSENCE_CODES = ['غياب']
    EMERGENCY_CODES = ['طارئة']
    SHIFT_CODES = ['نوبتجي']
    DAILY_CODES = ['يومي']
    ALLOWED_AFTER_ABSENCE = SHIFT_CODES + DAILY_CODES # Rule 5: Shift or "Two Days"(Daily)
    ALLOWED_AFTER_EMERGENCY = EMERGENCY_CODES + DAILY_CODES + SHIFT_CODES # Rule 6: Emergency, Daily, Attendance(Shift)
    
    date_list = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # State tracking for cumulative error reporting
    max_consecutive_rest = 0
    
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
                    errors.add("لا يجوز أكثر من يومين طارئة متتالية")

        # Rule 2: No Rest/Alt Rest after Patrol ('دورية') or Emergency
        if state in REST_CODES:
            if prev_state in ['دورية'] + EMERGENCY_CODES:
               errors.add("لا يجوز راحة بعد دورية أو طارئة")

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

        # Rule 4: No Vacation after Mission/Delegation/Special/Sick/Absence
        # Note: Rule 5 handles Absence more strictly. Rule 4 applies to others.
        # "Special" = 'خاصه', "Sick" = 'مرضي'
        if state in VACATION_CODES:
            if prev_state in MISSION_CODES:
                 errors.add("لا يجوز أجازة بعد فرقة/انتداب/خاصة/مرضي") # Combined msg or specific?
            elif prev_state in ABSENCE_CODES:
                 # Rule 5 covers this generally, but let's add specific Rule 4 msg if needed
                 pass 

        # Rule 5: After Absence, only Shift or 'Two Days'(Daily) allowed
        if prev_state in ABSENCE_CODES:
            if state not in ALLOWED_AFTER_ABSENCE:
                 errors.add("لا يجوز بعد الغياب إلا حضور")

        # Rule 6: Emergency followed only by Emergency (max 2), Daily, or Attendance(Shift)
        if prev_state in EMERGENCY_CODES and state not in ALLOWED_AFTER_EMERGENCY:
             errors.add("الطارئة لا يعقبها إلا حضور أو غياب")

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
                     errors.add(f"لا يجوز راحة الجمعة (العمل اليومي أقل من 4 أيام هذا الأسبوع)") # Removed count from message to uniqueness

    # Post loop: Add max violation for rest
    if max_consecutive_rest > 4:
         errors.add(f"لا يجوز أكثر من 4 أيام راحة متتالية (العدد الحالي: {max_consecutive_rest})")

    return sorted(list(errors))
