% Mutate by renaming of an identifier or type in any program in any C-like language
#pragma -char -comment -width 32767

% C tokens, so we don't break them up
include "jtokens.grm"

% Our grammar simply processes lines of text
define program
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
		[literal]
    |   [primitive_type]
    |	[key]
	|   [id]
end define

define primitive_type
        'boolean
    |   'char
    |   'byte
    |   'short
    |   'int
    |   'long
    |   'float
    |   'double
    |   'void
    |   'X
    |	'null
end define

define literal
         [numeric_literal] 
    |    [character_literal] 
    |    [string_literal] 
    |    [boolean_literal] 
end define

define numeric_literal
     [number] 
end define

define character_literal
     [charlit] 
end define

define string_literal
     [stringlit] 
end define

define boolean_literal
         'true 
    |    'false 
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
        Id [id]
    by
        'X
end rule

rule renamePrimitives
	replace $ [primitive_type]
		k [primitive_type]
	by
		'X
end rule

rule renameLiteral
	replace $ [literal]
		_ [literal]
	by
		0
end rule
