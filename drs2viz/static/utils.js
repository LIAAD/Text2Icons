$(document).ready(function() {
    
    $('#drs_select').change(changeViz);
    $('#viz_type').change(changeViz);

    function changeViz() {
        $("#drs-form").submit();
    }

});
