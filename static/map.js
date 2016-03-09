/* Weekend Wanderlust Map JavaScript. */

// show loader animation during ajax call
    $(document).ready(function() {
        $(document).ajaxStart(function() {
          $('#wait').css("display", "block");
        });
        $(document).ajaxComplete(function() {
          $('#wait').css("display", "none");
        });
    });

    // helper function to open and close trip panel
    function openPanel() {
      document.getElementById('trip-panel').style.display = "block";
      console.log("Finished open Trip Panel");
    }

    function closePanel() {
      document.getElementById('trip-panel').style.display = "none";
    }

    // display info in More-info box
    function showInfo(results) {
      console.log(results);
      $('#foursquare-photos').empty();
      $('#tips-content').empty();
      $('#normal-hours-content').empty();
      $('#popular-hours-content').empty();
      var markerId = results.marker_id;
      var venueName = results.name;
      var photoUrls = results.photos;
      var address = results.address;
      for (i=0; i < photoUrls.length; i++) {
        var photoHtml = '<img src="' + photoUrls[i] + '" class="panel-photo">'
        document.getElementById('foursquare-photos').innerHTML += photoHtml;
      }
      var tips = results.tips;
      for (i=0; i < tips.length; i++) {
        var tipHtml = '<p class="tip-text"><b>"</b>' + tips[i] +'<b>"</b></p>'
        document.getElementById("tips-content").innerHTML += tipHtml;
      }
      var normalHours = results.hours;
      for (i=0; i < normalHours.length; i++) {
        var normalHoursHtml = '<li class="commands-item"><span class="item-title">' + normalHours[i].days + '</span><span class="item-info">' + normalHours[i].open[0].renderedTime + '</span><button class="commands-item-action" id="addTripNote" data-id="' + markerId + '" data-name="' + venueName + '" data-address="' + address + '">Add trip note</button></li>';
        $('#normal-hours-content').append(normalHoursHtml);
        // document.getElementById("normal-hours-content").innerHTML += normalHoursHtml;
      }
      var popularHours = results.popular_hours;
      for (i=0; i < popularHours.length; i++) {
        var popularHoursHtml = '<li class="commands-item"><span class="item-title">' + popularHours[i].days + '</span><span class="item-info">' + popularHours[i].open[0].renderedTime + '</span><button class="commands-item-action"  id="addTripNote" data-id="' + markerId + '" data-name="' + venueName +'" data-address="' + address + '">Add trip note</button></li>';
        $('#popular-hours-content').append(popularHoursHtml);
        // document.getElementById("popular-hours-content").innerHTML += popularHoursHtml;
      }
      // console.log(tips);
    }


    // Add trip note of hiddengems from more-info panel
    $("#more-info").on('click', '#addTripNote', (function(e) {
      e.preventDefault();
      $(this).text("Trip note added!");
      var day = $(this).prev().prev().text();
      console.log(day);
      var hours = $(this).prev().text();
      console.log(hours);
      var target = document.querySelector('#addTripNote');
      var targetId = target.dataset.id;
      var targetName = target.dataset.name;
      var targetAddress = target.dataset.address;
      console.log(targetId);
      var newNote = '<div class="noteBlock"><span class="noteTitle">' + targetName + '</span><span class="noteAddress">' + targetAddress +'</span><span class="noteHours">' + day + " " + hours + '</span></div>';
      $('#tripPreviewContent').append(newNote);
      $.post('/add_trip_note', {
                              "marker_id": targetId,
                              "name": targetName,
                              "selected_day": day,
                              "selected_hour": hours
                            }, showStatus);
      $('#tripPreviewModal').addClass("modal-visible");
      // $.get('/update_trip_note', updateTripNoteBoard);
    }));


    // Add trip note of events from popup
    $('#map').on('click', '.event-add-note-btn', function (e){
      e.preventDefault();
      console.log(this.dataset.name);
      var targetId = this.dataset.id;
      var targetName = this.dataset.name;
      var targetAddress = this.dataset.address;
      var day = this.dataset.date;
      var hours = this.dataset.time;
      var newNote = '<div class="noteBlock"><span class="noteTitle">' + targetName + '</span><span class="noteAddress">' + targetAddress +'</span><span class="noteHours">' + day + " " + hours + '</span></div>';
      $('#tripPreviewContent').append(newNote);
      $.post('/add_trip_note', {
                              "marker_id": targetId,
                              "name": targetName,
                              "selected_day": day,
                              "selected_hour": hours
                            }, showStatus);
      $('#tripPreviewModal').addClass("modal-visible");
    });


    // open panel to show more info from Foursquare api
    function openMoreInfoPanel(data) {
      document.getElementById("grandMoreInfo").className = "animatedPanel rotate";
      $.get('/more_info_from_foursquare', {'marker_id': data}, showInfo);
      console.log(data);
    }

    // experiment
    // $('.drop').on('click', function(e) {
    //   e.preventDefault();
    //   $.get('/more_info_from_foursquare', {'marker_id': this.dataset.id}, showInfo);
    //   console.log("Finished showInfo");
    //   // overlay.classList.toggle('overlay--visible');

    //   // if (overlay.classList.contains('overlay--visible')) {
    //   //   reset(true);
    //   // }
    // });

    function closeMoreInfoPanel() {
      document.getElementById("grandMoreInfo").className = "animatedPanel";
    }

    // Scroll to sections in More Info Panel
    var tips = document.getElementById('tab-tips');
    var photos = document.getElementById('tab-photos');
    var other = document.getElementById('tab-other');

    tips.onclick = function(e) {
        photos.className = "tabs-label";
        other.className = "tabs-label";
        this.className = "tabs-label tabs-label--active";
        $('#more-info').scrollTo('#section1', {duration: 'slow'});        
    };

    photos.onclick = function(e) {
        tips.className = "tabs-label";
        other.className = "tabs-label";
        this.className = "tabs-label tabs-label--active";
        $('#more-info').scrollTo('#section2', {duration: 'slow'});        

    };

    other.onclick = function(e) {
        tips.className = "tabs-label";
        photos.className = "tabs-label";
        this.className = "tabs-label tabs-label--active";
        $('#more-info').scrollTo('#section3', {duration: 'slow', offset:{top:-55}}); 
    };


    // load mapbox public access token.
    L.mapbox.accessToken = 'pk.eyJ1IjoidGVycml3bGVlIiwiYSI6ImNpazZlaThsajAwcXdpMm0ycHUyZjhiYjkifQ.zvJK8nAc3HpNOtCAMh5QlQ';

    // load base map, set initial position, add search controller.
    var map = L.mapbox.map('map', 'mapbox.streets')
        .setView([37.71, -122.327], 10);
        // .addControl(L.mapbox.geocoderControl('mapbox.places')); //search


    // add event layer to map and load event markers geojson.
    var eventLayer = L.mapbox.featureLayer().addTo(map);
    eventLayer.loadURL('/events.geojson');

    // create hiddengemLayer, load geojson, but not add to map just yet.
    var hiddengemLayer = L.mapbox.featureLayer().loadURL('/hiddengems.geojson');

    // when click on any event marker, zoom in and show nearby hiddengems
    eventLayer.on('click', function(e) {
        map.setView(e.latlng, 14);
        map.panTo(e.latlng);
        hiddengemLayer.addTo(map);
        showWithin(e);
        countWithin(e);
        showInView();
        document.getElementById('gems').className = "label show";
      });

    // when click on hiddengem marker, zoom in, center and show info.
    hiddengemLayer.on('click', function(e) {
      map.setView(e.latlng, 14);
      map.panTo(e.latlng);
      showInView();
      var id = e.layer.feature.id;
      console.log(id);
      $('#coordinates').scrollTo('#'+ id, {duration: 'slow'});
    });


    // define the 1 mile radius circle for showWithin
    var RADIUS = 1610;
    var filterCircle_options = {
          color: "#33cccc",
          opacity: 1,
          weight: 1.5,
          fillOpacity: 0.1
        };
    var filterCircle = L.circle([0,0], RADIUS, filterCircle_options).addTo(map);


    // intend to add draggable marker to circle center, under development
    // function addDraggableMarker(e) {
    //   var marker = L.marker(new L.LatLng(e.latlng), {
    //     icon: L.mapbox.marker.icon({
    //       'marker-color': 'ff8888'
    //     }),
    //     draggable: true
    //   });
    // }

    // function to count hiddengems within radius circle
    function countWithin(e) {
      var counter = 0;
      hiddengemLayer.eachLayer(function(marker) {
        if (e.latlng.distanceTo(L.latLng(
          marker.feature.geometry.coordinates[1], marker.feature.geometry.coordinates[0])) < RADIUS) {
          counter += 1;
        }
      });
      document.getElementById('start').className = "label hide";
      document.getElementById('gems').className = "label";
      document.getElementById('counter').innerHTML = counter;
    }

    // function to show hiddengems within radius circle
    function showWithin(e) {
      filterCircle.setLatLng(e.latlng);
      console.log(e.latlng);
      hiddengemLayer.addTo(map);
      hiddengemLayer.setFilter(function showGems(feature) {
        return e.latlng.distanceTo(L.latLng(
          feature.geometry.coordinates[1],
          feature.geometry.coordinates[0])) < RADIUS;
      });
    }


    //  Explorer mode: 1 mile radius circle on mousemove
    $('#show-circle').on('click', function() {
      map.on('mousemove', function(e) {
        showWithin(e);
        countWithin(e);
      });
      map.on('click', function(e) {
        map.off('mousemove');
        showWithin(e);
        countWithin(e);
      });
      document.getElementById('explorer').className = "label show";
      document.getElementById('gems').className = "label hide";

    });

    // remove mousemove and reset filterCircle
    $('#remove-circle').on('click', function() {
      filterCircle.setLatLng([0,0]);
      map.off("mousemove");
      map.off("click");
      hiddengemLayer.setFilter(function showWithin(feature) {
        return true;
      });
      document.getElementById('explorer').className = "label hide";
      document.getElementById('start').className = "label show";
      console.log("Finished remove filterCircle");
    });
 

    function showInView() {
      $('#coordinates').empty();
      var bounds = map.getBounds();

      hiddengemLayer.eachLayer(function(marker) {

        // check if marker is in view, if yes, construct contents to show in preview box
        if (bounds.contains(marker.getLatLng())) {
          var listContent = '<div><img id="' + marker.feature.id + '"class="listImg" src="' + marker.feature.properties.img_url + '" /><div class="ui_box"><div class="ui_box__inner" id="container" data-id="' + marker.feature.id + '" data-latlng="' + marker.feature.geometry.coordinates + '">' + '<p><b>' + marker.feature.properties.name + '</b><br>' + marker.feature.properties.description + '</p></div><div class="drop" data-id="' + marker.feature.id + '" onclick="openMoreInfoPanel('+ marker.feature.id +')"><p>Take a closer look</p><div class="arrow"></div></div></div></div>';
            
          document.getElementById('coordinates').innerHTML += listContent;
        }
        
        // when mouseover preview box, dim the info box background and show corresponding marker
        $("#coordinates div").hover(
        function(){ // mouseenter
          // $(this).addClass("hover");
          var target = this.dataset.id;
          // console.log(target);
          hiddengemLayer.eachLayer(function(marker){
            // console.log(target);
            if (marker.feature.id == target) {
              marker.openPopup();
            }
          });
        }, 
        function(){ // mouseleave
          $(this).removeClass("hover");
        }); 
      });
    }


    // customize hiddengem popup content
    hiddengemLayer.on('layeradd', function(e) {
        var marker = e.layer,
            feature = marker.feature;

        var popupContent = '<b>' + feature.properties.name + '</b><br>' + feature.properties.address + '<br><form action="/add_waypoint"><input type="hidden" name="marker_id" onclick="openPanel()" value="' + feature.id + '"><button id="popupButton" class="trigger" onclick="openPanel()" data-id="' + feature.id + '" data-name="' + feature.properties.name + '">Add waypoint</button></form>'; 
        
        marker.bindPopup(popupContent, {
            closeButton: true,
            minWidth: 120
            });
    });

    // customize event popup content
    eventLayer.on('layeradd', function(e) {
        var marker = e.layer,
            feature = marker.feature;
            // console.log(feature);

        var popupContent = '<b>' + feature.properties.title + '</b><br><small>' + feature.properties.date + ' | ' + feature.properties.time + '</small><br>' + feature.properties.description + '<br><div><small>Address: ' + feature.properties.address + '</small></div><input type="hidden" name="marker_id" value="' + feature.id + '"><button id="popupButton" class="trigger" onclick="openPanel()" data-id="' + feature.id + '" data-name="' + feature.properties.name + '">Add waypoint</button><button id="eventTripNoteBtn" class="event-add-note-btn" data-id="'+ feature.id +'"data-name="' + feature.properties.name +'" data-address="'+ feature.properties.address +'" data-date="' + feature.properties['date-tier'] +'" data-time="'+ feature.properties.time + '">Add Trip Note</button>'; 
        
        marker.bindPopup(popupContent, {
            closeButton: true,
            minWidth: 120
            });
    });


    // show tooltips when mouse over onto event marker
    eventLayer.on('mouseover', function(e) {
        e.layer.openPopup();
    });

    hiddengemLayer.on('mouseover', function(e) {
        e.layer.openPopup();
    });


    // Toggling layers by event category
    var all = document.getElementById('filter-all');
    var friday = document.getElementById('filter-friday');
    var saturday = document.getElementById('filter-saturday');
    var sunday = document.getElementById('filter-sunday');

    friday.onclick = function(e) {
        all.className = '';
        saturday.className = '';
        sunday.className = '';
        this.className = 'active';
        eventLayer.setFilter(function(f) {
            return f.properties['date-tier'] === 'Friday Night';
        });
        return false;
    };

    saturday.onclick = function(e) {
        all.className = '';
        friday.className = '';
        sunday.className = '';
        this.className = 'active';
        eventLayer.setFilter(function(f) {
            return f.properties['date-tier'] === 'Saturday';
        });
        return false;
    };

    sunday.onclick = function(e) {
        all.className = '';
        friday.className = '';
        saturday.className = '';
        this.className = 'active';
        eventLayer.setFilter(function(f) {
            return f.properties['date-tier'] === 'Sunday';
        });
        return false;
    };

    all.onclick = function() {
        friday.className = '';
        saturday.className = '';
        sunday.className = '';
        this.className = 'active';
        eventLayer.setFilter(function(f) {
            return true;
        });
        return false;
    };

    // helper function to update the waypoint list
    function updateList(results) {
      var board = document.getElementById('waypoint-list');
      var info = '<li>' + results + '</li>';
      board.innerHTML += info;
      // $('#tripPreviewContent').append(info);
    }

    // helper function to show "add to trip" status
    function addWaypoint(results) {
      var status = results;
      $('#popupButton').html(status);
      console.log("Finished showStatus");
      if (status == "Waypoint added!") {
        $.get('/get_new_waypoint_name', updateList);
        console.log("Finished update list");
      }
    }

    // show status message in trip panel and fade out
    function showStatus(results) {
      $('#status').text(results).addClass("is-visible").delay(800).fadeOut();
      openPanel();
    }

    // helper function to update travel profile on planner panel
    function updateProfile(results) {
      var profile = results;
      $('#selected-profile').html(profile);
      console.log("Finished update profile")
    }

    // layer for route
    var routeLayer = L.geoJson().addTo(map);
    
    //function to show route and details
    function showRoute(results) {
        clearRoute();
        // get LineString geojson
        var myLines = results.geometry;
        // add LineString to routeLayer
        routeLayer.addData(myLines);
        // style route
        routeLayer.setStyle({
          "color": "#ff7800",
          "weight": 5,
          "opacity": 0.65 });
        // console.log for debugging
        console.log("Finished add routeLayer");
        // zoom to route
        map.fitBounds(routeLayer.getBounds(), {
          padding:[400, 200]
        });
        // get distance (in meters) from api response
        var distance = (results.distance / 1609.34).toFixed(2);
        document.getElementById('distance').innerHTML = (distance + " miles");
        // get duration (in seconds) from api response
        var duration = Math.round(results.duration / 60);
        document.getElementById('duration').innerHTML = (duration + " mins");
        // console.log for debugging
        console.log("Finished show route");
      }

    // get current location by HTML5 geolocation API
    var geolocate = document.getElementById('geolocate');    
    var currentLocationLayer = L.mapbox.featureLayer().addTo(map);

    // function to geolocate browser
    function findCurrentLocation(e) {
        console.log(e);
        e.preventDefault();
        e.stopPropagation();
        $('#wait').css("display", "block");
        map.locate();
      }

    // function to add marker
    function addMarker(latlng) {

      console.log(latlng);

      var currentMarker = {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [latlng.lng, latlng.lat]
          },
          properties: {
            'title': 'You are here! Click to explore',
            'marker-color': '#F03C02',
            'marker-symbol': 'star'
          }
        };

      currentLocationLayer.setGeoJSON(currentMarker).openPopup();

      console.log("marker added!");
    }

    // check if browser supports geolocation, 
    // if not, notify user;
    // if yes, start geolocation process.
    if (!navigator.geolocation) {
      geolocate.innerHTML = 'Geolocation is not available';
    } else {
      $('#geolocate').on('click', findCurrentLocation);
    }

    // if location is found, zoom in, add marker.
    map.on('locationfound', function(e) {
      
      map.fitBounds(e.bounds, {
        maxZoom: 14
      });

      addMarker(e.latlng);

      $('#wait').css("display", "none");

      // hide the 'to current location' button when finished
      geolocate.parentNode.removeChild(geolocate);

      // click on the newly added marker, show circle, show hiddengems within and count.  
      currentLocationLayer.on('click', function(e) {
        filterCircle.setLatLng(e.latlng);
        hiddengemLayer.addTo(map);
        hiddengemLayer.setFilter(function showGems(feature) {
        return e.latlng.distanceTo(L.latLng(
          feature.geometry.coordinates[1],
          feature.geometry.coordinates[0])) < RADIUS;
        });
        showInView();
        countWithin(e);
      });

    });

    map.on('locationerror', function() {
      geolocate.innerHTML = 'Position could not be found';
    });

    // with latlng from address, add marker on map, zoom in and show nearby
    function findAddress(results) {
      console.log(results);
      $('#wait').css("display", "none");
      if (results.status === "no found") {
        alert("Not found! Try again.");
        return "Not found! Try again.";
      }
      var lnglat = results.coordinates;
      var addressLayer = L.mapbox.featureLayer().addTo(map);

      var newMarker = {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: lnglat
          },
          properties: {
            'title': 'We found it! Click to explore',
            'marker-color': '#F03C02',
            'marker-symbol': 'pitch'
          }
        };

      addressLayer.setGeoJSON(newMarker).openPopup();

      map.fitBounds(addressLayer.getBounds(), {
        maxZoom: 14
      });

      var latlng = {
        lat: lnglat[1],
        lng: lnglat[0]
      };
      console.log(latlng);

      addressLayer.on('click', function(e) {
        filterCircle.setLatLng(e.latlng);
        hiddengemLayer.addTo(map);
        hiddengemLayer.setFilter(function showGems(feature) {
        return e.latlng.distanceTo(L.latLng(
          feature.geometry.coordinates[1],
          feature.geometry.coordinates[0])) < RADIUS;
        });
        showInView();
        countWithin(e);
      });
      
      console.log(newMarker.geometry.coordinates);
      return newMarker.geometry.coordinates
    }


    // On click "Add to trip" button in marker popup, check duplicate
    // and add to session, update status accordingly.
    // "Add to trip" button: the HTML doesn't exist yet, so we can't just say $('#mybutton'). Instead, we listen for click events on the map element which will bubble up from the tooltip, once it's created and someone clicks on it.
    $('#map').on('click', '.trigger', function (e){
      e.preventDefault();
      console.log(this.dataset.id);
      $.get('/add_waypoint', {'marker_id': this.dataset.id}, addWaypoint);
      console.log("Finished sending AJAX to add_waypoint");
    });


    // get or update travel profile by clicking radio button
    $('input[name$="profile"]').click(function() {
      var profile = $(this).val();
      $.get('/get_travel_profile', {'profile': profile}, updateProfile);
    });


    // get directions using mapbox directions api
    $('#get-route').on('click', function(e) {
      e.preventDefault();
      $.get('/get_route', showRoute);
    });

    // clear route from map
    function clearRoute() {
      // e.preventDefault();
      if (map.hasLayer(routeLayer)) {
        // map.removeLayer(routeLayer);}
        routeLayer.clearLayers();
      }
      console.log("Finished remove routeLayer"); 
    };

    $('#clear-route').on('click', function() {
      clearRoute();
    });

    // experiment.
    // $('#add-path').on('click', function(e) {
    //   e.preventDefault();
    //   $.get('/get_route_polyline', addPath);
    //   console.log("Finished add path");
    // });

    // experiment.
    $('#remove-path').on('click', function(e) {
      e.preventDefault();
    });

    // commit to database about saved trip and clear session and waypoints list
    $('#start-over').on('click', function(e){
      e.preventDefault();
      $('#waypoint-list').empty();
      console.log("Finished empty waypoint list");
      $('#selected-profile').empty();
      console.log("Finished empty profile");
      $('#tripPreviewContent').empty();
      $('#distance').empty();
      $('#duration').empty();
      clearRoute();
      $.get('/start_over', showStatus);
      console.log("Finished show status");
    });

    // when user press enter after typed in address, start findAddress process
    $('#type-address').keypress(function(e) {
      if(e.which == 13) {
        var address = $(this).val();
        console.log(address);
        $('#wait').css("display", "block");
        $.get('/geocode_address', {'address': address}, findAddress);
        console.log("Finished toAddress");

      }
    });

    // Trip note preview in modal
    $('#view-trip-note').on('click', function(e) {
      e.preventDefault();
      $('#tripPreviewModal').addClass("modal-visible");
    });

    $('#closeTripPreviewModal').on('click', function(e) {
      e.preventDefault();
      $('#tripPreviewModal').removeClass("modal-visible");
    });

    var modal = document.getElementById("tripPreviewModal");
    window.onclick = function(e) {
      if (e.target == modal) {
        $('#tripPreviewModal').removeClass("modal-visible");
      }
    }

    // when sms is successfully sent, flash message shows and fadeout
    function showResponse(results) {
      console.log(results);
      $('#status-area').text(results).fadeIn().delay(1000).fadeOut('normal', function() {
        $(this).remove();
        });
      $('#receiverNumber').val("");
    }

    // when user click 'send sms' button, type number box shows up
    $('#sendSmsBtn').on('click', function(e) {
      e.preventDefault();
      $('#receiverNumber').addClass("inline-block");
      console.log("number input should show!")
    });

    // when user type number and click, send ajax post request to server to send sms
    $('#receiverNumber').keypress(function(e) {
      console.log("enter is pressed!")
        if (e.which == 13) {
          var number = $(this).val();
          console.log(number);
          $.post('/send_sms', {'receiver_number': number}, showResponse);
        }
      });