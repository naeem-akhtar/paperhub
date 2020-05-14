// To follow / unfollow user
var follow_buttons = $('.follow_unfollow');
var username = (document.getElementById('user-username').innerHTML).slice(1);

// console.log(follow_button);

FollowStatus = function(operation, follow_button) {
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
follow_buttons.each(function() {
  FollowStatus('check', $(this));
  // console.log($(this));
})

// change follow status
$('.follow_unfollow').click(function() {
	FollowStatus('change', $(this));
});

follow_buttons.hover(
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