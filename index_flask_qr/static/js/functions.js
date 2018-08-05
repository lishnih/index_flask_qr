// stan 2016-05-26


function round_to_int(i) {
  return i + 0.5 | 0;
} // round_to_int


function to_int(i) {
  return i | 0;
} // to_int


var utility = {
    escapeQuotes: function(string) {
      return string.replace(/"/g, '\\"');
    },
    unescapeQuotes: function(string) {
      return string.replace(/\\"/g, '"');
    }
};


function doFormSubmit(form) {
  var url = form.attr("action");
  var formData = $(form).serializeArray();
  $.post(url, formData).done(function (data) {
    alert(data);
  });
  return true;
} // doFormSubmit


function append_rows(tr, rows) {
  rows.forEach(function(entry) {
    var td = "<td></td>";
    entry.forEach(function(i) {
      if ( i == null )
        td += '<td><i class="inactive">null<i></td>';
      else
        td += "<td>" + i + "</td>";
    });
    tr.before("<tr>" + td + "</tr>");
  });
} // append_rows


function show_info(text, event) {
  $( "#dialog #dialog_content" ).html(text);
  $( "#dialog" ).attr( "title", "info" );
  $( "#dialog" ).dialog( "open" );

  if (typeof event != "undefined")
    event.preventDefault();
} // show_info


function show_error(text, event) {
  $( "#dialog #dialog_content" ).html(text);
  $( "#dialog" ).attr( "title", "error" );
  $( "#dialog" ).dialog( "open" );

  if (typeof event != "undefined")
    event.preventDefault();
} // show_error
