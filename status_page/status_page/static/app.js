$(document).ready(function() {
    var servicesStatus = $("#service-status");

    var updateServices = function(data) {
        var services = data.services;
        servicesStatus.empty();
        servicesStatus.append("<table>");
        servicesStatus.append("<tr class='heading'><th>Service</th><th>Status</th><th>Last Updated</th><th>Comments</th></tr>");

        for (var i = 0; i < services.length; i++) {
            var service = services[i];

            var row = "<tr class='data'>";
            row += "<td>" + service.name + "</td>";
            row += "<td>" + service.status + "</td>";
            row += "<td>" + service.updated_at + "</td>";
            row += "<td>" + service.msg + "</td>";
            row += "</tr>";
            servicesStatus.append(row);
        }
        servicesStatus.append("</table>");

    };

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
    $.getJSON("/services").done(updateServices).always(
      function() {
        setTimeout(fetchServices, 1000);
      });
  })();
});
