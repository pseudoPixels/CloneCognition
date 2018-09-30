% Using java fragment grammar
include "java.grm"

%program must be a function (method or constructor) by itself
redefine program
		[method_declaration] % a whole method
	|	[constructor_declaration] % a whole constructor
end define

function main
	match [program]
	P [program]
end function
