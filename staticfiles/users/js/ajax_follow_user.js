// To check status and follow / unfollow user
FollowStatus = function(url, operation, follow_button, username) {
	// console.log(username);
	$.ajax({
		url : url,
		data : {
			'username' : username,
			'operation' : operation
		},
		dataType : 'json',
		success : function(follow) {
			// console.log(follow);
			if(follow.status == 'followed') {
				// btn btn-outline-info
				follow_button.addClass('btn-outline-info').removeClass('btn-info');
				follow_button.html('Following');
			}
			else {
				follow_button.addClass('btn-info').removeClass('btn-outline-info');
				follow_button.html('Follow');
			}
		}
	});
}

$('.follow_unfollow').hover(
	function() {
		// console.log('bitch');
		if($(this).html() == 'Following')
			$(this).html('Unfollow');
	},
	function() {
		if($(this).html() == 'Unfollow')
			$(this).html('Following');
	}
)