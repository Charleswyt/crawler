# Facebook Crawler
**Facebook crawler** with **python3.x** (the "ladder" need solving by yourself). <br>
The official website of Python is https://www.python.org. <br>

## Packages
**selenium**, **requests**, **BeautifulSoup4** and other built-in packages, such as **re**, **shutil**, **time**, **random**, **tkinter** and so on.

You can use **pychram**, **spyder** or **jupyter notebook** to debug the code. Here, **jupyter notebook** and **IPython** is recommanded as the tool for step debug.

**Install them with "pip" command**.

The homepage url of **selenium** is https://www.seleniumhq.org/download/.

## Browser
**Chrome | Firefox** (In this project, Chrome is applied.)

## How to use
1. Install the packages and browser mentioned above.
2. Check whether your browser can be opened via the code.
	+ If you use **Chrome browser** <br>
	
	Copy the **Chromedriver** into the python path or other path in the enviroment variables.
	The download link of Chromedriver is http://chromedriver.storage.googleapis.com/index.html. <br>
	Download the suitable version according to the version of Chrome browser. <br>
	The version of Chrome browser can be seen in "帮助 -> 关于Google Chrome"， either upgrade the Chrome browser or download corresponding Chromedriver is OK. <br>

	+ If you use **Firefox browser** <br>
	
	You just control Firefox at an appropriate version in order to avoid some incompatible error. <br>

3. Run the code
	+ For **Test**: to the path of the scripts and open the command line (Win + R and input "cmd"). Input "jupyter notebook", enter.
	+ For **Run**: Use arbitrary IDE such as PyCharm. Or, use C++ or C# to call the scripts.

## Critical Technology （This part is written in Chinese， and can be seen optionally.）
### Main procedure
#### 1. 模拟登录 <br>
模拟登录分为**初次登录**和**cookie登录**
Facebook的所有动态上传与数据下载均需在登录状态下完成，因此需先实现模拟登录
	* **初次登录**
	在初次登录中，使用**selenium**寻找Facebook的账号与密码输入框以及确定项，模拟手工操作实现登录。
	* **cookie登录**
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


#### 2. 状态发布 <br>
对网页进行解析，找到状态发布(Make Post)对应的元素，使用selenium对该元素进行定位，并在定位成功后实现点击，从而完成状态的发布，发布过程与直接使用浏览器登录Facebook并发布内容相同。

#### 3. URL解析 <br>
Facebook的用户链接分为两种：1. 用户名； 2.用户ID <br>
两种形式的用户主页链接分别为： <br>
	用户名形式：https://www.facebook.com/qiao.fengchun <br>
	用户ID形式：https://www.facebook.com/profile.php?id=100005030479034 <br>
	
+ 用户名

	Facebook的用户名从本质上来讲是唯一的，用户名分为两种，**显示用户名**和**实际用户名**，如显示用户名为**haha**时，实际用户名则可能为**haha.521**，因此直接通过显示用户名对用户进行检索会存在误差，实际用户名需在登录用户主页后才可获得。此外，Facebook会对用户名中的空格直接填充"."，如qiao fenchun的实际用户名为qiao.fengchun。<br>
	
+ 用户ID

	用户ID是唯一的，但是不直接对用户可见，需要对页面进行解析才可获取。 <br>
	
	在用户主页链接的基础上，用户的照片，视频等数据的链接为：<br>
	https://www.facebook.com/qiao.fengchun/friends <br>
	https://www.facebook.com/profile.php?id=100005030479034&sk=photos <br>
可选关键字：["about", "photos", "friends", "videos", "music", "movies", "books", "tv"]

#### 4. 下拉刷新 <br>
Facebook的页面均为Ajax动态加载，使用selenium模拟鼠标行为对页面进行下拉刷新，页面下拉刷新过程中可以预先设定下拉次数，但是会存在**页面信息预估不准**和**无效下拉**两种异常情况。因此，需要找到**页面底端标识**。 <br>
+ **页面信息预估不准**：当需要获取的用户量大于页面显示的用户量时会出现该类问题 <br>
+ **无效下拉**：当所有信息全部显示后仍执行额外的下拉操作 <br>
以上两种异常情况会影响程序的执行效率，应尽量避免。<br>
+ **解决方案**：<br>
Facebook有两类页面底端标识，搜索页面的**End of Results**和用户信息页面的**More about you/Username**，考虑到不同语言的情况，不使用关键字检索，使用页面元素检索。 <br>
以上两种底端标识对应的元素标识分别为：

Flag 	 				 | Class Name | id							  |XPath
:-:						 |:-:	      | :-:                           |:-:
 End of Results 		 | uiHeader   | -							  | //*[@id="timeline-medley"]/div/div[2]/div[1]
 More about you/Username | - 		  | browse_end_of_results_footer  | //*[@id="browse_end_of_results_footer"]
 

#### 5. 原图链接获取 <br>
Facebook的图像采用多级缩略图形式，**用户主页**，**用户图片主页**以及**图片预览**三种模式下的图片链接不完全相同，且从用户主页和用户图片主页均可进入到图片预览模式，两种模式下的链接不同，但均可实现图片的下载。本项目中使用从图片主页窗口进入的方式。 <br>
图片预览状态下获取图片链接易捕获无效链接，预览状态下的图片链接与全屏放大后的链接虽然相同，但是直接在预览状态下下载的图片仍不是原图，因此采用**全屏放大**后再获取链接的方式。<br>

#### 6. 图片信息获取 <br>
我们主要获取图片的**链接**，**发布时间**，**对应文字**，**尺寸**以及**发布位置**，对应文字和发布位置有可能为空

#### 7. 图片下载 <br>
使用requests和shutil库对图片进行下载

	if response.status_code == 200:
		photo_file_name = os.path.join("***.jpg")
		with open(photo_file_name, "wb") as file:
			shutil.copyfileobj(response.raw, file)

#### 8. 检索 <br>
Facebook采用的是**模糊检索**，随机输入一个关键字后会返回零个或多个相近结果，包括用户，照片，主页等，
不同的检索内容对应不同的URL：
URL: https://www.facebook.com/search/str/"**keyword**"/**type**
+ keyword为待检索的字符串
+ type为待检索的类型
在各类检索中，还可进一步进行条件筛选，筛选条件在URL中为**JSON**形式
	##### **用户 (People)**：keywords_users
	+ 筛选类型：<br>
	
		- CITY
			* Any city
			* Choose a City

		- EDUCTION
			* Any school
			* Choose a School
		
		- WORK
			* Any company
			* Choose a Company
		
		- MUTUAL FRIENDS
			* Anyone
			* Friends
			* Friends of Friends
			* Mutual Friends with  

		全部选**Any**时，URL为上述URL，当筛选条件存在时，则为:

		+ **filters_city**={"**name**":"users_location", "**args**":"110730292284790"}
		+ **filters_school**={"**name**":"user_school", "**args**": "7701216166"}
		+ **filters_employer**={"**name**":"users_employer**","**args**":"20528438720"}
		+ **filters_friends**={"**name**":"users_friends","**args**":"100024373853102"} **or** **filters_friends**={"**name**":"users_friends_of_friends","**args**":"100024373853102"} **or** **filters_friends**={"**name**":"users_friends","**args**":"100024373853102"}
		args的键值均为ID，使用filters_friends筛选时，ID为用户ID，可通过网页解析获取，其余ID均为先验 
			各JSON字段之间用"&"连接
	##### **主页 (pages)**：keywords_pages <br>
		
	+ 筛选类型：<br>

		- VERIFIED
			* Verified

		- CATEGORY
			* Any category
			* Local Business or Place
			* Company, Organization or Institution
			* Brand or Product
			* Artist, Band or Public Figure
			* Entertainment
			* Cause or Community
		
		全部选**Any**时，URL为上述URL，当筛选条件存在时，则为:
		
		+ **filters_verified**={"**name**":"pages_verified","**args**":""}
			
		+ **filters_category**={"**name**":"pages_category","**args**":"1006"}  <br>
			
			**args**:
				
			* 1006 (Local Business or Place) <br>
			* 1013 (Local Business or Place) <br>
			* 1009 (Brand or Product) <br>
			* 1007,180164648685982 (Artist, Band or Public Figure) <br>
			* 1019 (Entertainment) <br>
			* 2612 (Cause or Community) <br>
		
	##### **照片 (Photos)**：photos-keyword <br>

	+ 筛选类型：<br>
		
		- POSTED BY
			
			* Anyone
			* You
			* Your Friends
			* Your Friends and Groups
			* Choose a Source

		- TAGGED LOCATION
			* Anywhere
			* Choose a Location
	
		- DATE POSTED
			* Any date
			* 2018
			* 2017
			* 2016
			* Choose a Date
	
		全部选**Any**时，URL为上述URL，当筛选条件存在时，则为:

		+ **filters_rp_author**={"**name**":"author_me","**args**":""}
			
			**name**:
			
			- author_me (You)
			- author_friends (Your Friends)
			- author_friends_groups (Your Friends and Groups)
			- author (Choose a Source) args有值
		
		+ **filters_rp_location**={"**name**":"location","**args**":"106324046073002"}
		
		+ **filters_rp_creation_time**={"**name**":"creation_time","**args**":"{\"start_year\":\"2018\",\"start_month\":\"2018-01\",\"end_year\":\"2018\",\"end_month\":\"2018-12\"}"}
			**aregs**：
			+ 指定年份，如2017，则键值为:
					
					{
						"start_year":"2017",
						"start_month":"2017-01",
						"end_year":"2017",
						"end_month":"2017-12"
					}
			+ 不指定年份，选定的时间需具体到月份，键值为：
				
					{
						"start_month":"2017-05",
						"end_month":"2017-05"
					}

	##### **小组 (Group)** ：keywords_groups
	+ 筛选类型
		- SHOW ONLY
			
			* Any group
			* Public Groups
			* Closed groups
		- MEMBERSHIP
			* Any group
			* Friends' groups
			* My groups	
		
		全部选**Any**时，URL为上述URL，当筛选条件存在时，则为:
		
		+ **filters_groups_show_only**={"**name**":"public_groups","**args**":""}
			
			**name**:
			
			- public_groups (Public Groups)
			- closed_groups (Closed groups)

		+ **filters_groups_memebership**={"**name**":"friends_groups","**args**":""}

			**name**:
			
			- friends_groups (Friends' groups)
			- my_groups (My groups)
			
	##### **视频 (Videos)**：keywords_videos

	无筛选类型
	
	##### **事件 (Events)**：keywords_events

	+ 筛选类型：<br>

		- SHOW ONLY
			
			* Popular with Friends

		- LOCATION
			
			* Anywhere
			* Choose a City
			* My groups
		
		- DATE
			* Any date
			* Today
			* Tomorrow
			* This week
			* This weekend
			* Next week

		全部选**Any**时，URL为上述URL，当筛选条件存在时，则为:
		
		+ **filters_rp_events_popular_with_friends**={"**name**":"filter_events_popular_with_friends","**args**":""}

		+ **filters_rp_events_location**={"**name**":"filter_events_location","**args**":"106283509403187"}

		+ **filters_rp_events_date**={"**name**":"filter_events_date","**args**":"2018-04-26"}
			
			**args**:

			- 2018-04-26 (Today)
			- 2018-04-27 (Tomorrow)
			- 2018-04-23~2018-04-29 (This week)
			- 2018-04-28~2018-04-29 (This weekend)
			- 2018-04-30~2018-05-06 (Next week)
				
	##### **链接 (Links)** : links-keyword/articles-links
	无筛选类型
	
	##### **应用 (App)**   : keywords_apps
	无筛选类型
	
#### 9. 页面分析
页面分析使用**selenium**和**BeautifulSoup4**库
selenium用于**动态解析**，如页面加载等待，查找输入框等
BeautifulSoup4用于**静态解析**

#### 10. 页面返回信息为空
在用户检索和查看用户媒体内容时，会出现内容为空的情况，Facebook会给用户以相应的提示，通过该类标识元素即可对页面内容进行判断。
+ 用户搜索返回为空
通过查找id=empty_result_error的元素即可完成判断
+ 用户媒体内容返回为空
通过查找**No photos to show**字符串进行判断

## Flag Description

<table>

 Variable 						| 	 	Type 		| 		         Value					|   			  Function							|
 :-:							| 	 	:-:			| 		          :-					|					:-								|
 browse_results_container_id	|        ID			| 		  BrowseResultsContainer  		|   用于在**用户检索**时获取用户信息块的类名		   		|
 clearfix_flag  				|    Class Name 	|	      	    clearfix				| 	用于在**用户检索**时获取用户						|
 post_class_name				|    Class Name		|  **\_3jk** (may be changed regularly)	|   用于实现用户**动态发布** 							|
 user_cover_class_name			|    Class Name		| 			     cover  				|   用户封面类名，用于从用户主页**获取用户ID**			|
 bottom_class_name 				|	 Class Name		|		     uiHeaderTitle				|   用户照片，视频等媒体内容页面的底线，用于**下拉刷新**	|
 browse_end_of_results_footer	|	 	 ID			|      browse_end_of_results_footer		|   用户搜索页面的底线，用于**下拉刷新**				|
 full_screen_id					| 		 ID			|	  fbPhotoSnowliftFullScreenSwitch   |	用于**图片全屏点击**，方便获取图片URL				|
 homeSideNav					|    Class Name		|			  homeSideNav				|   facebook用户登录页导航栏，用于**判断是否登录成功**	|
 friends_list_class_name		|    Class Name		|		  uiProfileBlockContent			|	用于**获取好友信息**								|
 friends_number_id_name      	|    	 ID			|	  pagelet_timeline_medley_friends	|	用于**获取当前用户的好友数量**						|
 
 

### Screenshot <br>
Some Screenshots are shown below, the order is the same as the table in Flag Description. <br>
#### 用户信息获取
由于存储用户信息的类名**_4p2o**有可能定期变化，ID更改的几率较低，因此为了降低后期维护成本，通过改ID获取到类名后再进一步获取用户信息。
![](https://i.imgur.com/CjgN1dD.png)
#### 好友信息获取
![](https://i.imgur.com/QRkLbG9.png)
#### 图片信息获取
##### 图片链接与尺寸
![](https://i.imgur.com/UcGrNsb.png)
##### 图片发布位置
![](https://i.imgur.com/ZnQW9M3.png)
##### 图片发布时间
![](https://i.imgur.com/eSFTbne.png)
##### 图片发布对应文字
![](https://i.imgur.com/4ZHDvnn.png)


## Usage
A run demo can be saw in **demo.ipynb** file, the usage of jupyter can be seen in the "How to use" <br>

	user_name = "your user name"
	password = "your password"
	fb = Facebook(user_name, password)
	fb.sign_in()	# 账户登录
	fb.make_post()	# 状态发布
	fb.driver.quit()# 关闭浏览器 (选择使用)
	
	user_name = "qiaofengchun"	# 待检索用户昵称
	user_number = 3			# 待检索用户数量
	user_info_list = fb.search_users(user_name=user_name, user_number=user_number) 	# 获取用户信息

	# 打印检索得到的用户信息
	index = 1
	for user_info in user_info_list:
    	print("No.", index, "user info:", user_info)
    	index += 1

	# 图像的批量下载
	fb.download_photos_batch(user_info_list, "photos")


## API Documention
	class Facebook

	__init__(self, _email=None, _password=None, _browser_type="Chrome", _is_headless=False)
	function: constructor function
	parameters:
		_email: user email used for Facebook login
		_password: password used for Facebook login
		_browser_type: browser type (Chrome | Firefox)
		_is_headless: whether use headless browser or not (True | False)
	return:
		browser_state:
			0 - init fail
            1 - init success
	
	def get(self, url)
	function: web pages hop, avoid repeated hop. If the current url is the same as the url, no operation.
	parameters：
		url: the forthcoming url
	return:
		 

	login_with_account(self)
	function: facebook login via email and password
	parameters:
	return:

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

	
