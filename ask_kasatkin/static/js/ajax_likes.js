function change_rating(endpoint, eid, dif) {
  $.post(endpoint,
    {
      id: eid,
      like: dif
    },
    update_rating
  );

  function update_rating(result){
    if (result != "None") {
      $("div#" + eid).html("Rating: " + result);
    }
  }
}


$("span.question_like").click(function(){
    change_rating("/like_post/", $(this).attr('id'), 1);
});
 
$("span.question_dislike").click(function(){
    change_rating("/like_post/", $(this).attr('id'), -1);
});


$("span.ans_like").click(function(){
  change_rating("/like_answ/", $(this).attr('id'), 1);
});

$("span.ans_dislike").click(function(){
  change_rating("/like_answ/", $(this).attr('id'), -1);
});
