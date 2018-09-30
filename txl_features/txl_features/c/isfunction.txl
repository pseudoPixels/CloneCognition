include "c.grm"

#pragma -width 32726

redefine program
	[function_definition]
end define

function main
	replace [program]
		P [program]
	by
		P
end function


