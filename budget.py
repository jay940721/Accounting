# 設定每月預算
def set_monthly_budget(month):
    budget = input(f"請輸入 {month} 的預算金額: ")
    try:
        budget = float(budget)
        if budget < 0:
            raise ValueError("預算不能為負數")
    except ValueError as e:
        print(f"無效的預算金額: {e}")
        return None
    with open("monthly_budgets.txt", "a", encoding="utf-8") as f:
        f.write(f"{month},{budget}\n")
    print(f"{month} 的預算已設定為 {budget} 元")