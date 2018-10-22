$(document).ready(function() {
    var servicesStatus = $("#service-status");
    var serviceSubmit = $("#service-submit");
    var serviceAdd = $("#service-add");


    var updateServices = function(data) {
        var services = data.services;
        servicesStatus.empty();
        var table = "<table>";
        table += "<tr class='heading'><th>Service</th><th>Status</th><th>Last Updated</th><th>Comments</th><th>History</th></tr>";

        for (var i = 0; i < services.length; i++) {
            var service = services[i];

            var row = "<tr class='data'>";
            row += "<td>" + service.name + "</td>";
            row += "<td>" + service.status + "</td>";
            row += "<td>" + service.updated_at + "</td>";
            row += "<td>" + service.msg + "</td>";
	    row += "<td><a href=\"details/" + service.name + "\">history</a></td>";
            row += "</tr>";
            table += row;
        }
        table += "</table>";
        servicesStatus.append(table);
    };


    var handleSubmission = function(e) {
        e.preventDefault();
        var url = "/details/service:" + $("#service-add").val();
        console.log(url);
        window.location = url;
        return false;
    };

    serviceSubmit.click(handleSubmission);
    serviceAdd.on("keypress", function(e) {
        if (e.keyCode == 13) {
            return handleSubmission(e);
        }
        return true;
    });

    // Poll every second.
    (function fetchServices() {
        $.getJSON("/services").done(updateServices).always(
            function() {
                setTimeout(fetchServices, 1000);
            });
    })();
});
