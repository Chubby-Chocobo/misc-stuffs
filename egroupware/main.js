$(document).ready(function() {
  console.log("Starting auto-fill egroupware...");

  var config = {
    select : [
      {id: "exec[start_time][H]", value: "8"},
      {id: "exec[start_time][i]", value: "30"},
      {id: "exec[end_time][H]", value: "00"},
      {id: "exec[end_time][i]", value: "00"},
    ],
    input : [
      {id: "exec[ts_duration][value]", value: "8"},
      {id: "exec[ts_quantity]", value: "1"},
    ]
  }

  var tagName = "select";
  for (var i = 0; i < config[tagName].length; i++) {
    var elemId = config[tagName][i].id;
    var elemVal = config[tagName][i].value;

    var elem = document.getElementById(elemId);
    if (!elem) continue;
    for (var j = 0; j < elem.length; j++) {
      var opt = elem[j];
      opt.selected = parseInt(opt.value) == parseInt(elemVal) ? true : false;
    }
  }

  tagName = "input";
  for (var i = 0; i < config[tagName].length; i++) {
    var elemId = config[tagName][i].id;
    var elemVal = config[tagName][i].value;

    var elem = document.getElementById(elemId);
    if (!elem) continue;
    elem.value = elemVal;
  }

});