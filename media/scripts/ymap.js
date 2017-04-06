 var map;
 YMaps.jQuery(function () {
	map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);
	map.setCenter(new YMaps.GeoPoint(71.410184,51.162709), 13);//центр карты
	
	var nearestBusStops = new YMaps.ListBoxToggleItem("Остановки");
	var nearestBusStops2 = new YMaps.ListBoxItem("Остановки");
	var nearestListBox = new YMaps.ListBox({caption:"Ближайшие", width:100});
	//nearestListBox.add(nearestBusStops);
	nearestListBox.add(nearestBusStops2);
	//nearestListBox.add(new YMaps.ListBoxToggleItem("Банкоматы"));	
	
	var clearMapButton = new YMaps.ToolBarButton({ 
	    caption: "Очистить карту", 
	    hint: "Удаляет все объекты с карты"
	});
	YMaps.Events.observe(clearMapButton, clearMapButton.Events.Click, function () {
	    map.removeAllOverlays();
		busStopsShown.removeAll();
	}, map);
	
	var toolbar = new YMaps.ToolBar();		
	// Создание кнопки-флажка
    var nearestBtn = new YMaps.ToolBarToggleButton({ 
        icon: "http://icity.kz/media/images/controls/bus_icon.png", 
        hint: "Ближайшие остановки"
    });
	var nearestBtn2 = new YMaps.ToolBarButton({ 
        caption: "Остановки", 
        hint: "Ближайшие остановки"
    });
	// Добавление кнопки на панель инструментов
    //toolbar.add(nearestBtn);
	toolbar.add(nearestListBox);
	toolbar.add(clearMapButton);
	
	var scaleLine = new YMaps.ScaleLine();
	
	var searchMapBound = new YMaps.GeoBounds(new YMaps.GeoPoint(71.188054,51.037765), new YMaps.GeoPoint(71.665959,51.320886));
	
	map.addControl(new YMaps.Zoom(), new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Size(10, 5)));//зум
	map.addControl(new YMaps.TypeControl([YMaps.MapType.MAP, YMaps.MapType.SATELLITE, YMaps.MapType.HYBRID], [0, 1, 2], {width: 80}), new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Size(50, 5)));//тип карты (Схема, Спутник, Гибрид)
	map.addControl(toolbar, new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Size(160, 5)));//панель инструментов (рука, лупа, линейка)
	map.addControl(new YMaps.Traffic.Control(), new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Size(715, 5)));//модуль пробок            
	map.addControl(new YMaps.SearchControl({useMapBounds: false, geocodeOptions: {boundedBy: searchMapBound, strictBounds: true}}), new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Size(470, 5)));//поиск по карте
	map.addControl(scaleLine);//Масштабная линейка
	map.enableHotKeys();
	map.enableScrollZoom();
	
	//var ml = new YMaps.YMapsML("http://icity.kz/all_routes.xml");
	//var ml = new YMaps.YMapsML("http://icity.kz/routes/40.xml");
	var bus_stops_xml = new YMaps.YMapsML("http://icity.kz/all_bus_stops.xml");
	YMaps.Events.observe(bus_stops_xml, bus_stops_xml.Events.Load, function (bus_stops_xml) {
	    bus_stops_xml.get(0).forEach(function (obj) {
	        obj.setBalloonOptions({
	            margin: [33, 50, 20, 370]
	        });
	    });
	});
	
 	var tree;
	$(document).ready(function() {
		$("#tabs").tabs();
		tree = $("#menu_companies").treeview({
			collapsed: true,
			toggle: function(){
				if(this.id != ""){
					if(this.id.search("li-") != -1){
						retrieveJson(this);
					}
				}						
			}
			//animated: "medium"
		});
		
		orange_tree = $("#orange_companies").treeview({
			collapsed: true,
			toggle: function(){
				if(this.id != ""){
					if(this.id.search("li-") != -1){
						retrieveJson(this);
					}
				}						
			}
		});
		var li_items = $("li[id*='li-']");				
		initiateCompanyCollection(li_items);
	});
	var route;
	var routeLoadEventListener;
	var ymapsGroupBuses = new YMaps.Group();//группа для хранения загруженных маршрутов автобусов
	//var route = new YMaps.YMapsML("http://icity.kz/routes/40.xml");;
	$("#buses_tab table tbody tr td a").each(function (index, domEle) { 
			$("#"+domEle.id).bind("click", function() {
				var link = $(this);
				$("#" + link[0].id).activity({width: 4, length: 5});
				var bus_number = parseInt(link[0].id.substring(11));
				var bus_color = "#" + link[0].id.substring(4, 10);
//				YMaps.Events.observe(route, route.Events.Load, function(route) {
//					alert(route.get(0));
//				});
				
				if (link.hasClass("active")) {
					//link.parent().css("border", "1px solid #f9f9f9");		
					//map.removeOverlay(ymapsGroupBuses.get(parseInt(link[0].id.substring(4))));					
					map.removeOverlay(ymapsGroupBuses.filter(function(obj){ return obj.id == bus_number })[0]);
					link.activity(false);
					//link.parent().css("background-color", "#f9f9f9");
					link.parent().css("border", "5px solid #f9f9f9");					
				}
				else {
					//link.parent().css("border", "1px solid black");					
					//route.get(0).setBalloonOptions({margin: [33, 50, 20, 370]});
					if (ymapsGroupBuses.filter(function(obj){ return obj.id == bus_number }).length == 0) {						
						route = new YMaps.YMapsML("http://icity.kz/routes/" + bus_number + ".xml");	
						routeLoadEventListener = YMaps.Events.observe(route, route.Events.Load, function(route){
							route.id = bus_number;
						 	route.get(0).forEach(function (obj) {
					        	obj.setBalloonOptions({
						            margin: [33, 50, 20, 370]
						        });
						    });
							ymapsGroupBuses.add(route);
							map.addOverlay(route);
							link.activity(false);
							link.parent().css("border", "5px solid" + bus_color);
							//routeLoadEventListener.cleanup();
						});					
					}
					else {
						//map.addOverlay(ymapsGroupBuses.get(parseInt(link[0].id.substring(4))));
						map.addOverlay(ymapsGroupBuses.filter(function(obj){ return obj.id == bus_number })[0]);
						link.activity(false);		
						link.parent().css("border", "5px solid" + bus_color);	
					}				
					//route.get(0).openBalloon();
				}				

				link.toggleClass("active");				
				return false;
			}); 
		}
	);
	var bus;
//	YMaps.Events.observe(ml, ml.Events.Load, function (ml) {
//		ml.get(0).forEach(function (item) {
//			bus = "#bus_" + item.metaDataProperty.AnyMetaData.route * 1;
//			$(bus).bind("click", function() {
//				var link = $(this);
//				
//				if (link.hasClass("active")) {
//					link.parent().css("border", "1px solid #f9f9f9");		
//					map.removeOverlay(item);				
//				}
//				else {
//					link.parent().css("border", "1px solid black");
//					item.get(0).setBalloonOptions({margin: [33, 50, 20, 370]});
//					map.addOverlay(item);					
//					item.get(0).openBalloon();
//				}
//				
//				link.toggleClass("active");
//				
//				return false;
//			});		
//		});
//	}); 
	
	
//	YMaps.Events.observe(ml, ml.Events.Fault, function (ml, error) {
//	    alert('error: ' + error);
//	});
	
	YMaps.Events.observe(nearestBusStops, nearestBusStops.Events.Select, function () {
        map.addCursor(YMaps.Cursor.CROSSHAIR);
		//groupBusStops();
		busStopsGroup = bus_stops_xml.get(0);
		nearestBtnEventListener.enable();
		//setSize();
    });
	YMaps.Events.observe(nearestBusStops, nearestBusStops.Events.Deselect, function () {
	    map.removeCursor(YMaps.Cursor.CROSSHAIR);
		map.removeOverlay(myCircle);
		nearestBtnEventListener.disable();
	});
	
	YMaps.Events.observe(nearestBusStops2, nearestBusStops2.Events.Click, function () {
	    map.addCursor(YMaps.Cursor.CROSSHAIR);
		//groupBusStops();
		busStopsGroup = bus_stops_xml.get(0);
		nearestBtnEventListener.enable();
	}, map);
	
	var busStopsGroup = new YMaps.GeoObjectCollection();
	function groupBusStops() {
		bus_stops_xml.get(0).forEach(function (item) {
			for (i=0; i<item.length(); i++) {
				busStopsGroup.add(item.get(i));
			}	
		});
	}
	
	var busStopsShown = new YMaps.GeoObjectCollection();
	// Отображает метки, которые находятся рядом с точкой point
	function showObjects (point) {
		var filterObjects = busStopsGroup.filter(function (obj) {			
				// Если расстояние до метки меньше 500 м, то берем его в расчет
				return ( (obj.getGeoPoint().distance(point) < 500) && (-1 == busStopsShown.indexOf(obj)) );		        
	    });
	    
	    // Дальше можно делать что-то с отфильтрованными объектами,
	    // например, можно добавить их в группу и возвратить из функции
	    var group = new YMaps.GeoObjectCollection();
	    group.add(filterObjects);
	    busStopsShown.add(filterObjects);
	    return group;
	}
	
	var myCircle = new Circle2(new YMaps.GeoPoint(0.0,0.0), 0.5,{
	    style : {
	        polygonStyle : {
	            outline : true,
	            strokeWidth : 2,
	            strokeColor : "0000ff55",
	            fillColor : "0000ff22"
	        }
	    },
	    interactive : YMaps.Interactivity.NONE
    });
	
	var nearestBtnEventListener = YMaps.Events.observe(map, map.Events.Click, function (map, mEvent) {
		//var busStopsGroup = showObjects(mEvent.getGeoPoint());
		map.addOverlay(showObjects(mEvent.getGeoPoint()));
		myCircle.setCenter(map, mEvent.getGeoPoint());
		map.addOverlay(myCircle);
		map.removeCursor(YMaps.Cursor.CROSSHAIR);
		nearestBtnEventListener.disable();
	}, this);

	nearestBtnEventListener.disable();
	/*	
	var feedback_form = "<form>Ваш e-mail:<div><input type=\"text\" id=\"feedback-email\" width=\"30\"><span id=\"validEmail\"></span></div><p></p>Сообщение:<div><textarea rows=\"6\" cols=\"35\" wrap=\"hard\" style=\"width:400px;height:150px;\" name=\"text\" id=\"feedback_textarea\"></textarea></div><button disabled id=\"feedback-submit-button\">Отправить</button></form>"
	var $dialog = $('<div></div>')
		.html(feedback_form)
		.dialog({
			autoOpen: false,
			title: 'Сообщить об ошибке',
			height: 360,
			width: 450,
			modal: true,
	});
	
	var is_shown = false;
	$('#feedback').click(function() {	
		if(is_shown) {			
			$('#feedback-div').hide("fast");
			is_shown = false;
		}
		else {
			$('#feedback-div').show("fast");
			is_shown = true;
		}			
		//$('#feedback-div').show("fast");
		//$dialog.dialog('open');		
		// prevent the default action, e.g., following a link
		return false;
	});
	$('#feedback-cancel-button').click(function() {
		$('#feedback-div').hide("fast");
		is_shown = false;
		return false;
	});
	$('#feedback-submit-button').click(function() {
		$.post("feedback/", { email: $('#feedback-email').val(), message: $('#feedback_textarea').val() });
		$('#feedback-div').hide("fast");
		$('#feedback_textarea').val("");
		is_shown = false;
		alert("Спасибо. Сообщение отправлено.");
		//$dialog.dialog("close");		
		//event.preventDefault();
		return false;			
	});
	$("#feedback-email").keyup(function(){
		var email = $("#feedback-email").val();
		if(email != 0) {
			if(isValidEmailAddress(email)) {
				$("#validEmail").css({ "background-image": "url('http://icity.kz/media/images/feedback-form/validyes.png')" });
				$('#feedback-submit-button').attr("disabled", false);
			} else {
				$("#validEmail").css({ "background-image": "url('http://icity.kz/media/images/feedback-form/validno.png')" });
				$('#feedback-submit-button').attr("disabled", true);
				}
		} else {
			$("#validEmail").css({ "background-image": "none" });
			}
	});
	function isValidEmailAddress(emailAddress) {
		var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
		return pattern.test(emailAddress);
	}	
	*/
});	


// Функция, позволяющая осуществлять наследование без вызова конструктора родителя
// Подробнее о наследовании: http://javascript.ru/tutorial/object/inheritance
function extend (child, parent) {
    var c = function () {};
    c.prototype = parent.prototype;
    c.prototype.constructor = parent;
    return child.prototype = new c;
};

// Оверлей "Круг"
//
// center - географические координаты центра
// radius - радиус круга в км
// options.accuracy - количество граней многоугольника
function Circle2(center, radius, options){
	this.center = center;
	this.radius = radius;
	this.options = YMaps.jQuery.extend({
		accuracy: 360
	}, options);
	
	// Вызывает родительский конструктор
	YMaps.Polygon.call(this, [], this.options);
	
	// Вызывается при добавлении круга на карту
	this.onAddToMap = function(map, container){
		this.map = map;
		this.calculatePoints();
		
		YMaps.Polygon.prototype.onAddToMap.call(this, map, container);
	}
	
	// Устанавливает новый центр и радиус
	this.setCenter = function(map, newCenter, newRadius){
		this.map = map;
		if (this.map && (!this.center.equals(newCenter) || this.radius != newRadius)) {
			this.center = newCenter;
			this.radius = newRadius || this.radius;
			this.calculatePoints();
		}
	}
	
	// Вычисляет точки окружности
	this.calculatePoints = function(){
	
		// Откладываем геоточку от центра к северу на заданном расстоянии
		var northPoint = new YMaps.GeoPoint(this.center.getLng(), this.center.getLat() + this.radius / 112.2),  // Пиксельные координаты на последнем масштабе
		pixCenter = this.map.coordSystem.fromCoordPoint(this.center),  // Радиус круга в пикселях
		pixRadius = pixCenter.getY() - this.map.coordSystem.fromCoordPoint(northPoint).getY(),  // Вершины многоугол
		points = [],  // Вспомогательные переменные
		twoPI = 2 * Math.PI, delta = twoPI / this.options.accuracy;
		
		for (var alpha = 0; alpha < twoPI; alpha += delta) {
			points.push(this.map.coordSystem.toCoordPoint(new YMaps.Point(Math.cos(alpha) * pixRadius + pixCenter.getX(), Math.sin(alpha) * pixRadius + pixCenter.getY())))
		}
		
		this.setPoints(points);
	}
}

extend(Circle2, YMaps.Polygon);
		
function addEditItem (group, menuContainer) {
	YMaps.jQuery("<a href=\"#\">Редактировать</a>")
		.bind("click", function (){
			group.setEditingOptions({
						drawing: true,
	                 menuManager: function (index, menuItems) {
	                    menuItems.push({
	                        id: "StopEditing",
	                        title: '<span style="white-space:nowrap;">Завершить редактирование<span>',
	                        onClick: function (polyline, pointIndex) {
	                       polyline.stopEditing();	                      		
	                       YMaps.jQuery("#coords").attr("value", polyline.getPoints().join('\n'));
	                       YMaps.jQuery.post("upload.php", {coords : polyline.getPoints().join(';')});					   
	                        }
	                    });
	                    return menuItems;
	                }
	            }); 
				group.startEditing();       
		})		
		.appendTo(
            YMaps.jQuery("<li></li>").appendTo(menuContainer)
        )
};

function addMenuItem (group, map, menuContainer) {
    YMaps.jQuery("<a class=\"title\" href=\"#\">" + group.name + "</a>")
        .bind("click", function () {
            var link = YMaps.jQuery(this);
            if (link.hasClass("active")) {
                map.removeOverlay(group);
            } else {
                map.addOverlay(group);
				group.setEditingOptions({
						drawing: true,
	                 menuManager: function (index, menuItems) {
	                    menuItems.push({
	                        id: "StopEditing",
	                        title: '<span style="white-space:nowrap;">Завершить редактирование<span>',
	                        onClick: function (polyline, pointIndex) {
	                       polyline.stopEditing();	                      		
	                       YMaps.jQuery("#coords").attr("value", polyline.getPoints().join('\n'));
	                       YMaps.jQuery.post("upload.php", {coords : polyline.getPoints().join(';')});					   
	                        }
	                    });
	                    return menuItems;
	                }
	            }); 
				//group.startEditing();       
            }
            link.toggleClass("active");
            return false;
        })   
        .appendTo(
            YMaps.jQuery("<li></li>").appendTo(menuContainer)
        )
};

var company_plcmk;
var company_plcmk_style  = new YMaps.Style();
var company_plcmk_template;
var currentElement;
var generatedId;
var ulElement;
var start, elapsed;
function appendLi(collection, id, array) {
	//start = new Date().getTime();
	company_plcmk_style.iconStyle = new YMaps.IconStyle();
	company_plcmk_style.iconStyle.size = new YMaps.Point(32, 37);
	company_plcmk_style.iconStyle.offset = new YMaps.Point(-16, -37);
	for (var i=0; i<array.length; i++) {
		generatedId = id.replace("#", "") + "-" + (i+1);	
		company_plcmk = new YMaps.Placemark(YMaps.GeoPoint.fromString(array[i].coordinates));
		if(array[i].highlight != 0) {
			ulElement = $(id + "> ul").append('<li><span class=\"promoted_companies\"' + ' id=\"' + generatedId + '\">' + array[i].name + '</span></li>');
			//ulElement.children().children().last().addClass('promoted_companies');
		}	
		else {
			ulElement = $(id + "> ul").append('<li><span class=\"companies\"' + ' id=\"' + generatedId + '\">' + array[i].name + '</span></li>');			
			//ulElement.children().children().last().addClass('companies');
		}
		company_plcmk_style.iconStyle.href = array[i].icon;		
		company_plcmk.name = array[i].name;
		company_plcmk.description = createPlacemarkDescription(array[i]);
		company_plcmk.setBalloonOptions({margin: [33, 50, 20, 370], maxWidth:325});
		company_plcmk_template = new YMaps.Template("<div style=\"font-size:17px;font-weight:bold;\">$[name|объект]</div>\										    <div>$[description|Информация недоступна]</div>");
		company_plcmk_style.balloonContentStyle = new YMaps.BalloonContentStyle(company_plcmk_template);
		company_plcmk.setStyle(company_plcmk_style);	
		company_plcmk.id = generatedId;		
		YMaps.Events.observe(company_plcmk, company_plcmk.Events.BalloonOpen, function(obj) {
			$("#"+obj.id).addClass('back_color');
			$("a.grouped_elements").fancybox();
			$("a[rel*='fancyvideo']").fancybox({
                'titleShow'     : false,
                'transitionIn'  : 'elastic',
                'transitionOut' : 'elastic',			            
	            'type'      : 'swf',
	            'swf'       : {'wmode':'transparent','allowfullscreen':'true'}
	        });		
		});		
		YMaps.Events.observe(company_plcmk, company_plcmk.Events.BalloonClose, function(obj) {
			$("#"+obj.id).removeClass('back_color');
		});					
		$("#" + generatedId).bind('click', function(event){
			var link = $(this);
			var filteredObj = collection.filter(function(obj) {
				return obj.id == link.attr("id");
			});
			filteredObj[0].openBalloon();
			link.addClass('back_color');					
			return false
		});		
		collection.add(company_plcmk);
	}
	map.addOverlay(collection);	
	$(id + "> img").css('display', 'none');	
	//elapsed = new Date().getTime() - start;	
	//console.log(i + " " + elapsed);
}

var company_plcmk_description;
function createPlacemarkDescription(jsonObj) {
	company_plcmk_description = "";
	if(jsonObj.address != "") {
		company_plcmk_description = "<div style=\"font-size:13px;\">" + jsonObj.address + "</div>";	
	}
	if(jsonObj.phones.length != 0) {
		for(var i=0; i<jsonObj.phones.length; i++) {
			company_plcmk_description += "<div class=\"ballon_content_phones\"><strong>" + jsonObj.phones[i].phone + "</strong> <span style=\"color:#666;\">" + jsonObj.phones[i].description + "</span></div>"
		}	
	}
	if(jsonObj.work_hours != "") {
		company_plcmk_description += "<div class=\"ballon_content_div\"><span style=\"color:#666;\">Часы работы:</span> " + jsonObj.work_hours + "</div>"
	}	
	if(jsonObj.site != "") {
		company_plcmk_description += "<div style=\"height:20px;\"><a href=\"" + jsonObj.site + "\" target=\"_blank\">" + jsonObj.site + "</a></div>"
	}	
	if(jsonObj.email != "") {
		company_plcmk_description += "<div style=\"height:20px;\"><span style=\"color:#666;\">e-mail:</span> " + jsonObj.email + "</div>"
	}
	if(jsonObj.additional_info != "") {
		company_plcmk_description += "<div><strong>Дополнительная информация:</strong></div>";
		company_plcmk_description += "<div>" + jsonObj.additional_info + "</div>";
	}	
	if(jsonObj.photos.length != 0) {
		company_plcmk_description += "<div><strong>Фото:</strong></div>";
		company_plcmk_description += "<div style=\"margin:2px;width:300px;\">";
		for(var i=0; i<jsonObj.photos.length; i++) {
			company_plcmk_description += "<a class=\"grouped_elements\" rel=\"group1\" style=\"margin-right:5px;\" href=\"" + jsonObj.photos[i].href.replace("_XS","_XL") + "\"><img src=\"" + jsonObj.photos[i].href + "\"width=\"50\" style=\"border:4px solid #D8D8D8;\"height=\"50\" alt=\"\"/></a>"
		}
		company_plcmk_description += "</div>"
	} 
	if(jsonObj.video != "") {
		company_plcmk_description += "<div><strong>Видео:</strong></div>";
		company_plcmk_description += "<a rel=\"fancyvideo\" style=\"margin-right:5px\" href=\"" + jsonObj.video + "\"><img src=\"video.png\" alt=\"Смотреть видео\" width=\"48\" height=\"48\" /></a>"
	}	
	if(jsonObj.discount) {
		company_plcmk_description += "<div><strong>Скидка для держателей карт «Orange»: </strong>" + jsonObj.discount + "</div>";	
		if(jsonObj.discount_terms != "") {
			company_plcmk_description += "<div><strong>Условия скидки: </strong>" + jsonObj.discount_terms + "</div>";	
		}	
	}
	return company_plcmk_description;
}

var company_conteiner_collection = {};
var rubric_id, rubric_jquery_id, jsonFilename;		
var isBranchExpanded = {};

function retrieveJson(element){
	rubric_id = element.id.replace("li-", "");
	rubric_jquery_id = "#li-" + rubric_id;
	if(rubric_id[0] == 1) {//вкладка Компании
		jsonFilename = top.location.href.replace("#", "") + "companies/" + rubric_id;	
	}
	else {//вкладка Orange
		jsonFilename = top.location.href.replace("#", "") + "orange-companies/" + rubric_id;
	}	
	if(!isBranchExpanded[rubric_id]){
		$("#" + element.id + " > img").css('display', 'inline');
		company_conteiner_collection[rubric_id].removeAll();
		$.getJSON(jsonFilename, function(data) {
			appendLi(company_conteiner_collection[rubric_id], rubric_jquery_id, data.items);
		});
		isBranchExpanded[rubric_id] = true;
	}
	else{
		if(isBranchExpanded[rubric_id]){
			isBranchExpanded[rubric_id] = false;
			map.removeOverlay(company_conteiner_collection[rubric_id]);
			$(rubric_jquery_id + " > ul").empty();
		}	
	}										
}

function initiateCompanyCollection(aItems){
	aItems.each(function(index){
		company_conteiner_collection[aItems[index].id.replace("li-", "")] = new YMaps.GeoObjectCollection();
	});
}

//document.onclick = function(e){
//	e = e || event;
//    var t = e.target || e.srcElement;
//	alert(t.id);
//}
