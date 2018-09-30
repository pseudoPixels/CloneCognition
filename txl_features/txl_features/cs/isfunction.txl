include "csharp.grm"
include "bom.grm"

redefine program
	[method_declaration]
| 	[constructor_declaration]
end define

function main
    match [program]
	P [program]
end function
