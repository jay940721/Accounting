import os
import budget
from datetime import date

FILE_PATH = "expenses.txt"

def end_function(sentence):
    print(sentence)
    input("按任意鍵繼續...")

def record():
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
    if amount < 0:
        budget.update_budget(input_date[:7], amount)

    with open(FILE_PATH, "a") as file:
        file.write(f"{input_date},{amount},{reason}\n")

    end_function("紀錄成功！")


def view():
    if not os.path.exists(FILE_PATH):
        end_function("沒有任何支出紀錄。")
        return

    with open(FILE_PATH, "r") as file:
        expenses = file.readlines()
    if not expenses:
        end_function("沒有任何支出紀錄。")
        return

    pages = 0
    while True:
        start = pages * 10
        end = start + 10

        os.system("cls" if os.name == "nt" else "clear")

        print("No. | 日期       | 金額  | 原因")
        print("-" * 40)
        for i, line in enumerate(expenses[start:end], start=1 + start):
            try:
                date, amount, reason = line.strip().split(",")
                print(f"{i:>3} | {date} | {int(amount):>5} | {reason}")
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


def delete():
    if not os.path.exists(FILE_PATH):
        end_function("沒有任何支出紀錄可以刪除。")
        return

    with open(FILE_PATH, "r") as file:
        expenses = file.readlines()

    if not expenses:
        end_function("沒有任何支出紀錄可以刪除。")
        return

    original_expenses = expenses.copy()

    pages = 0
    while True:
        start = pages * 10
        end = start + 10
        os.system("cls" if os.name == "nt" else "clear")

        print("No. | 日期       | 金額  | 原因")
        print("-" * 40)
        for i, line in enumerate(expenses[start:end], start=1 + start):
            try:
                date, amount, reason = line.strip().split(",")
                print(f"{i:>3} | {date} | {int(amount):>5} | {reason}")
            except ValueError:
                continue

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
                for line in expenses:
                    date, amount, reason = line.strip().split(",")
                    budget.update_budget(date[:7], -int(amount))
                expenses = []
                end_function("紀錄已全部刪除。")
            else:
                end_function("已取消刪除。")
        elif choice == "exit":
            break
        elif choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(expenses):
                budget.update_budget(expenses[index - 1].strip().split(
                    ",")[0][:7], -int(expenses[index - 1].strip().split(",")[1]))
                del expenses[index - 1]
                end_function("紀錄已刪除。")
                break
            else:
                print("無效的編號，請輸入有效的編號。")
        elif choice == "next" and len(expenses) > end:
            pages += 1
        elif choice == "prev" and pages > 0:
            if not expenses:
                end_function("沒有任何支出紀錄可以刪除。")
                break

        # Write back to the file only if expenses were modified
        if expenses != original_expenses:
            with open(FILE_PATH, "w") as file:
                file.writelines(expenses)

        if not expenses:
            end_function("沒有任何支出紀錄可以刪除。")
            break



