# Facebook Crawler
**Facebook crawler** with **python3.x** (the "ladder" need solving by yourself)

## Packages
**selenium**, **requests**, **BeautifulSoup4** and other built-in packages, such as **re**, **shutil**, **time**, **random**, **tkinter** and so on <br>

You can use **pychram**, **spyder** or **jupyter notebook** to debug the code. Here, **jupyter notebook** and **IPython** is recommanded as the tool for step debug. <br>

**Install them with "pip" command**

## browser
**Chrome | Firefox**

## Critical technology
1. 模拟登录 <br>
模拟登录分为初次登录和cookie登录 <br>
Facebook的所有动态上传与数据下载均需在登录状态下完成，因此需先实现模拟登录<br>
	* **初次登录** <br>
	在初次登录中，使用selenium寻找Facebook的账号与密码输入框以及确定项，模拟手工操作实现登录。
	* **cookie登录** <br>
	cookie主要用于解决Facebook反爬检测。若用户频繁登录，则会被Facebook判定为异常，易被封号，因此在初次登录后保存cookie信息，用于后续的操作。
 
			cookie格式(JSON)：
			{
				"secure": true,
				"httpOnly": true, 
				"path": "/", 
				"value": "0J0JP757BRZglDevJ.AWU44Pk-lv2MkD1KmUbFSABhp58.Ba10h6.L8.AAA.0.0.Ba10h_.AWVfmtWL", 
				"name": "fr", 
				"domain": ".facebook.com", 
				"expiry": 1531834239.141339
			}
			其中，expiry为cookie失效日期，格式为Unix时间戳

2. 状态发布 <br>
对网页进行解析，找到状态发布(Make Post)对应的元素，使用selenium对该元素进行定位，并在定位成功后实现点击，从而完成状态的发布。

3. URL解析 <br>
Facebook的用户链接分为两种：1. 用户名； 2.用户ID
两种形式的用户主页链接分别为： <br>
	https://www.facebook.com/qiao.fengchun <br>
	https://www.facebook.com/profile.php?id=100005030479034 <br>
Facebook的用户名从本质上来讲是唯一的，Facebook的用户名分为两种，**显示用户名**和**实际用户名**，如显示用户名为**haha**时，实际用户名则为**haha.521**，因此直接通过用户名对用户进行检索会存在误差。<br>
	用户ID是唯一的，但是不直接对用户可见，需要对页面进行解析才可获取。 <br>
	在用户主页链接的基础上，用户的照片，视频等数据的链接为：<br>
	https://www.facebook.com/qiao.fengchun/friends <br>
	https://www.facebook.com/profile.php?id=100005030479034&sk=photos <br>
可选关键字：["about", "photos", "friends", "videos", "music", "movies", "books", "tv"]

4. 下拉刷新 <br>
Facebook的页面均为Ajax动态加载，使用selenium模拟鼠标行为对页面进行下拉刷新，页面下拉刷新过程中可以预先设定下拉次数，但是会存在**页面信息预估不准**和**无效下拉**两种异常情况。因此，需要找到页面底端标识。 <br>
Facebook有两类页面底端标识，搜索页面的**End of Results**和用户信息页面的**More about you/Username**，考虑到不同语言的情况，不使用关键字检索，使用页面元素检索。 <br>
以上两种底端标识对应的元素标识分别为：

Flag 	 				 | Class Name | id							  |XPath
:-:						 |:-:	      | :-:                           |:-:
 End of Results 		 | uiHeader   | -							  | //*[@id="timeline-medley"]/div/div[2]/div[1]
 More about you/Username | - 		  | browse_end_of_results_footer  | //*[@id="browse_end_of_results_footer"]

5. 原图链接获取 <br>
Facebook的图像采用多级缩略图形式，用户主页，用户图片主页，图片以及全屏图片四种模式下的图片链接不完全相同,且每次重新加载后图像链接会更改，链接无法多次使用。 <br>

6. 图片下载 <br>
使用requests和shutil库对图片进行下载

		if response.status_code == 200:
		photo_file_name = os.path.join("***.jpg")
		with open(photo_file_name, "wb") as file:
			shutil.copyfileobj(response.raw, file)

7. 用户检索 <br>
Facebook对用户检索采用的是**模糊检索**方式，随机输入一个昵称后会返回零个或多个相近结果，对页面分析后可得到用户的实际昵称，ID，主页链接和相关信息（如工作单位或所在城市等）

8. 页面分析 <br>
页面分析使用BeautifulSoup4库，使用find_all方法，找到指定的id，class，span，text后即可实现元素获取

## URL Descaiption
**homepage**

+ https://www.facebook.com/

**login failure**

+ https://www.facebook.com/login.php?login_attempt=1&lwv=110
+ https://www.facebook.com/login.php&lwv=110

**user homepage**
	
+ https://www.facebook.com/qiao.fengchun
+ https://www.facebook.com/profile.php?id=100005030479034
+ https://www.facebook.com/100005030479034

**search** <br>

- *https://www.facebook.com/search/"item"/?q="keyword"* <br>

"**item**" and "**keyword**" can be replaced according to the demand <br>
**item type**: posts, people, photos, videos, shop, pages, places, groups, apps, events, links <br>
In this project, we mainly use the search of **people**, **photos**, **videos**. <br>

+ https://www.facebook.com/search/people/?q=test
+ https://www.facebook.com/search/str/test/keywords_users
+ https://www.facebook.com/search/photos/?q=test
 
**user info** <br>

- *https://www.facebook.com/"user_name"/"keyword"/* <br>
- *https://www.facebook.com/profile.php?id="user_id"&sk="item"/* <br>

"**item**" and "**user_id**" can be replaced according to the demand <br>
**item type**: about, photos, friends, videos, music, movies, books, tv <br>

+ https://www.facebook.com/qiao.fengchun/friends
+ https://www.facebook.com/profile.php?id=100005030479034&sk=photos

## Mechanism
**User Search** <br>
<table>
<tr> <td>			      XPath						   								</td>   <td>   Variable    				 </td> </tr>
<tr> <td> //*[@id="BrowseResultsContainer"]/div[m]/div 								</td>	<td> m=1,2,3,4,5 				 </td> </tr>
<tr> <td> //*[@id="u_ps_fetchstream_0_3_0_browse_result_below_fold"]/div/div[n]/div </td>	<td> n=1,2,3,4,5,6 			 </td> </tr>
<tr> <td> //*[@id="fbBrowseScrollingPagerContaineri"]/div/div[j]/div 				</td>	<td> i=1,2,... j=1,2,3,4,5,6 </td> </tr>
</table>

**User Search** <br>

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

	
