
# a grammar is a dictionary of production rules
# a production rule has a left hand side (the key)
# and a right hand side

class Grammar:
    def __init__(self,rules,terminals,start):
        self.rules = rules
        self.terminals = set(terminals)
        self.start = start



def initial_item(rule,i=0):
    lhs,rhs = rule
    return (lhs,(),tuple(rhs),i)


def predictions(item,grammar):
    """Return the grammar items predicted by the first 
unprocessed symbol in item."""
    lhs,done,rest,i = item
    if rest == () or rest[0] in grammar.terminals:
        return []
    return [initial_item(rule,i) for rule in grammar.rules
            if rule[0] == rest[0]]

def scan(item):
    "Scan one unprocessed symbol in item."
    lhs,done,rest,i = item
    return (lhs,done+rest[0:1],rest[1:],i)

def completions(item,states):
    """Returns parent items associated with the given item.
Note that if item has unprocessed symbols, then there are no completions."""
    lhs,done,rest,i = item
    if rest != ():
        return []
    return [scan((x,a,b,j)) for (x,a,b,j) in states[i]
            if b != [] and b[0] == lhs]

def earley_table(grammar,string):
    states = []
    items = []
    next_items = [initial_item(rule) for rule in grammar.rules
                  if rule[0] == grammar.start]
    for i in range(len(string)):
        items,next_items = next_items,[]
        state = set()
        j = 0
        while j < len(items):
            lhs,a,b,k = item = items[j]
            if item not in state:
                if b == ():
                    items += completions(item,states)
                else:
                    if b[0] in grammar.terminals and b[0] == string[i]:
                        next_items.append(scan(item))
                    else:
                        items += predictions(item,grammar)
                state.add(item)
            j += 1
        states.append(state)
    return states

def itemstring(item):
    lhs,a,b,i = item
    rep = "(%d) %-12s -> %s . %s" % (i,lhs,' '.join(a),' '.join(b))
    return rep

def print_states(states):
    for i,state in enumerate(states):
        print("=== %d ===" % i)
        for item in state:
            print(itemstring(item))
        print("")

def test():
    rule = ("a",["b"])
    assert(initial_item(rule) == ("a",(),("b",),0))
    assert(initial_item(("a",["bcd"])) == ("a", (), ("bcd",), 0))
    item = ("a",(),("b",),0)
    assert(scan(item) == ("a",("b",),(),0))

    rule2 = ("b", ["0"])
    simple_grammar = Grammar([rule,rule2],"0","a")
    assert(predictions(item,simple_grammar) == [('b',(),('0',),0)])
    assert(predictions(('b',(),('0',),0),simple_grammar) == [])

    i1,i2 = initial_item(rule), initial_item(rule2)
    i3 = scan(i2)
    states = [[i1,i2], [i3]]
    assert(completions(i3,states) == [('a',('b',),(),0)])
    
    return "tests passed!"

rules = [('sum', ('sum', '+', 'product')),
         ('sum', ('product',)),
         ('product', ('product', '*', 'factor')),
         ('product', ('factor',)),
         ('factor', ('(', 'sum', ')')),
         ('factor', ('number',)),
         ('number', ('0',)),
         ('number', ('1',))]


terminals = "01"

start_state = 'sum'

simple_grammar = Grammar(rules,terminals,start_state)
