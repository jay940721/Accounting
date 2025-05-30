BUDGET_FILE = "monthly_budgets.txt"
# 設定每月預算
def set_monthly_budget(month):
    year, month = month.split("-")
    if not (year.isdigit() and month.isdigit() and 1 <= int(month) <= 12):
        print("月份輸入錯誤，請使用 YYYY-MM 格式")
        return None
    month = f"{year}-{int(month):02d}"
    
    budget = input(f"請輸入 {month} 的預算金額: ")
    try:
        budget = float(budget)
        if budget < 0:
            raise ValueError("預算不能為負數")
    except ValueError as e:
        print(f"無效的預算金額: {e}")
        return None
    with open(BUDGET_FILE, "a", encoding="utf-8") as f:
        f.write(f"{month},{budget},{budget}\n")
    print(f"{month} 的預算已設定為 {budget} 元")