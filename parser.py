
# a grammar is a dictionary of production rules
# a production rule has a left hand side (the key)
# and a right hand side

class Grammar:
    def __init__(self,rules,terminals,start):
        self.rules = rules
        self.terminals = set(terminals)
        self.start = start



rules = [("sum", ["sum", "+", "product"]),
         ("sum", ["product"]),
         ("product", ["product", "*", "factor"]),
         ("product", ["factor"]),
         ("factor", ["(", "sum", ")"]),
         ("factor", ["number"]),
         ("number", ["0"]),
         ("number", ["1"])]

terminals = "+*01"

start = "sum"

simple_grammar = Grammar(rules,terminals,start)


def initial_item(rule,i=0):
    lhs,rhs = rule
    return (lhs,[],rhs,i)


def predictions(item,grammar):
    lhs,done,rest,i = item
    if rest == [] or rest[0] in grammar.terminals:
        return []
    return [initial_item(rule,i) for rule in grammar.rules
            if rule[0] == rest[0]]


def test():
    rule = ("a",["b"])
    assert(initial_item(rule) == ("a",[],["b"],0))
    return "tests passed!"
