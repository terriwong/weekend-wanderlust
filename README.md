# Weekend Wanderlust
###A full-stack web app built in 4 weeks as Hackbright Fellowship final project
<img src="https://cloud.githubusercontent.com/assets/4592446/13552705/a176d93a-e322-11e5-8f97-170b77e42f39.png" alt="Weekend Wanderlust Homepage screenshot">
####Project Overview
Weekend Wanderlust is an interactive map for weekend explorers in San Francisco Bay Area. It maps upcoming weekend events, uncovers hidden-gems nearby, provides routing estimates and realtime updated information to help users plan for their weekend adventures. Hidden-gems are local businesses or unique spots that worth visiting if you are around. They are "hidden" by default, users can discover them by clicking on an event, typing an address, using current location or activating the "Explorer Circle" to sweep around - all will lead to a more detailed map showing hidden-gems within 1 mile, tips & photos, and normal/popular hours. User can save trip notes via sms for handy info on the go - and you will never get bored by discovering more.
####Project Tech Stack
PostgresSQL, SQLAlchemy, Python, Flask, JavaScript, JQuery, Ajax,  Jasmine, Selenium, HTML5, CSS3
####APIs Used
FuncheapSF, hiddenSF, Leaflet, Mapbox.js,  Google Geocoding, Mapbox Directions, Foursquare, Twilio
####GitHub Project URL
https://github.com/terriwong/weekend-wanderlust
####Features
#####Explore from upcoming weekend events
![Click event to discover nearby hiddengems](https://cloud.githubusercontent.com/assets/4592446/13623112/fe9ae5ba-e558-11e5-8c3c-33b2d3ffac48.gif)
* Filter events by Friday Night/Saturday/Sunday
* Mouse over event marker to see event info
* Click event marker to uncover hiddengems within 1 mile
* Click hiddengem marker to navigate info
* "Take a closer look" hidden button to show more info from Foursquare
* Add Trip Note of addresses & hours

#####Explore by activating Explorer Circle
![Explorer Circle](https://cloud.githubusercontent.com/assets/4592446/13623393/314f316c-e55b-11e5-9721-d7ff122970dd.gif)
* Constantly getting mouse's location to calculate and show hiddengems within 1 mile circle

#####Explore from current location
![demo-search-by-current-location](https://cloud.githubusercontent.com/assets/4592446/13626894/b54dc536-e57a-11e5-8c5e-56969213cd0f.gif)
* Get browser's location by HTML5 geolocation api

#####Explore from a typed address
![demo-search-by-address](https://cloud.githubusercontent.com/assets/4592446/13626726/63c1cb50-e579-11e5-891e-c22683b18368.gif)
* Locate typed address by Google Geocoding api

#####Get routing estimates from selected waypoints
![Get routing estimates from selected waypoints](https://cloud.githubusercontent.com/assets/4592446/13623502/e2d22cd2-e55b-11e5-8541-92efa6da782c.gif)
* Get smart route from Mapbox Directions api

#####Send Trip Note via SMS
![Send Trip Note via SMS](https://cloud.githubusercontent.com/assets/4592446/13623605/a1abebe8-e55c-11e5-8b2d-17dc7a922add.gif)
* Open Trip Note panel, send Trip Note in one SMS using Twilio programmable sms api

##### Formatted Trip Note SMS
![SMS](https://cloud.githubusercontent.com/assets/4592446/13623776/c9631908-e55d-11e5-8cf3-df6812c06730.gif)
* Trip Note SMS is formatted in a way that's handy on the go
