// To follow / unfollow user
var follow_button = $('#follow_unfollow');
var username = (document.getElementById('user-username').innerHTML).slice(1);

// console.log(follow_button);

FollowStatus = function(operation) {
	// console.log(username);
	$.ajax({
		url : '/ajax/follow/user/',
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

// check follow status
FollowStatus('check');

// change follow status
follow_button.click(function() {
	FollowStatus('change');
});

follow_button.hover(
	function() {
		// console.log('bitch');
		if(follow_button.html() == 'Following')
			follow_button.html('Unfollow');
	},
	function() {
		if(follow_button.html() == 'Unfollow')
			follow_button.html('Following');
	}
)