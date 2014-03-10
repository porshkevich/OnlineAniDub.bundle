######################################################################################
#
#	ANIME PLUS CHANNEL (BY TEHCRUCIBLE) - v1.01
#
######################################################################################

TITLE = "Anime Plus"
PREFIX = "/video/animeplus"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_NEXT = "icon-next.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_QUEUE = "icon-queue.png"
ICON_SERIES = "icon-series.png"
ICON_MOVIES = "icon-movies.png"
ICON_AZ = "icon-az.png"
ICON_GENRE = "icon-genre.png"
BASE_URL = "http://www.animeplus.tv"
RE_THUMB = Regex('http://videofun.me/frames/(.*)(?=".\s)')

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	PopupDirectoryObject.thumb = R(ICON)
	PopupDirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_COVER)
	VideoClipObject.art = R(ART)
	HTTP.CacheTime = CACHE_1HOUR
	
######################################################################################
# Menu hierarchy. page_count is used for pagination and should always start at 0.

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Most Popular", category = "/popular-anime/", page_count = 0), title = "Most Popular", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="New Anime", category = "/new-anime/", page_count = 0), title = "New Anime", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Recently Added", category = "/recent-anime/", page_count = 0), title = "Recently Added", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Ongoing Anime", category = "/ongoing-anime/", page_count = 0), title = "Ongoing Anime", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(SeriesMenu, title="Anime Series"), title = "Anime Series", thumb = R(ICON_SERIES)))
	oc.add(DirectoryObject(key = Callback(MoviesMenu, title="Anime Movies"), title = "Anime Movies", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(AZMenu, title="Browse A-Z"), title = "Browse A-Z", thumb = R(ICON_AZ)))
	oc.add(DirectoryObject(key = Callback(GenreMenu, title="Browse Genres"), title = "Browse Genres", thumb = R(ICON_GENRE)))
	oc.add(DirectoryObject(key = Callback(Bookmarks, title="My Bookmarks"), title = "My Bookmarks", thumb = R(ICON_QUEUE)))
	oc.add(InputDirectoryObject(key=Callback(Search), title = "Search", prompt = "Search for anime?", thumb = R(ICON_SEARCH)))
	
	return oc

@route(PREFIX + "/seriesmenu")
def SeriesMenu(title):

	oc = ObjectContainer(title1 = title)
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Most Popular", category = "/popular-shows/", page_count = 0), title = "Most Popular", thumb = R(ICON_SERIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="New Series", category = "/new-shows/", page_count = 0), title = "New Series", thumb = R(ICON_SERIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Recently Added", category = "/recent-shows/", page_count = 0), title = "Recently Added", thumb = R(ICON_SERIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Ongoing Series", category = "/ongoing-shows/", page_count = 0), title = "Ongoing Series", thumb = R(ICON_SERIES)))
	
	return oc

@route(PREFIX + "/moviesmenu")	
def MoviesMenu(title):

	oc = ObjectContainer(title1 = title)
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Most Popular", category = "/popular-movies/", page_count = 0), title = "Most Popular", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="New Movies", category = "/new-movies/", page_count = 0), title = "New Movies", thumb = R(ICON_MOVIES)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Recently Added", category = "/recent-movies/", page_count = 0), title = "Recently Added", thumb = R(ICON_MOVIES)))
	
	return oc

@route(PREFIX + "/azmenu")
def AZMenu(title):

	oc = ObjectContainer(title1 = title)
	page_data = HTMLElementFromURL(BASE_URL)
	
	for each in page_data.xpath("//div[@id='options_bar']/ul/li/a")[6:32]:
		page_title = each.xpath("./text()")[0]
		page_url = each.xpath("./@href")[0].split(BASE_URL)[1] + "/"
		oc.add(DirectoryObject(key = Callback(ShowCategory, title = page_title, category = page_url, page_count = 0), title = page_title, thumb = R(ICON_LIST)))
		
	return oc

@route(PREFIX + "/genremenu")
def GenreMenu(title):

	oc = ObjectContainer(title1 = title)
	page_data = HTMLElementFromURL(BASE_URL + "/anime-genres")
	
	for each in page_data.xpath("//table[@id='listing']//a"):
		page_title = each.xpath("./text()")[0]
		page_url = each.xpath("./@href")[0].split(BASE_URL)[1] + "/"
		oc.add(DirectoryObject(key = Callback(ShowCategory, title = page_title, category = page_url, page_count = 0), title = page_title, thumb = R(ICON_LIST)))
		
	return oc	

######################################################################################
# Loads bookmarked shows from Dict.  Titles are used as keys to store the show urls.

@route(PREFIX + "/bookmarks")	
def Bookmarks(title):

	oc = ObjectContainer(title1 = title)
	
	for each in Dict:
		show_url = Dict[each]
		page_data = HTMLElementFromURL(show_url)
		show_title = each
		show_thumb = page_data.xpath("//img[@id='series_image']/@src")[0]
		try:
			show_summary = page_data.xpath("//div[@class='right_col']/div/div[2]/div/span[2]/text()")[0].strip()
		except:
			show_summary = page_data.xpath("//div[@id='series_details']/div[2]/div/text()")[0].strip()
			
		oc.add(DirectoryObject(
			key = Callback(PageEpisodes, show_title = show_title, show_url = show_url),
			title = show_title,
			thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-cover.png'),
			summary = show_summary
			)
		)
	
	oc.add(DirectoryObject(
		key = Callback(ClearBookmarks),
		title = "Clear Bookmarks",
		thumb = R(ICON_QUEUE),
		summary = "CAUTION! This will clear your entire bookmark list!"
		)
	)
	
	return oc	

######################################################################################
# Takes query and formats it in a way that ShowCategory can use to display results.

@route(PREFIX + "/search")	
def Search(query):

	search_category = "/anime/search?key=" + query.replace(' ', '+') + "&page="
	return ShowCategory(title = query, category = search_category, page_count = 0)

######################################################################################
# Collects results from category and creates objects accordingly.

@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):
	
	oc = ObjectContainer(title1 = title)
	page_count = int(page_count) + 1
	page_data = HTMLElementFromURL(BASE_URL + str(category) + str(page_count))
	
	for each in page_data.xpath("//div[@class='series_list']/ul/li"):

		show_url = each.xpath("./div/h3/a/@href")[0]
		show_title = each.xpath("./div/h3/a/text()")[0].strip()
		show_thumb = each.xpath("./div/a/img/@src")[0]
		show_details = [x.strip() for x in each.xpath(".//div[@class='info_bar']/span/span/text()")]
		show_summary = each.xpath("./div/div[@class='descr']/text()")[0].split("[")[0].strip() + "\n\n" + " ".join(show_details[0:2]) + "\n" + " ".join(show_details[2:4]) + "\n" + " ".join(show_details[4:6])
		
		oc.add(DirectoryObject(
			key = Callback(PageEpisodes, show_title = show_title, show_url = show_url),
			title = show_title,
			thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-cover.png'),
			summary = show_summary
			)
		)
			
	if len(oc) >= 25:
		oc.add(NextPageObject(key = Callback(ShowCategory, title = title, category = category, page_count = page_count), title = "More...", thumb = R(ICON_NEXT)))
	
	if len(oc) < 1:
		Log ("No shows found! Check xpath queries.")
		return ObjectContainer(header="Error", message="Something has gone horribly wrong! Please let TehCrucible know, at the Plex forums.")  
	
	return oc

######################################################################################
# Checks for pagination on show_url and returns DirectoryObjects for each page	

@route(PREFIX + "/pageepisodes")
def PageEpisodes(show_title, show_url):

	oc = ObjectContainer(title1 = show_title)
	last_page = HTMLElementFromURL(show_url + "?page=99")
	show_thumb = last_page.xpath("//img[@id='series_image']/@src")[0]
	try:
		show_summary = last_page.xpath("//div[@class='right_col']/div/div[2]/div/span[2]/text()")[0].strip()
	except:
		show_summary = last_page.xpath("//div[@id='series_details']/div[2]/div/text()")[0].strip()
	
	#check show_url for pagination and return total number of pages		
	try:
		total_pages = int(last_page.xpath("//ul[@class='pagination']/li//span[@class='button-content']/text()")[len(last_page.xpath("//ul[@class='pagination']/li//span[@class='button-content']/text()")) - 1])
	except:
		total_pages = 1
		
	page_count = 0
	while page_count < total_pages:
		page_url = show_url + "?page=" + str(total_pages - page_count)
		oc.add(DirectoryObject(
			key = Callback(ListEpisodes, page_url = page_url),
			title = "Page " + str(page_count + 1) + " | Browse Episodes",
			thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-list.png'),
			summary = show_summary
				)
			)
		page_count = page_count + 1
		
	oc.add(DirectoryObject(
		key = Callback(AddBookmark, show_title = show_title, show_url = show_url),
		title = "Add Bookmark",
		summary = "You can add " + show_title + " to your Bookmarks list, to make it easier to find later.",
		thumb = R(ICON_QUEUE)
		)
	)	

	return oc

######################################################################################
# Returns a list of VideoClipObjects in reverse order

@route(PREFIX + "/listepisodes")
def ListEpisodes(page_url):	
	
	oc = ObjectContainer()
	page_data = HTMLElementFromURL(page_url)
	show_title = page_data.xpath("//div[@class='right_col']/h1/text()")[0].strip()
	
	for each in reversed(page_data.xpath("//div[@id='videos']/ul/li")):
		try:
			ep_title = each.xpath("./a/text()")[0].rsplit(show_title + " ")[1]
		except:
			ep_title = each.xpath("./a/text()")[0]
		ep_url = each.xpath("./a/@href")[0]
		ep_date = Datetime.ParseDate(each.xpath("./span[@class='right_text']/text()")[0])
		oc.add(VideoClipObject(
			url = ep_url,
			title = ep_title,
			summary = "Watch " + ep_title + " from AnimePlus.tv",
			thumb = Callback(GetThumb, ep_url = ep_url),
			originally_available_at = ep_date
			)
		)
	
	return oc

######################################################################################
# Grabs thumbnails from videofun iframes if available
	
@route(PREFIX + "/getthumb")
def GetThumb(ep_url):
	
	ep_data = HTMLElementFromURL(ep_url)
	for each in ep_data.xpath("//div[@id='streams']//iframe/@src"):
		if each.find("videofun") > -1:
			iframe_data = HTMLElementFromURL(each)
			string_data = HTML.StringFromElement(iframe_data)
			find_thumb = RE_THUMB.search(string_data).group()
			
	try:
		data = HTTP.Request(find_thumb, cacheTime=CACHE_1MONTH).content
		return DataObject(data, 'image/jpeg')
	except:
		return Redirect(R(ICON_COVER))	

######################################################################################
# Alternative to Plex framework HTML.ElementFromURL to deal with page refreshes.  Thanks Meo!
		
@route(PREFIX + "/httprequest")
def HTMLElementFromURL(url):
	
	request = HTTP.Request(url)
	if 'http-equiv="refresh"' in request.content:
		request = HTTP.Request(url, cacheTime = 0)
	
	return HTML.ElementFromString(request.content)

######################################################################################
# Adds a show to the bookmarks list using the title as a key for the url
	
@route(PREFIX + "/addbookmark")
def AddBookmark(show_title, show_url):
	
	Dict[show_title] = show_url
	Dict.Save()
	return ObjectContainer(header=show_title, message='This show has been added to your bookmarks.')
	
######################################################################################
# Clears the Dict that stores the bookmarks list
	
@route(PREFIX + "/clearbookmarks")
def ClearBookmarks():

	Dict.Reset()
	return ObjectContainer(header="My Bookmarks", message='Your bookmark list has been cleared.')