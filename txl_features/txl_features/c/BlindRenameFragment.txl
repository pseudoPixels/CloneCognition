% Mutate by renaming of an identifier or type in any program in any C-like language
#pragma -char -comment -width 32726

% C tokens, so we don't break them up
include "c.grm"

% Separate sequences of spaces and tabs so they cn be individually added or deleted
tokens
    space	" "
	    |	"	"
end tokens

% Our grammar simply processes lines of text
redefine program
    [repeat line]
    [repeat lineitem] 	% Some files don't have a final newline
end define

define line
    [repeat lineitem] [newline]
end define


define lineitem
	[space_comment]
    |	[space]
    |	[id_or_number]
    |	[not newline] [token]
end define

define space_comment
	[repeat space+] [comment]
end define

define id_or_number
    [simple_type_name]
|	[literal]
|	[key]
| 	[id]
end define

redefine simple_type_name %char, int, void, float, double, 
	'signed [space] 'long [space] 'long [space] 'int
|	'unsigned [space] 'long [space] 'long [space] 'int
|	'unsigned [space] 'long [space] 'int
|	'signed [space] 'long [space] 'int
| 	'signed [space] 'short [space] 'int
|	'unsigned [space] 'short [space] 'int
|	'unsigned [space] 'long [space] 'long
|	'signed [space] 'long [space] 'long
|	'long [space] 'long [space] 'int
|	'signed [space] 'char
|	'unsigned [space] 'char
|	'unsigned [space] 'long
|	'signed [space] 'long
|	'long [space] 'long
|	'unsigned [space] 'short
|	'signed [space] 'short
|	'short [space] 'int
|	'long [space] 'int
|	'unsigned [space] 'int
|	'signed [space] 'int
|	'long [space] 'double
|	'long 
|	'char
|	'short
|	'unsigned
|	'signed
|	'float
|	'double
|	'int
|	'void
| 	'X
end define

redefine literal
	[number]
%    |   'null %decided against null being literal
%    |   'NULL %decided against null being literal
    |   [float]
    |   [hex]
    |   [long]
    |   [SP] [dotfloat]		    % TXL doesn't defaultly space before .
    |   [charlit]                   % "single" character constant
    |   [string]
    |   [gnu_long_int]
    |   [gnu_long_int_string]
    |   [gnu_long_int_charlit]
    |   [hexfloat]
end define

% Main rule - initialize everything then mutate
function main
    replace [program]
        P [program]
    by
        P [rename] [renamePrimitives] [renameLiteral]
end function

% Choose some random id and rename it
rule rename
    replace $ [id]
        _ [id]
    by
        'X
end rule

rule renamePrimitives
	replace $ [simple_type_name]
		k [simple_type_name]
	by
		'X
end rule

rule renameLiteral
	replace $ [literal]
		_ [literal]
	by
		0
end rule
