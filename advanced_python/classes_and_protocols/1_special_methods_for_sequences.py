'''
Protocols are Informal Interfaces: In classic Python, a protocol isn't a strict class you inherit from. It is just an agreed-upon set of dunder methods you implement.

The Sequence Protocol: To make an object act like a standard Python sequence (list, tuple), you strictly need to implement just two methods: __len__ and __getitem__.

Duck Typing: "If it walks like a duck and quacks like a duck, it's a duck." Because Python evaluates types dynamically, it doesn't care if your class inherits from object or Sequence. If it has __len__ and __getitem__, Python treats it as a sequence.

Partial Implementations: Because dynamic protocols are informal, you can "cheat". If you know you only need an object to be iterable but don't care about its length, you can just implement __getitem__ and Python will happily loop over it.

Static Protocols (PEP 544): Modern Python added typing.Protocol for strict type-checking. If you use this, your IDE/linter will force you to implement every method in the protocol, bridging the gap between Python's dynamic nature and strict languages like C++ or Java.
'''


from array import array
import reprlib
import math
import operator
import functools
import itertools

class FeatureVector:
    """
    An immutable, memory-efficient N-dimensional feature vector.
    Acts as a native Python sequence (like a PyTorch 1D Tensor).
    """
    
    # Using 'd' (double-precision float) stores data directly in a contiguous 
    # C-array, vastly outperforming Python lists in memory usage.
    typecode = 'd'
    
    # -------------------------------------------------------------------------
    # TAKE #1: SEQUENCE BASICS & DUCK TYPING
    # -------------------------------------------------------------------------
    def __init__(self, components):
        # Accepts any iterable (generator, list, tuple)
        self._components = array(self.typecode, components)

    def __iter__(self):
        # THE ENGINE: Making this iterable allows duck typing to work its magic.
        # It enables tuple(self), unpacking (a, b, c = v), and for-loops.
        return iter(self._components)

    def __len__(self):
        # Fulfills half of the Sequence Protocol
        return len(self._components)

    def __repr__(self):
        # AI Benefit: If this is a 1024-dim ResNet embedding, printing it
        # would freeze the terminal. reprlib safely truncates it with '...'.
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'FeatureVector({components})'

    # -------------------------------------------------------------------------
    # TAKE #2: SLICE-AWARE GETITEM
    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Fulfills the second half of the Sequence Protocol.
        Handles both batched slicing (returns a new FeatureVector) 
        and single-item lookup (returns a float).
        """
        
        if isinstance(key, slice):
            # type(self) ensures that if we subclass this later, 
            # slicing returns the subclass, not the parent class.
            cls = type(self)
            return cls(self._components[key])
        
        # operator.index safely extracts an integer, rejecting floats/tuples 
        # with a clean, native TypeError.
        index = operator.index(key)
        return self._components[index]

    # -------------------------------------------------------------------------
    # TAKE #3: DYNAMIC ATTRIBUTES (FALLBACKS & PROTECTION)
    # -------------------------------------------------------------------------
    # Useful for accessing spatial/color channels easily (v.c, v.h, v.w)
    __match_args__ = ('c', 'h', 'w') 

    def __getattr__(self, name):
        # Triggered ONLY if the attribute doesn't exist normally.
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
            
        if 0 <= pos < len(self._components):
            return self._components[pos]
            
        raise AttributeError(f'{cls.__name__!r} object has no attribute {name!r}')

    def __setattr__(self, name, value):
        # CRITICAL BUG FIX: If we don't block assignment to 'c', 'h', 'w', 
        # users could write `v.c = 10`. This bypasses __getattr__ forever,
        # breaking synchronization with self._components.
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                raise AttributeError(f'readonly attribute {name!r}')
            elif name.islower():
                raise AttributeError(f"can't set attributes 'a' to 'z' in {cls.__name__!r}")
        
        # Pass legitimate assignments (like self._components) to the base object
        super().__setattr__(name, value)

    # -------------------------------------------------------------------------
    # TAKE #4: HIGH-PERFORMANCE HASHING & EQUALITY
    # -------------------------------------------------------------------------
    def __eq__(self, other):
        # AI Benefit: Short-circuiting.
        # 1. len() check is O(1). Mismatched embedding sizes fail instantly.
        if len(self) != len(other):
            return False
            
        # 2. zip() is LAZY (yields pairs without copying memory).
        # 3. all() is LAZY. It stops evaluating at the exact index of the first mismatch.
        return all(a == b for a, b in zip(self, other))

    def __hash__(self):
        # AI Benefit: Map-Reduce architecture.
        # We don't build a massive tuple in memory just to hash it.
        
        
        # MAP: A generator expression (...) yields hashes lazily. O(1) extra memory.
        hashes = (hash(x) for x in self._components)
        
        # REDUCE: functools.reduce applies bitwise XOR (operator.xor) cumulatively.
        # '0' is the safe initializer for empty sequences.
        return functools.reduce(operator.xor, hashes, 0)

    # -------------------------------------------------------------------------
    # TAKE #5: CUSTOM FORMATTING & CHAINING
    # -------------------------------------------------------------------------
    def __abs__(self):
        return math.hypot(*self)

    def __format__(self, fmt_spec=''):
        # Let's say 'n' stands for "norm appended". 
        # It outputs: <magnitude | val1, val2, ...>
        if fmt_spec.endswith('n'):
            fmt_spec = fmt_spec[:-1]
            
            # AI Benefit: itertools.chain links two iterables seamlessly.
            # We append the scalar magnitude to the front of the vector values
            # WITHOUT creating a new list or array in memory.
            coords = itertools.chain([abs(self)], self)
            outer_fmt = '<{} | {}>'
            
            # Format the magnitude
            mag = format(next(coords), fmt_spec)
            
            # Format the rest (generator expression = lazy!)
            components = (format(c, fmt_spec) for c in coords)
            return outer_fmt.format(mag, ', '.join(components))
            
        else:
            components = (format(c, fmt_spec) for c in self)
            return '({})'.format(', '.join(components))

# --- Quick Test to verify it behaves like a production tensor ---
if __name__ == "__main__":
    v = FeatureVector([1.5, 2.0, 3.1, 4.0, 5.0])
    
    print("Repr:  ", v)                   # Safe printing
    print("Slice: ", v[1:3])              # Returns a new FeatureVector
    print("Attr:  ", v.h)                 # Returns 2.0 (fallback magic)
    print("Format:", format(v, '.2fn'))   # Custom chaining format