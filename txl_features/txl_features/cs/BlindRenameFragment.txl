#pragma -char -comment

include "csharp.grm"
include "bom.grm"
redefine program
	[repeat line]
	[repeat lineitem] %some files don't have a final newline
end define

redefine simple_type
	...
|	'string
|	'X
|	'void
end define

redefine literal
	...
|	0
end define

define line
	[repeat lineitem] [newline]
end define

redefine null_literal
	...
|	'X
end define

define lineitem
	[space_comment]
|	[space]
|	[id_or_number]
|	[not newline][token]
end define

define space_comment
	[repeat space+][comment]
end define

define id_or_number
	[null_literal]
|	[literal]
|	[simple_type]
|	[key]
|	[id]
end define

function main
	replace [program]
		P [program]
	by
		P [rename_ids] [rename_null_literal] [rename_literal] [rename_primitives]
end function

rule rename_ids
	replace $ [id]
		_ [id]
	by
		'X
end rule

rule rename_null_literal
	replace $ [null_literal]
		_ [null_literal]
	by
		'X
end rule

rule rename_literal
	replace $ [literal]
		_ [literal]
	by
		0
end rule

rule rename_primitives
	replace $ [simple_type]
		_ [simple_type]
	by
		'X
end rule
