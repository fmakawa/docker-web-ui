/*$(document).on("click", ".show-inspect", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>inspect</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
*/
$(document).on("click", ".show-pause", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>pause</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
$(document).on("click", ".show-unpause", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>unpause</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
$(document).on("click", ".show-stop", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>stop</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
$(document).on("click", ".show-restart", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>restart</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
$(document).on("click", ".show-remove", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>remove</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});
$(document).on("click", ".show-run", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>run</b> container <b>"+name+"</b>",
                buttons: {
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    console.log(url);
                    if (result) {
                        window.location = url
                    }
                }
            });
});