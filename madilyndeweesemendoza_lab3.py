# Madilyn Deweese-mendoza Lab 3

def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*':
        return 2
    else:
        return 0
    
def infix_to_postfix(infix):
    stack = []
    output = []
    tokens = infix.split()

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() #remove '('
        else: #operator
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())
    
    return ' '.join(output)

def infix_to_prefix(infix):
    tokens = infix.split()
    tokens.reverse()

    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i] = ')'
        elif tokens[i] == ')':
            tokens[i] = '('
    
    #convert to postfix of the reversed expression
    reversed_infix = ' '.join(tokens)
    reversed_postfix = infix_to_postfix(reversed_infix)

    #reverse the result to get prefix
    prefix_tokens = reversed_postfix.split()
    prefix_tokens.reverse()

    return ' '.join(prefix_tokens)


def evaluate_postfix(postfix):
    stack = []
    tokens = postfix.split()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a+b)
            elif token == '-':
                stack.append(a-b)
            elif token == '*':
                stack.append(a*b)
    
    return stack[0]

def evaluate_prefix(prefix):
    stack = []
    tokens = prefix.split()
    tokens.reverse()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            a = stack.pop()
            b = stack.pop()
            if token == '+':
                stack.append(a+b)
            elif token == '-':
                stack.append(a-b)
            elif token == '*':
                stack.append(a*b)

    return stack[0]
    
if __name__ == "__main__":
    infix_expr = input("Enter an infix expression: ")

    postfix = infix_to_postfix(infix_expr)
    prefix = infix_to_prefix(infix_expr)
    postfix_result = evaluate_postfix(postfix)
    prefix_result = evaluate_prefix(prefix)

    print(f"Postfix: {postfix}")
    print(f"Prefix: {prefix}")
    print(f"Postfix Evaluation Result: {postfix_result}")
    print(f"Prefix Evaluation Result: {prefix_result}")






