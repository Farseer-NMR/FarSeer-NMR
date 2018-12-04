# How to contribute

- Report bugs and suggestions in the [issues tab](https://github.com/Farseer-NMR/FarSeer-NMR/issues), use TAGS as appropriate.
- **Always** submit a Pull Request from you Forked repository of Farseer-NMR.
- Pull Requests title shoud start with a proposal of version change and, if helpful, followed by a short title: `v1.3.12 - corrected bar color bug in barplot`
  - new version number should be updated in `install/system.py`.
  - follow versioning standards: [_major/visible_ [ _new feature_ [ _bug correction_]]
- Pull Request description should state the added improvements and corrections.
- Pull Request should close issues whenever applicable.

# Farseer-NMR code style

This document follows [PEP8](https://www.python.org/dev/peps/pep-0008/) and gathers rules/suggestions to uniform the coding style of Farseer-NMR. Please follow these rules when submitting a Pull Request.

## Length of line

Maximum line length 80 chars.
Maximum docstring length 72 chars.

## Indentation

Indentations are 4 spaces.

## Method call

If method call cannot fit one line, break the line after the "." followed by an extra indentation to the current indentation block. Continue this proceedure for consecutive calls.

```
"my name is {}".\
    format(name)
```

## Function call

Whenever a function call cannot fit a single line, create and indent block for **all** arguments, closing the call should be aligned with args:

Yes:
```
func_with_large_name(
    positional_arg1,
    positional_arg2,
    arg1='foo',
    arg2='bar'
    )
```
Alignment with opening delimiter it's feasible, but annoying and difficult to maintain because introduces partial indentation blocks. Let's not use it.

No:
```
func_with_large_name(positional_arg1,
                     positional_arg2,
                     arg1='foo',
                     arg2='bar')
```

### Kwargs

Create a line break "\" after the assignment statement of the kwarg if the argument can, in this way, fit a new line. Otherwise proceed as in [Function Call] and [Method Call].

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

Usage in case of method calls:
```
func(
    posvar1,
    message="this a big string with several {} {} {}".\
        format(a, b, c)
    kwargs=var1
    )
```

## Defining a function

In case all the positional args and kwargs can not fit a single line,
break line after "(" and write the args in a new indent block.
Give a blank line after the function definition.

```
def long_function_name(
        var_one,
        var_two,
        var_three,
        var_four,
        kwarg1='default',
        kwarg2=0.0
        ):
    
    print(var_one)
```

### Return statement

Citing PEP8: "Be consistent in return statements. Either all return statements in a function should return an expression, or none of them should."

## Conditionals

In if statements newlines should be followed by double indentation to separate from nested code and followed
by the necessary subindentation. If long conditionals have to be created feel free to create variables to assign temporary
short alias.

```
if (True and (True or False)) \
        and (True \
            or False) \
        and False:
    
    # do something
```

## List, Dictionaries and alike

Use the following. This applies also in function calls.
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

```
my_dict = {
    "var1": 1,
    "var2: 2
    }
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

## Break in binary operators.

[Break before as in PEP8](https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator).

## Strings

### Single line

When assigning to a variable break the line if such allows the string to fit a single line, you can even avoid
the usage of indentation if such allows the string to fit one line.

```
msg = \
"<resonance_type> argument must be 'Backbone' or 'Sidechains'."
```

even:
```
        msg = \
"<resonance_type> argument must be 'Backbone' or 'Sidechains'."
```

Otherwise break the string in logical parts with the ```\```. And break again to apply format.
You can/should avoid the use of indentation because this will be passed to the string.

If the string has to be formatted, break the method call to a new line and assign and additional indent.

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

In multiline strings always break the assignment statement to a new line and describe the string without indentation.
If the string has to be formatted, break the method call and give an additional indentation considering the
indentation of the varible to which the string is assigned:

```
        msg = \
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

## Blank lines and Whitespaces

Follow the [general rules of PEP8](https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements).

Inside the same indentation block, write the operations consecutively.
Optionally you can separate relevant logical blocks by new lines or, preferable, by comments.

### Separating indentation blocks

Separate a new indentation block with a preceeding and succeeding blank line.
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
    for digit in dct[char]:
        # Do something here
        # in the second for loop
    
    # continue with the first for loop
```
