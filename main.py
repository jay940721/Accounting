import os
import budget
import expense
from datetime import date


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n歡迎使用收支紀錄系統")
        print("expe   收支")
        print("budget 預算")
        print("exit   離開")
        choice = input(">> ").strip().lower().split()

        if choice[0] == "expe":
            if len(choice) == 1:
                print("recode 記錄收支")
                print("view   查看收支")
                print("delete 刪除收支")
                choice.append(input(">> ").strip().lower())
            if choice[1] == "recode":
                include = input("此項目是否列入預算?(y/n):")
                expense.record(include)
            elif choice[1] == "view":
                expense.view()
            elif choice[1] == "delete":
                expense.delete()
            else:
                print(f"{choice[1]} 不是一個正確的選項，請重新輸入選項。")
        elif choice[0] == "budget":
            if len(choice) == 1:
                print("set  設定預算")
                print("view 查看預算")
                choice.append(input(">> ").strip().lower())
            if choice[1] == "set" :
                month = input("請輸入年份-月份(YYYY-MM): ").strip()
                budget.set_monthly_budget(month)
            elif choice[1] == "view":
                month = input("請輸入年份-月份(YYYY-MM): ").strip()
                budget.get_monthly_budget(month)
            else:
                print(f"{choice[1]} 不是一個正確的選項，請重新輸入選項。")
        elif choice[0] == "exit":
            print("再見！")
            break
        else:
            print(f"{choice[0]}不是一個正確的選項，請重新輸入選項。")


if __name__ == "__main__":
    main()
