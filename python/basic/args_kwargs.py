def order(size, *args, **kwargs):
    print(size)
    print(args)
    print(kwargs)
order('big', 'apple', 'cheery', banana='2', orange = '4')