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
                        window.location = url;
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
                        window.location = url;
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
                        window.location = url;
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
                        window.location = url;
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
                        window.location = url;
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
                        window.location = url;
                    }
                }
            });
});
$(document).on("click", ".show-remove-volume", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>remove</b> container <b>"+name+"</b>?",
                buttons: {
                    confirm: {
                        label: '<a  href=# class="confirm-remove" data-name="'+name+'"data-url="'+url+'><i class="fa fa-check"></i></a> Confirm',
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
                        //window.location = "#";
                        return  bootbox.confirm({
                            message: "Container <b>"+name+"</b> does <strong style='color:red'>NOT have a mounted volume and you will lose all data</strong>. Do you <b>still</b> want to remove it?",
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
                                    window.location = url;
                                }
                            }
                        });
                    }
                }
            });
});
$(document).on("click", ".show-autoremove-volume", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>stop</b> container <b>"+name+"</b>?",
                buttons: {
                    confirm: {
                        label: '<a  href=# class="confirm-stop" data-name="'+name+'"data-url="'+url+'><i class="fa fa-check"></i></a> Confirm',
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
                        //window.location = "#";
                        return  bootbox.confirm({
                            message: "Container <b>"+name+"</b>  has <strong style='color:red'> AUTOREMOVE enabled </strong> which means it will be removed from docker when stopped. It also does <strong style='color:red'>NOT have a mounted volume and you will lose all data</strong>. Do you <b>still</b> want to stop it?",
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
                                    window.location = url;
                                }
                            }
                        });
                    }
                }
            });
});
$(document).on("click", ".show-autoremove", function(e) {
    var url = $(this).data("url");
    var name = $(this).data("name");
    return  bootbox.confirm({
                message: "Are you sure you would like to <b>stop</b> container <b>"+name+"</b>?",
                buttons: {
                    confirm: {
                        label: '<a  href=# class="confirm-stop" data-name="'+name+'"data-url="'+url+'><i class="fa fa-check"></i></a> Confirm',
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
                        //window.location = "#";
                        return  bootbox.confirm({
                            message: "Container <b>"+name+"</b>  has <strong style='color:red'> AUTOREMOVE enabled </strong> which means it will be removed from docker when stopped. It also <strong style='color:green'> DOES </strong> have a mounted volume and you will not lose all data</strong>. Do you <b>still</b> want to stop it?",
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
                                    window.location = url;
                                }
                            }
                        });
                    }
                }
            });
});