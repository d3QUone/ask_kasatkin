/* Mark answer as chosen */
function mark(endpoint, eid) {
  $.post(endpoint,
    {
      id: eid, 
      csrfmiddlewaretoken: $.cookie('csrftoken')
    },
    update
  );
  function update(result){
    if (result != "None") {
      if (result == "True") {
        $("span.question__has__answer").html("Has answer!");
        $("span#" + eid + ".correct__button").html("Correct!");
        //$("span#" + eid + ".correct__button").toggleClass("correct__button correct__bage");
      } else {
        $("span.question__has__answer").html("No answer");
        $("span#" + eid + ".correct__button").html("Press here to mark as true");
      }
    }
  }
}

$("span.correct__button").click(function(){
  mark("/mark_as_true/", $(this).attr('id'));
});
