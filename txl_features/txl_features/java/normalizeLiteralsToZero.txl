% Mutate by renaming of an identifier or type in any program in any C-like language
#pragma -char -comment -width 32767

% C tokens, so we don't break them up
include "java.grm"

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
		[literal]
    |   [primitive_type]
    |	[key]
	|   [id]
end define

redefine primitive_type
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
end define

% Main rule - initialize everything then mutate
function main
    replace [program]
        P [program]
    by
        P [renameLiteral]
end function

rule renameLiteral
	replace $ [literal]
		_ [literal]
	by
		'0
end rule