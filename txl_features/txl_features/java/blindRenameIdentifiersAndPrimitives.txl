% Preserve all formatting and comments exept identifier replacement
#pragma -char -comment -width 32767
include "java.grm"

redefine program
    [repeat line]
    [repeat lineitem] 	% Some files don't have a final newline
end define

define line
    [repeat lineitem] [newline]
end define

define lineitem
		[comment]
    |	[space]
	|	[key]
    |	[id]
	|	[primitive_type]
    |	[not newline] [token]
end define

function main
    replace [program]
        P [program]
    by
        P [renamePrimitives] [renameIdentifier]
end function

rule renameIdentifier
    replace $ [id]
        Id [id]
    by
        'X
end rule

rule renamePrimitives
	replace $ [lineitem]
		k [primitive_type]
	by
		'X
end rule