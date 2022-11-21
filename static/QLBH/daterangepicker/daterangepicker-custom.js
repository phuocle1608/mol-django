$(document).ready(function () {

    updateConfig();

    function updateConfig() {
        var options = {};

        options.showDropdowns = false;

        options.autoApply = true;

        options.ranges = {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        };

        options.locale = {
            direction: 'ltr',
            format: 'DD/MM/YYYY',
            separator: ' - ',
            applyLabel: 'Apply',
            cancelLabel: 'Cancel',
            fromLabel: 'From',
            toLabel: 'To',
            customRangeLabel: 'Custom',
            daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
            monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            firstDay: 1
        };
        options.showCustomRangeLabel = true;
        options.alwaysShowCalendars = true;
        options.startDate = moment().subtract(30, 'days')
        options.endDate = moment()

        options.opens = 'right';

        options.drops = 'down';

        // $('#config-text').val("$('#demo').daterangepicker(" + JSON.stringify(options, null, '    ') + ", function(start, end, label) {\n  console.log(\"New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')\");\n});");
        console.log("TEST2")

        $('#input__daterangepicker').daterangepicker(options, function (start, end, label) { 
            console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')'); ;
            // let daterangepick_element =  document.getElementById('daterangepicker__viewoption')
            
            if ($("#daterangepicker_type").length){
                $("#daterangepicker_type").attr("value", label)
            } else {
                $("#daterangepicker__viewoption").append('<input type="hidden" id = "daterangepicker_type" name="daterangepicker_type" value="' + label + '" /> ');
            }

            if ($("#daterangepicker_start").length) {
                $("#daterangepicker_start").attr("value", start.format('YYYY-MM-DD'))
            } else {
                $("#daterangepicker__viewoption").append('<input type="hidden" id = "daterangepicker_start" name="daterangepicker_start" value="' + start.format('YYYY-MM-DD') + '" /> ');
            }

            if ($("#daterangepicker_end").length) {
                $("#daterangepicker_end").attr("value", end.format('YYYY-MM-DD'))
            } else {
                $("#daterangepicker__viewoption").append('<input type="hidden" id = "daterangepicker_end" name="daterangepicker_end" value="' + end.format('YYYY-MM-DD') + '" /> ');
            }
            
            $("#input__daterangepicker").val(label)
            
            $("#daterangepicker__viewoption").submit()

            
        });;
        console.log(document.getElementById('input__daterangepicker').value.length)
        if (document.getElementById('input__daterangepicker').value.length === 0) {
            if (filteroption === "Custom") {
                document.getElementById('input__daterangepicker').value = start_date + ' - ' + end_date
            } else {
                document.getElementById('input__daterangepicker').value = filteroption
            }

        }

    }

});