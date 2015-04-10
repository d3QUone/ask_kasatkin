var channelId = $("div#channel_id").html();  // loads user_id from page

function check_messages() {
	$.get('/listen?cid=' + channelId, {}, function(r) {
		// Считаем, что у нас есть div c id=messages, куда мы дописываем сообщения
		//$('#messages').append(r);

		// r == question id ? full block

		setTimeout(check_messages, 500);
	}, 'json');
}

if (channelId != "None") {
	check_messages();
}
