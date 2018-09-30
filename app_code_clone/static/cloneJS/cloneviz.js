$(document).ready(function(){










$(document).on("click", ".vizPlugin" ,function(){
    var vizPluginName = $(this).attr("id"); //'biodatacleaning';
    //alert(vizPluginName);

    addNewVizTool(1, vizPluginName);



/*
      //append new module to the pipeline...
                $("#cloneVizPlugin").append(
                    '<div style="background-color:#DDD;width:100%;" class="module" id="module_id_'+ 'moduleID' +'">' +

                '<!-- Documentation -->' +
                '<div style="margin:10px;font-size:17px;color:#000000;">' +
                  ' ' + 'Clone Feature Distribution' + '<hr/>' +
                   ' Documentation: <a style="font-size:12px;color:#000000;" href="#" class="documentation_show_hide">(Show/Hide)</a>' +
                    '<div class="documentation" style="background-color:#DDDDDD;display:none;font-size:14px;">' + 'tool_documentation' + '</div>' +
                '</div>' +


                '<!-- Settings -->' +
                '<div style="margin:10px;font-size:17px;color:#000000;">' +
                 '   Settings: <a style="font-size:12px;color:#000000;" href="#" class="settings_show_hide">(Show/Hide)</a>' +
                '</div>' +

                '</div>'


            );//end of append

*/


});








//adds the module to the pipeline. moduleID is unique throughout the whole pipeline
//moduleName is the name of the module like: rgb2gray, medianFilter and so on
function addNewVizTool(moduleID, moduleName){

        var module_name = ''
        var documentation = ''
        var moduleSourceCode_settings = ''
        var moduleSourceCode_main = ''
        var moduleSourceCode_html = ''

        $.ajax({
            type: "POST",
            cache: false,
            url: "/get_viz_plugin_details",
            data: 'p_module_key=' + moduleName,
            success: function (option) {
                //alert("@ success");
                module_name = option.module_name
                documentation = option.documentation
                moduleSourceCode_settings = option.moduleSourceCode_settings
                moduleSourceCode_main = option.moduleSourceCode_main
                moduleSourceCode_html = option.moduleSourceCode_html


                //Parse the givn XML for tool definition
                var xmlDoc = $.parseXML( moduleSourceCode_html );
                var $xml_tool_definition = $(xmlDoc);

                //the tool configuration.
                //TODO: add the input port info.
                var tool_configs = $xml_tool_definition.find("toolConfigurations");
                tool_configs = tool_configs.html();


                var ioInformation = '';

                var $toolInput = $xml_tool_definition.find("toolInput");

                $toolInput.each(function(){

                    var label = $(this).find('label').text(),
                        dataFormat = $(this).find('dataFormat').text(),
                        referenceVariable = $(this).find('referenceVariable').text();

                        ioInformation +=  'Input Source: ' + '<select  class="setting_param module_input enableResourceDiscovery" referenceVariable="'+ referenceVariable + '"> <option> Select Input Datasource</option> </select> <br/>';

                });


                var $toolOutput = $xml_tool_definition.find("toolOutput");

                $toolOutput.each(function(){

                    var label = $(this).find('label').text(),
                        dataFormat = $(this).find('dataFormat').text(),
                        referenceVariable = $(this).find('referenceVariable').text();

                    //var thisPortOutput = 'module_id_' + moduleID + '_' + referenceVariable+'.' + dataFormat;
                    //var thisPortOutputPath = referenceVariable + '="' + thisPortOutput + '"';

                    ioInformation += '<input type="text" style="display:none;" class="setting_param module_output" size="45" value="'+ referenceVariable + '=&quot;/home/ubuntu/Webpage/app_code_clone/user_projects/golammostaeen@gmail.com/vizOutputs/'+referenceVariable+'.'+dataFormat+'&quot;"/><br/>';


                });






                //append new module to the pipeline...
                $("#cloneVizPlugin").append(
                    '<div style="background-color:#EEE;width:100%;" class="module" id="module_id_'+ '0' +  '">' +

                    '<!-- Documentation -->' +
                    '<div style="margin:10px;font-size:17px;color:#000000;">' +
                      ' ' + module_name +   '<hr/>' +
                    '</div>' +


                    '<!-- Settings -->' +
                    '<div style="margin:10px;font-size:17px;color:#000000;">' +
                     '   Settings: <a style="font-size:12px;color:#000000;" href="#" class="settings_show_hide">(Show/Hide)</a>' +
                     '   <div class="settings" style="background-color:#DDDDDD;font-size:14px;">' + tool_configs + '<br/>' + ioInformation +
                            '<input type="hidden" class="setting_param " size="45" id="module_id_'+ '0' +'_output_destination" />' +
                        '</div>' +
                    '</div>' +


                    '<div style="margin:10px;font-size:17px;color:#000000;" class="setting_section">' +
                    '    <a style="display:none;font-size:12px;color:#000000;" href="#" class="code_show_hide">(Show/Hide)</a>' +

                     '   <div class="edit_code" style="background-color:#888888;font-size:14px;">' +
                      '          <textarea rows=7 style="display:none;" cols=150 class="code_settings">' + moduleSourceCode_settings + '</textarea>' +
                       '         <p style="display:none;" style="color:#000000;">Main Implementation: </p>' +
                        '        <textarea style="display:none;" rows=10 cols=150>' + moduleSourceCode_main + '</textarea>' +
                        '</div>' +

                       ' <pre style="display:none;" style="background-color:#333333;width:100%;" class="pre_highlighted_code">' + '<code style="display:none;" class="python highlighted_code" >' + moduleSourceCode_settings +
                       ' ' +
                    moduleSourceCode_main + '</code></pre>' +

                   ' </div>' +

                    '</div>'


                );//end of append


                $("#module_id_"+ '0' + "_output_destination").val("output_destination = '/home/ubuntu/Webpage/app_collaborative_sci_workflow/workflow_outputs/test_workflow/Module_" + moduleID + "'").trigger('change');









             },
             error: function (xhr, status, error) {
                    alert(xhr.responseText);
             }

        });//end of ajax


}







$(document).on('change', ".setting_param" ,function () {//here
    //alert("you changed my value");
    //var prev_code = $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val();
    //alert(prev_code);
    //$(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val(prev_code + "\n" + $(this).val());
    $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val('');
    $(this).siblings(".setting_param").each(function () {
        //alert($(this).val());
        var prev_code = $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val();
        $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val("\n"+prev_code + "\n\n" + $(this).val());
    });
    var prev_code = $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val();
    $(this).parent().parent().siblings(".setting_section").children(".edit_code").find(".code_settings").val("\n"+prev_code + "\n\n" + $(this).val());



});





$("#run_vizPlugin").click(function () {
    //$("#pr_status").html("<span style='color:orange'>Running Pipeline...</span>");

    var sourceCode = ''
    $('textarea').each(
        function () {
            //alert($(this).val());
            sourceCode = sourceCode + "\n" +$(this).val();
        }
    );

    //alert(sourceCode);

    //encode the source code for any special characters like '+' , '/' etc
    sourceCode = encodeURIComponent(String(sourceCode));




    //alert(sourceCode);

    //send the code for running in pythoncom
    $.ajax({
        type: "POST",
        cache: false,
        url: "/execVizPlugin",
        data: 'textarea_source_code=' + sourceCode,
        success: function (option) {

            //alert(option);
            //get_workflow_outputs_list('test_workflow');
            //$("#pr_status").html("<span style='color:green'>Pipeline Completed Running Successfully.</span>");

            //$("#tool_vis_iframe").attr('src', 'data:text/html;charset=utf-8,' + encodeURIComponent(option.output));
            //$("#tool_vis_iframe").show();

            alert('Visualization Output Generated.');

        },
        error: function (xhr, status, error) {
            //alert(xhr.responseText);
            $("#pr_status").html("<span style='color:red'>Pipeline Running Failed!!!</span>");
        }

    });





});



















//For Dynamic Resource Discovery
$(document).on("focus",".enableResourceDiscovery", function(){

    $(this).html('');

    //alert($(this).attr('referenceVariable'));

    discoverResources(this, $(this).attr('referenceVariable'), 'test');
    /*$(this).append($('<option>', {
            value: $(this).attr('referenceVariable'),
            text: 'My option'
    }));*/

});





function discoverResources(domElement,referenceVariable,workflow_id){
	var thisWorkflowID = workflow_id;

    var fullPath = '/home/ubuntu/Webpage/app_code_clone/user_projects/golammostaeen@gmail.com/'

	//get the ouput list via async call
    	$.ajax({
		type: "POST",
		cache: false,
		url: "/cloneViz_get_workflow_outputs_list/",
		data: "workflow_id="+'test',
		success: function (option) {
			//$("#workflow_outputs").html("");
			for(var i=0;i<option['workflow_outputs_list'].length;i++){
				//var k = i+1;
				//$("#workflow_outputs").html("");
				$(domElement).append($('<option>', {
                    value: referenceVariable+'="'+fullPath+option['workflow_outputs_list'][i]+'"',
                    text: option['workflow_outputs_list'][i]
                }));

				//$("#workflow_outputs").append("<a href='/file_download?workflow_id=" + thisWorkflowID +"&file_id=" + option['workflow_outputs_list'][i]+"' class='a_workflow_output' id='"+option['workflow_outputs_list'][i] +"'>"  + option['workflow_outputs_list'][i] + "</a><br/>");
			}

		},
		error: function (xhr, status, error) {
	    		alert(xhr.responseText);
		}

    	});


}





function get_workflow_outputs_list(workflow_id){
	var thisWorkflowID = 'test';

	//get the ouput list via async call
    	$.ajax({
		type: "POST",
		cache: false,
		url: "/cloneViz_get_viz_output_list/",
		data: "workflow_id="+thisWorkflowID,
		success: function (option) {
			$("#workflow_outputs").html("");
			for(var i=0;i<option['workflow_outputs_list'].length;i++){
				var k = i+1;
				//$("#workflow_outputs").html("");
				var thisFileName = option['workflow_outputs_list'][i];
				var visulaizationLink = '';
				if(thisFileName.split('.').length>0){
				    var thisFileType = thisFileName.split('.')[thisFileName.split('.').length - 1];
				    if(thisFileType == 'html' || thisFileType == 'htm'){//currently supported file types for visualization.
				        visulaizationLink = "<a style='font-size:11px;' href='#' class='output_vis' viewid='"+ option['workflow_outputs_list'][i] +"'> (View) </a>";
				    }
				}



				$("#workflow_outputs").append(visulaizationLink + "<a href='/file_download?workflow_id=" + thisWorkflowID +"&file_id=" + option['workflow_outputs_list'][i]+"' class='a_workflow_output' id='"+option['workflow_outputs_list'][i] +"'>"  + option['workflow_outputs_list'][i] + "</a><br/>");
			}

		},
		error: function (xhr, status, error) {
	    		alert(xhr.responseText);
		}

    	});


}

get_workflow_outputs_list('test_workflow');





$(document).on('click', '.output_vis', function(){

    var fileName = $(this).attr('viewid');

    //alert(fileName);




    var fileType = fileName.split('.')[fileName.split('.').length - 1];

    $.ajax({
        type: "POST",
        cache: false,
        url: "/cloneViz_load_output_for_visualization",
        data: 'fileName=' + fileName,
        success: function (option) {
            if(fileType=='htm' || fileType=='html'){
                $("#tool_vis_iframe").attr('src', 'data:text/html;charset=utf-8,' + encodeURIComponent(option.output));
                $("#tool_vis_iframe").show();
            }


        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }

    });



});












});