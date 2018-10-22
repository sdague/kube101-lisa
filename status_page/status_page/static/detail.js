$(document).ready(function() {
    var servicesStatus = $("#service-history");
    var serviceStatus = $("#service-status");
    var serviceMsg = $("#service-msg");
    var serviceSubmit = $("#service-submit");

    var updateLog = function(data) {
        console.log(data);
        var services = data.history;
        servicesStatus.empty();
        var table = "<table>";
        table += "<tr class='heading'><th>Status</th><th>Last Updated</th><th>Comments</th></tr>";

        for (var i = 0; i < services.length; i++) {
            var service = services[i];
            var row = "<tr class='data'>";
            row += "<td class='status_" + service.status + "'>" + service.status + "</td>";
            row += "<td>" + service.updated_at + "</td>";
            row += "<td>" + service.msg + "</td>";
            row += "</tr>";
            table += row;
        }
        table += "</table>";
        servicesStatus.append(table);
    };

    var handleSubmission = function(e) {
        e.preventDefault();
        var status = serviceStatus.val();
        var msg = serviceMsg.val();
        $.post("/services/" + serviceName, JSON.stringify({"status": status, "msg": msg}));
        window.location = "/";
        return false;
    };

    serviceSubmit.click(handleSubmission);
    serviceMsg.on("keypress", function(e) {
        if (e.keyCode == 13) {
            return handleSubmission(e);
        }
        return true;
    });

    // Poll every second.
    (function fetchServices() {
        $.getJSON("/services/" + serviceName).done(updateLog).always(
            function() {
                setTimeout(fetchServices, 1000);
            });
    })();
});
