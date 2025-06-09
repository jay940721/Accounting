from datetime import date
BUDGET_FILE = "monthly_budgets.txt"


def set_monthly_budget(month):
    if month is "":
        month = date.today().strftime("%Y-%m")
    else:
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

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    new_lines = [line for line in lines if not line.startswith(month)]
    new_lines.append(f"{month},{budget},{budget}\n")
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"{month} 的預算已設定為 {budget} 元")
    input("按任意鍵繼續...")


def update_budget(month, amount):
    year, month = month.split("-")
    if not (year.isdigit() and month.isdigit() and 1 <= int(month) <= 12):
        print("月份輸入錯誤，請使用 YYYY-MM 格式")
        return None
    month = f"{year}-{int(month):02d}"

    updated = False
    with open(BUDGET_FILE, "r", encoding="utf-8") as f:
        budgets = f.readlines()
    new_budgets = []
    for line in budgets:
        if line.startswith(month):
            year_month, total, budget_amount = line.strip().split(",")
            budget_amount = float(budget_amount)
            new_amount = budget_amount + amount
            if amount >0:
                total += amount
            if new_amount < 0 and amount > 0:
                print(f"警告: {year_month} 的預算已超支！")
            new_budgets.append(f"{year_month},{total},{new_amount}\n")
            updated = True
        else:
            new_budgets.append(line)
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_budgets)
        if updated:
            print(f"{month} 的預算剩餘 {new_amount} 元")
        else:
            f.write(f"{month},0,{amount}\n")


def get_monthly_budget(month):
    year, month = month.split("-")
    if not (year.isdigit() and month.isdigit() and 1 <= int(month) <= 12):
        print("月份輸入錯誤，請使用 YYYY-MM 格式")
        return
    month = f"{year}-{int(month):02d}"

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(month):
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        print(f"{month} 的預算為 {parts[1]} 元，剩餘 {parts[2]} 元")
                        input("按任意鍵繼續...")
                        return
        print(f"{month} 尚未設定預算")
        return
    except FileNotFoundError:
        print("預算檔案不存在")
        return
