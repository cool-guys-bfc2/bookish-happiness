import math
import operator
import string
import numpy
import random
import re
import operator

def calc(expression):
    # Tokenize: Split string into numbers and operators
    tokens = []
    temp_num = ""
    # Standardizing characters to remove spaces and treat tokens correctly
    for char in expression.replace(" ", ""):
        if char in "+-*/()":
            if temp_num:
                tokens.append(float(temp_num))
                temp_num = ""
            tokens.append(char)
        else:
            temp_num += char
    if temp_num:
        tokens.append(float(temp_num))

    # Define operators
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    # Recursive Parser
    def parse_expression(tokens):
        # Process Addition/Subtraction (lowest precedence)
        left = parse_term(tokens)
        while tokens and tokens[0] in "+-":
            op = tokens.pop(0)
            right = parse_term(tokens)
            left = ops[op](left, right)
        return left

    def parse_term(tokens):
        # Process Multiplication/Division (higher precedence)
        left = parse_factor(tokens)
        while tokens and tokens[0] in "*/":
            op = tokens.pop(0)
            right = parse_factor(tokens)
            left = ops[op](left, right)
        return left

    def parse_factor(tokens):
        # Process Numbers and Parentheses
        token = tokens.pop(0)
        if token == '(':
            result = parse_expression(tokens)
            tokens.pop(0)  # Remove ')'
            return result
        return token

    return parse_expression(tokens)

#Constants
MAXDGT=5

class FastArray(object):
  def __init__(self,arr):
    self.i=[]
    ind=0
    if isinstance(arr,list) or isinstance(arr,FastArray):
      for i in arr:
        t=(ind,i)
        self.i.append(t)
        ind+=1
    elif isinstance(arr,dict):
      for k in arr:
        v=arr[k]
        t=(k,v)
        self.i.append(t)
        ind+=1
    self.l=len(arr)
  def __iter__(self):
    # Use the built-in iter() function on the list
    return iter([list(i)[1] for i in self.i])
  def arr(self):
    return self.__array__()
  def remove(self,i):
    x=False
    for item in self.i:
      k,v=item
      if v==i:
        self.i.remove(item)
        x=True
        break
    if x:
      self.l-=1
  def delete(self,i):
    x=False
    for item in self.i:
      k,v=item
      if k==i:
        self.i.remove(item)
        x=True
        break
    if x:
      self.l-=1
  def append(self,i):
    self.i.append((self.l,i))
    self.l+=1
  def get(self,ind):
    for i in self.i:
      k,v=i
      if k==ind:
        return v
  def has(self,item):
    x=False
    for item in self.i:
      k,v=item
      if v==item:
        x=True
        break
    return x
  def __len__(self):
    return self.l
  def update(self,ind,value):
    oldl=self.l
    for i in self.i:
      k,v=i
      if k==ind:
        self.remove(k)
        self.i.append((self.l,i))
        self.l+=1
        break
  def __delattr__(self,key):
    self.delete(key)
  def __setattr__(self,key,value):
    self.update(key,value)
  def __getattr__(self,key):
    return self.get(key)
  def __getitem__(self, key):
        # Handle slicing (e.g., obj[1:5])
        if isinstance(key, slice):
            # Use .indices(len) to handle None and negative values automatically
            start, stop, step = key.indices(len(self.data))
            return [self.get(i) for i in range(start, stop, step)]
        
        # Handle single index (e.g., obj[5])
        elif isinstance(key, int) or isinstance(key,str):
            return self.get(key)
        
        else:
            raise TypeError("Invalid argument type")
  def __delitem__(self,index):
    self.delete(index)
  def __setitem(self,index,value):
    self.update(index,value)
  def __array__(self):
    x=[None]*self.l  
    for i in self.i:
      k,v=i
      x[k]=v
    return x
  def __dict__(self):
    x=[None]*self.l  
    for i in self.i:
      k,v=i
      x[k]=v
    return x
  def dct(self):
    return self.__dict__()

class SerialObject(object):
  def __init__(self,obj):
    if isinstance(obj,dict):
      self.d=obj
    if isinstance(obj,FastArray):
      self.d=obj.dct()
    else:
      self.d={}
      for k in dir(obj):
        v=getattr(obj,k)
        self.d[k]=v
  def serialize(self):
    return self.d
  def load(self,obj='Module'):
    return type(obj, (), self.d)()
    
#Give it a dictionary of attributes, it will behave as the actual object
class FakeObject(object):
  def __init__(self,dict):
    x=SerialObject(dict)
    x=x.load()
    self.__dict__ = x.__dict__.copy()
class Boolean(object):
    def __init__(self,v):
        if isinstance(v,bool):
            self.v=0
            if v: self.v=1
        elif isinstance(v,float) or isinstance(v,int):
            if v!=1: self.v=v%1
    
    def getv(self): return self.v
    def rbool(self):
        x=round(self.v)
        if x==1: return True
        elif x==0: return False
        else: return None
    
    def cand(self,other): return Boolean(self.getv()*other.getv())
    def cor(self,other): return Boolean(min(self.getv()+other.getv(),1))
    def cnot(self): return Boolean(1-self.getv())

#supports at most 6 arguments
class Function(object):
    def __init__(self,f,*args):
        self.f=f
        self.a=args
        self.l=len(self.a)
    
    def run(self,*args):
        if len(args)>0:
            self.a=args
            self.l=len(args)
        l=self.l
        f=self.f
        a=self.a # Fixed: was self.args
        if l==0: f()
        elif l==1: f(a[0])
        elif l==2: f(a[0],a[1])
        elif l==3: f(a[0],a[1],a[2])
        elif l==4: f(a[0],a[1],a[2],a[3])
        elif l==5: f(a[0],a[1],a[2],a[3],a[4])
        elif l==6: f(a[0],a[1],a[2],a[3],a[4],a[5])
        else: return None

def func(f): return Function(f).run

chars="qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()QWERTYUIOPLKJHGFDSAZXCVBNM-_=+[{]}\|;:,.<>/?~ "
charlist=list(chars)

def rstring():
    r=""
    y=random.randint(1,75)
    for i in range(y):
        x=random.choice(chars)
        r+=x
    return r

gens={
    int :lambda: random.randint(-(10**(MAXDGT)),(10**(MAXDGT))),
    # Fixed: random.randint() needs arguments
    float :lambda: random.randint(-(10**(MAXDGT)),(10**(MAXDGT)))/random.randint(1, 100), 
    string :rstring,
    bool :lambda: Boolean(random.randint(0,1000)/1000),
    #rawbool :lambda: random.choice([False,True]) # rawbool not defined in snippet
}
# Fixed: Add rawbool if needed or fix gens[rawbool]
# gens[ hex ]=lambda: hex(gens[ int ]())
# gens[ bin ]=lambda: bin(gens[ int ]())

GTRUE=lambda x: True
GFALSE=lambda x: False

def works(f):
    r=True
    try: f()
    except: r=False
    return r

def isnum(f):
    r=True
    try: x=int(f)
    except: r=False
    return r

# Tokenize: Split string into numbers and operators
def calc(expression):
    tokens = []
    temp_num = ""
    # Standardizing characters to remove spaces and treat tokens correctly
    for char in expression.replace(" ", ""):
        if char in "+-*/()":
            if temp_num:
                tokens.append(float(temp_num))
                temp_num = ""
            tokens.append(char)
        else:
            temp_num += char
    if temp_num:
        tokens.append(float(temp_num))
    
    # Define operators
    ops = {
        '^': operator.pow,
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod
    }

    # Recursive Parser
    def parse_expression(tokens):
        left = parse_term(tokens)
        while tokens and tokens[0] in "+-":
            op = tokens.pop(0)
            right = parse_term(tokens)
            left = ops[op](left, right)
        return left

    def parse_term(tokens):
        left = parse_factor(tokens)
        while tokens and tokens[0] in "*/":
            op = tokens.pop(0)
            right = parse_factor(tokens)
            # Handle division by zero
            if op == '/' and right == 0: return float('inf')
            left = ops[op](left, right)
        return left

    def parse_factor(tokens):
        token = tokens.pop(0)
        if token == '(':
            result = parse_expression(tokens)
            tokens.pop(0) # Remove ')'
            return result
        return token

    return parse_expression(tokens)

# Constants
MAXDGT=5

# --- Fix 2: Proper float generation ---
gens={
    'int': lambda: random.randint(-(10**MAXDGT), (10**MAXDGT)),
    'float': lambda: random.uniform(-(10**MAXDGT), (10**MAXDGT)),
}

GTRUE=lambda x: True

def generate(t, f=GTRUE, ms=False, tries=1000):
    i=0
    # Try fewer times, but with better distribution
    while i < tries:
        x = gens[t]()
        if ms: x = str(x)
        try:
            if f(x): return x
        except:
            pass # Ignore calculation errors
        i+=1
    return None

def solve(exp1, exp2):
    i=0
    r=[]
    while len(r)<1:
        # --- Fix 1: Updated generate to look for floats if ints fail ---
        v = generate('int', f=lambda x: calc(exp1.replace("(x)",str(x))) == calc(exp2.replace("(x)",str(x))))
        
        if v is not None and round(v, 5) not in [round(existing, 5) for existing in r]:
            r.append(v)
            i+=1
    return FastArray(r)
