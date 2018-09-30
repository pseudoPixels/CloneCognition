% Preserve all formatting and comments except identifier replacement
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
    |	[id]
	|	[key]
    |	[not newline] [token]
end define

function main
    replace [program]
        P [program]
	construct Ids [repeat id]
		_ [^ P] [removeDuplicateIds]
	construct GenIds [repeat id]
		Ids [genIds 0]
    by
        P [$ each Ids GenIds]
end function

function removeDuplicateIds
    replace [repeat id]
        Id [id] 
	Rest [repeat id]
    by
	Id
        Rest [removeIds Id]
	     [removeDuplicateIds]
end function

rule removeIds Id [id]
    replace [repeat id]
        Id
	More [repeat id]
    by
        More
end rule

function genIds NM1 [number]
    replace [repeat id]
        _ [id] 
        Rest [repeat id] 
    construct N [number]
        NM1 [+ 1]
    construct GenId [id]
        _ [+ 'x] [+ N]
    by
        GenId 
        Rest [genIds N]
end function

