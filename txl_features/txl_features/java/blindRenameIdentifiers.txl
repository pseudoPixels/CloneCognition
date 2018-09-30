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
    |	[not newline] [token]
end define

% Main rule - initialize everything then mutate
function main
    replace [program]
        P [program]
    by
        P [renameIdentifier]
end function

% Choose some random id and rename it
rule renameIdentifier
    replace $ [id]
        Id [id]
    by
        'X
end rule