import math


#------------- EASING FUNCTIONS --------------------


def linear(t): return t

def ease_in_quad(t): return t * t
def ease_out_quad(t): return t * (2 - t)
def ease_in_out_quad(t): return 2*t*t if t < 0.5 else -1 + (4 - 2*t)*t

def ease_in_cubic(t): return t * t * t

def ease_in_out_cubic(t): return 4*t*t*t if t < 0.5 else (t-1)*(2*t-2)**2 + 1


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_out_quad(t):
    return 2*t*t if t < 0.5 else -1 + (4 - 2*t)*t

def ease_out_bounce(t):
    n1, d1 = 7.5625, 2.75
    if t < 1/d1:     return n1 * t * t
    elif t < 2/d1:   t -= 1.5/d1;   return n1*t*t + 0.75
    elif t < 2.5/d1: t -= 2.25/d1;  return n1*t*t + 0.9375
    else:            t -= 2.625/d1; return n1*t*t + 0.984375

def tween(style,value):
    val=None
    if style=="linear":
        val = linear(value)
    elif style=="ease_in_quad":
        val=ease_in_quad(value)
    elif style=="ease_out_quad":
        val=ease_out_quad(value)
    elif style=="ease_in_out_quad":
        val=ease_in_out_quad(value)
    elif style=="ease_in_cubic":
        val=ease_in_cubic(value)
    elif style=="ease_in_out_cubic":
        val=ease_in_quad(value)
    elif style=="ease_out_cubic":
        val=ease_out_cubic(value)
    elif style=="ease_out_bounce":
        val=ease_out_bounce(value)
    else:
        print("No style selected going lienar")
        val = linear(value)
    #print(val)
    return val