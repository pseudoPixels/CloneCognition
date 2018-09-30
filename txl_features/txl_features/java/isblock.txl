% Using java fragment grammar
include "java.grm"

%program must be a function (method or constructor) by itself
redefine program
		[block]
end define

function main
	match [program]
	P [program]
end function
