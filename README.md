# crawler
**Facebook crawler** with **python3.x** (the "ladder" need solving by yourself)

## Packages
**selenium**, **requests**, **BeautifulSoup4** and other built-in packages, such as **re**, **shutil**, **time**, **random** and so on <br>

You can use **pychram**, **spyder** or **jupyter notebook** to debug the code. Here, **jupyter notebook** and **IPython** is recommanded as the tool for step debug. <br>

**Install them with "pip" command**

## browser
**Chrome | Firefox**

## class name description

<table>
<tr> <td>Variable</td>         		<td>Value</td>    						<td>Function</td>
<tr> <td>id_class_name</td>    		<td>clearfix sideNavItem stat_elem</td> <td>get the user id</td>
<tr> <td>post_class_name</td>  		<td>_3jk</td>  							<td>make post</td>
<tr> <td>user_item_class_name</td>  <td>_4p2o</td>  						<td>used to search an user in search satus</td>
<tr> <td>user_info_class_name</td>  <td>_32mo</td>  						<td>get user info in search satus</td>
<tr> <td>location_class_name</td>   <td>_pac</td>  							<td>get user loaction in search satus</td>
<tr> <td>id_class_name</td>    		<td>_3u1 _gli _uvb</td>  				<td>get user id in search satus</td>
</table>

Note: these class name may be variant regularly

## Usage
some examples can be saw in **examples.ipynb** file

	user_name = "your user name"
	password = "your password"
	fb = Facebook(user_name, password)
	fb.login()
	

## Documention
	class Facebook

	__init__(self, _user_name=None, _password=None, _browser_type="Chrome", _is_headless=False, _speed_mode="Normal")
	function: constructor function
	parameters:
		_user_name: user name used for Facebook login
		_password: password used for Facebook login
		_browser_type: browser type (Chrome | Firefox)
		_is_headless: whether use headless browser or not (True | False)
		_speed_mode: run speed mode (Extreme | Fast | Normal | Slow)
			"Extreme":	self.timeout = 0
        	"Fast":		self.timeout = randint(1, 3)
  			"Normal":	self.timeout = randint(2, 5)
       		"Slow":		self.timeout = randint(3, 8)
	return:

	log_in(self)
	function: facebook login
	parameters:
	return:
		login_state (0 - False | 1 - True)

	make_post(self)
	function: post photos, videos, text or others to Facebook
	parameters:
	return:

	page_refresh(self, _refresh_times=0)
	function: drop-down refresh of the page
	parameters:
		_refresh_times: the times of refreshing
	return:

	enter_homepage_self(self)
	function: enter the homepage of the current user
	parameter:
	return:

	get_user_id(self, _user_homepage_url)
	function: get the user id via homepage url
	parameter:
		_user_homepage_url: the url of user's homepage
	return:
		user id

	get_friends_list(self, _friends_number=None)
	function: get friends information
	parameters:
		_friends_number: the number of friends to be searched, if None, return all friends information
	return:
		self.user_info_friends: a built-in list 
				Formtat: [user_name, user_id, homepage_url]
	
	
	search_users(self, _keyword, user_number)
	function: get user's information according to key words
	parameters:
		_keyword: user name to be searched
		user_number: the number of uesrs to be searched
	return:
		self.user_info_search: a built-in list
				Formtat: [user_name, user_id, location, homepage_url]

	get_photos_list(self, _homepage_url)
	function: get all photos href via the given homepage url
	parameters:
		_homepage_url: the given homepage url
	return:
		photos_href_list: a photos href list

	get_photo_info(self, _photo_href)
	function: get photo info including url, data, location, text and size
	parameters:
		_photo_href: a photo href
	return: all information about the photo1
				Format: [link, date, location, text, width, height]

	download_photos_one(self, _homepage_url, satrt_date=None, end_date=None,  _folder_name="./")
	function: downloada photos of one user according to the homepage url and date, if the start_date, end_start and other which can be added further are None, download all photos of this user	
	parameters:
		_homepage_url: the homepage url
		start_date: the start of the publish time
		end_date: the end of the publish time
		_folder_name: the floder name of the downloading photo, default is "./"
	return:
	
	download_photos_batch(self, _homepage_url_list, satrt_date=None, end_date=None,  _folder_name="./")
	function: downloada photos of  user according to the homepage url and date, if the start_date, end_start and other which can be added further are None, download all photos of this user	
	parameters:
		_homepage_url: the homepage url
		start_date: the start of the publish time
		end_date: the end of the publish time
		_folder_name: the floder name of the downloading photo, default is "./"
	return:

	
	utils.py
	
	get_packages()
	function: get all installed packages in the current machine
	parameters:
	return:
		_packages: all installed packages in the current machine

	package_check(packages=None)
	function: Check whether the current packages are installed or not
	parameters:
		packages: the packages which need checking
	return:

	folder_make(_folder_name="./")
	function: the encapsulation of function mkdir and exist
	parameters:
		_folder_name: the folder name which need creating
	return:


	get_time(_unix_time_stamp)
	function: exchange the expression of the from Unix timestamp to Beijing time
	parameters:
		_unix_time_stamp: Unix timestamp
	return:
		Beijing time in the format of "%Y-%m-%d %H:%M:%S"

	get_unix_stamp(_time_string)
	function: exchange the expression of the from  Beijing time to Unix timestamp
	parameters:
		_time_string: Beijing time in the format of "%Y-%m-%d %H:%M:%S" 
	return:
		Unix timestamp

	get_size(_style_string)
	function: get the width and height of the photo according to the style string extracted from the html page source
	parameters:
		_style_string: the style string extracted from the html page source
	return:
		_width, _height: the width and height of the photo	

	url_type_judge(_url)
	function: url type judgement
	there are two types of url:
		1. https://www.facebook.com/erlyn.jumawan.7
        2. https://www.facebook.com/profile.php?id=100025029671192
    the process mode of these two urls is different, if we want to enter the photos or friends page of the user, the urls are:
		1. https://www.facebook.com/erlyn.jumawan.7/photos
		   https://www.facebook.com/erlyn.jumawan.7/friends

		2. https://www.facebook.com/profile.php?id=100025029671192&sk=photos
		   https://www.facebook.com/profile.php?id=100025029671192&sk=friends
	Thus, we need to get the url type first, so it is convenient for us to get the data of the user
	parameters:
		_url: facebook url
	return:
		_url_type: 1 | 2

	get_jump_url(_main_page_url, _key)
	function: get the jump url according to the key words such as photos, friends, videos, music, books and so on
		_main_page_url: the base url
		_key: the keyword
	return:
		_url: the jump url
	e.g.
		_main_page_url: https://www.facebook.com/erlyn.jumawan.7
		_key: friends
		output: https://www.facebook.com/erlyn.jumawan.7/friends

		_main_page_url: https://www.facebook.com/profile.php?id=100025029671192
		_key: photos
		output: https://www.facebook.com/profile.php?id=100025029671192&sk=photos
	
	download_photos(_link, _folder_name="./", _name=None)
	function: download the photos
	parameters:
		_link: the photo href
		_folder_name: the folder name of downloading photo
		_name: the name of the downloading photo
	return:

	
