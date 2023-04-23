from itertools import product

# logic ops priorities for RPN parsing
ops_priority = {'not': 0,
                'and': 1,
                'or': 2,
                '<=': 3,
                '^': 4,
                '==': 5}

expr = input()

# add spaces around brackets for correct splitting
expr = expr.replace("(", "( ")
expr = expr.replace(")", " )")
# print(expr.split())

# parse logical expression to RPN (Reverse Polish notation)
stack = []
rpn = []
for x in expr.split():

    if x.isalpha() and x.isupper():
        rpn.append(x)
    elif x == "(":
        stack.append(x)
    elif x == ")":
        while (y := stack.pop()) != '(':
            rpn.append(y)
    else:
        if x == '->':
            x = '<='
        elif x == '~':
            x = '=='

        while len(stack) > 0 and stack[-1] != '(' and ops_priority[x] >= ops_priority[stack[-1]]:
            rpn.append(stack.pop())

        stack.append(x)

# final pop of ops from stack
for _ in range(len(stack)):
    rpn.append(stack.pop())
# print("RPN:", rpn)

# parsing variables from logic expression
vars_list = sorted([x for x in set(expr.split()) if x.isupper()])

# print header with variables
print(" ".join(vars_list), 'F')

# logical expression solving with all possible binary values
for i in product([0, 1], repeat=len(vars_list)):

    values = dict(zip(vars_list, i))
    stack = []
    # RPN solving for the current combination
    for j in rpn:
        if j.isalpha() and j.isupper():  # vars
            x = str(values[j])
            stack.append(x)
        else:  # ops
            if j != 'not':
                b = stack.pop()
                a = stack.pop()
            else:
                b = stack.pop()
                a = ''

            expr = a + ' ' + j + ' ' + b
            c = str(int(eval(expr,)))
            stack.append(c)

    f = stack.pop() # binary result
    s = [str(x) for x in i]
    print(" ".join(s), f)
