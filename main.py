import os
import budget
import expense
from datetime import date

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n歡迎使用收支紀錄系統")
        print("recode 記錄收支")
        print("view 查看收支")
        print("delete 刪除收支")
        print("budget 預算")
        print("exit 離開")
        choice = input(">> ")

        if choice == "recode":
            expense.record()
        elif choice == "view":
            expense.view()
        elif choice == "delete":
            expense.delete()
        elif choice == "budget":
            print("set - 設定預算")
            print("view - 查看預算")
            choice = input()
            if choice == "set" :
                month = input("請輸入年份-月份(YYYY-MM): ").strip()
                budget.set_monthly_budget(month)
            elif choice == "view":
                month = input("請輸入年份-月份(YYYY-MM): ").strip()
                budget.get_monthly_budget(month)
            else:
                print(f"{choice} 不是一個正確的選項，請重新輸入選項。")
        elif choice == "exit" or choice == "quit":
            print("再見！")
            break
        else:
            print(f"{choice}不是一個正確的選項，請重新輸入選項。")


if __name__ == "__main__":
    main()
