$(document).ready(function(){


	//Initializing the editors...
	//var editor = ace.edit("editor");
	//$("#txl_source").val(editor.getSession().getValue());
	//$("#txl_source").hide();
	//editor.setTheme("ace/theme/eclipse");


	//var pre_input = ace.edit("pre_input_to_parse");
	//$("#input_to_parse").val(pre_input.getSession().getValue());
	//$("#input_to_parse").hide();
	//pre_input.setTheme("ace/theme/eclipse");


	var var_txl_log = ace.edit("txl_log");
	var_txl_log.setTheme("ace/theme/eclipse");
	var_txl_log.setOption('readOnly', true);


	var var_txl_output = ace.edit("txl_output");
	var_txl_output.setTheme("ace/theme/eclipse");
	var_txl_output.setOption('readOnly', true);





	//compile and run the txl program on the specified input file
	$("#txl_exec").click(function(){


		//get the source and the input file
		var txl_source = $("#txl_source").val();
		txl_source = encodeURIComponent(String(txl_source));

		var input_to_parse = $("#input_to_parse").val();
		input_to_parse = encodeURIComponent(String(input_to_parse));




		//alert(txl_source);
		$.ajax({
			type: "POST",
			cache: false,
			url: "/txl",
			data: 'txl_source=' + txl_source + '&input_to_parse='+input_to_parse,
			dataType:'json',
			success: function (option) {
			    	//on success display the outputs to the specified fields
				var_txl_log.getSession().setValue(option.txl_log);
				var_txl_output.getSession().setValue(option.txl_output);


			},
			error: function (xhr, status, error) {
				//on error, alert the possible error (system error)
				alert(xhr.responseText);

			}

		    });

	});







//====================== CLONE VALIDATION========================
//selecting the clone file for validation
$("#selectCloneFile").on('change', function () {
    //alert($(this).val());



    var theUser = $("#user_id").text();
	var theCloneFile = $("#selectCloneFile").val();

    $.ajax({
        type: "POST",
        cache: false,
        url: "/srv_get_next_clone_pair_for_validation",
        data: 'theUser=' + theUser + '&theCloneFile='+theCloneFile,
        dataType:'json',
        success: function (option) {
            //alert(option.fragment1);
            //$("#txl_log").html(option.fragment1);
            //$("#txl_output").html(option.fragment2);
            $('#fragment_1_path').text(option.fragment_1_path);
            $('#fragment_1_start').text(option.fragment_1_startline);
            $('#fragment_1_end').text(option.fragment_1_endline);
            var_txl_log.getSession().setValue(option.fragment_1_clone);


            $('#fragment_2_path').text(option.fragment_2_path);
            $('#fragment_2_start').text(option.fragment_2_startline);
            $('#fragment_2_end').text(option.fragment_2_endline);
            var_txl_output.getSession().setValue(option.fragment_2_clone);


            var num_clones_validated = parseInt(option.clones_validated);
            var total_clones = parseInt(option.total_clones);
            $("#validation_percentage").text( ''+(num_clones_validated*100 / total_clones).toPrecision(2) );

            $("#num_validated_clones").text(option.clones_validated);
            $("#total_clones").text(option.total_clones);


        },
        error: function (xhr, status, error) {
            //on error, alert the possible error (system error)
            alert(xhr.responseText);

        }

        });




});





$(".manual_validation").on('click', function(){

    $(".manual_validation").attr("disabled", true);

    var theUser = $("#user_id").text();
    var theCloneFile = $("#selectCloneFile").val();

    var manual_validation_response = $(this).attr('res');
    var fragment_1_path = $("#fragment_1_path").text();
    var fragment_1_start_line = $("#fragment_1_start").text();
    var fragment_1_end_line = $("#fragment_1_end").text();

    var fragment_2_path = $("#fragment_2_path").text();
    var fragment_2_start_line = $("#fragment_2_start").text();
    var fragment_2_end_line = $("#fragment_2_end").text();






    $.ajax({
        type: "POST",
        cache: false,
        url: "/save_manual_clone_validation_res_and_get_new_clone_pair",
        data: 'theUser=' + theUser + '&theCloneFile='+theCloneFile + '&manual_validation_response=' + manual_validation_response + '&fragment_1_path='+fragment_1_path + '&fragment_1_start_line=' + fragment_1_start_line + '&fragment_1_end_line='+fragment_1_end_line +     '&fragment_2_path='+fragment_2_path + '&fragment_2_start_line=' + fragment_2_start_line + '&fragment_2_end_line='+fragment_2_end_line  ,
        dataType:'json',
        success: function (option) {
            //alert(option.fragment1);
            //$("#txl_log").html(option.fragment1);
            //$("#txl_output").html(option.fragment2);


            $('#fragment_1_path').text(option.fragment_1_path);
            $('#fragment_1_start').text(option.fragment_1_startline);
            $('#fragment_1_end').text(option.fragment_1_endline);
            var_txl_log.getSession().setValue(option.fragment_1_clone);


            $('#fragment_2_path').text(option.fragment_2_path);
            $('#fragment_2_start').text(option.fragment_2_startline);
            $('#fragment_2_end').text(option.fragment_2_endline);
            var_txl_output.getSession().setValue(option.fragment_2_clone);


            var num_clones_validated = parseInt(option.clones_validated);
            var total_clones = parseInt(option.total_clones);
            $("#validation_percentage").text( ''+(num_clones_validated*100 / total_clones).toPrecision(2) );

            $("#num_validated_clones").text(option.clones_validated);
            $("#total_clones").text(option.total_clones);





            $(".manual_validation").attr("disabled", false);


        },
        error: function (xhr, status, error) {
            //on error, alert the possible error (system error)
            alert(xhr.responseText);

        }

        });


});






$("#upload_clone_files").on('click', function(){
        var form_data = new FormData($('#upload-file')[0]);

        //append some non-form data also
        form_data.append('userID',$('#user_id').text());
        $.ajax({
            type: 'POST',
            url: '/upload_new_clone_file',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(data) {
                //console.log('Success!');
                alert("Clone File Upload Success");
            },
            error: function (xhr, status, error) {
                //on error, alert the possible error (system error)
                alert(xhr.responseText);

        }


        });

});




















































	//====================== EDITOR SETTINGS ========================

    	//settings: setting editor themes
	$("#select_editor_theme").on('change', function () {

		//editor.setTheme("ace/theme/"+$(this).val());
		//pre_input.setTheme("ace/theme/"+$(this).val());
		var_txl_log.setTheme("ace/theme/"+$(this).val());
		var_txl_output.setTheme("ace/theme/"+$(this).val());

	});


	//settings: setting editor font sizes
	$("#select_font_size").on('change', function () {

		//editor.setFontSize(parseInt($(this).val()));
		//pre_input.setFontSize(parseInt($(this).val()));
		var_txl_log.setFontSize(parseInt($(this).val()));
		var_txl_output.setFontSize(parseInt($(this).val()));

	});

	//settings: setting editor font family
	$("#select_font_family").on('change', function () {

		//editor.setOption('fontFamily', $(this).val());
		//pre_input.setOption('fontFamily', $(this).val());
		var_txl_log.setOption('fontFamily', $(this).val());
		var_txl_output.setOption('fontFamily', $(this).val());

	});

	//settings: setting editor show line number or not
	$("#show_line_number").on('change', function () {

		if($(this).val() == "False"){
			//editor.setOption('showLineNumbers', false);
			//pre_input.setOption('showLineNumbers', false);
			var_txl_log.setOption('showLineNumbers', false);
			var_txl_output.setOption('showLineNumbers', false);
		}
		else {
			//editor.setOption('showLineNumbers', true);
			//pre_input.setOption('showLineNumbers', true);
			var_txl_log.setOption('showLineNumbers', true);
			var_txl_output.setOption('showLineNumbers', true);
		}


	});





	//Handling Keyboard Shortcuts
	//actions on key down
	$(document).keydown(function(e) {
		//execute the txl with 'Shift' key shortcut
		if(e.which == 17) {
			$( "#txl_exec" ).trigger( "click" );
		}
	});





	//load example txl sources
	$('#load_example').on('change',function(){
		//alert('Trying to load example....');
		$.ajax({
			type: "POST",
			cache: false,
			url: "/load_example_txl_program",
			data: 'txl_example_program_name=' + $(this).val() ,
			dataType:'json',
			success: function (option) {
			        //alert(option.example_txl_source);
				editor.getSession().setValue(String(option.example_txl_source));
  				pre_input.getSession().setValue(String(option.input_to_parse));

			},
			error: function (xhr, status, error) {
				//on error, alert the possible error (system error)
				//alert(xhr.responseText);

			}

		    });
	});




});