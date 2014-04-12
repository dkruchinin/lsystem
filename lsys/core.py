class LToken(object):
    DRAW = 1
    FORWARD = 2
    TLEFT = 3
    TRIGHT = 4
    PUSH = 5
    POP = 6


class LStringParser(object):
    CONSTS = {
        'F': LToken.DRAW,
        'G': LToken.DRAW,
        'f': LToken.FORWARD,
        '+': LToken.TLEFT,
        '-': LToken.TRIGHT,
        '[': LToken.PUSH,
        ']': LToken.POP
    }

    def __init__(self, lstr):
        self._lstr = lstr
        self._pos = -1

    def first_token(self):
        self._pos = 0
        return self.next_token()

    def next_token(self):
        while self._pos < len(self._lstr):
            sym = self._lstr[self._pos]
            self._pos += 1
            if sym in self.CONSTS.keys():
                return self.CONSTS[sym]

        return None

    
class LGrammar(object):
    def __init__(self, rules):
        self._rules = rules
        self._alphabet = set(rules.keys() + LStringParser.CONSTS.keys())
        for val in self._rules.itervalues():
            self._validate_lstring(val)

    def generate(self, axiom, iters):
        self._validate_lstring(axiom)
        lstr = axiom
        for i in xrange(iters):
            lstr = self._apply_rules(lstr)

        return lstr

    def _apply_rules(self, lstr):
        res = ""
        for c in lstr:
            if c in self._rules.iterkeys():
                res += self._rules[c]
            else:
                res += c

        return res

    def _validate_lstring(self, value):
        for sym in value:
            if sym not in self._alphabet:
                raise ValueError("'%s' is neither a constant nor variable"
                                 % sym)
