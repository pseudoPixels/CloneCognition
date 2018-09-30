include "ctokens.grm"

#pragma -width 32726 -raw

define program
	[repeat programelement]
end define

define programelement
	[key] [NL]
|	[comment] [NL]
|	[token] [NL]
end define

function main
    match [program]
	P [program]
end function
