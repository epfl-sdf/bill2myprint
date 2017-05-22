jQuery(function($) {

	/**
	 * This object controls the nav bar. Implement the add and remove
	 * action over the elements of the nav bar that we want to change.
	 *
	 * @type {{flagAdd: boolean, elements: string[], add: Function, remove: Function}}
	 */
	var myNavBar = {

		flagAdd: true,

		elements: [],

		init: function (elements) {
		    this.elements = elements;
		},

		add : function() {
		    if(this.flagAdd) {
		        for(var i=0; i < this.elements.length; i++) {
		            document.getElementById(this.elements[i]).className += " fixed-theme";
		        }
		        this.flagAdd = false;
		    }
		},

		remove: function() {
		    for(var i=0; i < this.elements.length; i++) {
		        document.getElementById(this.elements[i]).className =
		                document.getElementById(this.elements[i]).className.replace( /(?:^|\s)fixed-theme(?!\S)/g , '' );
		    }
		    this.flagAdd = true;
		}

	};

	/**
	 * Init the object. Pass the object the array of elements
	 * that we want to change when the scroll goes down
	 */
	myNavBar.init(  [
		"header",
		"header-container",
		"brand"
	]);

	/**
	 * Function that manage the direction
	 * of the scroll
	 */
	function offSetManager(){

		var yOffset = 0;
		var currYOffSet = window.pageYOffset;

		if(yOffset < currYOffSet) {
		    myNavBar.add();
		}
		else if(currYOffSet == yOffset){
		    myNavBar.remove();
		}

	}

	/**
	 * bind to the document scroll detection
	 */
	window.onscroll = function(e) {
		offSetManager();
	}

	/**
	 * We have to do a first detectation of offset because the page
	 * could be load with scroll down set.
	 */
	offSetManager();


    /**
     * Manage the select list.
     */
/*
	$(function() {

		var maxHeight = 200;

		$(".btn-group").hover(function (e) {
			var $container = $(this);
			var $list = $container.find("ul");
			var origHeight = $container.height();
			var lines = $container.find("ul li").length;
			var height = 40.0 * lines * 1.1;       // make sure there is enough room at the bottom
			var multiplier = height / maxHeight;     // needs to move faster if list is taller
			$list.css({ paddingTop: origHeight }).show();
			// don't do any animation if list shorter than max
			if (multiplier > 1) {
				$container.mousemove(function(e) {
					var offset = $container.offset();
					var relativeY = (e.pageY - offset.top - origHeight) * multiplier;
					if (relativeY > origHeight) {
						$list.css("top", -relativeY + origHeight);
					}
				});
			}
		}, function() {
			$(this).find("ul").css({ top: 0 }).hide();   // put things back to normal
		});
	});
*/
	/**
     * Submit form when an element of list is chosen.
     */
    $("#homepage_semester ul li label").click(function() {
		$("#semester").val($(this).text());
		$("#homepage_form").submit();
	});

	$("#faculties_semester ul li label").click(function() {
		$("#semester").val($(this).text());
		$("#faculty_form").submit();
	});

	$("#faculties_faculty ul li label").click(function() {
		$("#faculty").val($(this).text());
		$("#faculty_form").submit();
	});

	$("#sections_semester ul li label").click(function() {
		$("#semester").val($(this).text());
		$("#section_form").submit();
	});

	$("#sections_faculty ul li label").click(function() {
		$("#faculty").val($(this).text());
		$("#section_form").submit();
	});

	$("#sections_section ul li label").click(function() {
		$("#section").val($(this).text());
		$("#section_form").submit();
	});


	/**
	 * Autocomplete
	 */

	// Allow to highlight (in bold) the keyed text in autocomplete input
    function highlight(s, t) {
        var matcher = new RegExp("("+$.ui.autocomplete.escapeRegex(t)+")", "ig");
        return s.replace(matcher, "<b>$1</b>");
    }

	$('.autocomplete-student').autocomplete({
        minLength: 2,
        source: function (request, response) {
            $.ajax({
                url: "/sciper",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function (data) {
                    response($.map(data, function(item) {
                        return {
                            student: item.student,
                            student_hl: highlight(item.student, request.term)
                        };
                    }));
                }
            });
        },
        focus: function (event, ui) {
            this.value = ui.item.student;
            event.preventDefault();
        },
        select: function (event, ui) {
			$("#student_form").submit();
        }
    }).data("ui-autocomplete")._renderItem = function (ul, item) {
        return $("<li></li>")
            .data("item.autocomplete", item)
            .append($("<a></a>").html(item.student_hl))
            .appendTo(ul);
    };

});
