$(document).ready(function() {
    var servicesStatus = $("#service-history");
    var serviceStatus = $("#service-status");
    var serviceMsg = $("#service-msg");
    var serviceSubmit = $("#service-submit");

    var updateLog = function(data) {
        console.log(data);
        var services = data.history;
        servicesStatus.empty();
        servicesStatus.append("<table>");
        servicesStatus.append("<tr><th>Status</th><th>Last Updated</th><th>Comments</th></tr>");

        for (var i = 0; i < services.length; i++) {
            var service = services[i];

            servicesStatus.append("<tr>");
            servicesStatus.append("<td>" + service.status + "</td>");
            servicesStatus.append("<td>" + service.updated_at + "</td>");
            servicesStatus.append("<td>" + service.msg + "</td>");
            servicesStatus.append("</tr>");
        }
        servicesStatus.append("</table>");

    };

    var handleSubmission = function(e) {
        e.preventDefault();
        var status = serviceStatus.val();
        var msg = serviceMsg.val();
        $.post("/services/" + serviceName, JSON.stringify({"status": status, "msg": msg}));
        // if (entryValue.length > 0) {
        //     entriesElement.append("<p>...</p>");
        //     $.getJSON("rpush/guestbook/" + entryValue, appendGuestbookEntries);
        //     entryContentElement.val("")
        // }
        return false;
    };

    serviceSubmit.click(handleSubmission);

  // var handleSubmission = function(e) {
  //   e.preventDefault();
  //   var entryValue = entryContentElement.val()
  //   if (entryValue.length > 0) {
  //     entriesElement.append("<p>...</p>");
  //     $.getJSON("rpush/guestbook/" + entryValue, appendGuestbookEntries);
  //         entryContentElement.val("")
  //   }
  //   return false;
  // }
  // var handleSubmission = function(e) {
  //   e.preventDefault();
  //   var entryValue = entryContentElement.val()
  //   if (entryValue.length > 0) {
  //     entriesElement.append("<p>...</p>");
  //     $.getJSON("rpush/guestbook/" + entryValue, appendGuestbookEntries);
  //         entryContentElement.val("")
  //   }
  //   return false;
  // }

  // // colors = purple, blue, red, green, yellow
  // var colors = ["#549", "#18d", "#d31", "#2a4", "#db1"];
  // var randomColor = colors[Math.floor(5 * Math.random())];
  // (function setElementsColor(color) {
  //   headerTitleElement.css("color", color);
  //   entryContentElement.css("box-shadow", "inset 0 0 0 2px " + color);
  //   submitElement.css("background-color", color);
  // })(randomColor);

  // submitElement.click(handleSubmission);
  // formElement.submit(handleSubmission);
  // hostAddressElement.append(document.URL);

  // Poll every second.
  (function fetchServices() {
    $.getJSON("/services/" + serviceName).done(updateLog).always(
      function() {
        setTimeout(fetchServices, 1000);
      });
  })();
});
