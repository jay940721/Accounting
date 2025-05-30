import os
import budget
from datetime import date

FILE_PATH = "expenses.txt"

CLEAR_SCREEN_ENABLED = True


def clear_screen():
    if CLEAR_SCREEN_ENABLED:
        os.system("cls" if os.name == "nt" else "clear")


def record_expense():
    while True:
        amount = input("輸入金額(支出為負數): ")
        try:
            amount = int(amount)
            break
        except ValueError:
            print("無效的金額，請輸入一個數字。")
    reason = input("輸入原因: ").strip()
    if not reason:
        reason = "(無原因)"
    
    input_date = ""
    while True:
        input_date = input("輸入日期 (YYYY-MM-DD) 或留空紀錄為本日: ").strip()
        if not input_date:
            input_date = date.today().strftime("%Y-%m-%d")
            break
        try:
            input_date = date.fromisoformat(input_date).strftime("%Y-%m-%d")
            break
        except ValueError:
            print("無效的日期格式或日期，請輸入有效的日期 (YYYY-MM-DD)。")
    with open(FILE_PATH, "a") as file:
        file.write(f"{input_date},{amount},{reason}\n")

    if amount < 0:
        budget.update_budget(input_date, amount)
        
    print("紀錄成功！")


def view_expenses():
    if not os.path.exists(FILE_PATH):
        print("沒有任何支出紀錄。")

    with open(FILE_PATH, "r") as file:
        expenses = file.readlines()
    if not expenses:
        print("沒有任何支出紀錄。")
        return

    pages = 0
    while True:
        start = pages * 10
        end = start + 10
        if CLEAR_SCREEN_ENABLED:
            clear_screen()

        print("No. | 日期       | 金額 | 原因")
        print("-" * 40)
        for i, line in enumerate(expenses[start:end], start=1 + start):
            try:
                date, amount, reason = line.strip().split(",")
                print(f"{i:>3} | {date} | {amount} | {reason}")
            except ValueError:
                print(f"{i:>3} | 格式錯誤的紀錄: {line.strip()}")
                print(f"{i:>3} | {date} | {amount} | {reason}")
            except ValueError:
                print(f"{i:>3} | [格式錯誤的紀錄，無法解析]")

        print("\n 選項:")
        if len(expenses) > end:
            print("next - 顯示下一頁")
        if pages > 0:
            print("prev - 顯示上一頁")
        print("exit - 退出")
        choice = input("請選擇一個選項: ").strip().lower()
        if choice == "next" and len(expenses) > end:
            pages += 1
        elif choice == "prev" and pages > 0:
            pages -= 1
        elif choice == "exit":
            break
        else:
            print(f"{choice}不是一個正確的選項，請重新輸入選項。")


def delete_expenses():
    if not os.path.exists(FILE_PATH):
        print("沒有任何支出紀錄可以刪除。")
        return

    with open(FILE_PATH, "r") as file:
        expenses = file.readlines()

    if not expenses:
        print("沒有任何支出紀錄可以刪除。")
        return

    original_expenses = expenses.copy()

    pages = 0
    while True:
        start = pages * 10
        end = start + 10
        clear_screen()

        print("No. | 日期       | 金額 | 原因")
        print("-" * 40)
        for i, line in enumerate(expenses[start:end], start=1 + start):
            date, amount, reason = line.strip().split(",")
            print(f"{i:>3} | {date} | {amount} | {reason}")

        print("\n 選項:")
        if len(expenses) > end:
            print("next - 顯示下一頁")
        if pages > 0:
            print("prev - 顯示上一頁")
        print("(編號) - 刪除指定編號的紀錄")
        print("clear - 刪除所有紀錄")
        print("exit - 退出")

        choice = input("請選擇一個選項: ").strip().lower()

        if choice == "clear":
            confirm = input("這會刪除全部紀錄，你確定嗎？(y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                expenses = []
                print("紀錄已全部刪除。")
            else:
                print("已取消刪除。")
        elif choice == "exit":
            break
        elif choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(expenses):
                del expenses[index - 1]
                print("紀錄已刪除。")
                break
            else:
                print("無效的編號，請輸入有效的編號。")
        elif choice == "next" and len(expenses) > end:
            pages += 1
        elif choice == "prev" and pages > 0:
            if not expenses:
                print("沒有任何支出紀錄可以刪除。")
                break

        # Write back to the file only if expenses were modified
        if expenses != original_expenses:
            with open(FILE_PATH, "w") as file:
                file.writelines(expenses)

        if not expenses:
            print("沒有任何支出紀錄可以刪除。")
            break


def main():
    while True:
        if CLEAR_SCREEN_ENABLED:
            clear_screen()
        print("\n歡迎使用收支紀錄系統")
        print("recode 記錄收支")
        print("view 查看收支")
        print("delete 刪除收支")
        print("budget 設定預算")
        print("exit 離開")
        choice = input("請選擇一個選項: ")

        if choice == "recode":
            record_expense()
        elif choice == "view":
            view_expenses()
        elif choice == "delete":
            delete_expenses()
        elif choice == "budget":
            month = input("請輸入年份-月份(YYYY-MM): ").strip()
            budget.set_monthly_budget(month)
        elif choice == "exit" or choice == "quit":
            print("再見！")
            break
        else:
            print("無效的選項，請重新輸入。")


if __name__ == "__main__":
    main()
