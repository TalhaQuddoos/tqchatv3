function createNewChatCard(id, lastmsg, lastmsgtime, name, username){
	var chatLink = document.createElement('a')
	classes = ['text-reset', 'nav-link', 'p-0', 'mb-6']
	for(cls of classes)
	    chatLink.classList.add(cls)
	chatLink.href = '/chat/'+username


	var card = document.createElement('div')
	card.className = 'card'
	card.classList.add('card-active-listener')


	var cardBody = document.createElement('div')
	cardBody.className = 'card-body'

	var media = document.createElement('div')
	media.className = 'media'

	var avatarDiv = document.createElement('div')
	avatarDiv.className = 'avatar'
	avatarDiv.classList.add('mr-5')

	var avatarImg = document.createElement('img')
	avatarImg.src = `/media/users/${id}`
	avatarImg.className = 'avatar-img'



	var mediaBody = document.createElement('div')
	mediaBody.className = 'media-body'
	mediaBody.classList.add('overflow-hidden')

	var mediaBodyInner = document.createElement('div')
	mediaBodyInner.className = 'd-flex'
	mediaBodyInner.classList.add('align-items-center')
	mediaBodyInner.classList.add('mb-1')

	var chatName = document.createElement('h6')
	chatName.className = 'text-truncate'
	chatName.classList.add('mb-0')
	chatName.classList.add('mr-auto')
	chatName.textContent = name

	var time = document.createElement('p')
	time.className = 'text-muted'
	time.classList.add('small')
	time.classList.add('text-nowrap')
	time.classList.add('ml-4')
	time.textContent = lastmsgtime

	var lastMsg = document.createElement('div')
	lastMsg.className = 'text-truncate'
	lastMsg.textContent = lastmsg



	mediaBodyInner.appendChild(chatName)
	mediaBodyInner.appendChild(time)

	mediaBody.appendChild(mediaBodyInner)
	mediaBody.appendChild(lastMsg)

	avatarDiv.appendChild(avatarImg)

	media.appendChild(avatarDiv)
	media.appendChild(mediaBody)

	cardBody.append(media)

	card.append(cardBody)

	chatLink.append(card)

}