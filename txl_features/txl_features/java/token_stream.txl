include "java.grm"

#pragma -raw -width 32767

redefine program
	[repeat programelement]
end define

define programelement
	[token] [SP]
|	[key] [SP]
end define

function main
    replace [program]
		P [program]
	by
		P 
end function

