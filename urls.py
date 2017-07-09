import views

def routes(app):
	@app.route('/') 
	def index(): return views.index()

	@app.route('/new', methods=['POST'])
	def new(): return views.new()

	@app.route('/edit/<friend_id>')
	def edit(friend_id): return views.edit(friend_id)

	@app.route('/update/<friend_id>', methods=['POST'])
	def update(friend_id): return views.update(friend_id)

	@app.route('/remove/<friend_id>', methods=['POST'])
	def remove(friend_id): return views.remove(friend_id)

	@app.route('/<path:path>')
	def catch_all(path): return 'Cannot find {}'.format(path)