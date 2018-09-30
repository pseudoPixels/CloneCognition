include "csharp.grm"
include "bom.grm"

redefine program
	[block]
end define

function main
    match [program]
	P [program]
end function
