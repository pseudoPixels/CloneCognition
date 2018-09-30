include "csharp.grm"
include "bom.grm"
define program
	[repeat programelement]
end define

define programelement
	[token] [NL]
|	[key] [NL]
|	[comment] [NL]
end define

function main
    match [program]
	P [program]
end function
