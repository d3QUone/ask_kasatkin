var channel_id = $('div#channel_id').html();  // loads user_id from page

function check_messages() {
	$.getJSON('/fetch_updates?cid=' + channel_id, {}, function(r) {
		if (r != 'None') {
			$('div#notf').css("display", "block");
			$.each(r, function (key, val) {
				$('div#notf').append('<a href="/question/' + val.q_id + '" class="notf__message">You have a new answer!</a>');
			})
		}
		setTimeout(check_messages, 700);
	});
}

if (channel_id != 'None') {
	check_messages();
}
