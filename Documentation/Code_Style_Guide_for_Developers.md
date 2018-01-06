# Farseer-NMR code style

This document follows [PEP8](https://www.python.org/dev/peps/pep-0008/) and gathers rules/suggestions to uniform the coding style of Farseer-NMR. Please follow these rules and submitting a Pull Request.

These rules mainly apply when command does not fit a single line.

## Length of line

Maximum line length 79 chars

## Indentation

Indentation are 4 spaces

## Function call

Whenever a function call cannot fit a single line, **all** arguments should be followed by newlines and an extra identation, closing the call should be aligned with args:

```
func(
    positional_arg1,
    positional_arg2,
    kwarg1='foo',
    kwarg2='bar'
    )
```

### Alignment

Aligned with opening delimiter it's feasible, but annoying and difficult to maintain because introduces partial indentation blocks. Let's not use it.
```
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

### Kwargs

Passing results from function calls as kwargs:

Preferable, if series_kwargs() call fit a single line:
```
func(
    posvar1,
    series_kwargs=\
        series_kwargs(fsuv, resonance_type=resonance_type)
    )
```
    
Yes, if series_kwargs() call cannot fit a single line:
```
func(
    posvar1,
    series_kwargs=series_kwargs(
        fsuv,
        resonance_type=resonance_type
        )
    )
```

## Defining a function,

Positional arguments should follow each other unless they don't fit all in a single line, in that case rule#2 applies allowing two args per line. Kwargs should **always** be preceded by 2 indents and followed by newline.

```
def long_function_name(
        var_one, var_two,
        var_three, var_four
        kwarg1='default',
        kwarg2=0.0):
    print(var_one)
```

## Conditionals

In if statements newlines should be followed by double indentation to separate from nested code and followed by the necessary subindentation.

```
if (True and (True or False)) \
        and (True \
            or False) \
        and False:
```

## List, Dictionaries and alike

Use the following.
```
my_list = [
    value1,
    value2,
    [
        value3,
        value4,
        value5
        ],
    ]
```
 
## For loops

For example, if long zip() are necessary:

Yes:
```
for sourcecol, targetcol in zip(
        fsuv["restraint_settings"].index[3:],
        ['Hgt_DPRE', 'Vol_DPRE']
        ):
```

### Nested loops

Use itertool library whenever possible.

Yes:
```
for dp2, dp1 in it.product(next_axis_2, next_axis):
    # DO
```

No:
```
for dp2 in next_axis_2:
    for dp1 in next_axis:
        # DO
```

## Method call

If method call cannot fit one line, break the line after the "." followed by an extra indentation to the current indentation block.

```
"my name is {}".\
    format(name)
```

## Break in binary operators.

[Break before as in PEP8](https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator).

## Strings

### Single line

When assigning to a variable break the line if such allows the string to fit a single line, you can even avoid the usage of indentation if such allows the string to fit one line.

```
msg = \
"<resonance_type> argument must be 'Backbone' or 'Sidechains'."
```

Otherwise break the string in logical parts with the ```\```. And break again to apply format. You can/should avoid the use of indentation.

```
logs = \
'**[{}][{}][{}]** new columns inserted:  {}  \
| sidechains user setting: {} \
| sidechains identified: {} | SD count: {}'.\
    format(
        a,
        b,
        c,
        etc...
```

### Multiline

In multiline strings receiving variables, even if the string does not reach the end of the line, using the following notation:

```
"""path: {}  
side chains: {}  
FASTA starting residue: {}  """.\
            format(
                spectra_path,
                self.has_sidechains,
                self.FASTAstart
                )
```

## Imports

Follow the [rules of PEP8](https://www.python.org/dev/peps/pep-0008/#imports).

Inside the same indentation block, write the operations consecutively. Optionally you can separate relevant logical blocks by new lines or by comments (better).

## Blank lines and Whitespaces

Follow the [general rules of PEP8](https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements).

### Separating indents

Separate a conditional or loop block with a preceeding and succeeding blank line.
Start the block right after the header. If a block initiates right after another avoid the preceeding blank line.

```
a = 1
b = 2

if a > 5:
    #do something

c = 4
```

or 

```
for char in string:
    for digit in big_number:
        # Do something here
        # in the second for loop
    
    # continue with the first for loop
```
