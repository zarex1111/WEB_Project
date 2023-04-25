try:
    a = input()
    b = int(input())
    print(a * b)
except Exception as exc:
    print(exc.__class__.__name__)