% Using java fragment grammar
include "java.grm"

%keys
%	'x
%end keys

% Redefinitions
%	Redifined enum such that it conformed to the same format as other grammar
%	components.  This is done so that a fragment can be the inner portion of
%	an enumeration.

% The body of enum redifined to capture its interanls in a single non-terminal
redefine enum_body
    '{                                    [IN]
		[enum_body_inner]
    '} [opt ';]                           [NL][NL]
end define

% The inner portion of a enum
define enum_body_inner
       [list enum_element] [opt ',]
       [repeat class_body_declaration]    [EX]
end define

% Redefine program to be any syntatically complete java code fragment
	% Syntatically complete fragment is one that does not bridge seperate
	% scopes.  Additionally, each { in the fragment must have a matching }
    % in the fragment.  The fragment is not necissarilly compilable.
redefine program
		[package_declaration] % a whole java file
	|	[repeat type_declaration] % whole java type(s) (class, interface, or enumeration)
	|	[class_body] % whole body of a class (incl { } but discluding header)
	|	[interface_body] % whole body of an interface (incl { } but discluding header)
	|	[enum_body] % whole body of an enumeration (incl { } but discluding header)
	|	[repeat class_body_declaration] % partial body of a class/interface (some portion within the { } of the class)
	|	[method_declaration] % a whole method
	|	[constructor_declaration] % a whole constructor
	|	[method_body] % the body of a method (incl { } but discluding header)
	|	[constructor_body] % the body of a constructor (incl { } but discluding header)
	|	[block] % a code block (including { })
	|	[repeat declaration_or_statement] % a series of statements
end define


