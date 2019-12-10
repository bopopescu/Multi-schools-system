$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-activity").modal("show");
            },
            success: function (data) {
                $("#modal-activity .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $("#activity-table tbody").html(data.html_activity_list);
                    $("#modal-activity").modal("hide");
                } else {
                    $("#modal-activity .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create activity
    $(".js-create-activity").click(loadForm);
    $("#modal-activity").on("submit", ".js-activity-create-form", saveForm);

    // view activity
    $("#activity-table").on("click", ".js-view-activity", loadForm);
    $("#modal-activity").on("submit", ".js-activity-view-form", saveForm);

    // Update activity
    $("#activity-table").on("click", ".js-update-activity", loadForm);
    $("#modal-activity").on("submit", ".js-activity-update-form", saveForm);

    // Delete activity
    $("#activity-table").on("click", ".js-delete-activity", loadForm);
    $("#modal-activity").on("submit", ".js-activity-delete-form", saveForm);

});