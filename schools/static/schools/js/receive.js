$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-receive").modal("show");
            },
            success: function (data) {
                $("#modal-receive .modal-content").html(data.html_form);
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
                    $("#receive-table tbody").html(data.html_receive_list);
                    $("#modal-receive").modal("hide");
                } else {
                    $("#modal-receive .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create receive
    $(".js-create-receive").click(loadForm);
    $("#modal-receive").on("submit", ".js-receive-create-form", saveForm);

    // view receive
    $("#receive-table").on("click", ".js-view-receive", loadForm);
    $("#modal-receive").on("submit", ".js-receive-view-form", saveForm);

    // Update receive
    $("#receive-table").on("click", ".js-update-receive", loadForm);
    $("#modal-receive").on("submit", ".js-receive-update-form", saveForm);

    // Delete receive
    $("#receive-table").on("click", ".js-delete-receive", loadForm);
    $("#modal-receive").on("submit", ".js-receive-delete-form", saveForm);

});