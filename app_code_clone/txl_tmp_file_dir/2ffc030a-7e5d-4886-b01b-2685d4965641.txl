%%% The_syntax_specification
define program
        [expression]
end define 
                  
define expression
        [number]
    |   [number] + [number]
end define 
                  



%%% The_rule_definition
rule resolveAddition
    replace [expression]
        N1 [number] + N2 [number]
    by
        N1 [+ N2]
end rule                 
                  




%%% The_main_rule
rule main
    replace [expression]
        E [expression]
    construct NewE [expression]
        E [resolveAddition]
    where not
        NewE [= E]
    by
        NewE
end rule                  
                  

                  


