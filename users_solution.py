try:
    a = input()
    if a == 'poka':
         print('privet')
    else:
          print('privet')
except Exception as exc:
    print(exc.__class__.__name__)